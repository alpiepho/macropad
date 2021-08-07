import os
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






# real timers for code.py
class Timer():
    delta = 1
    start = 0
    current = 0
    running = False
    paused = False
    color = "g"
    blink = "_"
    # G_  - green, solid
    # G.  - green, blink
    # g_  - green, solid, dim
    # g.  - green, blink, dim
    # Y_  - yellow, solid
    # Y.  - yellow, blink
    # y_  - yellow, solid, dim
    # y.  - yellow, blink, dim
    # O_  - orange, solid
    # O.  - orange, blink
    # o_  - orange, solid, dim
    # o.  - orange, blink, dim
    # R_  - red, solid
    # R.  - red, blink
    # r_  - red, solid, dim
    # r.  - red, blink, dim
    # S   - sound

timers = []

def dump_timers():
    for t in timers:
        print(vars(t))

def timer_add(start, delta):
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

def timer_reset(index):
    t = timers[index]
    t.current = 0
    t.paused = True
    if t.delta < 0:
        t.current = t.start
    t.color = "g"
    t.blink = "_"

def timers_start_all():
    for _, t in enumerate(timers):
        t.running = True
        t.paused = False

def timers_reset_all():
    for i, _ in enumerate(timers):
        timer_reset(i)

def timers_toggle_all():
    for _, t in enumerate(timers):
        t.paused = not t.paused 

def timers_update():
    for _, t in enumerate(timers):
        if t.running:
            if not t.paused:
                # update current time
                t.current = t.current + t.delta
                t.blink = "."
                if t.delta < 0:
                    if t.current < 0:
                        t.current = 0
                    # update color
                    percent = 100.0 * t.current / t.start
                    t.color = "G"
                    if percent < 70.0 :
                        t.color = "Y"
                    if percent < 40.0 :
                        t.color = "O"
                    if percent < 10.0 :
                        t.color = "R"
                    if percent < 10.0 :
                        t.color = "R"
                    if t.current == 0:
                        t.blink = "_"
                        t.running = False
                        # TODO update sound
                else:
                    t.color = "G"
            else:
                # update color
                t.color = t.color.lower()
                t.blink = "_"       

def timers_display():
    for i, t in enumerate(timers):
        M = (t.current // 100) // 60
        s = (t.current // 100) % 60
        m = t.current % 100
        text_areas[i].text = f'{M:02}:{s:02}:{m:02} {t.color}{t.blink}'

def timers_show():
    line = ""
    for i, ta in enumerate(text_areas):
        line = line + ta.text + "  "
        if (i+1) % 3 == 0:
            line = line + "\t"
    print(line)

def check_buttons():
    name_4x = "encoder_4x.txt"
    name_1x = "encoder_1x.txt"
    if os.path.exists(name_4x):
        os.remove(name_4x)
        timers_reset_all()
    if os.path.exists(name_1x):
        os.remove(name_1x)
        timers_toggle_all()
    for i, t in enumerate(timers):
        name_4x = "key" + str(i+1) + "_4x.txt"
        name_1x = "key" + str(i+1) + "_1x.txt"
        if os.path.exists(name_4x):
            os.remove(name_4x)
            timer_reset(i)
        if os.path.exists(name_1x):
            os.remove(name_1x)
            t.paused = not t.paused
            if not t.paused:
                t.running = True

def timers_run():
    timers_display()
    timers_show()

    timers_start_all()
    last = time.time()
    while True:
        check_buttons()
        current = time.time()
        if (current - last) > 1:
        #if (current - last) > 0.01:
            last = current
            timers_update()
            timers_display()
            timers_show()



timer_add(start=0, delta=1)
timer_add(start=10000, delta=-1)
timers_run()

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
