import board
import terminalio
from adafruit_display_text import label
import rotaryio


# for tone
from adafruit_macropad import MacroPad
import time

# for display
import displayio


# run tone
# delay 100
# run tone
# delay 200
# macropad = MacroPad()
# macropad.start_tone(988)
# time.sleep(0.1)
# macropad.stop_tone()
# macropad.start_tone(1319)
# time.sleep(0.2)
# macropad.stop_tone()


encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)

# print title
y = 0
title_text = "* Adafruit Macropad *"
title_text_area = label.Label(terminalio.FONT, text=title_text)
title_text_area.anchor_point = (0.0, 0.0)
title_text_area.anchored_position = (0, 0)


# for display
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
TEXT = "Key"

y = -4 + 20
ydelta = DISPLAY_HEIGHT / 3 - 2
text_area_key1 = label.Label(terminalio.FONT, text="KEY1")
text_area_key1.anchor_point = (0.0, 0.0)
text_area_key1.anchored_position = (0, y)

text_area_key2 = label.Label(terminalio.FONT, text="KEY2")
text_area_key2.anchor_point = (0.5, 0.0)
text_area_key2.anchored_position = (DISPLAY_WIDTH / 2, y)

text_area_key3 = label.Label(terminalio.FONT, text="KEY3")
text_area_key3.anchor_point = (1.0, 0.0)
text_area_key3.anchored_position = (DISPLAY_WIDTH, y)

y = y + ydelta
text_area_key4 = label.Label(terminalio.FONT, text="KEY4")
text_area_key4.anchor_point = (0.0, 0.5)
text_area_key4.anchored_position = (0, y)

text_area_key5 = label.Label(terminalio.FONT, text="KEY5")
text_area_key5.anchor_point = (0.5, 0.5)
text_area_key5.anchored_position = (DISPLAY_WIDTH / 2, y)

text_area_key6 = label.Label(terminalio.FONT, text="KEY6")
text_area_key6.anchor_point = (1.0, 0.5)
text_area_key6.anchored_position = (DISPLAY_WIDTH, y)

y = y + ydelta
text_area_key7 = label.Label(terminalio.FONT, text="KEY7")
text_area_key7.anchor_point = (0.0, 1.0)
text_area_key7.anchored_position = (0, y)

text_area_key8 = label.Label(terminalio.FONT, text="KEY8")
text_area_key8.anchor_point = (0.5, 1.0)
text_area_key8.anchored_position = (DISPLAY_WIDTH / 2, y)

text_area_key9 = label.Label(terminalio.FONT, text="KEY9")
text_area_key9.anchor_point = (1.0, 1.0)
text_area_key9.anchored_position = (DISPLAY_WIDTH, y)

y = y + ydelta
text_area_key10 = label.Label(terminalio.FONT, text="KEY10")
text_area_key10.anchor_point = (0.0, 1.5)
text_area_key10.anchored_position = (0, y)

text_area_key11 = label.Label(terminalio.FONT, text="KEY11")
text_area_key11.anchor_point = (0.5, 1.5)
text_area_key11.anchored_position = (DISPLAY_WIDTH / 2, y)

text_area_key12 = label.Label(terminalio.FONT, text="KEY12")
text_area_key12.anchor_point = (1.0, 1.5)
text_area_key12.anchored_position = (DISPLAY_WIDTH, y)

text_group = displayio.Group()
text_group.append(title_text_area)
text_group.append(text_area_key1)
text_group.append(text_area_key2)
text_group.append(text_area_key3)
text_group.append(text_area_key4)
text_group.append(text_area_key5)
text_group.append(text_area_key6)
text_group.append(text_area_key7)
text_group.append(text_area_key8)
text_group.append(text_area_key9)
text_group.append(text_area_key10)
text_group.append(text_area_key11)
text_group.append(text_area_key12)

board.DISPLAY.show(text_group)


# loop
last_position = None
while True:
    position = encoder.position
    if last_position is None or position != last_position:
        last_position = position
        # text_area_key1.text = ""
        y = text_area_key1.anchored_position[1]
        text_area_key1.anchored_position = (abs(position), y)
        # board.DISPLAY.show(title_text_area)
        board.DISPLAY.show(text_group)

    # print encoder position and direction

    # scan i2c

    # print encoder button
    # if encoder button presses, change brightness

    # change colors of all buttons 

    # check all keys, print KEYn if presses
