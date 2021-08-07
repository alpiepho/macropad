
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
- [done] Each timer will be associated with a key
- [done] Each timer will display on screen in form 00:00 in specific location on display
- [done] Each timer can count down or count up in seconds
- [done] Each timer can be started, paused, resume, reset with the associated key
- Rapid Key press x4 = reset
- Single Key press
    - [done] if not running -> running
    - [done] if running and not paused -> paused
    - [done] if running and paused -> not paused
- [done] The color of each timer will reflect the state of the timer
    - [done] if count down
        - [done] if not running -> green/dim
        - [done] if running and not paused
            - [done] 100% - 70% time remaining -> green/flashing
            - [done] 70% - 40% time remaining -> yellow/flashing
            - [done] 40% - 10% time remaining -> orange/flashing
            - [done] 10% - 0% time remaining -> red/flashing
            - [done] 0% time remaining -> red/solid
        [done] if running and paused -> above with solid/dim
    - [done] if count up
        - [done] if not running -> green/dim
        - [done] if running and not paused
            - [done] green/flashing
        [done] if running and paused -> above with solid/dim
- Each timer may play tone when done?
- Encoder is used to change overall settings
- Rapid encoder press 4x -> reset all and enter menu
    - menu: number
- [done]] encoder press 1x -> pause/play all
TODO Finish

- If all timers ready and waiting, display "Press 1x start, 4x reset"
- [done] If all timers ready and waiting, single encoder press -> start all
- [done] If all timers running, single encoder press -> pause all
- [done] If all timers running, single encoder press -> start all again
- [done] base structure
- [done] class Timer(): pass
- [done] t = Timer()
- [done] t.direction = 1 | -1
- [done] t.start_time in seconds
- [done] t.current_time in seconds
- [done] t.running bool
- [done] t.paused bool

TODO Finish