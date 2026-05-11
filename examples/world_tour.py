"""
5-minute world tour — ~300 seconds total
Each region gets a few colours with dwell times that add up.
Brightness locked at 25%.
"""
import time
from ishelly import ShellyRGBWPM, RGBWSetParams

strip = ShellyRGBWPM("192.168.1.80")

def s(r, g, b, w=0, dur=3.0):
    strip.rgbw.set(RGBWSetParams(id=0, on=True, rgb=[r,g,b], white=w, brightness=25))
    time.sleep(dur)

# Total target: 300 seconds
# Each region annotated with cumulative time

print("--- Arctic / Iceland ---")          # 0s
s(180, 220, 255, w=200, dur=4)  # icy white-blue aurora
s(0,   200, 180,         dur=4)  # teal aurora
s(80,  0,   200,         dur=4)  # violet aurora
s(200, 220, 255, w=255,  dur=4)  # polar white

print("--- Scandinavia / Northern Europe ---")  # 16s
s(0,   80,  160,         dur=3)  # deep Nordic fjord blue
s(180, 180, 200, w=100,  dur=3)  # grey winter sky
s(200, 160, 40,          dur=3)  # amber candlelight

print("--- UK / Ireland ---")              # 25s
s(0,   100, 40,          dur=3)  # Irish green
s(60,  80,  160,         dur=3)  # moody grey-blue
s(180, 60,  60,          dur=3)  # warm pub firelight

print("--- Mediterranean / Southern Europe ---")  # 34s
s(0,   120, 200,         dur=3)  # Aegean blue
s(255, 200, 40,          dur=3)  # Santorini sun
s(220, 80,  20,          dur=3)  # terracotta rooftops
s(255, 240, 180, w=80,   dur=3)  # warm afternoon haze

print("--- Morocco / North Africa ---")    # 46s
s(200, 40,  80,          dur=3)  # rose city pink
s(220, 100, 10,          dur=3)  # saffron spice
s(0,   80,  160,         dur=3)  # Moorish tile blue
s(180, 140, 40,          dur=3)  # gold souk

print("--- West Africa ---")              # 58s
s(220, 30,  0,           dur=3)  # kente red
s(220, 160, 0,           dur=3)  # kente gold
s(0,   100, 30,          dur=3)  # kente green
s(80,  0,   160,         dur=3)  # deep purple dusk

print("--- Congo / Central Africa ---")   # 70s
s(0,   100, 20,          dur=4)  # deep jungle
s(20,  180, 80,          dur=4)  # fresh canopy
s(0,   60,  40,          dur=4)  # dark undergrowth

print("--- East Africa / Savanna ---")    # 82s
s(0,   150, 50,          dur=3)  # savanna green
s(220, 160, 0,           dur=3)  # golden acacia
s(180, 60,  0,           dur=3)  # burnt sienna earth
s(200, 60,  10,          dur=3)  # sunset on the veldt

print("--- Southern Africa ---")          # 94s
s(150, 20,  60,          dur=3)  # dusk purple
s(30,  10,  120,         dur=3)  # night sky indigo
s(255, 100, 0,           dur=3)  # Kruger sunset

print("--- Middle East ---")              # 103s
s(200, 150, 20,          dur=3)  # desert gold
s(0,   100, 80,          dur=3)  # Persian tile teal
s(160, 40,  0,           dur=3)  # sand dune shadow
s(200, 180, 100, w=60,   dur=3)  # noon haze

print("--- India ---")                    # 115s
s(255, 100, 0,           dur=3)  # marigold orange
s(180, 0,   100,         dur=3)  # Rajasthan pink
s(0,   120, 60,          dur=3)  # Kerala green
s(100, 0,   180,         dur=3)  # Holi purple
s(220, 180, 0,           dur=3)  # turmeric gold

print("--- Southeast Asia ---")           # 130s
s(0,   160, 120,         dur=3)  # Mekong teal
s(220, 60,  80,          dur=3)  # temple red
s(255, 200, 0,           dur=3)  # Buddhist gold
s(0,   80,  40,          dur=3)  # rice paddy green

print("--- China / East Asia ---")        # 142s
s(200, 0,   20,          dur=3)  # imperial red
s(220, 160, 0,           dur=3)  # imperial gold
s(0,   60,  160,         dur=3)  # porcelain blue
s(200, 200, 220, w=100,  dur=3)  # misty mountain white

print("--- Japan ---")                    # 154s
s(255, 100, 140,         dur=4)  # cherry blossom
s(200, 220, 255, w=80,   dur=3)  # winter moon
s(180, 20,  20,          dur=3)  # torii red
s(0,   60,  40,          dur=4)  # bamboo forest

print("--- Pacific / Oceania ---")        # 168s
s(0,   160, 220,         dur=4)  # Pacific ocean blue
s(0,   200, 140,         dur=4)  # reef turquoise
s(255, 160, 40,          dur=4)  # coral sunset
s(200, 240, 255, w=120,  dur=3)  # tropical white

print("--- Australia / Outback ---")      # 183s
s(200, 60,  10,          dur=4)  # red dirt outback
s(220, 140, 20,          dur=3)  # spinifex gold
s(80,  40,  160,         dur=3)  # Milky Way indigo
s(255, 80,  20,          dur=3)  # Uluru sunset

print("--- Alaska / Canada ---")          # 196s
s(0,   160, 100,         dur=3)  # boreal green
s(180, 220, 255, w=160,  dur=4)  # northern lights
s(0,   80,  180,         dur=3)  # glacier blue

print("--- USA ---")                      # 206s
s(255, 0,   0,           dur=2)  # red
s(255, 255, 255, w=255,  dur=2)  # white
s(0,   0,   255,         dur=2)  # blue
s(255, 120, 0,           dur=3)  # Route 66 sunset
s(0,   80,  20,          dur=3)  # forest national park

print("--- Mexico / Central America ---") # 218s
s(220, 40,  0,           dur=3)  # fiesta red
s(0,   160, 60,          dur=3)  # jungle green
s(220, 180, 0,           dur=3)  # marigold Dia de Muertos
s(100, 0,   180,         dur=3)  # twilight purple

print("--- Caribbean ---")               # 230s
s(0,   180, 220,         dur=3)  # turquoise sea
s(255, 160, 0,           dur=3)  # reggae gold
s(180, 20,  20,          dur=3)  # reggae red
s(0,   120, 40,          dur=3)  # reggae green

print("--- Amazon / South America ---")  # 242s
s(0,   140, 30,          dur=4)  # Amazon canopy
s(20,  200, 80,          dur=4)  # jungle floor
s(200, 60,  0,           dur=3)  # toucan orange
s(80,  0,   160,         dur=3)  # morpho butterfly blue

print("--- Andes / Patagonia ---")       # 254s
s(0,   60,  180,         dur=3)  # Andean sky
s(200, 200, 220, w=160,  dur=3)  # glacier white
s(180, 100, 40,          dur=3)  # condor brown

print("--- Antarctica / Finale ---")     # 263s
s(180, 220, 255, w=255,  dur=4)  # polar ice
s(0,   200, 180,         dur=3)  # aurora teal
s(80,  0,   200,         dur=3)  # aurora violet
s(200, 220, 255, w=200,  dur=4)  # final white fade

print("--- Tour complete ---")           # 277s ~ 4m37s + loop overhead ~ 5min
