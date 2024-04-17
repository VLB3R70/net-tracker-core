from results import JSONResult
from ..model.model import Device
from mongoengine import ValidationError


class DeviceDAO:
    def __init__(self, json_data: JSONResult):
        self.data = json_data

    def new_device(self):
        try:
            host = self.data.get_host()
            device = Device(
                device_id="",
                device_name="",
                address=self.data.get_address(host),
                netmask="",
                gateway="",
                services=self.data.get_services(host),
                os_type=self.data.get_os(host),
            )
            # device.save()
        except ValidationError as e:
            return e.message, False
