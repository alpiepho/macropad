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


# Show text areas
def timers_show():
    pass

# Macropad Buttons
def encoder_pressed():
    global macropad
    result = False
    if macropad.encoder_switch:
        result = True
    return result

# encoder_pressed_count = 0
# def encoder_long_pressed():
#     global macropad
#     global encoder_pressed_count
#     result = False
#     if macropad.encoder_switch:
#         encoder_pressed_count = encoder_pressed_count + 1
#         if encoder_pressed_count > 200: # 200 x 0.01 = 2 seconds
#             result = True
#             encoder_pressed_count = 0
#     else: 
#         encoder_pressed_count = 0
#     return result

def key_pressed(index):
    global macropad
    result = False
    event = macropad.keys.events.get()
    if event:
        print(str(index) + " " + str(event.key_number))
        if event.pressed and event.key_number == index:
            result = True
    return result

# key_pressed_index = -1
# key_pressed_count = 0
# def key_long_pressed(index):
#     # TODO: will macropad event stay active when pressed and held, or is it edge triggered?
#     global macropad
#     global key_pressed_index
#     global key_pressed_count
#     result = False
#     event = macropad.keys.events.get()
#     if event:
#         if event.pressed and event.key_number == index:
#             if index == key_pressed_index:
#                 key_pressed_count = key_pressed_count + 1
#                 if key_pressed_count > 200: # 200 x 0.01 = 2 seconds
#                     result = True
#                     key_pressed_count = 0
#             else:
#                 key_pressed_index = index
#                 key_pressed_count = 0
#             result = True
#         else:
#             key_pressed_index = -1
#             key_pressed_count = 0
#     return result

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

# DEBUG
# def dump_timers():
#     for t in timers:
#         print(vars(t))

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
def timer_reset(index):
    t = timers[index]
    t.current = 0
    t.paused = True
    if t.delta < 0:
        t.current = t.start
    t.color = "g"
    t.blink = "_"

def timers_start_all():
    global timers
    for _, t in enumerate(timers):
        t.running = True
        t.paused = False

def timers_reset_all():
    global timers
    for i, _ in enumerate(timers):
        timer_reset(i)

def timers_toggle_all():
    global timers
    for _, t in enumerate(timers):
        t.paused = not t.paused 
        if not t.paused:
            t.running = True

def timers_update():
    global timers
    for _, t in enumerate(timers):
        if t.running:
            if not t.paused:
                # update current time
                t.current = max(0, t.current + t.delta)
                t.blink = "."
                if t.delta < 0:
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
                        if t.sound:
                            sound_play()
                else:
                    t.color = "G"
            else:
                # update color
                t.color = t.color.lower()
                t.blink = "_"       
    
menu_state = 0
menu_timer_count = 1
menu_timer_index = -1
menu_timer_direction = "up"
menu_timer_start = 60
menu_timer_sound = "off"
menu_current_position = 0
menu_last_position = 0

def seconds_to_M_s(seconds):
    M = (seconds) // 60
    s = (seconds) % 60
    return f'{M:02}:{s:02}'

def check_menu():
    global index_line1
    global menu_state
    global menu_timer_count
    global menu_timer_index
    global menu_timer_direction
    global menu_timer_start
    global menu_timer_sound
    global menu_current_position
    global menu_last_position

    menu_last_position = menu_current_position
    menu_current_position = encoder_position()
    # print("menu_state: " + str(menu_state))

    if menu_state == 1: # menu start
        text_areas[index_line1].text = "setup..."
        if encoder_pressed():
            menu_state = 2

    elif menu_state == 2: # number timers
        text_areas[index_line1].text = "number timers: " + str(menu_timer_count)
        if menu_current_position > menu_last_position:
            menu_timer_count = min(12, menu_timer_count + 1)
        if menu_current_position < menu_last_position:
            menu_timer_count = max(1, menu_timer_count - 1)
        if encoder_pressed():
            menu_state = 3

    elif menu_state == 3: # number timers loop
        if menu_timer_index >= (menu_timer_count - 1):
            menu_state = 10
        else:
            menu_timer_index = menu_timer_index + 1
            menu_state = 4

    elif menu_state == 4: # timer direction
        text_areas[index_line1].text = "tmr" + str(menu_timer_index+1) + " direction: " + menu_timer_direction
        if menu_current_position > menu_last_position:
            menu_timer_direction = "up"
        if menu_current_position < menu_last_position:
            menu_timer_direction = "down"
        if encoder_pressed():
            if menu_timer_direction == "up":
                timer_add(start=0, delta=1, sound=False)
                menu_timer_direction = "up"
                menu_timer_start = 60
                menu_timer_sound = "off"
                menu_state = 3
            if menu_timer_direction == "down":
                menu_state = 5

    elif menu_state == 5: # timer start
        text_areas[index_line1].text = "tmr" + str(menu_timer_index+1) + " start: " + seconds_to_M_s(menu_timer_start)
        if menu_current_position > menu_last_position:
            menu_timer_start = min(3600, menu_timer_start + 1)
        if menu_current_position < menu_last_position:
            menu_timer_start = max(0, menu_timer_start - 1)
        if encoder_pressed():
            menu_state = 6

    elif menu_state == 6: # timer sound
        text_areas[index_line1].text = "tmr" + str(menu_timer_index+1) + " sound: " + menu_timer_sound
        if menu_current_position > menu_last_position:
            menu_timer_sound = "y"
        if menu_current_position < menu_last_position:
            menu_timer_sound = "n"
        if encoder_pressed():
            # create timer
            delta = 1
            if menu_timer_direction == "down":
                delta = -1
            sound = False
            if menu_timer_sound == "y":
                sound = True
            timer_add(start=(menu_timer_start*100), delta=delta, sound=sound)
            menu_timer_direction = "up"
            menu_timer_start = 60
            menu_timer_sound = "off"
            menu_state = 3

    elif menu_state == 10: # menu done
        text_areas[index_line1].text = "macropad timers"
        menu_state = 0
        menu_timer_count = 1
        menu_timer_index = -1
        timers_reset_all()


def check_buttons():
    global menu_state
    global timers

    if menu_state > 0:
        timers_dim(dim=True)
        return
    timers_dim(dim=False)
    if encoder_pressed():
    #     timers_toggle_all()
    # if encoder_long_pressed():
        # timers_reset_all()
        timers = []
        menu_state = 1
    for i, t in enumerate(timers):
        if key_pressed(index=i):
            t.paused = not t.paused
            if not t.paused:
                t.running = True
        # if key_long_pressed(index=i):
        #     timer_reset(i)


# DEBUG
timer_add(start=0, delta=1)
timer_add(start=10000, delta=-1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timer_add(start=0, delta=1)
# timers[0].blink = "."

# Add to Arduino setup
timers_display()
timers_show()

timers_start_all()
last = 0
current = 0
last_position = None

# Arduino loop
while True:
    check_buttons()
    current = current + 1
    if (current - last) > 10: # TODO test scale
        last = current
        timers_update()
        timers_display()
        timers_show()
        check_menu()

