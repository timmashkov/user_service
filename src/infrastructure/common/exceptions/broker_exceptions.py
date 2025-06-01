class SendingDataError(Exception):
    _message = "Error while sending data"

    def __init__(self) -> None:
        super().__init__(self._message)

    def __str__(self) -> str:
        return f"SendingDataError: {self._message}"
