from requests import post

from ishelly.components.switch import *
from ishelly.components.schedule import *
from ishelly.components.shelly import *


class ShellyClient(object):
    def __init__(self, device_url):
        self.device_api_url = device_url + "/rpc"
        self.shelly_gen = None
        self.shelly_app = None
        device_info = self.get_device_info()
        self.shelly_gen = device_info.gen
        self.shelly_app = device_info.app

    def get_device_info(self):
        print("Getting device info")
        req = ShellyGetDeviceInfoRequest(
            id=1, params=ShellyGetDeviceInfoParams(ident=True)
        )
        response = post(self.device_api_url, json=req.model_dump())
        shelly_get_device_info_response = ShellyGetDeviceInfoResponse(
            **response.json()["result"]
        )
        return shelly_get_device_info_response


class ShellyPlug(ShellyClient):
    def __init__(self, device_url):
        super().__init__(device_url)
        print("Base init completed")
        self.switch = Switch(self.device_api_url, 0)
        self.schedule = Scheduler(self.device_api_url)


class Shelly2PM(ShellyClient):
    def __init__(self, device_url):
        super().__init__(device_url)
        print("Base init completed")
        self.switch = [Switch(self.device_api_url, 0), Switch(self.device_api_url, 1)]
        self.schedule = Scheduler(self.device_api_url)


class ShellyPro4PM(ShellyClient):
    def __init__(self, device_url):
        super().__init__(device_url)
        print("Base init completed")
        self.switch = [
            Switch(self.device_api_url, 0),
            Switch(self.device_api_url, 1),
            Switch(self.device_api_url, 2),
            Switch(self.device_api_url, 3),
        ]
        self.schedule = Scheduler(self.device_api_url)
