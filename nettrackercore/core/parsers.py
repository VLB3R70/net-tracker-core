import ipaddress

from nettrackercore.core.exceptions import InvalidPortsException, InvalidAddressException, IllegalArgumentException


class NmapParser:
    """
    NmapParser se encarga de formatear los parámetros introducidos por el usuario y los devuelve como una lista.
    """

    @staticmethod
    def validate_address(address):
        """
        Este método se encarga de validar las direcciones IP ya sean de red o no con el módulo
        `ipaddress <https://docs.python.org/3/library/ipaddress.html#module-ipaddress>`_

        :param address: Es la dirección IP a validar
        :type address: str
        :return: Verdadero o falso en función de la dirección IP
        :rtype: bool
        """
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
        """
        Este método se encarga de validar los puertos introducidos por el usuario dentro de una lista. Si existe algún
        puerto inválido se lanza una excepción.

        :param port_list: Es la lista de puertos a validar
        :type port_list: list
        :raise exceptions.InvalidPortsException:
        """
        for port in port_list:
            try:
                port = int(port)
                if not 0 < port < 65536:
                    raise InvalidPortsException(f"Port {port} is invalid")
            except ValueError:
                raise InvalidPortsException(f"Port {port} is invalid")

    @staticmethod
    def parse_targets(targets):
        """
        Este método se encarga de devolver las direcciones correctamente validadas. Si no son válidas se lanza una excepción.

        :param targets: Dirección IP introducida por el usuario.
        :type targets: str
        :raise InvalidAddressException:
        :return: Direcciones IP validadas
        :rtype: str
        """
        if not NmapParser.validate_address(targets):
            raise InvalidAddressException("Target address {} is invalid".format(targets))
        return targets

    @staticmethod
    def parse_ports(ports):
        """
        Este método se encarga de formatear y validar los puertos introducidos por el usuario.

        :param ports: Son los puertos a validar
        :type ports: str
        :return: Puertos validados
        :rtype: str
        """
        ports = ports.replace(' ', '')
        NmapParser.validate_ports(NmapParser.ports_to_list(ports))
        return ports

    @staticmethod
    def ports_to_list(ports):
        """
        Por cómo funciona Nmap, es posible establecer los puertos con comas (,) o guiones (-) para establecer rangos o
        puertos concretos.

        :param ports: Son los puertos a validar.
        :type ports: str
        :return: Puertos introducidos en formato de lista.
        :rtype: list
        """
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
        """
        Este método se encarga de devolver los parámetros opcionales introducidos por el usuario formateados como una
        lista.

        :param params: Parámetros opcionales introducidos por el usuario.
        :type params: str
        :raise IllegalArgumentException:
        :return: Lista de parámetros opcionales introducidos por el usuario.
        :rtype: list[str]
        """
        invalid_params = ['-oX', '-oN', '-oS', '-oG']

        if any(option in params for option in invalid_params):
            raise IllegalArgumentException("The extra parameter or parameters contains an output option.")
        return params.split()

    @staticmethod
    def create_command(targets=None, ports=None, params=None, sudo=False, temp_file=None) -> list:
        """
        El objeto `Popen <https://docs.python.org/3/library/subprocess.html#popen-objects>`_ necesita los argumentos que
        posteriormente ejecutará en un formato de lista.

        Este método es el encargado de crear dicha lista después de validar todos los parámetros introducidos por el
        usuario. Además, el resultado de la ejecución se debe de almacenar en un fichero XML por lo que de forma
        predeterminada se establece el parámetro `-oX`.

        :param targets: Direcciones IP introducidas por el usuario.
        :type targets: str
        :param ports: Son los puertos introducidos por el usuario.
        :type ports: str
        :param params: Son los parámetros opcionales introducidos por el usuario.
        :type params: str
        :param sudo: Opción elegida por el usuario para ejecutar el comando con privilegios o no.
        :type sudo: bool
        :param temp_file: Ruta absoluta del fichero temporal donde se almacenará el resultado en formato XML.
        :type temp_file: str

        :return: La lista del comando completo que se ejecutará con :py:mod:`subprocess`
        :rtype: list[str]
        """
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
