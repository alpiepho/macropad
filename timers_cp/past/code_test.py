import time
import board
import displayio
import terminalio
from adafruit_display_text import label  # display
from adafruit_macropad import MacroPad   # tone
from rainbowio import colorwheel


macropad = MacroPad()

# turn off pixels
for i in range(len(macropad.pixels)):
    macropad.pixels[i] = 0x000000
macropad.pixels.brightness = 1.0

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
ta.anchored_position = (0, y-8)
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

text_areas[index_line1].text = "macropad timers"
board.DISPLAY.show(text_group)


# Macropad Buttons
def encoder_pressed():
    global macropad
    result = False
    if macropad.encoder_switch:
        result = True
    return result

encoder_pressed_count = 0
def encoder_long_pressed():
    global macropad
    global encoder_pressed_count
    result = False
    if macropad.encoder_switch:
        encoder_pressed_count = encoder_pressed_count + 1
        if encoder_pressed_count > 200: # 200 x 0.01 = 2 seconds
            result = True
            encoder_pressed_count = 0
    else: 
        encoder_pressed_count = 0
    return result

def key_pressed(index):
    global macropad
    result = False
    event = macropad.keys.events.get()
    if event:
        if event.pressed and event.key_number == index:
            result = True
    return result

key_pressed_index = -1
key_pressed_count = 0
def key_long_pressed(index):
    # TODO: will macropad event stay active when pressed and held, or is it edge triggered?
    global macropad
    global key_pressed_index
    global key_pressed_count
    result = False
    event = macropad.keys.events.get()
    if event:
        if event.pressed and event.key_number == index:
            if index == key_pressed_index:
                key_pressed_count = key_pressed_count + 1
                if key_pressed_count > 200: # 200 x 0.01 = 2 seconds
                    result = True
                    key_pressed_count = 0
            else:
                key_pressed_index = index
                key_pressed_count = 0
            result = True
        else:
            key_pressed_index = -1
            key_pressed_count = 0
    return result

# Macropad Encoder
encoder_value = 0
def encoder_position():
    global macropad
    return macropad.encoder

# Macropad sound
def sound_play():
    global macropad
    macropad.play_tone(1319, 0.1)
    macropad.play_tone(988, 0.1)

# Macropad display and lights
def timers_display():
    global timers
    global text_areas
    global index_keys
    current = time.time()
    for i, t in enumerate(timers):
        M = (t.current // 100) // 60
        s = (t.current // 100) % 60
        m = t.current % 100
        text_areas[index_keys+i].text = f'{M:2}:{s:02}{m:02}'
        # https://forums.blinkstick.com/t/blinkstick-led-tips-info/406/2
        color_value = 0x000000
        if t.color == "G":
            color_value = 0x00FF00
        if t.color == "Y":
            color_value = 0xFFFF00
        if t.color == "O":
            color_value = 0xFFCC33
        if t.color == "R":
            color_value = 0xFF0000
        macropad.pixels[i] = color_value

        # process blink
        if t.blink == ".":
            if (current - t.blink_last) > 0.1:
                t.blink_on = not t.blink_on
                if not t.blink_on:
                    macropad.pixels[i] = 0x000000
            t.blink_last = current


def timers_dim(dim):
    if dim:
        macropad.pixels.brightness = 0.2
    else:
        macropad.pixels.brightness = 1.0

# Timer core logic
timers = []

class Timer():
    delta = 1
    start = 0
    current = 0
    running = False
    paused = False
    color = "G"
    blink = "_"
    blink_on = False
    blink_last = 0
    sound = False

def timer_add(start, delta, sound=False):
    global timers
    t = Timer()
    t.start = 0
    t.current = 0
    t.running = False
    t.paused = True
    t.delta = delta
    if delta < 0:
        t.start = start
        t.current = start
    timers.append(t)

# TODO: add Timer stuff here


# DEBUG
timer_add(start=0, delta=1)
timer_add(start=10000, delta=-1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timer_add(start=0, delta=1)
timers[0].blink = "."

# loop
last = time.time()
last_position = None
while True:
    current = time.time()
    #if (current - last) > 1:
    if (current - last) > 0.01:
        last = current
        # timers_update()
        timers_display()
        # timers_show()
        # check_menu()



    # TEST encoder position
    position = encoder_position()
    if last_position is None or position != last_position:
        last_position = position
        text_areas[index_line2].text = "rotary encoder: " + str(position)
        timers_dim(dim=False)

    # # TEST encoder press
    # if encoder_pressed():
    #     print("Encoder pressed")
    #     # TEST sound
    #     sound_play()

    # TEST encoder long press
    if encoder_long_pressed():
        print("Encoder long pressed")
        # TEST dim
        timers_dim(dim=True)
 
    # # check all keys, print KEYn if presses
    # for i in range(12):
    #     # TEST key press
    #     if key_pressed(i):
    #         text_areas[index_keys + i].text = "key" + str(i + 1)
    #     else:
    #         text_areas[index_keys + i].text = ""

    #     # TEST key long press
    #     if key_long_pressed(i):
    #         text_areas[index_keys + i].text = "KEY" + str(i + 1)
    #     else:
    #         text_areas[index_keys + i].text = ""

