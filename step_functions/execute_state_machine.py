from argparse import ArgumentParser, Namespace
from exceptions import StateMachineNotFoundError, StateMachineNotUniqueError
from subprocess import CompletedProcess, run
from time import sleep
import json


def get_state_machine_arn_by_name(profile: str, name: str) -> str:
    query: str = f"stateMachines[?contains(name, '{name}')]"
    return _get_state_machine_arn(profile, query)


def _get_state_machine_arn(profile: str, query: str) -> str:
    command_args: list[str] = [
        f"aws",
        f"stepfunctions",
        f"list-state-machines",
        f"--profile={profile}",
        f"--query={query}",
    ]
    process: CompletedProcess = run(
        args=command_args,
        capture_output=True,
        text=True,
    )
    state_machines: list[dict[str, str]] = json.loads(process.stdout)

    if len(state_machines) == 0:
        raise StateMachineNotFoundError(profile, query)
    if len(state_machines) > 1:
        raise StateMachineNotUniqueError(
            profile=profile,
            query=query,
            state_machines=[machine["name"] for machine in state_machines],
        )
    return state_machines[0]["stateMachineArn"]


def execute_state_machine(profile: str, state_machine_arn: str) -> str:
    command_args: list[str] = [
        f"aws",
        f"stepfunctions",
        f"start-execution",
        f"--profile={profile}",
        f"--state-machine-arn={state_machine_arn}",
    ]
    process: CompletedProcess = run(
        args=command_args,
        capture_output=True,
        text=True,
    )
    execution_detail: dict[str, str] = json.loads(process.stdout)
    return execution_detail["executionArn"]


def get_execution_result(profile: str, execution_arn: str) -> str:
    command_args: list[str] = [
        f"aws",
        f"stepfunctions",
        f"describe-execution",
        f"--profile={profile}",
        f"--execution-arn={execution_arn}",
    ]

    while True:
        process: CompletedProcess = run(
            args=command_args,
            capture_output=True,
            text=True,
        )
        execution_detail: dict[str, str] = json.loads(process.stdout)
        if execution_detail["status"] != "RUNNING":
            break
        print("RUNNING")
        sleep(30)
    return json.dumps(execution_detail)


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        "--aws-profile",
        dest="aws_profile",
        type=str,
        required=True,
        help="AWS profile to use for security",
    )
    parser.add_argument(
        "--state-machine-name",
        dest="state_machine_name",
        type=str,
        required=True,
        help="Name of the state machine to execute (search is contains)",
    )
    args: Namespace = parser.parse_args()

    state_machine_arn: str = get_state_machine_arn_by_name(
        profile=args.aws_profile,
        name=args.state_machine_name,
    )
    execution_arn: str = execute_state_machine(
        profile=args.aws_profile,
        state_machine_arn=state_machine_arn,
    )
    result: str = get_execution_result(args.aws_profile, execution_arn)
    print(result)

