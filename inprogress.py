import board
import terminalio
from adafruit_display_text import label
import rotaryio


text = "Hello world"
text_area = label.Label(terminalio.FONT, text=text)
text_area.x = 10
text_area.y = 10
board.DISPLAY.show(text_area)

encoder = rotaryio.IncrementalEncoder(board.ROTA, board.ROTB)


last_position = None
while True:
    position = encoder.position
    if last_position is None or position != last_position:
        text_area.x = abs(position)
        board.DISPLAY.show(text_area)
