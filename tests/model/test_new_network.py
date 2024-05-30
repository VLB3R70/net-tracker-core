import pytest
from mongoengine import *

from nettrackercore.model.model import *


@pytest.fixture(scope='function')
def db_connection():
    connect('nettracker-test', alias='new-network')
    yield
    disconnect('new-network')


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


def test_new_network(db_connection, sample_data):
    service1, service2, device1, device2, device3 = sample_data
    network = Network(network_id='1', network_name='network1', address='192.168.1.0', gateway=device1, subnet_mask=24,
                      devices=[device1, device2, device3])

    try:
        network.save()
    except Exception:
        pytest.fail('Could not save network')
