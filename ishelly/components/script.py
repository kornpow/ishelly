from pydantic import BaseModel, Field
from requests import post
from typing import Optional, List, Any

from ishelly.components.base import JSONRPCRequest


# Script.Create
class ScriptCreateParams(BaseModel):
    name: str = Field(..., description="Name of the script")


class ScriptCreateRequest(JSONRPCRequest):
    method: str = Field("Script.Create", description="Method to be invoked")
    params: ScriptCreateParams = Field(..., description="Parameters for the method")


class ScriptCreateResponse(BaseModel):
    id: int = Field(..., description="Id of the created script")


# Script.Delete
class ScriptDeleteParams(BaseModel):
    id: int = Field(..., description="Id of the script")


class ScriptDeleteRequest(JSONRPCRequest):
    method: str = Field("Script.Delete", description="Method to be invoked")
    params: ScriptDeleteParams = Field(..., description="Parameters for the method")


# Script.PutCode
class ScriptPutCodeParams(BaseModel):
    id: int = Field(..., description="Id of the script")
    code: str = Field(..., description="JavaScript code to upload")
    append: Optional[bool] = Field(
        None, description="If true, append to existing code instead of replacing"
    )


class ScriptPutCodeRequest(JSONRPCRequest):
    method: str = Field("Script.PutCode", description="Method to be invoked")
    params: ScriptPutCodeParams = Field(..., description="Parameters for the method")


class ScriptPutCodeResponse(BaseModel):
    len: int = Field(..., description="Number of bytes written")


# Script.GetCode
class ScriptGetCodeParams(BaseModel):
    id: int = Field(..., description="Id of the script")
    offset: Optional[int] = Field(None, description="Byte offset to start reading from")


class ScriptGetCodeRequest(JSONRPCRequest):
    method: str = Field("Script.GetCode", description="Method to be invoked")
    params: ScriptGetCodeParams = Field(..., description="Parameters for the method")


class ScriptGetCodeResponse(BaseModel):
    data: str = Field(..., description="Code chunk")
    left: int = Field(..., description="Bytes remaining after this chunk")


# Script.Start
class ScriptStartParams(BaseModel):
    id: int = Field(..., description="Id of the script")


class ScriptStartRequest(JSONRPCRequest):
    method: str = Field("Script.Start", description="Method to be invoked")
    params: ScriptStartParams = Field(..., description="Parameters for the method")


class ScriptStartResponse(BaseModel):
    was_running: bool = Field(
        ..., description="True if the script was already running before this call"
    )


# Script.Stop
class ScriptStopParams(BaseModel):
    id: int = Field(..., description="Id of the script")


class ScriptStopRequest(JSONRPCRequest):
    method: str = Field("Script.Stop", description="Method to be invoked")
    params: ScriptStopParams = Field(..., description="Parameters for the method")


class ScriptStopResponse(BaseModel):
    was_running: bool = Field(
        ..., description="True if the script was running before this call"
    )


# Script.Eval
class ScriptEvalParams(BaseModel):
    id: int = Field(..., description="Id of the script")
    code: str = Field(..., description="JavaScript expression to evaluate")


class ScriptEvalRequest(JSONRPCRequest):
    method: str = Field("Script.Eval", description="Method to be invoked")
    params: ScriptEvalParams = Field(..., description="Parameters for the method")


class ScriptEvalResponse(BaseModel):
    result: Any = Field(..., description="Return value of the evaluated expression")


# Script.List
class ScriptInfo(BaseModel):
    id: int = Field(..., description="Id of the script")
    name: str = Field(..., description="Name of the script")
    enable: bool = Field(..., description="True if the script is set to run on boot")
    running: bool = Field(..., description="True if the script is currently running")


class ScriptListRequest(JSONRPCRequest):
    method: str = Field("Script.List", description="Method to be invoked")
    params: dict = Field(default_factory=dict, description="No parameters needed")


class ScriptListResponse(BaseModel):
    scripts: List[ScriptInfo] = Field(..., description="List of scripts on the device")


# Script.GetStatus
class ScriptGetStatusParams(BaseModel):
    id: int = Field(..., description="Id of the script")


class ScriptGetStatusRequest(JSONRPCRequest):
    method: str = Field("Script.GetStatus", description="Method to be invoked")
    params: ScriptGetStatusParams = Field(..., description="Parameters for the method")


class ScriptStatus(BaseModel):
    id: int = Field(..., description="Id of the script")
    running: bool = Field(..., description="True if the script is currently running")
    errors: Optional[List[str]] = Field(None, description="Error conditions")


# Script.GetConfig / Script.SetConfig
class ScriptConfig(BaseModel):
    id: int = Field(..., description="Id of the script")
    name: str = Field(..., description="Name of the script")
    enable: bool = Field(
        ..., description="True if the script should start automatically on boot"
    )


class ScriptGetConfigParams(BaseModel):
    id: int = Field(..., description="Id of the script")


class ScriptGetConfigRequest(JSONRPCRequest):
    method: str = Field("Script.GetConfig", description="Method to be invoked")
    params: ScriptGetConfigParams = Field(..., description="Parameters for the method")


class ScriptSetConfigParams(BaseModel):
    id: int = Field(..., description="Id of the script")
    config: ScriptConfig = Field(..., description="New configuration for the script")


class ScriptSetConfigRequest(JSONRPCRequest):
    method: str = Field("Script.SetConfig", description="Method to be invoked")
    params: ScriptSetConfigParams = Field(..., description="Parameters for the method")


class ScriptSetConfigResponse(BaseModel):
    restart_required: bool = Field(
        ..., description="True if a restart is required to apply the new configuration"
    )


class Script:
    def __init__(self, device_rpc_url: str):
        self.device_rpc_url = device_rpc_url

    def create(self, name: str) -> ScriptCreateResponse:
        req = ScriptCreateRequest(id=1, params=ScriptCreateParams(name=name))
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptCreateResponse(**response.json()["result"])

    def delete(self, script_id: int) -> None:
        req = ScriptDeleteRequest(id=1, params=ScriptDeleteParams(id=script_id))
        post(self.device_rpc_url, json=req.model_dump())

    def put_code(
        self, script_id: int, code: str, append: bool = False
    ) -> ScriptPutCodeResponse:
        req = ScriptPutCodeRequest(
            id=1,
            params=ScriptPutCodeParams(id=script_id, code=code, append=append or None),
        )
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptPutCodeResponse(**response.json()["result"])

    def get_code(
        self, script_id: int, offset: Optional[int] = None
    ) -> ScriptGetCodeResponse:
        req = ScriptGetCodeRequest(
            id=1, params=ScriptGetCodeParams(id=script_id, offset=offset)
        )
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptGetCodeResponse(**response.json()["result"])

    def start(self, script_id: int) -> ScriptStartResponse:
        req = ScriptStartRequest(id=1, params=ScriptStartParams(id=script_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptStartResponse(**response.json()["result"])

    def stop(self, script_id: int) -> ScriptStopResponse:
        req = ScriptStopRequest(id=1, params=ScriptStopParams(id=script_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptStopResponse(**response.json()["result"])

    def eval(self, script_id: int, code: str) -> ScriptEvalResponse:
        req = ScriptEvalRequest(id=1, params=ScriptEvalParams(id=script_id, code=code))
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptEvalResponse(**response.json()["result"])

    def list(self) -> ScriptListResponse:
        req = ScriptListRequest(id=1)
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptListResponse(**response.json()["result"])

    def get_status(self, script_id: int) -> ScriptStatus:
        req = ScriptGetStatusRequest(id=1, params=ScriptGetStatusParams(id=script_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptStatus(**response.json()["result"])

    def get_config(self, script_id: int) -> ScriptConfig:
        req = ScriptGetConfigRequest(id=1, params=ScriptGetConfigParams(id=script_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptConfig(**response.json()["result"])

    def set_config(
        self, script_id: int, config: ScriptConfig
    ) -> ScriptSetConfigResponse:
        req = ScriptSetConfigRequest(
            id=1, params=ScriptSetConfigParams(id=script_id, config=config)
        )
        response = post(self.device_rpc_url, json=req.model_dump())
        return ScriptSetConfigResponse(**response.json()["result"])
