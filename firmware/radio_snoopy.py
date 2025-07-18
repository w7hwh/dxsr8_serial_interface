"""
radio_snoopy.py

 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250710 2351 hrs by hwh


 edit history:


 Emulate the radio side of the connection, to poke/prod at the head
 unit.

"""
VERSION="v0.1"

import select
import time
from machine import Pin, UART, I2C
from dxsr8_screen import *
from dxsr8_config import *
import sh1106

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

fdisp = FrequencyDisplay()
mdisp = ModeDisplay()
rfdisp = RFPowerDisplay()
agcdisp = AGCDisplay()
smeterdisp = SMeterDisplay()
backlightdisp = BacklightDisplay()
miscdisp = MiscDisplay()

def intWithCommas(x):
    #if type(x) not in [type(0), type(0L)]:
    if type(x) is not int:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


def print_state(sin):
    print("print_state() type(sin)=", type(sin))
    
    if not sin.startswith("LCSA"):
        return
    
    #s = [ ord(c) for c in sin ]

    for s in sin:
        print("print_state type(s)=", type(s))
        
        #try:
        mode = mdisp.decode(s)
        '''
            rxstate = "%s RF:%+2d %s" % (agcdisp.decode(s), rfdisp.decode(s), smeterdisp.decode_string(s))

            line = "" # "%2d>" % backlightdisp.decode(s) # if you care about the backlight intensity.

            if fdisp.is_freq(s):
                line += "[%s] f = %s %s" % (mode, intWithCommas(fdisp.freq(s)), rxstate)
            else:
                line += "[%s] > %s < %s" % (mode, fdisp.decode(s), rxstate)

            line += str(sorted(miscdisp.decode(s)))

            print(line)
           
        except (Exception) as e:
            print()
            print("Caught exception: " + str(e))
            print()
            print("Input %s" % (s))
            print()
        '''

print("Radio Snoopy", VERSION)
print("radio2head only")

display.fill(0)
display.text("Radio Snoopy", 0, display_line(0))
display.text("radio2head only", 0, display_line(3))
display.text(VERSION, 0, display_line(7))
display.show()

curline = b""

while True:
    led.toggle()
    time.sleep(0.1)
    
    if radio_poll_obj.poll(0):
        x = radio_uart.read()
        print("curline before += ", type(curline))
        curline += x
        print("curline after += ", type(curline))
         
        print("curline=", curline)
        
        if -1 != curline.find(b"AL~READY"):
            print("GOT AL~READY.")
            n = curline.find(b"AL~READY")
            curline = curline[n+8+1:]
        
        if 1 <= curline.find(b"LCSA"):
            print("SEEK to LCSA: %d" % curline.find(b"LCSA"))
            print()
            n = curline.find(b"LCSA")
            radio_uart.write(curline[0:n])
            curline = curline[n:]
        
        while len(curline) >= 34:
            print("curline before print_state ", type(curline))
            #print("line: " + "".join([ "%02x" % ord(c) for c in curline ]))
            print_state(curline[0:34])
            print("curline after print_state ", type(curline))
            radio_uart.write(curline[0:34])
            curline = curline[34:]
        