from flask import Flask, jsonify, redirect
from flask_mongoengine import MongoEngine
from mongoengine import DoesNotExist

from nettrackercore.config import Configuration
from nettrackercore.core.controller import NettrackerDAO

config = Configuration()

db = MongoEngine()
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'db': config.data['db'], 'host': config.data['db_host'], 'port': config.data['db_port'], }
db.init_app(app)


@app.route('/')
def home():
    return redirect('/networks')


@app.route('/networks', methods=['GET'])
def get_networks():
    networks = NettrackerDAO.get_all_networks()
    return jsonify(networks), 200


@app.route('/networks/<network_name>', methods=['GET'])
def get_network(network_name):
    network = NettrackerDAO.get_network_from_name(network_name)
    if network:
        return jsonify(network), 200
    else:
        return jsonify({'error': 'Network not found'}), 404


@app.route('/networks/<network_name>/devices', methods=['GET'])
def get_devices(network_name):
    try:
        devices = NettrackerDAO.get_devices_from_network(network_name)
        return jsonify(devices), 200
    except AttributeError:
        return jsonify({'error': 'Network not found'}), 404


@app.route('/networks/<network_name>/devices/<address>', methods=['GET'])
def get_device_from_address(network_name, address):
    try:
        device = NettrackerDAO.get_device_from_address(network_name, address)
        if device:
            return jsonify(device), 200
        else:
            return jsonify({'error': 'Device not found'}), 404
    except DoesNotExist:
        return jsonify({'error': 'Network not found'}), 404


if __name__ == '__main__':
    app.run()
