from typing import Union
from collections.abc import Iterable


class Scanner:
    """
    Objeto que representa un escáner. Este escáner se encarga de usar el paquete de Nmap previamente instalado en la máquina.

    El usuario establece ciertos parámetros que posteriormente serán usados por el paquete Nmap. Dichos parámetros son:

    - **Objetivos**: puede ser una dirección de red en formato CIDR, una dirección IP o varias direcciones IP separadas por comas.

    - **Puertos**: es un parámetro que establece los puertos que se escnearán, si no se establece nada se escanean todos.

    - **Parámetros**: son otros parámetros permitidos por Nmap

    :param targets: Dirección IP o varias direcciones IP separadas por comas.
    :param ports: Puertos que se escanearán.
    :param params: Parámetros adicionales permitidos por el paquete Nmap. **Ejemplo:** -O, -sV, -sS, etc.

    :return: Se devuelve un objeto que representa el resultado de la ejecución de Nmap.
    :rtype: ScannerResult
    """

    def __init__(self, targets: Union[str, Iterable] = None, ports: Union[None, int, str, Iterable] = None,
                 params: str = None):
        self.targets = targets
        self.ports = ports
        self.params = params

    def scan(self):
        pass


class ScannerResult:
    pass
