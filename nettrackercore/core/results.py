class JSONResult(dict):
    """
    Este objeto encapsula el resultado de la ejecución del escaneo. Este objeto hereda el objeto
    `dict <https://docs.python.org/3/library/stdtypes.html#dict>`_ y obtiene un diccionario mediante el constructor que
    actualiza su valor. Este diccionario se obtiene en la lectura del fichero XML con el resultado del escaneo.
    """

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], dict) and 'nmaprun' in args[0]:
            self.update(args[0]['nmaprun'])
        else:
            super().__init__(*args, **kwargs)

    def get_values(self):
        """
        Obtiene todos los valores del objeto JSONResult.

        :return: lista con todos los valores del objeto.
        :rtype: list
        """
        return list(self.values())

    def get_keys(self):
        """
        Obtiene todas las claves del objeto JSONResult.

        :return: lista con todas las claves del objeto.
        :rtype: list
        """
        return list(self.keys())

    def get_items(self):
        """
        Obtiene todos los pares clave-valor del objeto JSONResult.

        :return: lista con todos los pares clave-valor del objeto.
        :rtype: list
        """
        return list(self.items())

    def get_host(self):
        """
        Obtiene el valor cuya clave corresponde a `host`.

        :return: el valor que corresponde a `host`.
        """
        return self.get('host')

    def get_hostname(self, host):
        try:
            hostname = host['hostnames']['hostname']
            return hostname['@name']
        except TypeError:
            return "None"

    def get_address(self, host):
        """
        Obtiene el valor cuya clave corresponde a `address`. Este método además tiene en cuenta que el escaneo detecta
        la dirección MAC del equipo. Dicho valor se añade a la clave `address` y corresponde a una lista.

        .. code-block::
            :caption: Ejemplo

                {
                ...,
                'address': [{'@addr': <IP>, '@addrtype': 'ipv4'}, {'@addr': <MAC>, '@addrtype': 'mac', '@vendor': vendor}],
                ...
                }

        :param host: el valor que corresponde a `host`.
        :type host: dict
        :return: el valor que corresponde a `address`.
        :rtype: str
        """
        address = host['address']
        if isinstance(address, dict):
            return address['@addr']
        elif isinstance(address, list):
            return address[0]['@addr']

    def get_os(self, host):
        """
        Este método obtiene el valor de la calve que corresponde a `os` dentro de `host`. Este valor a su vez contiene
        más información que para la lógica del programa no es relevante por lo que el dato final corresponde a `osmatch`.

        Al igual que con las direcciones, es posible que el escaneo detecte varios sistemas operativos en una misma
        máquina; estos, los muestra como una lista con su información. El escáner Nmap, al encontrar varios sistemas
        operativos, indica un porcentaje de veracidad; este porcentaje indica lo seguro que está de dicho escaneo. El
        primer valor siempre es el más elevado (el más confiable) por lo que, si el valor es una lista, siempre se
        escoge el primer valor de la lista.

        También es posible que el escáner no sea capaz de detectar un sistema operativo válido. En estos casos el valor
        de `osmatch` corresponde a `None` o `Null` en otros lenguajes. Si obtenemos un valor nulo y queremos trabajar
        con él se lanzará una excepción `TypeError <https://docs.python.org/3/library/exceptions.html#TypeError>`_ y, en
        ese caso, se retornará una cadena indicando que no se ha podido encontrar un sistema operativo válido.

        :param host: el valor que corresponde a `host`.
        :type host: dict
        :return: el valor que corresponde a `osmatch`.
        :rtype: str
        """
        try:
            os = host['os']['osmatch']
            if isinstance(os, dict):
                return os['@name']
            elif isinstance(os, list):
                return os[0]['@name']
        except TypeError:
            return "OS not found."
        except KeyError:
            return 0

    def get_services(self, host):
        """
        Este método se encarga de obtener los valores correspondientes a los puertos abiertos y los servicios corriendo
        en ellos. Se retorna una lista de diccionarios donde la sintaxis de estos es la siguiente:

        .. code-block::
            :caption: Sintaxis de estos puertos abiertos

                {"name": nombre, "port":puerto, "protocol": protocolo}

        :param host: el valor que corresponde a `host`.
        :type host: dict
        :return: lista de diccionarios con los valores de los servicios correspondientes a los puertos abiertos.
        :rtype: list
        """
        service_list = []

        try:
            ports = host['ports']['port']
            for port in ports:
                service = {
                    "name": port['service']['@name'],
                    "port": port['@portid'],
                    "protocol": port["@protocol"]
                }
                service_list.append(service)
        except KeyError:
            service_list.append(0)

        return service_list
