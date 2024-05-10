from rich.table import Table

from nettrackercore.core.controller import NettrackerDAO


class DBA:
    def __init__(self):
        self.dao = NettrackerDAO()

    def get_networks(self):
        networks_table = Table(title="Redes")
        networks = self.dao.get_all_networks()
        networks_table.add_column("ID", style="cyan")
        networks_table.add_column("Nombre", style="cyan")
        networks_table.add_column("Dirección de red", style="cyan")

        for network in networks:
            networks_table.add_row(network.network_id, network.network_name, network.address)
        return networks_table

    def get_network(self, network_name):
        network_table = Table(title="Red " + network_name)
        network = self.dao.get_network_from_name(network_name)
        network_table.add_column("ID", style="cyan")
        network_table.add_column("Nombre", style="cyan")
        network_table.add_column("Dirección de red", style="cyan")
        network_table.add_column("Puerta de enlace", style="cyan")
        network_table.add_column("Máscara de subred", style="cyan")
        network_table.add_column("Dispositivos", style="cyan")

        network_table.add_row(network.network_id, network.network_name, network.address, network.gateway.address,
                              str(network.subnet_mask), str(len(network.devices)))
        return network_table

    def get_devices(self, network_name):
        devices = self.dao.get_devices_from_network(network_name)
        devices_table = Table(title="Disposistivos de " + network_name)
        devices_table.add_column("ID", style="cyan")
        devices_table.add_column("Nombre", style="cyan")
        devices_table.add_column("Dirección IP", style="cyan")
        devices_table.add_column("Sistema operativo", style="cyan")
        devices_table.add_column("Servicios activos", style="cyan")

        for device in devices:
            devices_table.add_row(device.device_id, device.device_name, device.address, device.os_type,
                                  str(len(device.services)))
        return devices_table

    def get_services(self, network_name, device_address):
        device = self.dao.get_device_from_address(network_name, device_address)
        services_table = Table(title="Servicios activos")
        services_table.add_column("Nombre", style="cyan")
        services_table.add_column("Puerto", style="cyan")
        services_table.add_column("Protocolo", style="cyan")

        for service in device.services:
            services_table.add_row(service.name, str(service.port), service.protocol)
        return services_table
