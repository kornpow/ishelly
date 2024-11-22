import pytest
from ishelly.client import ShellyPlug, Shelly2PM, ShellyPro4PM

class MockDeviceInfo:
    gen = "gen_mock"
    app = "app_mock"

@pytest.fixture
def mock_get_device_info(monkeypatch):
    def mock_get_device_info_func(self):
        return MockDeviceInfo()
    monkeypatch.setattr("ishelly.client.ShellyClient.get_device_info", mock_get_device_info_func)

@pytest.fixture
def shelly_plug(mock_get_device_info):
    return ShellyPlug("http://10.0.0.1")

@pytest.fixture
def shelly_2pm(mock_get_device_info):
    return Shelly2PM("http://10.0.0.2")

@pytest.fixture
def shelly_pro_4pm(mock_get_device_info):
    return ShellyPro4PM("http://10.0.0.3")

def test_shelly_plug_initialization(shelly_plug):
    assert isinstance(shelly_plug, ShellyPlug)

def test_shelly_2pm_initialization(shelly_2pm):
    assert isinstance(shelly_2pm, Shelly2PM)

def test_shelly_pro_4pm_initialization(shelly_pro_4pm):
    assert isinstance(shelly_pro_4pm, ShellyPro4PM)
