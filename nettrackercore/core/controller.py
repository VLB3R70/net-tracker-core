from hashlib import sha256

from mongoengine import connect, DoesNotExist

from nettrackercore.core.results import JSONResult
from nettrackercore.model.model import Device, Service, Network


class NettrackerDAO:
    """
    El objeto **NettrackerDAO** corresponde al objeto de acceso a datos, más conocido como DAO(Data Access Object). Este
    objeto es el encargado de realizar las llamadas a la base de datos mediante el módulo
    `mongoengine <https://docs.mongoengine.org/index.html>`_, el cual es un ODM (Object-Document Mapper) y nos permite
    operar con la base de datos de forma más sencilla.

    Este objeto trabaja con el resultado obtenido del escaneo en forma del
    objeto :py:class:`~nettrackercore.core.results.JSONResult`.
    """

    def __init__(self, json_data: JSONResult = None):
        self.data = json_data
        connect("nettracker-test")

    def __build_services(self, host):
        """
        Este método es el encargado de obtener la lista de servicios del host designado y devuelve una lista de objetos
        :py:class:`~nettrackercore.model.model.Service`. Si el host con el que se está trabajando no tiene servicios
        abiertos o el escáner no ha encontrado ninguno la lista se devuelve vacía. El valor obtenido del objeto `JSONResult`
        corresponde a una lista diccionarios con los datos de los servicios. Dicha lista se recorre y se desgrana la
        información de cada servicio para crear nuevos objetos.
        Para mejorar la legibilidad del método se hace una llamada a un método complementario que devuelve los servicios
        en forma de objetos.

        :param host: Es el valor correspondiente al host dentro del objeto :py:class:`~nettrackercore.core.results.JSONResult`.
        :type host: dict
        :return: Lista de objetos :py:class:`~nettrackercore.model.model.Service`
        :rtype: list[Service | None]
        """
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
        """
        Este método obtiene la información de los servicios dentro de un host y devuelve un objeto
        :py:class:`~nettrackercore.model.model.Service`.

        :param service_data: Corresponde a un diccionario con los datos de los servicios.
        :type service_data: dict
        :return: Un objeto :py:class:`~nettrackercore.model.model.Service`
        :rtype: Service | None
        """
        name = service_data.get('name')
        port = service_data.get('port')
        protocol = service_data.get('protocol')

        if None in (name, port, protocol):
            return None  # Devuelve None si falta alguno de los campos requeridos

        service = Service(name=name, port=port, protocol=protocol)
        return service

    def __build_devices(self):
        """
        Este método se encarga de obtener la lista completa con los dispositivos y toda su información. Primero se
        obtienen los `hosts` dentro del objeto :py:class:`~nettrackercore.core.results.JSONResult`, lo cual
        corresponde a una lista y posteriormente se obtiene el objeto :py:class:`~nettrackercore.model.model.Device`
        después de hacer una llamada al método complementario
        :py:func:`~nettrackercore.core.controller.NettrackerDAO.__build_device_from_host`.

        :return: Lista de objetos :py:class:`~nettrackercore.model.model.Device`
        :rtype: list[Device]
        """
        hosts = self.data.get_host()
        device_list = []

        if not isinstance(hosts, list):
            return device_list  # Devuelve una lista vacía si no hay hosts

        for host in hosts:
            device = self.__build_device_from_host(host)
            device_list.append(device)

        return device_list

    def __build_device_from_host(self, host):
        """
        Este método es uno complementario que se encarga de devolover un objeto :py:class:`~nettrackercore.model.model.Device`.
        Los datos del objeto se obtienen desde :py:class:`~nettrackercore.core.results.JSONResult`.

        :param host: Es el valor del host obtenido del objeto :py:class:`~nettrackercore.core.results.JSONResult`
        :type host: dict
        :return: Un objeto :py:class:`~nettrackercore.model.model.Device`
        :rtype: Device
        """
        device_name = self.data.get_hostname(host)
        address = self.data.get_address(host)
        os_type = self.data.get_os(host) if isinstance(self.data.get_os(host), str) else ''
        device_id = sha256(f"{device_name}_{address}".encode()).hexdigest()

        device = Device(device_name=device_name, address=address, os_type=os_type, services=self.__build_services(host),
                        device_id=device_id)
        return device

    def __build_gateway(self):
        """
        Dentro de la lógica de la base de datos la puerta de enlace de la red corresponde a un
        objeto :py:class:`~nettrackercore.model.model.Device`. Generalmente las puertas de enlace tienen un nombre como:
        `gateway` o parecido.
        El método recorre todos los dispositivos ya definidos en el método
        :py:func:`~nettrackercore.core.controller.NettrackerDAO.__build_devices` y comprueba su nombre, si es como el
        indicado anteriormente devuelve dicho objeto.

        :return: Un objeto :py:class:`~nettrackercore.model.model.Device`
        :rtype: Device | None
        """
        devices = self.__build_devices()
        for device in devices:
            if 'gateway' in device.device_name:
                return device
        return ''

    def new_network(self, name: str, address: str, submask: int):
        """
        Este método realiza una operación CRUD de creación de un nuevo registro en la base de datos. Los datos obtenidos
        por parámetros son definidos por el usuario durante la ejecución del programa, el resto deben ser obtenidos con
        los métodos pseudo-privados complementarios.
        La operación fuerza la inserción en la base de datos ya que `mongoengine` permite la operación `upsert`. Si la
        operación sufre algún error será posteriormente capturada en el programa.

        :param name: El nombre de la red. Debe ser único.
        :type name: str
        :param address: La dirección de red a guardar.
        :type address: str
        :param submask: La dirección de la máscara de red en forma numérica.
        :type submask: int
        """
        network_id = sha256(f'{name}_{address}_{submask}'.encode()).hexdigest()
        devices = self.__build_devices()
        gateway = self.__build_gateway()
        network = (
            Network(network_id=network_id, network_name=name, address=address, gateway=gateway, subnet_mask=submask, devices=devices))
        network.save(force_insert=True)  # se obliga a realizar una inserción

    def update_network(self, name: str, address: str, submask: int):
        """
        Este método se encarga de actualizar los valores de la base de datos a los últimos obtenidos en el escaneo. La
        operación de actualización es atómica por lo que se actualizará todo el documento y sus valores.  De esta forma
        siempre nos aseguramos de tener la información más actualizada posible.
        """
        network_id = sha256(f'{name}_{address}_{submask}'.encode()).hexdigest()
        devices = self.__build_devices()
        gateway = self.__build_gateway()
        network = Network.objects.get(network_id=network_id)
        network.update(network_name=name, address=address, gateway=gateway, subnet_mask=submask, devices=devices)

    @staticmethod
    def get_all_networks():
        """
        Este método realiza una consulta a la base de datos para obtener el id y el nombre de todas las redes.
        :return: Se devuelve el resultado de la consulta realizada
        :rtype: :py:class:`~mongoengine.queryset.queryset.QuerySet`
        """
        return Network.objects.all()

    @staticmethod
    def get_network_from_name(name):
        """
        Este método obtiene la información de una red específica por su nombre.
        :param name: El nombre de la red.
        :type name: str
        :return: Se devuelve el resultado de la consulta realizada
        :rtype: Network
        """
        return Network.objects(network_name=name).first()

    @staticmethod
    def get_devices_from_network(network_name):
        """
        Este método obtiene todos los dispositivos dentro de una red específica.
        :param network_name: El nombre de la red.
        :type network_name: str
        :return: Se devuelve el resultado de la consulta realizada. Si no existen disopsitivos se devuelve una lista vacía
        :rtype: :py:class:`~mongoengine.base.datastructures.BaseList` | list
        """
        network = Network.objects(network_name=network_name).first()
        return network.devices if network else []

    @staticmethod
    def get_device_from_address(network_name, address):
        """
        Este método obtiene la información de un dispositivo específico dentro de una red también específica.
        :param network_name: El nombre de la red.
        :type network_name: str
        :param address: La dirección de red del dispositivo.
        :type address: str

        :return: La información del dispositivo específico.
        :rtype: nettrackercore.model.model.Device
        """
        network = Network.objects(network_name=network_name).first()
        if network:
            for device in network.devices:
                if device.address == address:
                    return device
        raise DoesNotExist
