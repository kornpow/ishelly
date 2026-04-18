import json
import pytest
from unittest.mock import MagicMock, patch

from ishelly.client import ShellyPlug, Shelly2PM, ShellyPro4PM
from ishelly.components.switch import SwitchSetParams


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class MockDeviceInfo:
    gen = 2
    app = "PlugUS"


def make_response(result: dict):
    """Return a mock requests.Response whose .json() returns the given result envelope."""
    mock = MagicMock()
    mock.status_code = 200
    mock.json.return_value = {"id": 1, "result": result}
    return mock


DEVICE_INFO_RESPONSE = {
    "name": None,
    "id": "shellyplugus-083af20074a0",
    "mac": "083AF20074A0",
    "slot": 1,
    "model": "SNPL-00116US",
    "gen": 2,
    "fw_id": "20260120-145258/1.7.4-gf9878b6",
    "ver": "1.7.4",
    "app": "PlugUS",
    "auth_en": False,
    "auth_domain": None,
}

SWITCH_STATUS_RESPONSE = {
    "id": 0,
    "source": "HTTP_in",
    "output": True,
    "apower": 5.4,
    "voltage": 121.9,
    "current": 0.079,
    "aenergy": {
        "total": 752227.797,
        "by_minute": [89.185, 89.742, 89.185],
        "minute_ts": 1776480240,
    },
    "temperature": {"tC": 42.5, "tF": 108.6},
}

SWITCH_CONFIG_RESPONSE = {
    "id": 0,
    "name": "Pressure Cooker",
    "initial_state": "off",
    "auto_on": False,
    "auto_on_delay": 60.0,
    "auto_off": False,
    "auto_off_delay": 60.0,
    "power_limit": 4480,
    "voltage_limit": 280,
    "autorecover_voltage_errors": False,
    "current_limit": 16.0,
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_get_device_info(monkeypatch):
    def _mock(self):
        return MockDeviceInfo()

    monkeypatch.setattr("ishelly.client.ShellyClient.get_device_info", _mock)


@pytest.fixture
def shelly_plug(mock_get_device_info):
    return ShellyPlug("http://10.0.0.1")


@pytest.fixture
def shelly_2pm(mock_get_device_info):
    return Shelly2PM("http://10.0.0.2")


@pytest.fixture
def shelly_pro_4pm(mock_get_device_info):
    return ShellyPro4PM("http://10.0.0.3")


# ---------------------------------------------------------------------------
# Initialization tests
# ---------------------------------------------------------------------------


def test_shelly_plug_initialization(shelly_plug):
    assert isinstance(shelly_plug, ShellyPlug)


def test_shelly_2pm_initialization(shelly_2pm):
    assert isinstance(shelly_2pm, Shelly2PM)


def test_shelly_pro_4pm_initialization(shelly_pro_4pm):
    assert isinstance(shelly_pro_4pm, ShellyPro4PM)


def test_shelly_plug_has_switch_and_schedule(shelly_plug):
    from ishelly.components.switch import Switch
    from ishelly.components.schedule import Scheduler
    from ishelly.components.kvs import KVS

    assert isinstance(shelly_plug.switch, Switch)
    assert isinstance(shelly_plug.schedule, Scheduler)
    assert isinstance(shelly_plug.kvs, KVS)


def test_shelly_2pm_has_two_switches(shelly_2pm):
    assert len(shelly_2pm.switch) == 2
    assert shelly_2pm.switch[0].switch_id == 0
    assert shelly_2pm.switch[1].switch_id == 1


def test_shelly_pro_4pm_has_four_switches(shelly_pro_4pm):
    assert len(shelly_pro_4pm.switch) == 4


# ---------------------------------------------------------------------------
# Switch operation tests (HTTP mocked)
# ---------------------------------------------------------------------------


def test_switch_get_status(shelly_plug):
    with patch("ishelly.components.switch.post") as mock_post:
        mock_post.return_value = make_response(SWITCH_STATUS_RESPONSE)
        status = shelly_plug.switch.get_status()
    assert status.output is True
    assert status.apower == 5.4
    assert status.voltage == 121.9
    assert status.temperature.tC == 42.5


def test_switch_set_on(shelly_plug):
    with patch("ishelly.components.switch.post") as mock_post:
        mock_post.return_value = make_response({"was_on": False})
        result = shelly_plug.switch.set(SwitchSetParams(id=0, on=True))
    assert result.was_on is False
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Switch.Set"
    assert call_body["params"]["on"] is True


def test_switch_toggle(shelly_plug):
    with patch("ishelly.components.switch.post") as mock_post:
        mock_post.return_value = make_response({"was_on": True})
        result = shelly_plug.switch.toggle()
    assert result.was_on is True
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Switch.Toggle"


def test_switch_get_config(shelly_plug):
    with patch("ishelly.components.switch.post") as mock_post:
        mock_post.return_value = make_response(SWITCH_CONFIG_RESPONSE)
        config = shelly_plug.switch.get_config()
    assert config.name == "Pressure Cooker"
    assert config.auto_on_delay == 60.0
    assert config.current_limit == 16.0


def test_switch_reset_counters(shelly_plug):
    reset_response = {"aenergy": {"total": 752227.797}}
    with patch("ishelly.components.switch.post") as mock_post:
        mock_post.return_value = make_response(reset_response)
        result = shelly_plug.switch.reset_counters()
    assert result.aenergy.total == 752227.797
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Switch.ResetCounters"


# ---------------------------------------------------------------------------
# KVS operation tests (HTTP mocked)
# ---------------------------------------------------------------------------


def test_kvs_set(shelly_plug):
    with patch("ishelly.components.kvs.post") as mock_post:
        mock_post.return_value = make_response({"etag": "abc123==", "rev": 1})
        result = shelly_plug.kvs.set("mykey", "myvalue")
    assert result.etag == "abc123=="
    assert result.rev == 1


def test_kvs_get(shelly_plug):
    with patch("ishelly.components.kvs.post") as mock_post:
        mock_post.return_value = make_response({"etag": "abc123==", "value": "myvalue"})
        result = shelly_plug.kvs.get("mykey")
    assert result.value == "myvalue"


def test_kvs_delete(shelly_plug):
    with patch("ishelly.components.kvs.post") as mock_post:
        mock_post.return_value = make_response({"rev": 2})
        result = shelly_plug.kvs.delete("mykey")
    assert result.rev == 2


# ---------------------------------------------------------------------------
# Schedule operation tests (HTTP mocked)
# ---------------------------------------------------------------------------


def test_schedule_list_empty(shelly_plug):
    with patch("ishelly.components.schedule.post") as mock_post:
        mock_post.return_value = make_response({"jobs": [], "rev": 0})
        result = shelly_plug.schedule.list()
    assert result.jobs == []


def test_schedule_delete_all(shelly_plug):
    with patch("ishelly.components.schedule.post") as mock_post:
        mock_post.return_value = make_response({"rev": 5})
        result = shelly_plug.schedule.delete_all()
    assert result.rev == 5
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Schedule.DeleteAll"


# ---------------------------------------------------------------------------
# get_device_info (HTTP mocked)
# ---------------------------------------------------------------------------


def test_get_device_info():
    with patch("ishelly.client.post") as mock_post:
        mock_post.return_value = make_response(DEVICE_INFO_RESPONSE)
        plug = ShellyPlug.__new__(ShellyPlug)
        plug.device_api_url = "http://10.0.0.1/rpc"
        info = plug.get_device_info()
    assert info.gen == 2
    assert info.app == "PlugUS"
    assert info.mac == "083AF20074A0"


# ---------------------------------------------------------------------------
# Script operation tests (HTTP mocked)
# ---------------------------------------------------------------------------


def test_script_create(shelly_plug):
    with patch("ishelly.components.script.post") as mock_post:
        mock_post.return_value = make_response({"id": 1})
        result = shelly_plug.script.create("my-timer")
    assert result.id == 1
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Script.Create"
    assert call_body["params"]["name"] == "my-timer"


def test_script_put_code(shelly_plug):
    with patch("ishelly.components.script.post") as mock_post:
        mock_post.return_value = make_response({"len": 42})
        result = shelly_plug.script.put_code(1, "print('hello')")
    assert result.len == 42
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Script.PutCode"


def test_script_start(shelly_plug):
    with patch("ishelly.components.script.post") as mock_post:
        mock_post.return_value = make_response({"was_running": False})
        result = shelly_plug.script.start(1)
    assert result.was_running is False
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Script.Start"


def test_script_stop(shelly_plug):
    with patch("ishelly.components.script.post") as mock_post:
        mock_post.return_value = make_response({"was_running": True})
        result = shelly_plug.script.stop(1)
    assert result.was_running is True
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Script.Stop"


def test_script_list(shelly_plug):
    scripts_response = {
        "scripts": [{"id": 1, "name": "my-timer", "enable": True, "running": True}]
    }
    with patch("ishelly.components.script.post") as mock_post:
        mock_post.return_value = make_response(scripts_response)
        result = shelly_plug.script.list()
    assert len(result.scripts) == 1
    assert result.scripts[0].name == "my-timer"
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Script.List"


def test_shelly_plug_has_script_and_webhook(shelly_plug):
    from ishelly.components.script import Script
    from ishelly.components.webhook import Webhook

    assert isinstance(shelly_plug.script, Script)
    assert isinstance(shelly_plug.webhook, Webhook)


# ---------------------------------------------------------------------------
# Webhook operation tests (HTTP mocked)
# ---------------------------------------------------------------------------


def test_webhook_create(shelly_plug):
    from ishelly.components.webhook import WebhookCreateParams

    params = WebhookCreateParams(
        cid=0,
        enable=True,
        event="switch.on",
        urls=["http://example.com/notify"],
    )
    with patch("ishelly.components.webhook.post") as mock_post:
        mock_post.return_value = make_response({"id": 3})
        result = shelly_plug.webhook.create(params)
    assert result.id == 3
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Webhook.Create"


def test_webhook_list(shelly_plug):
    hooks_response = {
        "hooks": [
            {
                "id": 3,
                "cid": 0,
                "enable": True,
                "event": "switch.on",
                "urls": ["http://example.com/notify"],
            }
        ],
        "rev": 1,
    }
    with patch("ishelly.components.webhook.post") as mock_post:
        mock_post.return_value = make_response(hooks_response)
        result = shelly_plug.webhook.list()
    assert len(result.hooks) == 1
    assert result.hooks[0].event == "switch.on"
    call_body = mock_post.call_args[1]["json"]
    assert call_body["method"] == "Webhook.List"
