import re
from PIL import Image, ImageDraw

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

def newCode128(code, barHeight, thickness = 3, barcodeType=None):
  if barcodeType == None:
    barcodeType = code128Detect(code)
  if (barcodeType=='C' and len(code) % 2 == 1):
    code = '0' + code
  c = code128ParseBarcode(code, barcodeType)
  wx = thickness
  st = wx*10
  top = st
  ss =sum(map(sum, c))
  
  w = ss * wx + (st*2)
  h = barHeight + (st*2)
  shape = [(0, 0), (w - 1, h - 1)]
  img = Image.new("RGB", (w, h))
  img1 = ImageDraw.Draw(img)  
  img1.rectangle(shape, fill ="#ffffff")
  for pk in c:
    clrIX = 0
    for ptns in pk:
      if clrIX == 0:
        # Only draw the rectangle if it's black
        shape = [(st, top), (st + (wx*ptns) -1, (top+barHeight-1))]
        img1.rectangle(shape, fill = "#000000")
        clrIX = 1
      else:
        clrIX = 0
      st += (wx*ptns)
  return img

if __name__ == "__main__":
  myText = "Kongduino"
  img = newCode128(myText, 60, 2)
  img.show()
