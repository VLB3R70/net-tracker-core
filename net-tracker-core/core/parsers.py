import shlex
from collections.abc import Iterable


class NmapParser:
    """
    NmapParser se encarga de formatear los parámetros introducidos por el usuario y los devuelve como una lista.
    """
    @staticmethod
    def split(command):
        return shlex.split(command)

    def parse_targets(self, targets):
        if type(targets) is str:
            _ = self.split(targets)
            return targets
        elif type(targets) is Iterable:
            aux = ' '.join(targets)
            _ = self.split(aux)
            return aux

    def parse_ports(self, ports):
        ports = ports.replace(' ', '')
        _ = self.split(ports)
        return ports

    def parse_args(self, args):
        pass

    def create_command(self, targets=None, ports=None, args=None) -> list:
        nmap_command = 'nmap '
        if targets:
            parsed_targets = self.parse_targets(targets)
            nmap_command += parsed_targets

        if ports:
            parsed_ports = self.parse_ports(ports)
            nmap_command += f' -p {parsed_ports}'

        return self.split(nmap_command)


class JSONNmapParser:
    pass
