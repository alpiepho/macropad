import board
import displayio
import keypad
import rotaryio
import terminalio
import time
from adafruit_display_text import label  # display
from adafruit_macropad import MacroPad   # tone





key_pins = (board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6,
            board.KEY7, board.KEY8, board.KEY9, board.KEY10, board.KEY11, board.KEY12)
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)

encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)

# TODO MacroPad conflicts with keypad
# macropad = MacroPad()
# macropad.start_tone(988)
# time.sleep(0.1)
# macropad.stop_tone()
# macropad.start_tone(1319)
# time.sleep(0.2)
# macropad.stop_tone()

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

y = 18
index_keys = len(text_areas)
ta = label.Label(terminalio.FONT, text="")
ta.anchor_point = (0.0, 0.0)
ta.anchored_position = (0, y)
text_areas.append(ta)

ta = label.Label(terminalio.FONT, text="")
ta.anchor_point = (0.5, 0.0)
ta.anchored_position = (DISPLAY_WIDTH / 2, y)
text_areas.append(ta)

text_area_key3 = label.Label(terminalio.FONT, text="")
text_area_key3.anchor_point = (1.0, 0.0)
text_area_key3.anchored_position = (DISPLAY_WIDTH, y)
text_areas.append(text_area_key3)

y = y + ydelta
text_area_key4 = label.Label(terminalio.FONT, text="")
text_area_key4.anchor_point = (0.0, 0.5)
text_area_key4.anchored_position = (0, y)
text_areas.append(text_area_key4)

text_area_key5 = label.Label(terminalio.FONT, text="")
text_area_key5.anchor_point = (0.5, 0.5)
text_area_key5.anchored_position = (DISPLAY_WIDTH / 2, y)
text_areas.append(text_area_key5)

text_area_key6 = label.Label(terminalio.FONT, text="")
text_area_key6.anchor_point = (1.0, 0.5)
text_area_key6.anchored_position = (DISPLAY_WIDTH, y)
text_areas.append(text_area_key6)

y = y + ydelta
text_area_key7 = label.Label(terminalio.FONT, text="")
text_area_key7.anchor_point = (0.0, 1.0)
text_area_key7.anchored_position = (0, y)
text_areas.append(text_area_key7)

text_area_key8 = label.Label(terminalio.FONT, text="")
text_area_key8.anchor_point = (0.5, 1.0)
text_area_key8.anchored_position = (DISPLAY_WIDTH / 2, y)
text_areas.append(text_area_key8)

text_area_key9 = label.Label(terminalio.FONT, text="")
text_area_key9.anchor_point = (1.0, 1.0)
text_area_key9.anchored_position = (DISPLAY_WIDTH, y)
text_areas.append(text_area_key9)

y = y + ydelta
text_area_key10 = label.Label(terminalio.FONT, text="")
text_area_key10.anchor_point = (0.0, 1.5)
text_area_key10.anchored_position = (0, y)
text_areas.append(text_area_key10)

text_area_key11 = label.Label(terminalio.FONT, text="")
text_area_key11.anchor_point = (0.5, 1.5)
text_area_key11.anchored_position = (DISPLAY_WIDTH / 2, y)
text_areas.append(text_area_key11)

text_area_key12 = label.Label(terminalio.FONT, text="")
text_area_key12.anchor_point = (1.0, 1.5)
text_area_key12.anchored_position = (DISPLAY_WIDTH, y)
text_areas.append(text_area_key12)

text_group = displayio.Group()
for ta in text_areas:
    text_group.append(ta)

board.DISPLAY.show(text_group)


# loop
last_position = None
while True:
    text_areas[index_line1].text = "* Adafruit Macropad *"


    event = keys.events.get()
    if event:
        text = "KEY" + str(event.key_number + 1)
        if event.pressed:
            text_areas[index_keys+event.key_number].text = text
        else:
            text_areas[index_keys+event.key_number].text = ""

    position = encoder.position
    if last_position is None or position != last_position:
        last_position = position
        y = text_areas[index_keys+0].anchored_position[1]
        text_areas[index_keys+0].anchored_position = (abs(position), y)
        # board.DISPLAY.show(text_group)

    # print encoder position and direction

    # scan i2c

    # print encoder button
    # if encoder button presses, change brightness

    # change colors of all buttons 

    # check all keys, print KEYn if presses
