from rich.table import Table

from nettrackercore.config import Translator, Configuration
from nettrackercore.core.controller import NettrackerDAO

config = Configuration()
translator = Translator()


class DBA:
    """
    El objeto **DBA** se encarga de realizar consultas a la base de datos mediante
    :py:class:`~nettrackercore.core.controller.NettrackerDAO` y mostrar los resultados en forma de tabla para el
    usuario. Como la base de datos no es relacional, los datos que se muestran en las tablas son simples. Para datos más
    complejos como las listas u objetos dentro del modelo se usan comandos específicos.
    """

    def __init__(self, db_name=config.data['db'], alias='main-nettracker'):
        self.dao = NettrackerDAO(db_name=db_name, alias=alias)

    def get_networks(self):
        """
        Este método devuelve una tabla con el resultado de obtener todas las redes de la base de datos. Los datos que se
        muestran son: el identificador, el nombre dado y la dirección de red. Esta información es necesaria para poder
        realizar otras consultas.

        :return: Una tabla con las redes de la base de datos.
        :rtype: :py:class:`~rich.table.Table`
        """
        networks_table = Table(title=translator._("Redes"))
        networks = self.dao.get_all_networks()
        networks_table.add_column(translator._("ID"), style="cyan")
        networks_table.add_column(translator._("Nombre"), style="cyan")
        networks_table.add_column(translator._("Dirección de red"), style="cyan")

        for network in networks:
            networks_table.add_row(network.network_id, network.network_name, network.address)
        return networks_table

    def get_network(self, network_name):
        """
        Este método se encarga de obtener el resultado completo de una red específica y muestra en forma de tabla el
        mismo. Dentro del modelo de datos la puerta de enlace dentro de una red corresponde a un objeto, este valor es
        demasiado complejo para `~rich.table.Table` por lo que solo se muestra la dirección de IP del dispositivo. En el
        caso de la lista de dispositivos ocurre lo mismo por lo que solo se muestra el número total de valores de la
        lista. Se necesita un nombre de red para realizar la consulta.

        :param network_name: es el nombre de la red
        :type network_name: str
        :return: Una tabla con la información completa de una red.
        :rtype: :py:class:`~rich.table.Table`
        """
        network_table = Table(title=translator._("Red {network_name}").format(network_name=network_name))
        network = self.dao.get_network_from_name(network_name)
        network_table.add_column(translator._("ID"), style="cyan")
        network_table.add_column(translator._("Nombre"), style="cyan")
        network_table.add_column(translator._("Dirección de red"), style="cyan")
        network_table.add_column(translator._("Puerta de enlace"), style="cyan")
        network_table.add_column(translator._("Máscara de subred"), style="cyan")
        network_table.add_column(translator._("Dispositivos"), style="cyan")

        network_table.add_row(network.network_id, network.network_name, network.address, network.gateway.address,
                              str(network.subnet_mask), str(len(network.devices)))
        return network_table

    def get_devices(self, network_name):
        """
        Este método se encarga de obtener la lista de dispositivos de una red determinada y los devuelve en forma de
        tabla. En este caso, se muestra el número total de servicios activos, ya que dentro del modelo de datos los
        servicios objetos y esto es un valor demasiado complejo para `~rich.table.Table`.

        :param network_name: es el nombre de la red
        :type network_name: str
        :return: Una tabla con la información de los dispositivos
        :rtype: :py:class:`~rich.table.Table`
        """
        devices = self.dao.get_devices_from_network(network_name)
        devices_table = Table(title=translator._("Disposistivos de {network_name}").format(network_name=network_name))
        devices_table.add_column(translator._("ID"), style="cyan")
        devices_table.add_column(translator._("Nombre"), style="cyan")
        devices_table.add_column(translator._("Dirección IP"), style="cyan")
        devices_table.add_column(translator._("Sistema operativo"), style="cyan")
        devices_table.add_column(translator._("Servicios activos"), style="cyan")

        for device in devices:
            devices_table.add_row(device.device_id, device.device_name, device.address, device.os_type,
                                  str(len(device.services)))
        return devices_table

    def get_services(self, network_name, device_address):
        """
        Este método se encarga de obtener los servicios activos de un dispositivo determinado en una red determinada y
        los muestra en forma de tabla. Se muestra el nombre del servicio, el número del puerto y el protocolo en el que
        está trabajando.

        :param network_name: es el nombre de la red
        :param device_address: es la dirección IP del dispositivo
        :type network_name: str
        :type device_address: str

        :return: Una tabla con la información de los servicios
        :rtype: :py:class:`~rich.table.Table`
        """
        device = self.dao.get_device_from_address(network_name, device_address)
        services_table = Table(
            title=translator._("Servicios activos del dispositivo {device_address} dentro de {network_name}").format(
                device_address=device_address, network_name=network_name))
        services_table.add_column(translator._("Nombre"), style="cyan")
        services_table.add_column(translator._("Puerto"), style="cyan")
        services_table.add_column(translator._("Protocolo"), style="cyan")

        for service in device.services:
            services_table.add_row(service.name, str(service.port), service.protocol)
        return services_table
