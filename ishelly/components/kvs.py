from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from ishelly.components.base import JSONRPCRequest


# KVS.Set
class KVSSetParams(BaseModel):
    key: str = Field(..., description="The key to be added or updated")
    value: Any = Field(..., description="Value for the key")
    etag: Optional[str] = Field(
        None, description="Generated hash uniquely identifying the key-value pair"
    )


class KVSSetRequest(JSONRPCRequest):
    method: str = Field("KVS.Set", description="Method to be invoked")
    params: KVSSetParams = Field(..., description="Parameters for the method")


class KVSSetResponse(BaseModel):
    etag: str = Field(
        ..., description="Generated hash of the newly created or updated item"
    )
    rev: int = Field(..., description="Revision of the store (after update)")


# KVS.Get
class KVSGetParams(BaseModel):
    key: str = Field(..., description="The key to be looked up")


class KVSGetRequest(JSONRPCRequest):
    method: str = Field("KVS.Get", description="Method to be invoked")
    params: KVSGetParams = Field(..., description="Parameters for the method")


class KVSGetResponse(BaseModel):
    etag: str = Field(..., description="Generated hash of the requested item")
    value: Any = Field(..., description="The value for the key")


# KVS.GetMany
class KVSGetManyParams(BaseModel):
    match: Optional[str] = Field(
        None, description="Pattern against which keys are matched"
    )


class KVSGetManyRequest(JSONRPCRequest):
    method: str = Field("KVS.GetMany", description="Method to be invoked")
    params: KVSGetManyParams = Field(..., description="Parameters for the method")


class KVSGetManyResponse(BaseModel):
    items: Dict[str, Dict[str, Any]] = Field(
        ..., description="JSON object containing a set of JSON objects"
    )


# KVS.List
class KVSListParams(BaseModel):
    match: Optional[str] = Field(
        None, description="Pattern against which keys are matched"
    )


class KVSListRequest(JSONRPCRequest):
    method: str = Field("KVS.List", description="Method to be invoked")
    params: KVSListParams = Field(..., description="Parameters for the method")


class KVSListResponse(BaseModel):
    keys: Dict[str, str] = Field(
        ..., description="Keys matched against the requested pattern"
    )
    rev: int = Field(..., description="Current revision of the store")


# KVS.Delete
class KVSDeleteParams(BaseModel):
    key: str = Field(..., description="The key to be deleted")
    etag: Optional[str] = Field(
        None, description="Generated hash uniquely identifying the key-value pair"
    )


class KVSDeleteRequest(JSONRPCRequest):
    method: str = Field("KVS.Delete", description="Method to be invoked")
    params: KVSDeleteParams = Field(..., description="Parameters for the method")


class KVSDeleteResponse(BaseModel):
    rev: int = Field(..., description="Revision of the store (after delete)")


req = KVSSetRequest(id=1, params=KVSSetParams(key="sample_key1", value="sample_value1"))

response = post(device_rpc_url, json=req.model_dump())
kvs_set_response = KVSSetResponse(**response.json()["result"])

req = KVSGetRequest(id=1, params=KVSGetParams(key="sample_key"))
response = post(device_rpc_url, json=req.model_dump())


req = KVSGetManyRequest(id=1, params=KVSGetManyParams(key="sample_key*"))
response = post(device_rpc_url, json=req.model_dump())
kvs_getmany_response = KVSGetManyResponse(**response.json()["result"])


req = KVSDeleteRequest(
    id=1, params=KVSDeleteParams(key="sample_key", etag="0E8HnTToCT8e6BNK29wR1UGA==")
)
response = post(device_rpc_url, json=req.model_dump())
kvs_delete_response = KVSDeleteResponse(**response.json()["result"])
