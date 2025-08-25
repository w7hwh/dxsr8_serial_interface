from machine import Pin, I2C
import sh1106
import time

#
i2c = I2C(scl=Pin(17), sda=Pin(16), freq=400000)
#display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
display.sleep(False)
display.rotate(True)

while True:
    display.fill(0)
    # text, x-position, y-position
    display.text("Hello World!", 0, 0) 
    display.text("Hank was here", 0, 8)
    display.text("sh1106_demo.py", 0, 16)
    display.text("0123456789012345", 0, 24)
    display.text("Line 4", 0, 32)
    display.text("Line 5", 0, 40)
    display.text("Line 6", 0, 48)
    display.text("Line 7", 0, 56)
    # Show the updated display
    display.show()


    time.sleep(4)

    display.fill(0)
    display.text("Horizontal Line", 0, 0)
    display.hline(0,32,128,1)
    display.show()

    time.sleep(1)

    display.fill(0)
    display.text("Vertical Line", 0, 0)
    display.vline(64,20,40,1)
    display.show()

    time.sleep(1)

    display.fill(0)
    display.text("Rectangle", 0, 0)
    display.rect(32,16,64,32,1)
    display.show()

    time.sleep(1)

    display.fill(0)
    display.text("Filled Rectangle", 0, 0)
    display.fill_rect(32, 16, 64, 32, 1)
    display.show()
    time.sleep(1)
