import json

from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import StringField, IntField, ListField, EmbeddedDocumentField


class Service(EmbeddedDocument):
    name = StringField(required=True)
    port = IntField(required=True)
    protocol = StringField(required=True)

    def to_json(self):
        return json.dumps(self.to_mongo(), indent=4)


class Device(EmbeddedDocument):
    device_id = StringField(primary_key=True)
    device_name = StringField(required=True)
    address = StringField(required=True)
    services = ListField(EmbeddedDocumentField(Service))
    os_type = StringField(required=True)

    def to_json(self):
        return json.dumps(self.to_mongo(), indent=4)


class Network(Document):
    network_id = StringField(primary_key=True)
    network_name = StringField(required=True)
    address = StringField(required=True)
    gateway = EmbeddedDocumentField(Device, required=True)
    subnet_mask = IntField(required=True)
    devices = ListField(EmbeddedDocumentField(Device), required=True)

    def to_json(self):
        return json.dumps(self.to_mongo(), indent=4)
