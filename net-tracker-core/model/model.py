class Network:
    def __init__(self, name, ip, subnet_mask):
        self.name = name
        self.ip = ip
        self.subnet_mask = subnet_mask
        self.devices = []

    def asignar_dispositivo(self, device):
        self.devices.append(device.to_dict())

    def to_dict(self):
        return {
            "Name": self.name,
            "IP": self.ip,
            "Subnet_mask": self.subnet_mask,
            "Devices": [device.to_dict() for device in self.devices]
        }


class Device:
    def __init__(self, name, ip, subnet_mask, gateway, services, os):
        self.name = name
        self.ip = ip
        self.subnet_mask = subnet_mask
        self.gateway = gateway
        self.services = services
        self.OS = os

    def to_dict(self):
        return {
            "Name": self.name,
            "IP": self.ip,
            "Subnet_mask": self.subnet_mask,
            "Gateway": self.gateway,
            "Services": self.services,
            "OS": self.OS
        }
