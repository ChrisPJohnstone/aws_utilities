class StateMachineNotFoundError(Exception):
    def __init__(self, profile: str, state_machine_name: str) -> None:
        self.name: str = "StateMachineNotFoundError"
        self.message: str = (
            f"{state_machine_name} found no state machines in {profile}"
        )

    def __str__(self) -> str:
        return self.message
