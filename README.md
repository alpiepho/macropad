
Collection of arduino and circuitpython files related to the ADABox019 kit with the MacroPad RS2040.

[MacroPad Overview](https://learn.adafruit.com/adafruit-macropad-rp2040/overview)

The pre-installed application source code is in the file 'demo.ino'.  

Some notes on using the demo:
- seems like I had to re-add the includes for Adafruit_SH110X.h, Adafruit_NeoPixel.h, RotaryEncoder.h
- to load code, need to unplug usb and hold button.  Maybe reset + button will work?
- uncommenting the 'tone' calls seems to hang the board



[Macropad Example on Github](https://github.com/adafruit/Adafruit_Learning_System_Guides/tree/main/Adafruit_MacroPad)

[Other Macropad Example on Github](https://github.com/adafruit/Adafruit_CircuitPython_MacroPad/tree/main/examples)

[Other Examples on Github](https://github.com/adafruit/Adafruit_Learning_System_Guides)


## Re-create arduino demo using circuitpython

The Macropad board has a demo pre-installed.  It is written as a .ino file (see demo.ino).

The circuitpython script in demo_py re-creates that demo.

Basic steps of demo:
- setup 

TODO List
- [done] setup and create tone
- [done] comment out tune
- [done] build display
    - anchor_point vs anchor_position?
    - title
    - rotary
    - direction
    - 12 keys
- [done] pixel colors
- [done] button press for brightness
- [done] comment with demo.ino?
- [done] refactor and clean up python
- [done] how to run a clock

## Multiple Timers

Leverage the demo_cp project to run up to 12 timers.  
- Each timer will be associated with a key
- Each timer will display on screen in form 00:00 in specific location on display
- Each timer can count down or count up in seconds
- Each timer can be started, paused, resume, reset with the associated key
- Rapid Key press x4 = reset
- Single Key press
    - if not running -> running
    - if running and not paused -> paused
    - if running and paused -> not paused
- The color of each timer will reflect the state of the timer
    - if count down
        - if not running -> green/dim
        - if running and not paused
            - 100% - 70% time remaining -> green/flashing
            - 70% - 40% time remaining -> yellow/flashing
            - 40% - 10% time remaining -> orange/flashing
            - 10% - 0% time remaining -> red/flashing
            - 0% time remaining -> red/solid
        if running and paused -> above with solid/dim
    - if count up
        - if not running -> green/dim
        - if running and not paused
            - green/flashing
        if running and paused -> above with solid/dim
- Each timer may play tone when done?
- Encoder is used to change overall settings
- Rapid encoder press 4x -> reset all and enter menu
    - menu: number
TODO Finish

- If all timers ready and waiting, display "Press 1x start, 4x reset"
- If all timers ready and waiting, single encoder press -> start all
- If all timers running, single encoder press -> pause all
- If all timers running, single encoder press -> start all again
- base structure
- class Timer(): pass
- t = Timer()
- t.direction = 1 | -1
- t.start_time in seconds
- t.current_time in seconds
- t.running bool
- t.paused bool

TODO Finish