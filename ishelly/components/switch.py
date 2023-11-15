from pydantic import BaseModel, Field
from typing import Optional, Union, Dict, Any, List

# Configuration
class SwitchConfig(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")
    name: Optional[Union[str, None]] = Field(None, description="Name of the switch instance")
    in_mode: str = Field(..., description="Mode of the associated input")
    initial_state: str = Field(..., description="Output state to set on power_on")
    auto_on: bool = Field(..., description="True if the 'Automatic ON' function is enabled, false otherwise")
    auto_on_delay: int = Field(..., description="Seconds to pass until the component is switched back on")
    auto_off: bool = Field(..., description="True if the 'Automatic OFF' function is enabled, false otherwise")
    auto_off_delay: int = Field(..., description="Seconds to pass until the component is switched back off")
    autorecover_voltage_errors: Optional[bool] = Field(None, description="True if switch output state should be restored after over/undervoltage error is cleared, false otherwise")
    input_id: Optional[int] = Field(None, description="Id of the Input component which controls the Switch")
    power_limit: Optional[int] = Field(None, description="Limit (in Watts) over which overpower condition occurs")
    voltage_limit: Optional[int] = Field(None, description="Limit (in Volts) over which overvoltage condition occurs")
    undervoltage_limit: Optional[int] = Field(None, description="Limit (in Volts) under which undervoltage condition occurs")
    current_limit: Optional[int] = Field(None, description="Limit (in Amperes) over which overcurrent condition occurs")

# Status
class ActiveEnergy(BaseModel):
    total: float = Field(..., description="Total energy consumed in Watt-hours")
    by_minute: List[float] = Field(..., description="Energy consumption by minute (in Milliwatt-hours) for the last three minutes")
    minute_ts: int = Field(..., description="Unix timestamp of the first second of the last minute (in UTC)")

class Temperature(BaseModel):
    tC: Optional[Union[float, None]] = Field(None, description="Temperature in Celsius")
    tF: Optional[Union[float, None]] = Field(None, description="Temperature in Fahrenheit")

class SwitchStatus(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")
    source: str = Field(..., description="Source of the last command")
    output: bool = Field(..., description="true if the output channel is currently on, false otherwise")
    timer_started_at: Optional[int] = Field(None, description="Unix timestamp, start time of the timer (in UTC)")
    timer_duration: Optional[int] = Field(None, description="Duration of the timer in seconds")
    apower: Optional[float] = Field(None, description="Last measured instantaneous active power (in Watts)")
    voltage: Optional[float] = Field(None, description="Last measured voltage in Volts")
    current: Optional[float] = Field(None, description="Last measured current in Amperes")
    pf: Optional[float] = Field(None, description="Last measured power factor")
    freq: Optional[float] = Field(None, description="Last measured network frequency in Hz")
    aenergy: Optional[ActiveEnergy] = Field(None, description="Information about the active energy counter")
    temperature: Optional[Temperature] = Field(None, description="Information about the temperature")
    errors: Optional[List[str]] = Field(None, description="Error conditions occurred")


# Methods
# Switch.Set
class SwitchSetParams(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")
    on: bool = Field(..., description="State to set the switch")
    toggle_after: Optional[int] = Field(None, description="Seconds to pass until the switch state is toggled")

class SwitchSetRequest(JSONRPCRequest):
    method: str = Field("Switch.Set", description="Method to be invoked")
    params: SwitchSetParams = Field(..., description="Parameters for the method") 

class SwitchSetResponse(BaseModel):
    was_on: bool = Field(..., description="True if the switch was on before the method was executed, false otherwise")

# Switch.Toggle
class SwitchToggleParams(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")

class SwitchToggleRequest(JSONRPCRequest):
    method: str = Field("Switch.Toggle", description="Method to be invoked")
    params: SwitchToggleParams = Field(..., description="Parameters for the method")

class SwitchToggleResponse(BaseModel):
    was_on: bool = Field(..., description="True if the switch was on before the method was executed, false otherwise")

# Switch.GetStatus
class SwitchGetStatusParams(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")

class SwitchGetStatusRequest(JSONRPCRequest):
    method: str = Field("Switch.GetStatus", description="Method to be invoked")
    params: SwitchGetStatusParams = Field(..., description="Parameters for the method")

# Switch.SetConfig
class SwitchSetConfigParams(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")
    config: SwitchConfig = Field(..., description="Configuration for the Switch")

class SwitchSetConfigRequest(JSONRPCRequest):
    method: str = Field("Switch.SetConfig", description="Method to be invoked")
    params: SwitchSetConfigParams = Field(..., description="Parameters for the method")

# Switch.GetConfig
class SwitchGetConfigParams(BaseModel):
    id: int = Field(..., description="Id of the Switch component instance")

class SwitchGetConfigRequest(JSONRPCRequest):
    method: str = Field("Switch.GetConfig", description="Method to be invoked")
    params: SwitchGetConfigParams = Field(..., description="Parameters for the method")




device_rpc_url = "http://192.168.1.26/rpc"
payload_id = 1
page = "Switch.Set"
values = {"id": 0, "on": True, "toggle_after": 10}
request = JSONRPCRequest(method=page, params=values, id=payload_id)

response = post(device_rpc_url, json=request)

# Create Pydantic model instance
switch_id = 0
req = SwitchSetRequest(
    id=1,
    params=SwitchSetParams(id=switch_id, on=True, toggle_after=10)
)
response = post(device_rpc_url, json=req.model_dump())

# Get status example
req = SwitchGetStatusRequest(
    id=1,
    params=SwitchGetStatusParams(id=0)
)
response = post(device_rpc_url, json=req.model_dump())
SwitchStatus(**response.json()["result"])


# set config example
req = SwitchSetConfigRequest(
    id=1,
    params=SwitchSetConfigParams(
        id=0,
        config=SwitchConfig(
            id=0,
            name="the best switch",
            in_mode="momentary",
            initial_state="on",
            auto_on=True,
            auto_on_delay=10,
            auto_off=False,
            auto_off_delay=20,
            # other fields...
        )
    )
)
response = post(device_rpc_url, json=req.model_dump())