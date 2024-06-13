from botocore.paginate import Paginator
from time import sleep
from typing import Any, TypeAlias
import boto3
import json

from exceptions import StateMachineNotFoundError, StateMachineNotUniqueError

JsonType: TypeAlias = dict[str, Any]


class StepFunctionsClient:
    SERVICE_NAME: str = "stepfunctions"

    def __init__(self, aws_profile: str, **kwargs) -> None:
        self.profile: str = aws_profile
        boto3.setup_default_session(profile_name=self.profile)
        self.client = boto3.client(StepFunctionsClient.SERVICE_NAME)

    def get_state_machine_arn_by_name(self, state_machine_name: str) -> str:
        """
        This method uses contains for the find because CDK deploy adds unique
        identifiers to state machine names
        """

        list_paginator: Paginator = self.client.get_paginator(
            operation_name="list_state_machines",
        )
        state_machines: list[str] = []
        for page in list_paginator.paginate():
            for state_machine in page.get("stateMachines", []):
                if state_machine_name in state_machine["name"]:
                    state_machines.append(state_machine["stateMachineArn"])

        if len(state_machines) == 0:
            raise StateMachineNotFoundError(self.profile, state_machine_name)
        elif len(state_machines) > 1:
            raise StateMachineNotUniqueError(
                profile=self.profile,
                state_machine_name=state_machine_name,
                state_machines=state_machines,
            )
        return state_machines[0]

    def execute_state_machine(
        self,
        state_machine_arn: str,
        state_machine_input: str = None,
    ) -> str:
        exec_kwargs: dict[str, str] = {"stateMachineArn": state_machine_arn}
        if state_machine_input:
            exec_kwargs["input"] = state_machine_input
        response: JsonType = self.client.start_execution(**exec_kwargs)
        return response["executionArn"]

    def get_execution_result(self, execution_arn: str) -> JsonType:
        while True:
            response: JsonType = self.client.describe_execution(
                executionArn=execution_arn,
            )
            status: str = response["status"]

            if status != "RUNNING":
                return response
            print(status)
            sleep(30)
