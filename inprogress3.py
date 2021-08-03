import board
import digitalio
import displayio
import keypad
import neopixel
import rotaryio
import terminalio
import time
from adafruit_display_text import label  # display
from adafruit_macropad import MacroPad   # tone
from rainbowio import colorwheel

# NOTE: This circuitpython applications tries to follow the flow of the arduino demo.ino
# that is pre-installed on the Adafruit MacroPad board.
# Several of the comments from demo.ino are included here.  Look for '# //'.  This
# should help align the two applications despite the language/library differences.


# // Create the neopixel strip with the built in definitions NUM_NEOPIXEL and PIN_NEOPIXEL
pixels = neopixel.NeoPixel(board.NEOPIXEL, 12, brightness=0.1)

# // Create the rotary encoder
encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# // Start OLED
# // text display tests
# set up (empty) text areas in a text_group, then display the groups
# this differs from demo.ino where display.setCursor() is used to set text position
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
text_areas = []
y = -4
ydelta = DISPLAY_HEIGHT / 7

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

# ta = label.Label(terminalio.FONT, text="")
# ta.anchor_point = (0.0, 0.0)
# ta.anchored_position = (0, y)
# text_areas.append(ta)

# ta = label.Label(terminalio.FONT, text="")
# ta.anchor_point = (0.5, 0.0)
# ta.anchored_position = (DISPLAY_WIDTH / 2, y)
# text_areas.append(ta)

# text_area_key3 = label.Label(terminalio.FONT, text="")
# text_area_key3.anchor_point = (1.0, 0.0)
# text_area_key3.anchored_position = (DISPLAY_WIDTH, y)
# text_areas.append(text_area_key3)

# y = y + ydelta
# text_area_key4 = label.Label(terminalio.FONT, text="")
# text_area_key4.anchor_point = (0.0, 0.5)
# text_area_key4.anchored_position = (0, y)
# text_areas.append(text_area_key4)

# text_area_key5 = label.Label(terminalio.FONT, text="")
# text_area_key5.anchor_point = (0.5, 0.5)
# text_area_key5.anchored_position = (DISPLAY_WIDTH / 2, y)
# text_areas.append(text_area_key5)

# text_area_key6 = label.Label(terminalio.FONT, text="")
# text_area_key6.anchor_point = (1.0, 0.5)
# text_area_key6.anchored_position = (DISPLAY_WIDTH, y)
# text_areas.append(text_area_key6)

# y = y + ydelta
# text_area_key7 = label.Label(terminalio.FONT, text="")
# text_area_key7.anchor_point = (0.0, 1.0)
# text_area_key7.anchored_position = (0, y)
# text_areas.append(text_area_key7)

# text_area_key8 = label.Label(terminalio.FONT, text="")
# text_area_key8.anchor_point = (0.5, 1.0)
# text_area_key8.anchored_position = (DISPLAY_WIDTH / 2, y)
# text_areas.append(text_area_key8)

# text_area_key9 = label.Label(terminalio.FONT, text="")
# text_area_key9.anchor_point = (1.0, 1.0)
# text_area_key9.anchored_position = (DISPLAY_WIDTH, y)
# text_areas.append(text_area_key9)

# y = y + ydelta
# text_area_key10 = label.Label(terminalio.FONT, text="")
# text_area_key10.anchor_point = (0.0, 1.5)
# text_area_key10.anchored_position = (0, y)
# text_areas.append(text_area_key10)

# text_area_key11 = label.Label(terminalio.FONT, text="")
# text_area_key11.anchor_point = (0.5, 1.5)
# text_area_key11.anchored_position = (DISPLAY_WIDTH / 2, y)
# text_areas.append(text_area_key11)

# text_area_key12 = label.Label(terminalio.FONT, text="")
# text_area_key12.anchor_point = (1.0, 1.5)
# text_area_key12.anchored_position = (DISPLAY_WIDTH, y)
# text_areas.append(text_area_key12)

text_group = displayio.Group()
for ta in text_areas:
    text_group.append(ta)


# // set all mechanical keys to inputs
key_pins = (board.KEY1, board.KEY2, board.KEY3, board.KEY4, board.KEY5, board.KEY6,
            board.KEY7, board.KEY8, board.KEY9, board.KEY10, board.KEY11, board.KEY12)
keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)


# // We will use I2C for scanning the Stemma QT port
# TODO
# // Wire.begin();


# // tone(PIN_SPEAKER, 988, 100);  // tone1 - B5
# // delay(100);
# // tone(PIN_SPEAKER, 1319, 200); // tone2 - E6
# // delay(200);
# TODO MacroPad conflicts with keypad (saw similar issue with demo.ino using tone)
# macropad = MacroPad()
# macropad.start_tone(988)
# time.sleep(0.1)
# macropad.stop_tone()
# macropad.start_tone(1319)
# time.sleep(0.2)
# macropad.stop_tone()


last_position = None
loop_count = 0 # // uint8_t j = 0

# // void loop()
while True:
    # // display.println("* Adafruit Macropad *");
    text_areas[index_line1].text = "* Adafruit Macropad *"
    text_areas[index_line2].text = ""
    text_areas[index_line3].text = ""
    text_areas[index_line4].text = ""

    # print encoder position and direction
    # // check the encoder
    position = encoder.position
    if last_position is None or position != last_position:
        print("Encoder: " + str(position))
        print("Direction: " + str(encoder.direction))
        last_position = position
        text_areas[index_line2].text = "Rotary encoder: " + str(position)

    # scan i2c
    # TODO
    #   // Scanning takes a while so we don't do it all the time
    #   if ((j & 0x3F) == 0) {
    #     Serial.println("Scanning I2C: ");
    #     Serial.print("Found I2C address 0x");
    #     for (uint8_t address = 0; address <= 0x7F; address++) {
    #       Wire.beginTransmission(address);
    #       i2c_found[address] = (Wire.endTransmission () == 0);
    #       if (i2c_found[address]) {
    #         Serial.print("0x");
    #         Serial.print(address, HEX);
    #         Serial.print(", ");
    #       }
    #     }
    #     Serial.println();
    #   }
    
    #   display.setCursor(0, 16);
    #   display.print("I2C Scan: ");
    #   for (uint8_t address=0; address <= 0x7F; address++) {
    #     if (!i2c_found[address]) continue;
    #     display.print("0x");
    #     display.print(address, HEX);
    #     display.print(" ");
    #   }

    # // check encoder press
    if not button.value:
        print("Encoder button")
        text_areas[index_line4].text = "Encoder pressed "
        pixels.brightness = 1.0
    else:
        pixels.brightness = 0.1

    # change colors of all buttons
    # // for(int i=0; i< pixels.numPixels(); i++) {
    for i in range(len(pixels)):
        color_value = ((i * 256 / len(pixels)) + loop_count) % 255
        pixels[i] = colorwheel(color_value)

    # check all keys, print KEYn if presses
    event = keys.events.get()
    if event:
        if event.pressed:
            print("Switch " + str(event.key_number + 1))
            text = "KEY" + str(event.key_number + 1)
            pixels[event.key_number] = colorwheel(255)
            text_areas[index_keys+event.key_number].text = text
            print(text)
        else:
            text_areas[index_keys+event.key_number].text = ""

    # // show neopixels, incredment swirl
    loop_count = loop_count + 1 # // j++





