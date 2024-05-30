from rich.table import Table

from nettrackercore.core.dba import DBA

dba = DBA('nettracker', 'dba-test')


def test_get_networks():
    networks = dba.get_networks()
    assert isinstance(networks, Table)


def test_get_network():
    network = dba.get_network('redCasa')
    assert isinstance(network, Table)


def test_get_devices():
    devices = dba.get_devices('redCasa')
    assert isinstance(devices, Table)


def test_get_services():
    services = dba.get_services('redCasa', '192.168.1.1')
    assert isinstance(services, Table)
