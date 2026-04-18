from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

from requests import post

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
    params: Optional[KVSListParams] = Field(
        None, description="Parameters for the method"
    )


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


class KVS:
    def __init__(self, device_rpc_url: str):
        self.device_rpc_url = device_rpc_url

    def set(self, key: str, value: Any, etag: Optional[str] = None) -> KVSSetResponse:
        req = KVSSetRequest(id=1, params=KVSSetParams(key=key, value=value, etag=etag))
        response = post(self.device_rpc_url, json=req.model_dump())
        return KVSSetResponse(**response.json()["result"])

    def get(self, key: str) -> KVSGetResponse:
        req = KVSGetRequest(id=1, params=KVSGetParams(key=key))
        response = post(self.device_rpc_url, json=req.model_dump())
        return KVSGetResponse(**response.json()["result"])

    def get_many(self, match: Optional[str] = None) -> KVSGetManyResponse:
        req = KVSGetManyRequest(id=1, params=KVSGetManyParams(match=match))
        response = post(self.device_rpc_url, json=req.model_dump())
        return KVSGetManyResponse(**response.json()["result"])

    def list(self, match: Optional[str] = None) -> KVSListResponse:
        params = KVSListParams(match=match) if match is not None else None
        req = KVSListRequest(id=1, params=params)
        response = post(self.device_rpc_url, json=req.model_dump())
        return KVSListResponse(**response.json()["result"])

    def delete(self, key: str, etag: Optional[str] = None) -> KVSDeleteResponse:
        req = KVSDeleteRequest(id=1, params=KVSDeleteParams(key=key, etag=etag))
        response = post(self.device_rpc_url, json=req.model_dump())
        return KVSDeleteResponse(**response.json()["result"])
