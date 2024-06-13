from argparse import ArgumentParser, Namespace
from step_functions_client import StepFunctionsClient
from typing import Any, TypeAlias

JsonType: TypeAlias = dict[str, Any]


def _get_state_machine_arn(state_machine_arn: str, test_case: str) -> str:
    if test_case is not None:
        return f"{state_machine_arn}#{test_case}"
    return state_machine_arn


def handler(event: dict[str, str], context: Any) -> JsonType:
    client: StepFunctionsClient = StepFunctionsClient(
        aws_profile=event["aws_profile"],
        endpoint_url=event["endpoint_url"],
    )
    state_machine_arn: str = _get_state_machine_arn(
        state_machine_arn=event["state_machine_arn"],
        test_case=event["test_case"],
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
        "--endpoint-url",
        dest="endpoint_url",
        type=str,
        required=True,
        help="Endpoint URL for the Step Functions service",
    )
    parser.add_argument(
        "--state-machine-arn",
        dest="state_machine_arn",
        type=str,
        required=True,
        help="Name of the state machine to execute (search is contains)",
    )
    parser.add_argument(
        "--test-case",
        dest="test_case",
        type=str,
        required=False,
        help="Test case to use for state machine execution if any",
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
        "endpoint_url": args.endpoint_url,
        "state_machine_arn": args.state_machine_arn,
        "test_case": args.test_case,
        "state_machine_input": args.state_machine_input,
    }
    result: JsonType = handler(local_event, None)
    print(result)
