# ishelly
A shelly api wrapper library which uses pydantic models to use the api and as much of the shelly v2 features as possible. No shelly v1 support planned.

## Supported Devices
At the moment the only device I have available for testing is the Shelly Plug US.

**Available Devices**
- Shelly Plug US


## Usage
```python
from ishelly.client import ShellyPlug

plug_1 = ShellyPlug("http://192.168.1.201")
plug_1.switch.get_status()
plug_1.switch.get_config()


# Toggle the relay output
plug_1.switch.toggle()

# Update the global config of the device
old_config = plug_1.switch.get_config()
new_config = old_config.model_copy()
new_config.initial_state = "on"
new_config.name = "electric burner #1"
# note: use the auto_off_delay as the control factor for a pid loop!!!
new_config.auto_off_delay = 25
plug_1.switch.set_config(new_config)

```