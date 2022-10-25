# Code128_Python

This is a simple Code128 1D barcode library for Python, working with the PIL library. The code can easily be reworked for other graphic libraries by changing the filled rectangle drawing code. That's the only part that relies on the PIL.

The library auto-detects whether it needs Code128B (uppercase and lowercase), C (only numbers), or A (uppercase). You pass it a string, the thickness of each module in pixels, and the height of the bars. It does the rest.

```python
myText = "Kongduino"
img = newCode128(myText, 60, 2)
img.show()
```

![Kongduino128](Kongduino128.png)

*Yes, I know I should make a class out of this code. But it's a simple demo. YOU do it.*

## CircuitPython

Included is a CircuitPython working on my 01Studio Board (nRF52840) with displayio.

```python
if __name__ == "__main__":
  my_group = displayio.Group()
  rect = Rect(0, 0, 320, 240, fill=0xFFFFFF)
  my_group.append(rect)
  myText = "Code128"
  newCode128(my_group, myText, 60, 2)
  myText = "Kongduino"
  newCode128(my_group, myText, 60, 2, 0, 120)
  # bar height, bar thickness, px, py
```

![TwoBarcodes](TwoBarcodes.jpg)