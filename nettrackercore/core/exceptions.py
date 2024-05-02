class NettrackerException(Exception):
    """
    Excepción base para todas las excepciones del programa.
    """

    def __init__(self, message="System exception", code=1, *args, **kwargs):
        self.message = message
        self.code = code
        super().__init__(message, *args, **kwargs)


class InvalidArgumentsException(NettrackerException):
    """
    Esta excepción se lanza cuando un argumento introducido por el usuario no es válido.
    """

    def __init__(self, message="One or more arguments are invalid.", code=2, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)


class ExecutionError(NettrackerException):
    """
    Esta excepción se lanza cuando ocurre un error durante la ejecución del programa.
    """

    def __init__(self, message="An error occurred during the execution of the program.", code=3, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)


class IllegalArgumentException(NettrackerException):
    """
    Esta excepción se lanza cuando el usuario ha introducido un argumento que no debería introducir.
    """

    def __init__(self, message="One or more arguments are illegal.", code=4, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)


class InvalidPortsException(NettrackerException):
    """
    Esta excepción se lanza cuando los puertos introducidos por el usuario no son válidos.
    """

    def __init__(self, message="The ports introduced are invalid.", code=5, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)


class InvalidAddressException(NettrackerException):
    """
    Esta excepción se lanza cuando la dirección IP introducida por el usuario no es válida.
    """

    def __init__(self, message="The address or addresses introduced are invalid.", code=6, *args, **kwargs):
        super().__init__(message, code, *args, **kwargs)
