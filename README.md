# ishelly
A shelly api wrapper library which uses pydantic models to use the api and as much of the shelly v2 features as possible. No shelly v1 support planned.

This library was built with the support of the LightningSpore open-source mushroom growing project: 
- https://lightningspore.com
- https://github.com/lightningspore/mushroom-monorepo

## Supported Devices

**Available Devices**
- Shelly Plug US
- Shelly 2PM
- Shelly Pro 4PM

## Install
```bash
pip install ishelly
```


## Usage
### Switch Control
```python
from ishelly.components.switch import *
from ishelly.components.schedule import *
from ishelly.components.shelly import *
from ishelly.client import ShellyPlug, Shelly2PM, ShellyPro4PM

# Initialize a Shelly Pro 4PM device object
plug_pro = ShellyPro4PM("http://192.168.1.125")

# Switch IDs for the high power outlets
switch_id_high_power_1 = 0
switch_id_high_power_2 = 3

# Step 1: Create a schedule to turn on the high power outlet 1 every 5 minutes
timespec_on = "0 */5 * * * *"
turn_on = SwitchSetRequest(
    id=1,
    params=SwitchSetParams(id=switch_id_high_power_1, toggle_after=90, on=True),
)

# Step 2: Add the scheduled task to the device
plug_pro.schedule.create(enable=True, timespec=timespec_on, calls=[turn_on])


# Step 3: Print the current schedules on the device
current_schedule = plug_pro.schedule.list()
for task in current_schedule.jobs:
    print(task)


# Step 4: Update an existing schedule (ID 4) to turn on the high power outlet 1 every 5 minutes
plug_pro.schedule.update(4, False, "0 */5 * * * *", calls=[turn_on])

# Step 5: Delete the schedule with ID 4
plug_pro.schedule.delete(4)
```

### JavaScript Scripts

Shelly Gen2 devices can run JavaScript scripts on-device. Scripts can toggle outputs,
respond to events, run timers, and more. Up to 3 scripts can run simultaneously.

> **Upload limit**: The device accepts at most ~8 KB per `PutCode` call. For larger
> scripts use `put_code_from_file`, which automatically splits the file into 1024-byte
> chunks using the `append` flag — matching Shelly's own recommended tooling.

#### Inline script (small scripts)

```python
from ishelly.client import ShellyPlug
from ishelly.components.script import ScriptConfig

plug = ShellyPlug("192.168.1.38")

# 1. Create a script slot
s = plug.script.create("1min-cycle")

# 2. Upload JavaScript code
CODE = """
var on = true;
function cycle() {
  Shelly.call("Switch.Set", {id: 0, on: on}, null, null);
  on = !on;
  Timer.set(60000, false, cycle, null);
}
cycle();
"""
plug.script.put_code(s.id, CODE)

# 3. Enable auto-start on boot
cfg = ScriptConfig(id=s.id, name="1min-cycle", enable=True)
plug.script.set_config(s.id, cfg)

# 4. Start it now
plug.script.start(s.id)
```

#### Upload from a file (large scripts)

```python
from ishelly.client import ShellyPlug
from ishelly.components.script import ScriptConfig

plug = ShellyPlug("192.168.1.38")

s = plug.script.create("my-script")

# Uploads in 1024-byte chunks automatically
total_bytes = plug.script.put_code_from_file(s.id, "my_script.js")
print(f"Uploaded {total_bytes} bytes")

cfg = ScriptConfig(id=s.id, name="my-script", enable=True)
plug.script.set_config(s.id, cfg)
plug.script.start(s.id)
```

#### Managing scripts

```python
# List all scripts
for script in plug.script.list().scripts:
    print(script.id, script.name, "running:", script.running)

# Check status (memory usage, errors)
status = plug.script.get_status(1)
print(f"running={status.running} mem_used={status.mem_used} mem_free={status.mem_free}")

# Stop and delete
plug.script.stop(1)
plug.script.delete(1)
```

### Device Discovery
```python
from ishelly.client import ShellyDiscovery
discovery = ShellyDiscovery("10.0.0.0/24")
discovery.discover_devices()
```


## Example
The above example code, and more is located at: [examples](examples)

---

## Alternatives

| Library | PyPI | Style | Gen2 | Notes |
|---|---|---|---|---|
| **aioshelly** | [`aioshelly`](https://pypi.org/project/aioshelly/) | async (`asyncio`) | ✅ | Official Home Assistant library. Actively maintained. Requires Python ≥ 3.11. No Pydantic models — designed for HA integration, not general scripting. |
| **pyShelly** | [`pyShelly`](https://pypi.org/project/pyShelly/) | sync | ⚠️ partial | Gen1-focused. Last release Dec 2024. Less comprehensive Gen2 support. |

**ishelly** is the right choice if you want:
- Synchronous, script-friendly API (no `async/await` boilerplate)
- Typed Pydantic models for all requests and responses
- Full Gen2 component coverage: Switch, Schedule, KVS, Script, Webhook
- Python 3.9+

