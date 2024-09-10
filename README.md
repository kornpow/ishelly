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
```python
from pprint import pprint
from requests import post


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