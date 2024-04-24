from mongoengine import connect

from results import JSONResult
from ..model.model import Network


class NettrackerDAO:
    def __init__(self, json_data: JSONResult):
        self.data = json_data
        connect("nettracker-test")

    # en construcción
    def new_network(self):
        network = Network(
            network_name="",
            address="",
            gateway="",
            subnet_mask="",
            devices=""
        ).modify(upsert=True, new=True)
