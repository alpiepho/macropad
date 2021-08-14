import board
import displayio
import terminalio
from adafruit_display_text import label  # display
from adafruit_macropad import MacroPad   # tone
from rainbowio import colorwheel

#############################
# Constants/Globals
#############################

LOOP_FACTOR = 1
DELTA = 7

MAX_KEYS = 12

BLINK_LOOPS = 20
ENCODER_LOOPS = 1
KEY_LOOPS = 10

BRIGHTNESS_LOW = 0.2
BRIGHTNESS_HIGH = 1.0

GREEN = 0x00FF00
YELLOW = 0xFFFF00
ORANGE = 0xFF8C00
RED = 0xFF0000

GREEN_DIM = 0x002200
YELLOW_DIM = 0x222200
ORANGE_DIM = 0x221200
RED_DIM = 0x220000

MENU_IDLE = 0
MENU_SETUP = 1
MENU_NUM_TIMERS = 2
MENU_NUM_TIMERS_LOOP = 3
MENU_TMR_DIRECTION = 4
MENU_TMR_START = 5
MENU_TMR_SOUND = 6
MENU_DONE = 10

BLINK_BLINK = "."
BLINK_STEADY = "_"

class Timer():
    delta = DELTA
    start = 0
    current = 0
    formatted = "0:00.0"
    running = False
    paused = False
    color = GREEN
    color_dim = GREEN_DIM
    current_yellow = 0
    current_orange = 0
    current_red = 0
    blink = BLINK_BLINK
    blink_on = False
    blink_last = 0
    sound = False
    pressed_last = 0

macropad = MacroPad()

#############################
# Setup - Hardware
#############################

# turn off pixels
for i in range(len(macropad.pixels)):
    macropad.pixels[i] = 0x000000
macropad.pixels.brightness = BRIGHTNESS_HIGH

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

#############################
# Macropad Functions
#############################

def sound_play():
    global macropad
    macropad.play_tone(1319, 0.1)
    macropad.play_tone(988, 0.1)

encoder_pressed_count = 0
def encoder_pressed():
    global macropad
    global encoder_pressed_count
    result = False
    if macropad.encoder_switch:
        encoder_pressed_count = encoder_pressed_count + 1
        if encoder_pressed_count > ENCODER_LOOPS:
            result = True
            encoder_pressed_count = 0
    else: 
        encoder_pressed_count = 0
    return result

def key_pressed(loops):
    event = macropad.keys.events.get()
    if event:
        i = event.key_number
        if event.pressed:
            timers[i].paused = not timers[i].paused
            if not timers[i].paused:
                timers[i].running = True
            timers[i].pressed_last = loops
        if event.released:
            if (loops - timers[i].pressed_last) > KEY_LOOPS:
                timer_reset(i)
            timers[i].pressed_last = 0

def timers_display(loops):
    global timers
    global text_areas
    global index_keys
    global menu_state

    if menu_state > MENU_IDLE:
        for i in range(MAX_KEYS):
            text_areas[index_keys+i].text = ""
            macropad.pixels[i] = 0x000000
        return

    for i, t in enumerate(timers):
        text_areas[index_keys+i].text = t.formatted
        if t.blink != BLINK_BLINK:
            macropad.pixels[i] = t.color

        if t.blink == BLINK_BLINK:
            macropad.pixels[i] = t.color_dim
            # if (loops - t.blink_last) > BLINK_LOOPS:
            #     t.blink_on = not t.blink_on
            #     if not t.blink_on:
            #         macropad.pixels[i] = t.color_dim
            #     t.blink_last = loops


#############################
# Timer Functions
#############################
timers = []

def timer_formatted(current):
    # assume current is in 0.1sec
    m = (current % 10)
    s = (current // 10)
    M = (s // 60)
    s = s - (60*M)
    if M > 60:
        M = 0
    return f'{M:2}:{s:02}.{m:1}'
    #return f'{current}'

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
    t.formatted = timer_formatted(t.current)
    t.sound = sound

    t.current_yellow = t.start // 7
    t.current_orange = t.start // 4
    t.current_red = t.start // 10

    timers.append(t)

def timer_reset(index):
    t = timers[index]
    t.current = 0
    t.paused = True
    if t.delta < 0:
        t.current = t.start
    t.formatted = timer_formatted(t.current)
    t.color = GREEN
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
        if not t.running and not t.paused:
            t.running = True

def timers_update(loops):
    global timers
    for _, t in enumerate(timers):
        if t.running:
            if not t.paused:
                # update current time
                t.current = max(0, t.current + t.delta)
                t.formatted = timer_formatted(t.current)
                t.blink = BLINK_STEADY
                if t.delta < 0:
                    # update color
                    t.color = GREEN
                    t.color_dim = GREEN_DIM
                    if t.current < t.current_yellow:
                        t.color = YELLOW
                        t.color = YELLOW_DIM
                    if t.current < t.current_orange:
                        t.color = ORANGE
                        t.color = ORANGE_DIM
                    if t.current < t.current_red:
                        t.color = RED
                        t.color = RED_DIM
                    if t.current == 0:
                        t.blink = "_"
                        t.running = False
                        if t.sound:
                            print("play sound")
                            sound_play()
                else:
                    t.color = GREEN
            else:
                # update color
                t.blink = BLINK_BLINK       

#############################
# Menu Functions
#############################

menu_state = MENU_IDLE
menu_timer_count = 1
menu_timer_index = -1
menu_timer_direction = "up"
menu_timer_start = 60
menu_timer_sound = "off"
menu_current_position = 0
menu_last_position = 0

# TODO adjust these, may get choppy, but should be able to adjust to consisitent time
def set_loop_factor():
    global LOOP_FACTOR
    global DELTA
    total = len(timers)
    if total == 1:
        LOOP_FACTOR = 9000
        DELTA = 7
    if total == 2:
        LOOP_FACTOR = 8000
        DELTA = 7
    if total == 3:
        LOOP_FACTOR = 7000
        DELTA = 7
    if total == 4:
        LOOP_FACTOR = 6000
        DELTA = 7
    if total == 5:
        LOOP_FACTOR = 5000
        DELTA = 7
    if total == 6:
        LOOP_FACTOR = 4000
        DELTA = 7
    if total == 7:
        LOOP_FACTOR = 3500
        DELTA = 7
    if total == 8:
        LOOP_FACTOR = 3000
        DELTA = 7
    if total == 9:
        LOOP_FACTOR = 2000
        DELTA = 7
    if total == 10:
        LOOP_FACTOR = 1000
        DELTA = 7
    if total == 11:
        LOOP_FACTOR = 500
        DELTA = 7
    if total == 12:
        LOOP_FACTOR = 1
        DELTA = 12

def check_menu(loops):
    global index_line1
    global menu_state
    global menu_timer_count
    global menu_timer_index
    global menu_timer_direction
    global menu_timer_start
    global menu_timer_sound
    global menu_current_position
    global menu_last_position
    global LOOP_FACTOR

    menu_last_position = menu_current_position
    menu_current_position = macropad.encoder

    if menu_state == MENU_SETUP:
        text_areas[index_line1].text = "setup..."
        text_areas[index_line2].text = ""
        text_areas[index_line3].text = ""
        text_areas[index_line4].text = ""
        if encoder_pressed():
            menu_state = MENU_NUM_TIMERS

    elif menu_state == MENU_NUM_TIMERS:
        text_areas[index_line1].text = "number timers: " + str(menu_timer_count)
        if menu_current_position > menu_last_position:
            menu_timer_count = min(MAX_KEYS, menu_timer_count + 1)
        if menu_current_position < menu_last_position:
            menu_timer_count = max(1, menu_timer_count - 1)
        if encoder_pressed():
            menu_state = MENU_NUM_TIMERS_LOOP

    elif menu_state == MENU_NUM_TIMERS_LOOP:
        if menu_timer_index >= (menu_timer_count - 1):
            menu_state = MENU_DONE
        else:
            menu_timer_index = menu_timer_index + 1
            menu_state = MENU_TMR_DIRECTION

    elif menu_state == MENU_TMR_DIRECTION:
        text_areas[index_line1].text = "tmr" + str(menu_timer_index+1) + " direction: " + menu_timer_direction
        if menu_current_position > menu_last_position:
            menu_timer_direction = "up"
        if menu_current_position < menu_last_position:
            menu_timer_direction = "down"
        if encoder_pressed():
            if menu_timer_direction == "up":
                timer_add(start=0, delta=DELTA, sound=False)
                menu_timer_direction = "up"
                menu_timer_start = 60
                menu_timer_sound = "off"
                menu_state = MENU_NUM_TIMERS_LOOP
            if menu_timer_direction == "down":
                menu_state = MENU_TMR_START

    elif menu_state == MENU_TMR_START:
        M = (menu_timer_start) // 60
        s = (menu_timer_start) % 60
        text_areas[index_line1].text = "tmr" + str(menu_timer_index+1) + " start: " + f'{M:02}:{s:02}'
        if menu_current_position > menu_last_position:
            menu_timer_start = min(3600, menu_timer_start + 1)
        if menu_current_position < menu_last_position:
            menu_timer_start = max(0, menu_timer_start - 1)
        if encoder_pressed():
            menu_state = MENU_TMR_SOUND

    elif menu_state == MENU_TMR_SOUND:
        text_areas[index_line1].text = "tmr" + str(menu_timer_index+1) + " sound: " + menu_timer_sound
        if menu_current_position > menu_last_position:
            menu_timer_sound = "y"
        if menu_current_position < menu_last_position:
            menu_timer_sound = "n"
        if encoder_pressed():
            # create timer
            delta = DELTA
            if menu_timer_direction == "down":
                delta = -1 * DELTA
            sound = False
            if menu_timer_sound == "y":
                sound = True
            timer_add(start=(menu_timer_start*100), delta=delta, sound=sound)
            menu_timer_direction = "up"
            menu_timer_start = 60
            menu_timer_sound = "off"
            menu_state = MENU_NUM_TIMERS_LOOP

    elif menu_state == MENU_DONE:
        text_areas[index_line1].text = "macropad timers"
        menu_state = 0
        menu_timer_count = 1
        menu_timer_index = -1
        timers_reset_all()
        set_loop_factor()


#############################
# Button Functions
#############################

def check_buttons(current):
    global menu_state
    global timers

    if menu_state > MENU_SETUP:
        macropad.pixels.brightness = BRIGHTNESS_LOW
        return
    macropad.pixels.brightness = BRIGHTNESS_HIGH
    if encoder_pressed():
        timers_reset_all()
        timers = []
        menu_state = MENU_SETUP
    key_pressed(current)


#############################
# Setup - Application
#############################

# DEBUG
timer_add(start=0, delta=DELTA)
timer_add(start=300, delta=(-1*DELTA), sound=False)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)
timer_add(start=0, delta=DELTA)

loops = 0
timers_display(loops)
timers_start_all()

#############################
# Main Loop - Application
#############################
while True:
    loops = loops + 1
    if (loops % LOOP_FACTOR) == 0:
        check_buttons(loops)
        check_menu(loops)
        timers_update(loops)
        timers_display(loops)

