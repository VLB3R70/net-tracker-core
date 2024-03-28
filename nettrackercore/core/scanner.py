from parsers import NmapParser


class Scanner:
    """
    Objeto que representa un escáner. Este escáner se encarga de usar el paquete de Nmap previamente instalado en la máquina.

    El usuario establece ciertos parámetros que posteriormente serán usados por el paquete Nmap. Dichos parámetros son:

    - **Objetivos**: puede ser una dirección de red en formato CIDR, una dirección IP o varias direcciones IP separadas por comas.

    - **Puertos**: es un parámetro que establece los puertos que se escanearán, si no se establece nada se escanean todos.
    El formato de los puertos es:
        - '80' -> Solo se escanea el puerto 80
        - '80,443' -> Se escanean los puertos 80 y 443 únicamente
        - '1-1024' -> Solo se escanean los puertos comprendidos entre el 1 y el 1024

    - **Parámetros**: son otros parámetros permitidos por Nmap

    :param targets: Dirección IP o varias direcciones IP separadas por comas.
    :param ports: Puertos que se escanearán.
    :param params: Parámetros adicionales permitidos por el paquete Nmap. **Ejemplo:** -O, -sV, -sS, etc.

    :return: Se devuelve un objeto que representa el resultado de la ejecución de Nmap.
    :rtype: ScannerResult
    """

    def __init__(self, targets=None, ports=None, params=None):
        self.targets = targets
        self.ports = ports
        self.params = params
        self.parser = NmapParser()

    def scan(self):
        command = self.parser.create_command(self.targets, self.ports, self.params)
        print(command)


class ScannerResult:
    pass

