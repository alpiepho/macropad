
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
- build display
    - anchor_point vs anchor_position?
    - title
    - rotary
    - direction
    - 12 keys
- pixel colors
- button press for brightness
- comment with demo.ino?
- refactor and clean up python
- how to run a clock