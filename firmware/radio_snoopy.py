"""
radio_snoopy.py

 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250720 2035 hrs by hwh


 edit history:


 Emulate the radio side of the connection, to poke/prod at the head
 unit.

"""
VERSION="v0.3"

SHOW_LINE        = True
USE_HEXBYTES     = True

SHOW_RADIO_READY = False
SHOW_RADIO_LCSA  = False
SHOW_RADIO_STATE = False

LCSA_LENGTH      = 34

import select
import time
from machine import Pin, UART, I2C
from dxsr8_screen import *
from dxsr8_config import *
import sh1106
from utility import *

dxsr8_config=dxsr8_config()

led = dxsr8_config.led

head_uart = UART(1, baudrate=dxsr8_config.baud_rate, tx=dxsr8_config.head_tx_pin, rx=dxsr8_config.head_rx_pin)
head_uart.init(bits=dxsr8_config.bits, parity=dxsr8_config.parity, stop=dxsr8_config.stop)
head_poll_obj = select.poll()
head_poll_obj.register(head_uart,select.POLLIN)

radio_uart = UART(0, baudrate=dxsr8_config.baud_rate, tx=dxsr8_config.radio_tx_pin, rx=dxsr8_config.radio_rx_pin)
radio_uart.init(bits=dxsr8_config.bits, parity=dxsr8_config.parity, stop=dxsr8_config.stop)
radio_poll_obj = select.poll()
radio_poll_obj.register(radio_uart,select.POLLIN)

i2c = I2C(scl=dxsr8_config.display_scl_pin, sda=dxsr8_config.display_sda_pin, freq=400000)
# display is 128x64 giving 8 lines of 16 characters
display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
display.sleep(False)
display.rotate(True)

def display_line(x):
    return x * 8

fdisp         = FrequencyDisplay()
mdisp         = ModeDisplay()
rfdisp        = RFPowerDisplay()
agcdisp       = AGCDisplay()
smeterdisp    = SMeterDisplay()
backlightdisp = BacklightDisplay()
miscdisp      = MiscDisplay()


def print_state(sin):
    print("print_state(%s)" % hexBytes2(sin))
   
    if not sin.startswith("LCSA"):
        return
        
    try:
        mode = mdisp.decode(sin)
        
        rxstate = "%s RF:%+2d %s" % (agcdisp.decode(sin), rfdisp.decode(sin), smeterdisp.decode_string(sin))
        
        line = ""

        if fdisp.is_freq(sin):
            line += "[%s] f = %s %s" % (mode, intWithCommas(fdisp.freq(sin)), rxstate)
        else:
            line += "[%s] > %s < %s" % (mode, fdisp.decode(sin), rxstate)

        line += str(sorted(miscdisp.decode(sin)))

        line += " <BL%2d>" % backlightdisp.decode(sin) # if you care about the backlight intensity.

        print(line)
        
    except (Exception) as e:
        print()
        print("Caught exception: " + str(e))
        print()
        print("Input %s" % (sin))
        print("Input %s" % hexBytes2(sin))
        print()

def print_bit_header():
    print('-'*((LCSA_LENGTH*3)-1))
    for i in range(LCSA_LENGTH):
        print("%2d" % ((i*8)//100), end = ' ')
    print()
    for i in range(LCSA_LENGTH):
        print("%02d" % ((i*8)%100), end = ' ')
    print()
    print('-'*((LCSA_LENGTH*3)-1))


print("Radio Snoopy", VERSION)
print("radio2head only")

display.fill(0)
display.text("Radio Snoopy", 0, display_line(0))
display.text("radio2head only", 0, display_line(3))
display.text(VERSION, 0, display_line(7))
display.show()


curline = b""

if SHOW_LINE:
    print_bit_header()
    
while True:
    led.toggle()
    
    if radio_poll_obj.poll(0):
        x = radio_uart.read()
        curline += x
        
        if SHOW_LINE:
            if USE_HEXBYTES:
                print(hexBytes(x))
            else:
                print(x)

        
        if -1 != curline.find(b"AL~READY"):
            if SHOW_RADIO_READY:
                print("GOT AL~READY.")
            n = curline.find(b"AL~READY")
            curline = curline[n+8+1:]
        
        if 1 <= curline.find(b"LCSA"):
            if SHOW_RADIO_LCSA:
                print("SEEK to LCSA: %d" % curline.find(b"LCSA"))
                print()
            n = curline.find(b"LCSA")
            # send the part before LCSA on to the head
            radio_uart.write(curline[0:n])
            # remove that part from the buffer
            curline = curline[n:]
        
        while len(curline) >= LCSA_LENGTH:
            if SHOW_RADIO_STATE:
                print_state(curline[0:LCSA_LENGTH])
            radio_uart.write(curline[0:LCSA_LENGTH])
            curline = curline[LCSA_LENGTH:]
        