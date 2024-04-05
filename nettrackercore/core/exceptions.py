class NettrackerException(Exception):
    def __init__(self, message):
        super().__init__(self, message)


class InvalidArgumentsException(NettrackerException):
    def __init__(self, message):
        super().__init__(message)


class IllegalArgumentException(InvalidArgumentsException):
    def __init__(self, message):
        super().__init__(message)


class InvalidPortsException(NettrackerException):
    def __init__(self, message):
        super().__init__(message)


class InvalidAddressException(NettrackerException):
    def __init__(self, message):
        super().__init__(message)
