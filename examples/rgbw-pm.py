"""
Shelly RGBW PM example
======================
Replace DEVICE_IP with your device's IP address before running.

Run from the repo root:
    .venv/bin/python examples/rgbw-pm.py
"""

from ishelly import ShellyRGBWPM, RGBWSetParams

DEVICE_IP = "192.168.1.XXX"  # <-- set this

strip = ShellyRGBWPM(DEVICE_IP)

# Print device info
info = strip.get_device_info()
print(f"Connected to: {info.app} (model={info.model}, gen={info.gen}, fw={info.ver})")

# Print current status
status = strip.rgbw.get_status()
print(f"Output on: {status.output}, brightness: {status.brightness}, rgb: {status.rgb}")

# Set a warm amber color at 60% brightness with a 1-second fade
strip.rgbw.set_color(255, 120, 20, brightness=60, transition_duration=1.0)
print("Set amber color.")

# Switch to full white channel at 80% brightness
strip.rgbw.set_white(255, brightness=80)
print("Set white channel.")

# Low-level raw call -- flash red for 3 seconds then auto-off
strip.rgbw.set(
    RGBWSetParams(id=0, on=True, rgb=[255, 0, 0], brightness=100, toggle_after=3.0)
)
print("Red flash triggered (auto-off in 3s).")

# Turn off
strip.rgbw.turn_off()
print("Turned off.")
