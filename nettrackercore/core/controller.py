from hashlib import sha256

from mongoengine import connect, DoesNotExist

from nettrackercore.core.results import JSONResult
from nettrackercore.model.model import Device, Service, Network


class NettrackerDAO:
    def __init__(self, json_data: JSONResult):
        self.data = json_data
        connect("nettracker-test")

    def __build_services(self, host):
        services = self.data.get_services(host)
        service_list = []

        if not isinstance(services, list):
            return service_list  # Devuelve una lista vacía si los servicios no son válidos

        for service_data in services:
            if not isinstance(service_data, dict):
                continue  # Salta los datos de servicio no válidos

            service = self.__build_service_from_data(service_data)
            service_list.append(service)

        return service_list

    def __build_service_from_data(self, service_data):
        name = service_data.get('name')
        port = service_data.get('port')
        protocol = service_data.get('protocol')

        if None in (name, port, protocol):
            return None  # Devuelve None si falta alguno de los campos requeridos

        service = Service(
            name=name,
            port=port,
            protocol=protocol
        )
        return service

    def __build_devices(self):
        hosts = self.data.get_host()
        device_list = []

        if not isinstance(hosts, list):
            return device_list  # Devuelve una lista vacía si no hay hosts

        for host in hosts:
            device = self.__build_device_from_host(host)
            device_list.append(device)

        return device_list

    def __build_device_from_host(self, host):
        device_name = self.data.get_hostname(host)
        address = self.data.get_address(host)
        os_type = self.data.get_os(host) if isinstance(self.data.get_os(host), str) else ''
        device_id = sha256(f"{device_name}_{address}".encode()).hexdigest()

        device = Device(
            device_name=device_name,
            address=address,
            os_type=os_type,
            services=self.__build_services(host),
            device_id=device_id
        )
        return device

    def new_network(self, name: str, address: str, submask: int):
        network_id = sha256(f'{name}_{address}_{submask}'.encode()).hexdigest()
        devices = self.__build_devices()
        Network(
            network_id=network_id,
            network_name=name,
            address=address,
            gateway='',
            subnet_mask=submask,
            devices=devices
        ).save(force_insert=True)  # se obliga a realizar una inserción

    @staticmethod
    def get_all_networks():
        return Network.objects.only('network_name')

    @staticmethod
    def get_network_from_name(name):
        return Network.objects(network_name=name).first()

    @staticmethod
    def get_devices_from_network(network_name):
        network = Network.objects(network_name=network_name).first()
        return network.devices if network else []

    @staticmethod
    def get_device_from_address(network_name, address):
        network = Network.objects(network_name=network_name).first()
        if network:
            for device in network.devices:
                if device.address == address:
                    return device
        raise DoesNotExist

