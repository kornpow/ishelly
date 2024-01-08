from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from requests import post

from ishelly.components.base import JSONRPCRequest


# Schedule Object
class Schedule(BaseModel):
    id: int = Field(..., description="Id assigned to the job when it is created")
    enable: bool = Field(
        ..., description="True to enable the execution of this job, false otherwise"
    )
    timespec: str = Field(..., description="As defined by cron")
    calls: List[JSONRPCRequest] = Field(
        ...,
        description="RPC methods and arguments to be invoked when the job gets executed",
    )


# Schedule Create Request and Response
class ScheduleCreateParams(BaseModel):
    enable: bool = Field(
        True, description="True to enable the execution of this job, false otherwise"
    )
    timespec: str = Field(..., description="As defined by cron")
    calls: List[JSONRPCRequest] = Field(
        ...,
        description="RPC methods and arguments to be invoked when the job gets executed",
    )


class ScheduleCreateRequest(JSONRPCRequest):
    method: str = Field("Schedule.Create", description="Method to be invoked")
    params: ScheduleCreateParams = Field(..., description="Parameters for the method")


class ScheduleCreateResponse(BaseModel):
    id: int = Field(..., description="Id assigned to the created job")
    rev: int = Field(
        ..., description="Current revision number of the schedule instances"
    )


# Schedule Update Request and Response
class ScheduleUpdateParams(BaseModel):
    id: int = Field(..., description="Id assigned to the job when it is created")
    enable: bool = Field(
        True, description="True to enable the execution of this job, false otherwise"
    )
    timespec: str = Field(..., description="As defined by cron")
    calls: List[JSONRPCRequest] = Field(
        ...,
        description="RPC methods and arguments to be invoked when the job gets executed",
    )


class ScheduleUpdateRequest(JSONRPCRequest):
    method: str = Field("Schedule.Update", description="Method to be invoked")
    params: ScheduleUpdateParams = Field(..., description="Parameters for the method")


class ScheduleUpdateResponse(BaseModel):
    rev: int = Field(
        ..., description="Current revision number of the schedule instances"
    )


# Schedule.List Request and Response
class ScheduleListRequest(JSONRPCRequest):
    method: str = Field("Schedule.List", description="Method to be invoked")


class ScheduleListResponse(BaseModel):
    jobs: List[Schedule] = Field(..., description="List of schedule job objects")
    rev: int = Field(
        ..., description="Current revision number of the schedule instances"
    )


# Schedule.Delete Request and Response
class ScheduleDeleteParams(BaseModel):
    id: int = Field(..., description="Id of the job to be deleted")


class ScheduleDeleteRequest(JSONRPCRequest):
    method: str = Field("Schedule.Delete", description="Method to be invoked")
    params: ScheduleDeleteParams = Field(..., description="Parameters for the method")


class ScheduleDeleteResponse(BaseModel):
    rev: int = Field(
        ..., description="Current revision number of the schedule instances"
    )


# Schedule.DeleteAll Request and Response
class ScheduleDeleteAllRequest(JSONRPCRequest):
    method: str = Field("Schedule.DeleteAll", description="Method to be invoked")


class ScheduleDeleteAllResponse(BaseModel):
    rev: int = Field(
        ..., description="Current revision number of the schedule instances"
    )


# switch_id = 0
# job = SwitchToggleRequest(
#     id=1,
#     params=SwitchToggleParams(id=switch_id)
# )

# req = ScheduleCreateRequest(
#     id=1,
#     params=ScheduleCreateParams(
#         enable=True,
#         timespec="*/10 * * * * *",
#         calls=[job.model_dump()]
#     )
# )

# response = post(device_rpc_url, json=req.model_dump())


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


# req = ScheduleListRequest(id=1)
# response = post(device_rpc_url, json=req.model_dump())
# ScheduleListResponse(**response.json()["result"])


# req = ScheduleDeleteRequest(
#     id=1,
#     params=ScheduleDeleteParams(id=1)
# )
# response = post(device_rpc_url, json=req.model_dump())
# a = ScheduleDeleteResponse(**response.json()["result"])

# req = ScheduleDeleteAllRequest(id=1)
# response = post(device_rpc_url, json=req.model_dump())
# ScheduleDeleteAllResponse(**response.json()["result"])


class Scheduler():
    def __init__(self, device_rpc_url):
        self.device_rpc_url = device_rpc_url

    def create(self, enable: bool, timespec: str, calls: List[JSONRPCRequest]):
        new_schedule = ScheduleCreateParams(
                enable=enable, timespec=timespec, calls=calls
            )
        req = ScheduleCreateRequest(
            id=1,
            params=new_schedule
        )

        response = post(self.device_rpc_url, json=req.model_dump())
        schedule_create_1 = ScheduleCreateResponse(**response.json()["result"])
        return schedule_create_1

    def list(self):
        req = ScheduleListRequest(id=1)
        response = post(self.device_rpc_url, json=req.model_dump())
        scheduled_tasks = ScheduleListResponse(**response.json()["result"])
        return scheduled_tasks

    def update(self, id, enabled=None, timespec=None, calls=None):
        scheduled_tasks = self.list()
        power_control_active = True
        req = ScheduleUpdateRequest(
            id=1,
            params=ScheduleUpdateParams(
                id=id, enable=enabled, timespec=scheduled_tasks.jobs[0].timespec, calls=scheduled_tasks.jobs[0].calls
            ),
        )
        response = post(self.device_rpc_url, json=req.model_dump())
        schedule_update = ScheduleUpdateResponse(**response.json()["result"])
        return schedule_update

    def delete(self):
        pass

    def delete_all(self):
        pass
    