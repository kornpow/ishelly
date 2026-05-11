import time
from ishelly import ShellyRGBWPM

strip = ShellyRGBWPM("192.168.1.80")
print("connected, christmas mode go")

pattern = [
    (220,  10,  10,   0, 0.3),   # red
    (  0,   0,   0,   0, 0.2),   # off
    (220,  10,  10,   0, 0.3),   # red
    (  0,   0,   0,   0, 0.2),   # off
    ( 10, 180,  30,   0, 0.3),   # green
    (  0,   0,   0,   0, 0.2),   # off
    ( 10, 180,  30,   0, 0.3),   # green
    (  0,   0,   0,   0, 0.2),   # off
    (255, 200, 200, 255, 0.2),   # white sparkle
    (  0,   0,   0,   0, 0.2),   # off
]

while True:
    for r, g, b, w, dur in pattern:
        strip.rgbw.set_color(r, g, b, white=w, brightness=100, transition_duration=0.0)
        time.sleep(dur)
