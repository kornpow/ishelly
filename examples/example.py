from pprint import pprint
from requests import post


from ishelly.components.switch import SwitchToggleRequest, SwitchToggleParams, SwitchSetRequest, SwitchSetParams
from ishelly.components.schedule import ScheduleCreateRequest, ScheduleCreateParams, ScheduleListRequest, ScheduleListResponse

device_rpc_url = "http://192.168.1.200/rpc"

switch_id = 0
job = SwitchSetRequest(
    id=1,
    params=SwitchSetParams(id=switch_id, toggle_after=3600, on=True)
)

## cron jobs!
# every 2 hours
timespec1 = "0 0 */2 * * *"
# every 2 hours between 8am and 6pm
timespec2 = "0 8-18/2 * * * *"

# create a new scheduled task
req = ScheduleCreateRequest(
    id=1, 
    params=ScheduleCreateParams(
        enable=True, 
        timespec=timespec1, 
        calls=[job.model_dump()]
    )
)

response = post(device_rpc_url, json=req.model_dump())


req = ScheduleCreateRequest(
    id=1, 
    params=ScheduleCreateParams(
        enable=True, 
        timespec=timespec2, 
        calls=[job.model_dump()]
    )
)

response = post(device_rpc_url, json=req.model_dump())

# update an existing scheduled task
# req = ScheduleUpdateRequest(
#     id=1, 
#     params=ScheduleUpdateParams(
#         id=1,
#         enable=False, 
#         timespec="*/5 * * * * *", 
#         calls=[job.model_dump()]
#     )
# )
# response = post(device_rpc_url, json=req.model_dump())


# List scheduled tasks
req = ScheduleListRequest(id=1)
response = post(device_rpc_url, json=req.model_dump())
scheduled_tasks = ScheduleListResponse(**response.json()["result"])

print(f"There are {len(scheduled_tasks.jobs)} scheduled tasks currently saved.")