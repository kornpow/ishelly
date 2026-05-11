from pydantic import BaseModel, Field
from requests import post
from typing import Optional, Union, List

from ishelly.components.base import JSONRPCRequest


# ── Shared sub-models ────────────────────────────────────────────────────────

class RGBWActiveEnergy(BaseModel):
    total: float = Field(..., description="Total energy consumed in Watt-hours")
    by_minute: List[float] = Field(
        ...,
        description="Energy consumption by minute (mWh) for the last three minutes",
    )
    minute_ts: int = Field(
        ...,
        description="Unix timestamp of the first second of the last minute (UTC)",
    )


class RGBWTemperature(BaseModel):
    tC: Optional[Union[float, None]] = Field(None, description="Temperature in Celsius")
    tF: Optional[Union[float, None]] = Field(None, description="Temperature in Fahrenheit")


# ── Status ────────────────────────────────────────────────────────────────────

class RGBWStatus(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")
    source: str = Field(..., description="Source of the last command")
    output: bool = Field(..., description="True if the output is currently on")
    brightness: Optional[int] = Field(None, description="Current brightness (0-100)")
    white: Optional[int] = Field(None, description="Current white channel value (0-255)")
    rgb: Optional[List[int]] = Field(None, description="Current RGB values [r, g, b] each 0-255")
    transition_duration: Optional[float] = Field(
        None, description="Duration of the active transition in seconds"
    )
    timer_started_at: Optional[float] = Field(
        None, description="Unix timestamp when the timer was started (UTC)"
    )
    timer_duration: Optional[float] = Field(
        None, description="Duration of the timer in seconds"
    )
    apower: Optional[float] = Field(
        None, description="Last measured instantaneous active power (Watts)"
    )
    voltage: Optional[float] = Field(None, description="Last measured voltage in Volts")
    current: Optional[float] = Field(None, description="Last measured current in Amperes")
    pf: Optional[float] = Field(None, description="Last measured power factor")
    freq: Optional[float] = Field(None, description="Last measured network frequency in Hz")
    aenergy: Optional[RGBWActiveEnergy] = Field(
        None, description="Active energy counter information"
    )
    temperature: Optional[RGBWTemperature] = Field(
        None, description="Component temperature"
    )
    errors: Optional[List[str]] = Field(None, description="Error conditions")


# ── Config ────────────────────────────────────────────────────────────────────

class RGBWConfig(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")
    name: Optional[Union[str, None]] = Field(None, description="Name of the RGBW instance")
    initial_state: Optional[str] = Field(
        None, description="Output state on power-on: on, off, restore_last, match_input"
    )
    auto_on: Optional[bool] = Field(None, description="True if Auto-ON is enabled")
    auto_on_delay: Optional[float] = Field(
        None, description="Seconds until the component switches back on"
    )
    auto_off: Optional[bool] = Field(None, description="True if Auto-OFF is enabled")
    auto_off_delay: Optional[float] = Field(
        None, description="Seconds until the component switches back off"
    )
    default: Optional[dict] = Field(
        None,
        description="Default light values restored on power-on or after auto-on/off",
    )
    night_mode: Optional[dict] = Field(
        None, description="Night mode configuration"
    )


# ── RGBW.Set ─────────────────────────────────────────────────────────────────

class RGBWSetParams(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")
    on: Optional[bool] = Field(None, description="Turn the output on or off")
    brightness: Optional[int] = Field(
        None, description="Brightness level 0-100 (applies in both rgb and white modes)"
    )
    white: Optional[int] = Field(
        None, description="White channel intensity 0-255"
    )
    rgb: Optional[List[int]] = Field(
        None, description="RGB color as [r, g, b], each 0-255"
    )
    transition_duration: Optional[float] = Field(
        None, description="Duration for the color/brightness transition in seconds"
    )
    toggle_after: Optional[float] = Field(
        None, description="Seconds until the output state is toggled"
    )


class RGBWSetRequest(JSONRPCRequest):
    method: str = Field("RGBW.Set", description="Method to be invoked")
    params: RGBWSetParams = Field(..., description="Parameters for the method")


class RGBWSetResponse(BaseModel):
    was_on: bool = Field(
        ..., description="True if the output was on before the method was executed"
    )


# ── RGBW.Toggle ──────────────────────────────────────────────────────────────

class RGBWToggleParams(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")


class RGBWToggleRequest(JSONRPCRequest):
    method: str = Field("RGBW.Toggle", description="Method to be invoked")
    params: RGBWToggleParams = Field(..., description="Parameters for the method")


class RGBWToggleResponse(BaseModel):
    was_on: bool = Field(
        ..., description="True if the output was on before the method was executed"
    )


# ── RGBW.GetStatus ───────────────────────────────────────────────────────────

class RGBWGetStatusParams(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")


class RGBWGetStatusRequest(JSONRPCRequest):
    method: str = Field("RGBW.GetStatus", description="Method to be invoked")
    params: RGBWGetStatusParams = Field(..., description="Parameters for the method")


# ── RGBW.GetConfig / RGBW.SetConfig ─────────────────────────────────────────

class RGBWGetConfigParams(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")


class RGBWGetConfigRequest(JSONRPCRequest):
    method: str = Field("RGBW.GetConfig", description="Method to be invoked")
    params: RGBWGetConfigParams = Field(..., description="Parameters for the method")


class RGBWSetConfigParams(BaseModel):
    id: int = Field(..., description="Id of the RGBW component instance")
    config: RGBWConfig = Field(..., description="Configuration to apply")


class RGBWSetConfigRequest(JSONRPCRequest):
    method: str = Field("RGBW.SetConfig", description="Method to be invoked")
    params: RGBWSetConfigParams = Field(..., description="Parameters for the method")


class RGBWSetConfigResponse(BaseModel):
    restart_required: bool = Field(
        ..., description="True if a restart is required to apply the new configuration"
    )


# ── Component class ───────────────────────────────────────────────────────────

class RGBW:
    """Represents one RGBW channel on a Shelly RGBW PM device."""

    def __init__(self, device_rpc_url: str, rgbw_id: int = 0):
        self.rgbw_id = rgbw_id
        self.device_rpc_url = device_rpc_url

    # ── Core control ─────────────────────────────────────────────────────────

    def set(self, params: RGBWSetParams) -> RGBWSetResponse:
        req = RGBWSetRequest(id=1, params=params)
        response = post(self.device_rpc_url, json=req.model_dump(exclude_none=True))
        result = response.json().get("result") or {}
        # Some firmware versions return null result on success
        return RGBWSetResponse(was_on=result.get("was_on", False))

    def toggle(self) -> RGBWToggleResponse:
        req = RGBWToggleRequest(id=1, params=RGBWToggleParams(id=self.rgbw_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        result = response.json().get("result") or {}
        return RGBWToggleResponse(was_on=result.get("was_on", False))

    # ── Status / config ───────────────────────────────────────────────────────

    def get_status(self) -> RGBWStatus:
        req = RGBWGetStatusRequest(id=1, params=RGBWGetStatusParams(id=self.rgbw_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        return RGBWStatus(**response.json()["result"])

    def get_config(self) -> RGBWConfig:
        req = RGBWGetConfigRequest(id=1, params=RGBWGetConfigParams(id=self.rgbw_id))
        response = post(self.device_rpc_url, json=req.model_dump())
        return RGBWConfig(**response.json()["result"])

    def set_config(self, config: RGBWConfig) -> RGBWSetConfigResponse:
        req = RGBWSetConfigRequest(
            id=1, params=RGBWSetConfigParams(id=self.rgbw_id, config=config)
        )
        response = post(self.device_rpc_url, json=req.model_dump())
        return RGBWSetConfigResponse(**response.json()["result"])

    # ── Convenience helpers ───────────────────────────────────────────────────

    def turn_on(self, brightness: Optional[int] = None) -> RGBWSetResponse:
        """Turn the output on, optionally setting brightness (0-100)."""
        params = RGBWSetParams(id=self.rgbw_id, on=True, brightness=brightness)
        return self.set(params)

    def turn_off(self) -> RGBWSetResponse:
        """Turn the output off."""
        params = RGBWSetParams(id=self.rgbw_id, on=False)
        return self.set(params)

    def set_color(
        self,
        r: int,
        g: int,
        b: int,
        white: int = 0,
        brightness: Optional[int] = None,
        transition_duration: Optional[float] = None,
    ) -> RGBWSetResponse:
        """Set RGBW color. r/g/b/white are each 0-255. brightness is 0-100.
        The device requires all four channels; white defaults to 0.
        Avoid passing transition_duration=0.0 — use None to omit it."""
        params = RGBWSetParams(
            id=self.rgbw_id,
            on=True,
            rgb=[r, g, b],
            white=white,
            brightness=brightness,
            transition_duration=transition_duration if transition_duration else None,
        )
        return self.set(params)

    def set_white(
        self,
        white: int,
        brightness: Optional[int] = None,
        transition_duration: Optional[float] = None,
    ) -> RGBWSetResponse:
        """Set white channel with RGB zeroed out. brightness is 0-100.
        Avoid passing transition_duration=0.0 — use None to omit it."""
        params = RGBWSetParams(
            id=self.rgbw_id,
            on=True,
            rgb=[0, 0, 0],
            white=white,
            brightness=brightness,
            transition_duration=transition_duration if transition_duration else None,
        )
        return self.set(params)
