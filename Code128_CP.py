import re, board
import displayio
from adafruit_ili9341 import ILI9341
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.line import Line
from adafruit_display_text import label
import terminalio

displayio.release_displays()
spi = board.SPI()
tft_cs = board.D11
tft_dc = board.D9
tft_rst = board.D10
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = ILI9341(display_bus, width=320, height=240, rotation=180)

PATTERNS = [[2, 1, 2, 2, 2, 2], [2, 2, 2, 1, 2, 2], [2, 2, 2, 2, 2, 1], [1, 2, 1, 2, 2, 3], [1, 2, 1, 3, 2, 2], [1, 3, 1, 2, 2, 2], [1, 2, 2, 2, 1, 3], [1, 2, 2, 3, 1, 2], [1, 3, 2, 2, 1, 2], [2, 2, 1, 2, 1, 3], [2, 2, 1, 3, 1, 2], [2, 3, 1, 2, 1, 2], [1, 1, 2, 2, 3, 2], [1, 2, 2, 1, 3, 2], [1, 2, 2, 2, 3, 1], [1, 1, 3, 2, 2, 2], [1, 2, 3, 1, 2, 2], [1, 2, 3, 2, 2, 1], [2, 2, 3, 2, 1, 1], [2, 2, 1, 1, 3, 2], [2, 2, 1, 2, 3, 1], [2, 1, 3, 2, 1, 2], [2, 2, 3, 1, 1, 2], [3, 1, 2, 1, 3, 1], [3, 1, 1, 2, 2, 2], [3, 2, 1, 1, 2, 2], [3, 2, 1, 2, 2, 1], [3, 1, 2, 2, 1, 2], [3, 2, 2, 1, 1, 2], [3, 2, 2, 2, 1, 1], [2, 1, 2, 1, 2, 3], [2, 1, 2, 3, 2, 1], [2, 3, 2, 1, 2, 1], [1, 1, 1, 3, 2, 3], [1, 3, 1, 1, 2, 3], [1, 3, 1, 3, 2, 1], [1, 1, 2, 3, 1, 3], [1, 3, 2, 1, 1, 3], [1, 3, 2, 3, 1, 1], [2, 1, 1, 3, 1, 3], [2, 3, 1, 1, 1, 3], [2, 3, 1, 3, 1, 1], [1, 1, 2, 1, 3, 3], [1, 1, 2, 3, 3, 1], [1, 3, 2, 1, 3, 1], [1, 1, 3, 1, 2, 3], [1, 1, 3, 3, 2, 1], [1, 3, 3, 1, 2, 1], [3, 1, 3, 1, 2, 1], [2, 1, 1, 3, 3, 1], [2, 3, 1, 1, 3, 1], [2, 1, 3, 1, 1, 3], [2, 1, 3, 3, 1, 1], [2, 1, 3, 1, 3, 1], [3, 1, 1, 1, 2, 3], [3, 1, 1, 3, 2, 1], [3, 3, 1, 1, 2, 1], [3, 1, 2, 1, 1, 3], [3, 1, 2, 3, 1, 1], [3, 3, 2, 1, 1, 1], [3, 1, 4, 1, 1, 1], [2, 2, 1, 4, 1, 1], [4, 3, 1, 1, 1, 1], [1, 1, 1, 2, 2, 4], [1, 1, 1, 4, 2, 2], [1, 2, 1, 1, 2, 4], [1, 2, 1, 4, 2, 1], [1, 4, 1, 1, 2, 2], [1, 4, 1, 2, 2, 1], [1, 1, 2, 2, 1, 4], [1, 1, 2, 4, 1, 2], [1, 2, 2, 1, 1, 4], [1, 2, 2, 4, 1, 1], [1, 4, 2, 1, 1, 2], [1, 4, 2, 2, 1, 1], [2, 4, 1, 2, 1, 1], [2, 2, 1, 1, 1, 4], [4, 1, 3, 1, 1, 1], [2, 4, 1, 1, 1, 2], [1, 3, 4, 1, 1, 1], [1, 1, 1, 2, 4, 2], [1, 2, 1, 1, 4, 2], [1, 2, 1, 2, 4, 1], [1, 1, 4, 2, 1, 2], [1, 2, 4, 1, 1, 2], [1, 2, 4, 2, 1, 1], [4, 1, 1, 2, 1, 2], [4, 2, 1, 1, 1, 2], [4, 2, 1, 2, 1, 1], [2, 1, 2, 1, 4, 1], [2, 1, 4, 1, 2, 1], [4, 1, 2, 1, 2, 1], [1, 1, 1, 1, 4, 3], [1, 1, 1, 3, 4, 1], [1, 3, 1, 1, 4, 1], [1, 1, 4, 1, 1, 3], [1, 1, 4, 3, 1, 1], [4, 1, 1, 1, 1, 3], [4, 1, 1, 3, 1, 1], [1, 1, 3, 1, 4, 1], [1, 1, 4, 1, 3, 1], [3, 1, 1, 1, 4, 1], [4, 1, 1, 1, 3, 1], [2, 1, 1, 4, 1, 2], [2, 1, 1, 2, 1, 4], [2, 1, 1, 2, 3, 2], [2, 3, 3, 1, 1, 1, 2]]
START_BASE = 38
STOP = 106

def code128Detect(code):
  rslt = re.search(r'^[0-9]+$', code)
  if rslt != None:
    return 'C'
  rslt = re.search(r'[a-z]', code)
  if rslt != None:
    return 'B'
  return 'A'

def code128AddBar(bars, nr, check):
  nrCode = PATTERNS[nr]
  if len(bars)==0:
    check = nr
  else:
    check += nr * len(bars)
  bars.append(nrCode)
  return check

def code128ParseBarcode(barcode, barcodeType):
  bars = []
  check = 0
  check = code128AddBar(bars, START_BASE + ord(barcodeType), check)
  ln = len(barcode)
  for i in range(0, ln):
    code = 0
    if barcodeType=='C':
      code = barcode[i]+barcode[i+1]
      i += 1
    else:
      code = barcode[i]
    converted = code128FromType(barcodeType, code)
    check = code128AddBar(bars, converted, check)
  bars.append(PATTERNS[check % 103])
  bars.append(PATTERNS[STOP])
  return bars

def code128FromType(barcodeType, code):
  charCode = ord(code)
  if barcodeType == 'A':
    if charCode>=0 and charCode<32:
      return charCode+64
    if charCode>=32 and charCode<96:
      return charCode-32
    return charCode
  if barcodeType == 'B':
    if charCode>=32 and charCode<128:
      return charCode-32
    return charCode
  if barcodeType == 'C':
    return charCode

def newCode128(group, code, barHeight, thickness = 3, px = 0, py = 0, barcodeType=None):
  if barcodeType == None:
    barcodeType = code128Detect(code)
  if (barcodeType=='C' and len(code) % 2 == 1):
    code = '0' + code
  c = code128ParseBarcode(code, barcodeType)
  wx = thickness
  left = wx*10 + px
  st = left
  top = 0
  if py > 0:
    top = py
  else:
    top = st + py
  ss = sum(map(sum, c))
  w = ss * wx + (st*2)
  h = barHeight + (st*2)
  print(f"w = {w}, h = {h}, st = {st}, wx = {wx}")
  print(c)
  for ptns in c:
    clrIX = 0
    for pk in ptns:
      if clrIX == 0:
        # Only draw the rectangle if it's black
        rect = Rect(st, top, pk*wx, barHeight, fill=0x000000)
        #print(f"Rect({st}, {top}, {pk*wx}, {barHeight}, fill=BLACK)")
        group.append(rect)
        clrIX = 1
      else:
        #print(f"Rect({st}, {top}, {pk*wx}, {barHeight}, fill=WHITE)")
        clrIX = 0
      st += (wx*pk)
  my_label = label.Label(terminalio.FONT, text=code, color=0x000000)
  my_label.x = int(st/2) - int(my_label.width/2)
  my_label.y = top + barHeight + 10
  group.append(my_label)
  display.show(group)

if __name__ == "__main__":
  my_group = displayio.Group()
  rect = Rect(0, 0, 320, 240, fill=0xFFFFFF)
  my_group.append(rect)
  myText = "Code128"
  newCode128(my_group, myText, 60, 2)
  myText = "Kongduino"
  newCode128(my_group, myText, 60, 2, 0, 120)
