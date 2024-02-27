class StateMachineNotUniqueError(Exception):
    def __init__(
        self,
        profile: str,
        state_machine_name: str,
        state_machines: list[str],
    ) -> None:
        self.name: str = "StateMachineNotFoundError"
        message_args: list[str] = [
            (
                f"{state_machine_name} found multiple state"
                f" machines in {profile}:"
            ),
            *state_machines,
        ]
        self.message: str = "\n- ".join(message_args)

    def __str__(self) -> str:
        return self.message
