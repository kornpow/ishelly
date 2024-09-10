from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any, List


class BaseComponent:
    def __init__(self):
        pass


# Generic JSON-RPC Request
class JSONRPCRequest(BaseModel):
    jsonrpc: str = Field("2.0", description="JSON-RPC version")
    id: Optional[int] = Field(None, description="Unique identifier for the request")
    method: str = Field(..., description="Method to be invoked")
    params: Optional[Dict[str, Any]] = Field(
        None, description="Parameters for the method"
    )
