import time

# import board
# import displayio
# import terminalio
# from adafruit_display_text import label  # display
# from adafruit_macropad import MacroPad   # tone
# from rainbowio import colorwheel

# # NOTE: This circuitpython applications tries to follow the flow of the arduino demo.ino
# # that is pre-installed on the Adafruit MacroPad board.

# # NOTE: MacroPad has a display_text, build on displayio, but we need more control
# # https://github.com/adafruit/Adafruit_CircuitPython_Display_Text

# macropad = MacroPad()
# macropad.play_tone(988, 0.1)
# macropad.play_tone(1319, 0.2)

# mock label and text_areas
class Label():
    line = str(0)
    text = ""

text_areas = []

for i in range(12):
    label = Label()
    label.line = str(i+1)
    label.text = "00:00"
    text_areas.append(label)

def dump_text_areas():
    line = ""
    for i, ta in enumerate(text_areas):
        line = line + ta.text + " "
        if (i+1) % 3 == 0:
            line = line + "  "
    print(line)




# real timers for code.py
class Timer():
    down = False
    start = 0
    current = 0
    running = False
    paused = False

timers = []

def dump_timers():
    for t in timers:
        print(vars(t))

def addTimer(start, down):
    t = Timer()
    t.start = 0
    t.current = 0
    t.running = False
    t.paused = False
    t.down = down
    if down:
        t.start = start
        t.current = start
    timers.append(t)

def default_timers():
    timers = []
    addTimer(start=0, down=False)
    addTimer(start=120, down=True)

def prompt_timers():
    timers = []
    val = input("Number timers: ")
    count = int(val)
    if count < 1:
        count = 1
    if count > 12:
        count = 12
    for i in range(count):
        print("timer " + str(i+1) + ": ")
        val = input("down (y/n): ")
        down = False
        start = 0
        if val == 'y':
            down = True
            val = input("start: ")
            start = int(val)
        addTimer(start=start, down=down)

def update_timers():
    pass

def set_text_areas():
    # cycle all timers,
    # format current and set text area
    # update current
    pass
    for i, t in enumerate(timers):
        m = t.current // 60
        s = t.current % 60
        text_areas[i].text = f'{m:02}:{s:02}'


def run_timers(total):
    set_text_areas()
    last = time.time()
    count = 0
    while True:
        current = time.time()
        if (current - last) > 1:
            last = current
            count = count + 1
            dump_text_areas()
        if (total > 0 and count >= total):
            break



# prompt_timers()
default_timers()
dump_timers()

run_timers(5)

dump_text_areas()

# # for display
# # set up (empty) text areas in a text_group
# DISPLAY_WIDTH = 128
# DISPLAY_HEIGHT = 64
# text_areas = []
# y = -4
# ydelta = 18

# index_line1 = len(text_areas)
# ta = label.Label(terminalio.FONT, text="")
# ta.anchor_point = (0.0, 0.0)
# ta.anchored_position = (0, y)
# text_areas.append(ta)
# y = y + ydelta

# index_line2 = len(text_areas)
# ta = label.Label(terminalio.FONT, text="")
# ta.anchor_point = (0.0, 0.0)
# ta.anchored_position = (0, y)
# text_areas.append(ta)
# y = y + ydelta

# index_line3 = len(text_areas)
# ta = label.Label(terminalio.FONT, text="")
# ta.anchor_point = (0.0, 0.0)
# ta.anchored_position = (0, y)
# text_areas.append(ta)
# y = y + ydelta

# index_line4 = len(text_areas)
# ta = label.Label(terminalio.FONT, text="")
# ta.anchor_point = (0.0, 0.0)
# ta.anchored_position = (0, y)
# text_areas.append(ta)
# y = y + ydelta

# y = ydelta
# index_keys = len(text_areas)
# b = 0.0
# for row in range(4):
#     a = 0.0
#     x = 0
#     for col in range(3):
#         ta = label.Label(terminalio.FONT, text="")
#         ta.anchor_point = (a, b)
#         ta.anchored_position = (x, y)
#         text_areas.append(ta)
#         a = a + 0.5
#         x = x + DISPLAY_WIDTH / 2
#     b = b + 0.5
#     y = y + ydelta

# text_group = displayio.Group()
# for ta in text_areas:
#     text_group.append(ta)
# text_areas[index_line1].text = "* Adafruit Macropad *"
# board.DISPLAY.show(text_group)

# # loop
# last_position = None
# loops = 0
# while True:
#     # check encoder position
#     position = macropad.encoder
#     if last_position is None or position != last_position:
#         last_position = position
#         text_areas[index_line2].text = "Rotary encoder: " + str(position)

#     # scan i2c
#     # TODO

#     # check encoder press
#     if not macropad.encoder_switch_debounced:
#         print("Encoder pressed")
#         macropad.pixels.brightness = 1.0
#     else:
#         macropad.pixels.brightness = 0.2

#     # change colors of all buttons 
#     for i in range(len(macropad.pixels)):
#         color_value = ((i * 256 / len(macropad.pixels)) + loops) % 255
#         macropad.pixels[i] = colorwheel(color_value)
 
#     # check all keys, print KEYn if presses
#     event = macropad.keys.events.get()
#     if event:
#         text_areas[index_line2].text = ""
#         text_areas[index_line3].text = ""
#         text_areas[index_line4].text = ""
#         if event.pressed:
#             macropad.pixels[event.key_number] = 0xffffffff
#             text_areas[index_keys + event.key_number].text = "KEY" + str(event.key_number + 1)
#             time.sleep(0.2) # hold white
#         else:
#             text_areas[index_keys + event.key_number].text = ""

#     loops = loops + 1
