import json

from rich.table import Table

from nettrackercore.core.controller import NettrackerDAO


class DBA:
    def __init__(self):
        self.dao = NettrackerDAO()

    def get_networks(self):
        networks = self.dao.get_all_networks()
        return networks.to_json()

    def get_network(self, network_name):
        network = self.dao.get_network_from_name(network_name)
        return network.to_json()

    def get_devices(self, network_name):
        devices = self.dao.get_devices_from_network(network_name)
        return devices

    def get_device(self, network_name, device_address):
        device = self.dao.get_device_from_address(network_name=network_name, address=device_address)
        return device.to_json()
