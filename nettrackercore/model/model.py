from mongoengine import Document, StringField, ListField, DictField, EmbeddedDocument, EmbeddedDocumentField, IntField


class Device(EmbeddedDocument):
    device_id = StringField(primary_key=True)
    device_name = StringField(required=True)
    address = StringField(required=True)
    netmask = IntField(required=True)
    gateway = StringField(required=True)
    services = ListField(DictField(required=True))
    os_type = StringField(required=True)


class Network(Document):
    network_id = StringField(primary_key=True)
    network_name = StringField(required=True)
    address = StringField(required=True)
    subnet_mask = IntField(required=True)
    devices = ListField(EmbeddedDocumentField(Device), required=True)
