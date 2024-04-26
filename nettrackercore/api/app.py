from flask import Flask
from flask import jsonify
from flask_mongoengine import MongoEngine

from nettrackercore.model.model import Network

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'db': 'nettracker-test', 'host': 'localhost', 'port': 27017, }
db = MongoEngine(app)
db.init_app(app)


@app.route('/network', methods=['GET'])
def get_networks():
    networks = Network.objects().all()
    return jsonify(networks), 200


@app.route('/networks/<network_id>', methods=['GET'])
def get_network(network_id):
    network = Network.objects(network_id=network_id).first()
    if network:
        return jsonify(network), 200
    else:
        return jsonify({'error': 'Device not found'}), 404


if __name__ == '__main__':
    app.run(debug=False)
