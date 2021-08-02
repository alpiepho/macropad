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
macropad = MacroPad()
macropad.start_tone(988)
time.sleep(0.1)
macropad.stop_tone()
macropad.start_tone(1319)
time.sleep(0.2)
macropad.stop_tone()


encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)

# print title
title_text = "* Adafruit Macropad *"
title_text_area = label.Label(terminalio.FONT, text=title_text)
title_text_area.x = 0
title_text_area.y = 0
board.DISPLAY.show(title_text_area)


# for display
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
TEXT = "Key"

text_area_top_left = label.Label(terminalio.FONT, text="TEXT1")
text_area_top_left.anchor_point = (0.0, 0.0)
text_area_top_left.anchored_position = (0, 0)

text_area_top_middle = label.Label(terminalio.FONT, text="TEXT2")
text_area_top_middle.anchor_point = (0.5, 0.0)
text_area_top_middle.anchored_position = (DISPLAY_WIDTH / 2, 0)

text_area_top_right = label.Label(terminalio.FONT, text="TEXT3")
text_area_top_right.anchor_point = (1.0, 0.0)
text_area_top_right.anchored_position = (DISPLAY_WIDTH, 0)

text_area_middle_left = label.Label(terminalio.FONT, text="TEXT4")
text_area_middle_left.anchor_point = (0.0, 0.5)
text_area_middle_left.anchored_position = (0, DISPLAY_HEIGHT / 2)

text_area_middle_middle = label.Label(terminalio.FONT, text="TEXT5")
text_area_middle_middle.anchor_point = (0.5, 0.5)
text_area_middle_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)

text_area_middle_right = label.Label(terminalio.FONT, text="TEXT6")
text_area_middle_right.anchor_point = (1.0, 0.5)
text_area_middle_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT / 2)

text_area_bottom_left = label.Label(terminalio.FONT, text="TEXT7")
text_area_bottom_left.anchor_point = (0.0, 1.0)
text_area_bottom_left.anchored_position = (0, DISPLAY_HEIGHT)

text_area_bottom_middle = label.Label(terminalio.FONT, text="TEXT8")
text_area_bottom_middle.anchor_point = (0.5, 1.0)
text_area_bottom_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT)

text_area_bottom_right = label.Label(terminalio.FONT, text="TEXT9")
text_area_bottom_right.anchor_point = (1.0, 1.0)
text_area_bottom_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

text_group = displayio.Group()
text_group.append(title_text_area)
text_group.append(text_area_top_middle)
text_group.append(text_area_top_left)
text_group.append(text_area_top_right)
text_group.append(text_area_middle_middle)
text_group.append(text_area_middle_left)
text_group.append(text_area_middle_right)
text_group.append(text_area_bottom_middle)
text_group.append(text_area_bottom_left)
text_group.append(text_area_bottom_right)

board.DISPLAY.show(text_group)


# loop
last_position = None
while True:
    position = encoder.position
    if last_position is None or position != last_position:
        title_text_area.x = abs(position)
        board.DISPLAY.show(title_text_area)
        #board.DISPLAY.show(text_group)

    # print encoder position and direction

    # scan i2c

    # print encoder button
    # if encoder button presses, change brightness

    # change colors of all buttons 

    # check all keys, print KEYn if presses
