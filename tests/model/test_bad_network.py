import pytest
from mongoengine import *

from nettrackercore.core.parsers import NmapParser
from nettrackercore.model.model import *


@pytest.fixture(scope='function')
def db_connection():
    connect('nettracker-test', alias='bad-network')
    yield
    disconnect('bad-network')


@pytest.fixture
def parser():
    return NmapParser()


@pytest.fixture
def sample_data():
    service1 = Service(name='service_name1', port=1234, protocol='tcp')
    service2 = Service(name='service_name2', port=4321, protocol='udp')

    device1 = Device(device_id='1', device_name='device1', address='192.168.1.1', services=[service1, service2],
                     os_type='Linux')
    device2 = Device(device_id='2', device_name='device2', address='192.168.1.2', services=[service1, service2],
                     os_type='Linux')
    device3 = Device(device_id='3', device_name='device3', address='192.168.1.3', services=[service1],
                     os_type='Windows')
    return service1, service2, device1, device2, device3


def test_bad_network_address(db_connection, parser, sample_data):
    service1, service2, device1, device2, device3 = sample_data
    network = Network(network_id='1', network_name='network1', address='pepe', gateway=device1, subnet_mask=24,
                      devices=[device1, device2, device3])

    if not parser.validate_address(network.address):
        assert True


def test_bad_network_format(db_connection, sample_data):
    service1, service2, device1, device2, device3 = sample_data
    network = Network(network_id=7, network_name=110010, address='pepe', gateway=device1, subnet_mask=24,
                      devices=[device1, device2, device3])

    with pytest.raises(ValidationError):
        network.save()


def test_bad_network_save(db_connection):
    with pytest.raises(ValidationError):
        network = Network()
        network.save()


def test_invalid_operation(db_connection, sample_data):
    service1, service2, device1, device2, device3 = sample_data
    with pytest.raises(AttributeError):
        service1.save()
