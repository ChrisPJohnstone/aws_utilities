class StateMachineNotUniqueError(Exception):
    def __init__(
        self,
        profile: str,
        query: str,
        state_machines: list[str],
    ) -> None:
        self.name: str = "StateMachineNotFoundError"
        message_args: list[str] = [
            f"{query} found multiple state machines in {profile}:",
            *state_machines,
        ]
        self.message: str = "\n- ".join(message_args)

    def __str__(self) -> str:
        return self.message
