class NettrackerException(Exception):
    """
    Excepción base para todas las excepciones del programa.
    """

    def __init__(self, message):
        super().__init__(self, message)


class InvalidArgumentsException(NettrackerException):
    """
    Esta excepción se lanza cuando un argumento introducido por el usuario no es válido.
    """

    def __init__(self, message):
        super().__init__(message)


class ExecutionError(NettrackerException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class IllegalArgumentException(InvalidArgumentsException):
    """
    Esta excepción se lanza cuando el usuario ha introducido un argumento que no debería introducir. La diferencia entre
    :py:class:`InvalidArgumentsException` e :py:class:`IllegalArgumentException` es que: la primera corresponde a un
    error del usuario y la segunda a una opción no permitida por la lógica del programa.
    """

    def __init__(self, message):
        super().__init__(message)


class InvalidPortsException(NettrackerException):
    """
    Esta excepción se lanza cuando los puertos introducidos por el usuario no son válidos.
    """

    def __init__(self, message):
        super().__init__(message)


class InvalidAddressException(NettrackerException):
    """
    Esta excepción se lanza cuando la dirección IP introducida por el usuario no es válida.
    """

    def __init__(self, message):
        super().__init__(message)
