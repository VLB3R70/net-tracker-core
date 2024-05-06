from nettrackercore.core.controller import NettrackerDAO


class DBA:
    def __init__(self, dao: NettrackerDAO):
        self.dao = dao

    def get_networks(self):
        pass

    def get_network(self, network_name):
        pass

    def get_devices(self, network_name):
        pass

    def get_device(self, device_address):
        pass
