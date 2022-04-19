class ClosedSocketException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidMessageException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)