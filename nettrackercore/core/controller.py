from hashlib import sha256

from mongoengine import connect

from nettrackercore.core.results import JSONResult
from nettrackercore.model.model import Device, Service, Network


class NettrackerDAO:
    def __init__(self, json_data: JSONResult):
        self.data = json_data
        connect("nettracker-test")

    def __build_services(self, host):
        services = self.data.get_services(host)
        service_list = []

        if isinstance(services, list):
            for service_data in services:
                service = Service(
                    name=service_data['name'],
                    port=service_data['port'],
                    protocol=service_data['protocol']
                )
                service_list.append(service)

        return service_list

    def __build_devices(self):
        hosts = self.data.get_host()
        device_list = []

        if isinstance(hosts, list):
            for host in hosts:
                device = Device(
                    device_name=self.data.get_hostname(host),
                    address=self.data.get_address(host),
                    os_type=self.data.get_os(host) if isinstance(self.data.get_os(host), str) else '',
                    services=self.__build_services(host),
                    device_id=sha256(
                        f"{self.data.get_hostname(host)}_{self.data.get_address(host)}".encode()).hexdigest()
                )
                device_list.append(device)
        return device_list

    def new_network(self, name: str, address: str, submask: int):
        network_id = sha256(f'{name}_{address}_{submask}'.encode()).hexdigest()
        devices = self.__build_devices()
        Network.objects(
            network_id=network_id,
            network_name=name,
            address=address,
            subnet_mask=submask
        ).modify(
            upsert=True,
            new=True,
            add_to_set__devices=devices
        )
