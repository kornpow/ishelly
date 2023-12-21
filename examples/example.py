from pprint import pprint
from requests import post


from ishelly.components.switch import *
# (
#     SwitchToggleRequest,
#     SwitchToggleParams,
#     SwitchSetRequest,
#     SwitchSetParams,
# )
from ishelly.components.schedule import *
from ishelly.components.shelly import *

# (
#     ScheduleCreateRequest,
#     ScheduleCreateParams,
#     ScheduleUpdateRequest,
#     ScheduleUpdateParams,
#     ScheduleUpdateResponse,
#     ScheduleListRequest,
#     ScheduleListResponse,
# )

device_rpc_url = "http://192.168.1.201/rpc"

switch_id = 0
SECONDS_IN_HOUR = 3600
job = SwitchSetRequest(
    id=1,
    params=SwitchSetParams(id=switch_id, toggle_after=2 * SECONDS_IN_HOUR, on=True),
)

## cron jobs!
# every 2 hours
timespec1 = "0 0 10 * * *"
# every 2 hours between 8am and 6pm
timespec2 = "0 */8 * * * *"

# CREATE NEW scheduled tasks
req = ScheduleCreateRequest(
    id=1,
    params=ScheduleCreateParams(
        enable=True, timespec=timespec1, calls=[job.model_dump()]
    ),
)

response = post(device_rpc_url, json=req.model_dump())
schedule_create_1 = ScheduleCreateResponse(**response.json()["result"])

req = ScheduleCreateRequest(
    id=1,
    params=ScheduleCreateParams(
        enable=True, timespec=timespec2, calls=[job.model_dump()]
    ),
)

response = post(device_rpc_url, json=req.model_dump())
schedule_create_2 = ScheduleCreateResponse(**response.json()["result"])

### UPDATE existing scheduled task
timespec_updated = "0 0 11 * * *"
req = ScheduleUpdateRequest(
    id=1,
    params=ScheduleUpdateParams(
        id=1, enable=True, timespec=timespec_updated, calls=[job.model_dump()]
    ),
)
response = post(device_rpc_url, json=req.model_dump())
schedule_update = ScheduleUpdateResponse(**response.json()["result"])


### LIST scheduled tasks
req = ScheduleListRequest(id=1)
response = post(device_rpc_url, json=req.model_dump())
scheduled_tasks = ScheduleListResponse(**response.json()["result"])

print(f"There are {len(scheduled_tasks.jobs)} scheduled tasks currently saved.")

### DELETE a scheduled task
req = ScheduleDeleteRequest(
    id=1,
    params=ScheduleDeleteParams(id=3),
)
response = post(device_rpc_url, json=req.model_dump())
schedule_delete = ScheduleDeleteResponse(**response.json()["result"])


### GET STATUS of SWITCH
req = SwitchGetStatusRequest(
    id=1,
    params=SwitchGetStatusParams(id=0)
)
response = post(device_rpc_url, json=req.model_dump())
SwitchStatus(**response.json()["result"])