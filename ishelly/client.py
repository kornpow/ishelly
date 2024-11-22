from requests import post
from urllib.parse import urlparse


from ishelly.components.switch import *
from ishelly.components.schedule import *
from ishelly.components.shelly import *


class ShellyClient(object):
    def __init__(self, device_url):
        parsed_url = urlparse(device_url)
        if not parsed_url.scheme:
            device_url = f"http://{device_url}"
        self.device_api_url = f"{device_url}/rpc"
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



import socket
from urllib.parse import urlparse
from ishelly.components.shelly import ShellyGetDeviceInfoRequest, ShellyGetDeviceInfoParams
from requests import post
import requests
import ipaddress

import concurrent.futures

class ShellyDiscovery:
    def __init__(self, network_prefix="10.0.0.0/24"):
        self.network_prefix = network_prefix

    def discover_devices(self):
        print(f"Searching for Shelly devices on network: {self.network_prefix}")
        devices = []
        network = ipaddress.ip_network(self.network_prefix)
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self._check_device, ip) for ip in network.hosts()]
            for future in concurrent.futures.as_completed(futures):
                try:
                    device_url = future.result()
                    if device_url:
                        devices.append(device_url)
                except Exception as e:
                    pass
        return devices

    def _check_device(self, ip):
        device_url = f"http://{ip}/rpc"
        try:
            req = ShellyGetDeviceInfoRequest(
                id=1, params=ShellyGetDeviceInfoParams(ident=True)
            )
            response = post(device_url, json=req.model_dump(), timeout=2)
            # Check for valid response code and properly formatted response
            if response.status_code == 200 and "id" in response.json():
                return ip
        except (requests.exceptions.RequestException, socket.timeout):
            pass
        return None