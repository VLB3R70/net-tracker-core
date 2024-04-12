class JSONResult(dict):
    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], dict) and 'nmaprun' in args[0]:
            self.update(args[0]['nmaprun'])
        else:
            super().__init__(*args, **kwargs)

    def get_values(self):
        """Obtiene todos los valores del objeto JSONResult."""
        return list(self.values())

    def get_keys(self):
        """Obtiene todas las claves del objeto JSONResult."""
        return list(self.keys())

    def get_items(self):
        """Obtiene todos los pares clave-valor del objeto JSONResult."""
        return list(self.items())

    def get_host(self):
        return self.get('host')

    def get_address(self, host):
        address = host['address']
        if isinstance(address, dict):
            return address['@addr']
        elif isinstance(address, list):
            return address[0]['@addr']

    def get_os(self, host):
        try:
            os = host['os']['osmatch']
            if isinstance(os, dict):
                return os['@name']
            elif isinstance(os, list):
                return os[0]['@name']
        except TypeError:
            return "OS not found."

    def get_services(self, host):
        ports = host['ports']['port']
        services = {}
        for port in ports:
            services[port['@portid']] = port['service']['@name']
        return services
