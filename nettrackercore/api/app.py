from flask import Flask, jsonify, redirect
from flask_mongoengine import MongoEngine
from mongoengine import DoesNotExist

from nettrackercore.model.model import Network

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'db': 'nettracker-test', 'host': 'localhost', 'port': 27017, }
db = MongoEngine(app)


@app.route('/')
def home():
    return redirect('/networks')


@app.route('/networks', methods=['GET'])
def get_networks():
    networks = Network.objects().all()
    return jsonify(networks), 200


@app.route('/networks/<network_name>', methods=['GET'])
def get_network(network_name):
    network = Network.objects(network_name=network_name).first()
    if network:
        return jsonify(network), 200
    else:
        return jsonify({'error': 'Network not found'}), 404


@app.route('/networks/<network_name>/devices', methods=['GET'])
def get_devices(network_name):
    try:
        network = Network.objects(network_name=network_name).first()
        devices = network.devices
        return jsonify(devices), 200
    except AttributeError:
        return jsonify({'error': 'Network not found'}), 404


@app.route('/networks/<network_name>/devices/<address>', methods=['GET'])
def get_device_from_address(network_name, address):
    try:
        network = Network.objects.get(network_name=network_name)
        device = next((device for device in network.devices if device.address == address), None)
        if device:
            return jsonify(device.to_mongo()), 200
        else:
            return jsonify({'error': 'Device not found'}), 404
    except DoesNotExist:
        return jsonify({'error': 'Network not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
