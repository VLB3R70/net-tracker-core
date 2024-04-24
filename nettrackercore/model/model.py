from mongoengine import Document, StringField, ListField, EmbeddedDocument, EmbeddedDocumentField, IntField


class Service(EmbeddedDocument):
    name = StringField(required=True)
    port = IntField(required=True)
    protocol = StringField(required=True)


class Device(EmbeddedDocument):
    device_id = StringField(primary_key=True)
    device_name = StringField(required=True)
    address = StringField(required=True)
    services = ListField(EmbeddedDocumentField(Service))
    os_type = StringField(required=True)


class Network(Document):
    network_id = StringField(primary_key=True)
    network_name = StringField(required=True)
    address = StringField(required=True)
    gateway = StringField(required=True)
    subnet_mask = IntField(required=True)
    devices = ListField(EmbeddedDocumentField(Device), required=True)
