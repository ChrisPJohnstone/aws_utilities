from argparse import ArgumentParser, Namespace
from step_functions_client import StepFunctionsClient
from typing import Any, TypeAlias

JsonType: TypeAlias = dict[str, Any]


def handler(event: dict[str, str], context: Any) -> JsonType:
    client: StepFunctionsClient = StepFunctionsClient(event["aws_profile"])
    state_machine_arn: str = client.get_state_machine_arn_by_name(
        state_machine_name=event["state_machine_name"],
    )
    execution_arn: str = client.execute_state_machine(
        state_machine_arn=state_machine_arn,
        state_machine_input=event["state_machine_input"],
    )
    return client.get_execution_result(execution_arn)


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
    parser.add_argument(
        "--state-machine-input",
        dest="state_machine_input",
        type=str,
        required=False,
        help="Input for state machine if any",
    )
    args: Namespace = parser.parse_args()

    local_event: dict[str, str] = {
        "aws_profile": args.aws_profile,
        "state_machine_name": args.state_machine_name,
        "state_machine_input": args.state_machine_input,
    }
    result: JsonType = handler(local_event, None)
    print(result)
