from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union, List

from ishelly.components.base import JSONRPCRequest


# Shelly.ListMethods
class ShellyListMethodsRequest(JSONRPCRequest):
    method: str = Field("Shelly.ListMethods", description="Method to be invoked")
    params: Optional[Dict[str, Any]] = Field(
        None, description="Parameters for the method"
    )


class ShellyListMethodsResponse(BaseModel):
    methods: List[str] = Field(..., description="Names of the methods allowed")


# Shelly.GetDeviceInfo
class ShellyGetDeviceInfoParams(BaseModel):
    ident: Optional[bool] = Field(
        None,
        description="Flag specifying if extra identifying information should be displayed",
    )


class ShellyGetDeviceInfoRequest(JSONRPCRequest):
    method: str = Field("Shelly.GetDeviceInfo", description="Method to be invoked")
    params: ShellyGetDeviceInfoParams = Field(
        ..., description="Parameters for the method"
    )


class ShellyGetDeviceInfoResponse(BaseModel):
    id: str = Field(..., description="Id of the device")
    mac: str = Field(..., description="Mac address of the device")
    model: str = Field(..., description="Model of the device")
    gen: int = Field(..., description="Generation of the device")
    fw_id: str = Field(..., description="Id of the firmware of the device")
    ver: str = Field(..., description="Version of the firmware of the device")
    app: str = Field(..., description="Application name")
    profile: Optional[str] = Field(None, description="Name of the device profile")
    auth_en: bool = Field(
        ..., description="True if authentication is enabled, false otherwise"
    )
    auth_domain: Optional[Union[str, None]] = Field(
        None, description="Name of the domain"
    )
    discoverable: Optional[bool] = Field(
        None, description="If true, device is shown in 'Discovered devices'"
    )
    key: Optional[str] = Field(None, description="Cloud key of the device")
    batch: Optional[str] = Field(None, description="Batch used to provision the device")
    fw_sbits: Optional[str] = Field(None, description="Shelly internal flags")


# Example usage
# Building request model
# req = ShellyListMethodsRequest(id=1)

# response = post(device_rpc_url, json=req.model_dump())
# shelly_list_methods_response = ShellyListMethodsResponse(**response.json()["result"])

# req = ShellyGetDeviceInfoRequest(id=1, params=ShellyGetDeviceInfoParams(ident=True))
# response = post(device_rpc_url, json=req.model_dump())
# shelly_get_device_info_response = ShellyGetDeviceInfoResponse(
#     **response.json()["result"]
# )
