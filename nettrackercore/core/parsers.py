import ipaddress

import xmltodict

from .exceptions import InvalidPortsException, InvalidAddressException, IllegalArgumentException


class NmapParser:
    """
    NmapParser se encarga de formatear los parámetros introducidos por el usuario y los devuelve como una lista.
    """

    @staticmethod
    def validate_address(address):
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:  # Si no es una dirección IP válida se lanza el error
            try:
                ipaddress.ip_network(address)
                return True
            except ValueError:  # Se comprueba que la dirección pasada es una red válida
                return address == 'localhost'  # Por último se comprueba si el usuario ha escrito 'localhost'

    @staticmethod
    def validate_ports(port_list):
        for port in port_list:
            port = int(port)
            if not 0 < port < 65536:
                raise InvalidPortsException("Port {} is invalid".format(port))

    @staticmethod
    def parse_targets(targets):
        if not NmapParser.validate_address(targets):
            raise InvalidAddressException("Target address {} is invalid".format(targets))
        return targets

    @staticmethod
    def parse_ports(ports):
        ports = ports.replace(' ', '')
        NmapParser.validate_ports(NmapParser.ports_to_list(ports))
        return ports

    @staticmethod
    def ports_to_list(ports):
        if ',' in ports:
            ports_list = ports.split(',')
            return ports_list
        elif '-' in ports:
            ports_list = ports.split('-')
            return ports_list
        else:
            return ports.split()

    @staticmethod
    def parse_params(params):
        inavlid_params = ['-oX', '-oN', '-oS', '-oG']

        if any(option in params for option in inavlid_params):
            raise IllegalArgumentException("The extra parameter or parameters contains an output option.")
        return params.split()

    @staticmethod
    def create_command(targets=None, ports=None, params=None, sudo=False, temp_file=None) -> list:
        nmap_command = ['nmap']
        output_format = ['-oX', temp_file]

        if sudo:
            nmap_command.insert(0, 'sudo')

        if targets:
            parsed_targets = NmapParser.parse_targets(targets)
            nmap_command.append(parsed_targets)

        if ports:
            parsed_ports = NmapParser.parse_ports(ports)
            nmap_command.extend(['-p', parsed_ports])

        if params:
            parsed_params = NmapParser.parse_params(params)
            nmap_command.extend(parsed_params)

        nmap_command.extend(output_format)

        return nmap_command


class JSONNmapParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.data = self.get_data()

    def get_data(self):
        with open(self.xml_file, 'r', encoding='utf-8') as file:
            content = file.read()

        json_data = xmltodict.parse(content)

        return json_data

    def get_hosts(self):
        return self.data['nmaprun']['host']

    def get_host_address(self, host):
        return host['address']['@addr']
