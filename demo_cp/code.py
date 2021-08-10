import time
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label  # display
from adafruit_macropad import MacroPad   # tone
from rainbowio import colorwheel


# depends on 
# Adafruit CircuitPython
# Bus Device
# Adafruit framebuf
import adafruit_ssd1306

# NOTE: This circuitpython applications tries to follow the flow of the arduino demo.ino
# that is pre-installed on the Adafruit MacroPad board.

# NOTE: MacroPad has a display_text, build on displayio, but we need more control
# https://github.com/adafruit/Adafruit_CircuitPython_Display_Text

macropad = MacroPad()

# Play Tone
# macropad.play_tone(1319, 0.1)
# macropad.play_tone(988, 0.1)

# Init I2C
i2c = busio.I2C(board.SCL, board.SDA)

# for display
# set up (empty) text areas in a text_group
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
text_areas = []
y = -4
ydelta = 18

index_line1 = len(text_areas)
ta = label.Label(terminalio.FONT, text="")
ta.anchor_point = (0.0, 0.0)
ta.anchored_position = (0, y)
text_areas.append(ta)
y = y + ydelta

index_line2 = len(text_areas)
ta = label.Label(terminalio.FONT, text="")
ta.anchor_point = (0.0, 0.0)
ta.anchored_position = (0, y)
text_areas.append(ta)
y = y + ydelta

index_line3 = len(text_areas)
ta = label.Label(terminalio.FONT, text="")
ta.anchor_point = (0.0, 0.0)
ta.anchored_position = (0, y)
text_areas.append(ta)
y = y + ydelta

index_line4 = len(text_areas)
ta = label.Label(terminalio.FONT, text="")
ta.anchor_point = (0.0, 0.0)
ta.anchored_position = (0, y)
text_areas.append(ta)
y = y + ydelta

y = ydelta
index_keys = len(text_areas)
b = 0.0
for row in range(4):
    a = 0.0
    x = 0
    for col in range(3):
        ta = label.Label(terminalio.FONT, text="")
        ta.anchor_point = (a, b)
        ta.anchored_position = (x, y)
        text_areas.append(ta)
        a = a + 0.5
        x = x + DISPLAY_WIDTH / 2
    b = b + 0.5
    y = y + ydelta

text_group = displayio.Group()
for ta in text_areas:
    text_group.append(ta)
text_areas[index_line1].text = "* Adafruit Macropad *"
board.DISPLAY.show(text_group)

# scan i2c
i2c.try_lock()
i2c_list = i2c.scan()
i2c.unlock()
oled_addr = 0
oled_x = 0
oled_y = 0
oled_deltax = 10
oled_deltay = 1
if len(i2c_list) > 0:
    text_areas[index_line3].text = "I2C: " + str(i2c_list)
    oled_addr = i2c_list[0]
    oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, addr=60)
    oled.fill(0)
    oled.show()

# loop
last_position = None
loops = 0
while True:
    # check encoder position
    position = macropad.encoder
    if last_position is None or position != last_position:
        last_position = position
        text_areas[index_line2].text = "Rotary encoder: " + str(position)

    # check encoder press
    if macropad.encoder_switch:
        print("Encoder pressed")
        macropad.pixels.brightness = 1.0
    else:
        macropad.pixels.brightness = 0.2

    # change colors of all buttons 
    for i in range(len(macropad.pixels)):
        color_value = ((i * 256 / len(macropad.pixels)) + loops) % 255
        macropad.pixels[i] = colorwheel(color_value)

    # if i2c_addr set, assume the is an SSD1306 Oled display
    if oled_addr > 0:
        oled.pixel(oled_x, oled_y, 0)
        if oled_x > 127:
            oled_deltax = -10
            oled_y = oled_y + 1
        if oled_x < 0:
            oled_deltax = 10
            oled_y = oled_y + 1
        oled_x = oled_x + oled_deltax
        if oled_y > 31:
            oled_y = 0
        oled.pixel(oled_x, oled_y, 1)
        oled.show()

 
    # check all keys, print KEYn if presses
    event = macropad.keys.events.get()
    if event:
        text_areas[index_line2].text = ""
        text_areas[index_line3].text = ""
        text_areas[index_line4].text = ""
        if event.pressed:
            macropad.pixels[event.key_number] = 0xffffffff
            text_areas[index_keys + event.key_number].text = "KEY" + str(event.key_number + 1)
            time.sleep(0.2) # hold white
        else:
            text_areas[index_keys + event.key_number].text = ""

    loops = loops + 1
