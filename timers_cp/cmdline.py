import os
import time

# Mock Text Areas
class Label():
    text = ""

text_areas = []


line1_index = 0
label = Label()
label.text = "Macropad Timers"
text_areas.append(label)

keys_index = 1
for i in range(12):
    label = Label()
    label.text = "00:00"
    text_areas.append(label)

# Mock Buttons
def encoder_pressed():
    result = False
    name = "encoder_pressed.txt"
    if os.path.exists(name):
        os.remove(name)
        result = True
    return result

def encoder_long_pressed():
    result = False
    name = "encoder_long_pressed.txt"
    if os.path.exists(name):
        os.remove(name)
        result = True
    return result

def key_pressed(index):
    result = False
    name = "key" + str(index+1) + "_pressed.txt"
    if os.path.exists(name):
        os.remove(name)
        result = True
    return result

def key_long_pressed(index):
    result = False
    name = "key" + str(index+1) + "_long_pressed.txt"
    if os.path.exists(name):
        os.remove(name)
        result = True
    return result

# Mock Encoder
encoder_value = 0
def encoder_position():
    global encoder_value
    name = "encoder_up.txt"
    if os.path.exists(name):
        os.remove(name)
        encoder_value = encoder_value + 1
    name = "encoder_down.txt"
    if os.path.exists(name):
        os.remove(name)
        encoder_value = encoder_value - 1
    return encoder_value

# Mock sound
def sound_play():
    print("sound")


# color/blink combinations (using chars so we can share with command line)
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

# base Timer class and functions
class Timer():
    delta = 1
    start = 0
    current = 0
    running = False
    paused = False
    color = "g"
    blink = "_"
    sound = False

timers = []

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
    print("len(timers): " + str(len(timers)))

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
    
def timers_display():
    global timers
    global text_areas
    global keys_index
    for i, t in enumerate(timers):
        M = (t.current // 100) // 60
        s = (t.current // 100) % 60
        m = t.current % 100
        text_areas[keys_index+i].text = f'{M:02}:{s:02}:{m:02} {t.color}{t.blink}'

def timers_show():
    global timers
    global text_areas
    # Mock for command line
    global keys_index
    line = ""
    for i, ta in enumerate(text_areas):
        if i == 0:
            line = ta.text + "\n"
        if i >= keys_index:
            line = line + ta.text + "  "
            if (keys_index+i+1) % 3 == 0:
                line = line + "\t"
    print(line)

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
    global line1_index
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
    print("menu_state: " + str(menu_state))

    if menu_state == 1: # menu start
        text_areas[line1_index].text = "Setup timers..."
        if encoder_pressed():
            menu_state = 2

    elif menu_state == 2: # number timers
        text_areas[line1_index].text = "number timers: " + str(menu_timer_count)
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
        text_areas[line1_index].text = "tmr" + str(menu_timer_index+1) + " direction: " + menu_timer_direction
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
        text_areas[line1_index].text = "tmr" + str(menu_timer_index+1) + " start: " + seconds_to_M_s(menu_timer_start)
        if menu_current_position > menu_last_position:
            menu_timer_start = min(3600, menu_timer_start + 1)
        if menu_current_position < menu_last_position:
            menu_timer_start = max(0, menu_timer_start - 1)
        if encoder_pressed():
            menu_state = 6

    elif menu_state == 6: # timer sound
        text_areas[line1_index].text = "tmr" + str(menu_timer_index+1) + " sound: " + menu_timer_sound
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
        text_areas[line1_index].text = "Macropad Timers"
        menu_state = 0
        menu_timer_count = 1
        menu_timer_index = -1
        timers_reset_all()


def check_buttons():
    global menu_state
    global timers

    if menu_state > 0:
        return
    if encoder_pressed():
        timers_toggle_all()
    if encoder_long_pressed():
        # timers_reset_all()
        timers = []
        menu_state = 1
    for i, t in enumerate(timers):
        if key_pressed(index=i):
            t.paused = not t.paused
            if not t.paused:
                t.running = True
        if key_long_pressed(index=i):
            timer_reset(i)


# DEBUG
timer_add(start=0, delta=1)
timer_add(start=10000, delta=-1)


# Add to Arduino setup
timers_display()
timers_show()

timers_start_all()
last = time.time()

# Add to Arduino loop
while True:
    check_buttons()
    current = time.time()
    if (current - last) > 1:
    #if (current - last) > 0.01:
        last = current
        timers_update()
        timers_display()
        timers_show()
        check_menu()
