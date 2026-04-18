from pydantic import BaseModel, Field
from requests import post
from typing import Optional, List, Any, Dict

from ishelly.components.base import JSONRPCRequest


# Shared models
class WebhookCondition(BaseModel):
    name: str = Field(..., description="Condition name (e.g. 'Switch.on')")
    condition: Optional[str] = Field(None, description="Optional filter expression")
    repeat_period: Optional[int] = Field(
        None, description="Minimum seconds between repeated triggers (0 = always)"
    )


class WebhookInfo(BaseModel):
    id: int = Field(..., description="Id of the webhook")
    cid: int = Field(..., description="Id of the component that owns this webhook")
    enable: bool = Field(..., description="True if the webhook is enabled")
    event: str = Field(..., description="Event that triggers the webhook")
    name: Optional[str] = Field(None, description="Name of the webhook")
    ssl_ca: Optional[str] = Field(
        None, description="CA certificate for SSL verification"
    )
    urls: List[str] = Field(..., description="List of URLs to call")
    active_between: Optional[List[str]] = Field(
        None, description="Time range during which the webhook is active"
    )
    condition: Optional[str] = Field(None, description="Optional filter expression")
    repeat_period: Optional[int] = Field(
        None, description="Minimum seconds between repeated triggers"
    )


# Webhook.Create
class WebhookCreateParams(BaseModel):
    cid: int = Field(..., description="Id of the component that owns this webhook")
    enable: bool = Field(..., description="True to enable the webhook")
    event: str = Field(..., description="Event that triggers the webhook")
    name: Optional[str] = Field(None, description="Name of the webhook")
    ssl_ca: Optional[str] = Field(
        None, description="CA certificate for SSL verification"
    )
    urls: List[str] = Field(..., description="List of URLs to call on trigger")
    active_between: Optional[List[str]] = Field(
        None, description="Time range during which the webhook is active"
    )
    condition: Optional[str] = Field(None, description="Optional filter expression")
    repeat_period: Optional[int] = Field(
        None, description="Minimum seconds between repeated triggers (0 = always)"
    )


class WebhookCreateRequest(JSONRPCRequest):
    method: str = Field("Webhook.Create", description="Method to be invoked")
    params: WebhookCreateParams = Field(..., description="Parameters for the method")


class WebhookCreateResponse(BaseModel):
    id: int = Field(..., description="Id of the created webhook")


# Webhook.Update
class WebhookUpdateParams(BaseModel):
    id: int = Field(..., description="Id of the webhook to update")
    enable: Optional[bool] = Field(None, description="True to enable the webhook")
    event: Optional[str] = Field(None, description="Event that triggers the webhook")
    name: Optional[str] = Field(None, description="Name of the webhook")
    ssl_ca: Optional[str] = Field(
        None, description="CA certificate for SSL verification"
    )
    urls: Optional[List[str]] = Field(
        None, description="List of URLs to call on trigger"
    )
    active_between: Optional[List[str]] = Field(
        None, description="Time range during which the webhook is active"
    )
    condition: Optional[str] = Field(None, description="Optional filter expression")
    repeat_period: Optional[int] = Field(
        None, description="Minimum seconds between repeated triggers"
    )


class WebhookUpdateRequest(JSONRPCRequest):
    method: str = Field("Webhook.Update", description="Method to be invoked")
    params: WebhookUpdateParams = Field(..., description="Parameters for the method")


# Webhook.Delete
class WebhookDeleteParams(BaseModel):
    id: int = Field(..., description="Id of the webhook to delete")


class WebhookDeleteRequest(JSONRPCRequest):
    method: str = Field("Webhook.Delete", description="Method to be invoked")
    params: WebhookDeleteParams = Field(..., description="Parameters for the method")


# Webhook.List
class WebhookListRequest(JSONRPCRequest):
    method: str = Field("Webhook.List", description="Method to be invoked")
    params: dict = Field(default_factory=dict, description="No parameters needed")


class WebhookListResponse(BaseModel):
    hooks: List[WebhookInfo] = Field(..., description="List of webhooks on the device")
    rev: int = Field(..., description="Revision number of the webhook list")


# Webhook.GetStatus
class WebhookGetStatusRequest(JSONRPCRequest):
    method: str = Field("Webhook.GetStatus", description="Method to be invoked")
    params: dict = Field(default_factory=dict, description="No parameters needed")


class WebhookStatusItem(BaseModel):
    id: int = Field(..., description="Id of the webhook")
    last_errors: Optional[List[str]] = Field(None, description="Last delivery errors")
    last_ok: Optional[float] = Field(
        None, description="Unix timestamp of last successful delivery"
    )


class WebhookGetStatusResponse(BaseModel):
    hooks: List[WebhookStatusItem] = Field(..., description="Status for each webhook")
    rev: int = Field(..., description="Revision number")


class Webhook:
    def __init__(self, device_rpc_url: str):
        self.device_rpc_url = device_rpc_url

    def create(self, params: WebhookCreateParams) -> WebhookCreateResponse:
        req = WebhookCreateRequest(id=1, params=params)
        response = post(self.device_rpc_url, json=req.model_dump())
        return WebhookCreateResponse(**response.json()["result"])

    def update(self, params: WebhookUpdateParams) -> None:
        req = WebhookUpdateRequest(id=1, params=params)
        post(self.device_rpc_url, json=req.model_dump())

    def delete(self, webhook_id: int) -> None:
        req = WebhookDeleteRequest(id=1, params=WebhookDeleteParams(id=webhook_id))
        post(self.device_rpc_url, json=req.model_dump())

    def list(self) -> WebhookListResponse:
        req = WebhookListRequest(id=1)
        response = post(self.device_rpc_url, json=req.model_dump())
        return WebhookListResponse(**response.json()["result"])

    def get_status(self) -> WebhookGetStatusResponse:
        req = WebhookGetStatusRequest(id=1)
        response = post(self.device_rpc_url, json=req.model_dump())
        return WebhookGetStatusResponse(**response.json()["result"])
