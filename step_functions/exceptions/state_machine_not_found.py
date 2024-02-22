class StateMachineNotFoundError(Exception):
    def __init__(self, profile: str, query: str) -> None:
        self.name: str = "StateMachineNotFoundError"
        self.message: str = f"{query} found no state machines in {profile}"

    def __str__(self) -> str:
        return self.message
