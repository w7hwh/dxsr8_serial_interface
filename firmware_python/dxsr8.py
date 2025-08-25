"""
dxsr8.py

 This class stores the project pin settings, etc.
 
 last edit: 20250725 1023 hrs by hwh

 edit history:


 todo:


"""
from machine import Pin, UART, I2C
import select
import sh1106

class dxsr8():
    
    led=Pin("LED", Pin.OUT)
    
    #baud_rate=76800
    baud_rate=38400
    #baud_rate=19200
    #baud_rate=9600
    bits=8
    parity=None
    stop=1
    rxbuf=2048
    
    # Pin numbers for head to radio
    head_rx_pin=Pin(5)
    head_tx_pin=Pin(4)
    
    # Pin numbers for radio to head
    radio_rx_pin=Pin(13)
    radio_tx_pin=Pin(12)
    
    # Pin numbers for display
    display_scl_pin=Pin(17)
    display_sda_pin=Pin(16)

    # Pin number for relay
    relay_pin=Pin(22)

    #,rxbuf=1024
    head_uart = UART(1, baudrate=baud_rate, tx=head_tx_pin, rx=head_rx_pin, rxbuf=rxbuf)
    head_uart.init(bits=bits, parity=parity, stop=stop)
    
    head_poll_obj = select.poll()
    head_poll_obj.register(head_uart,select.POLLIN)

    radio_uart = UART(0, baudrate=baud_rate, tx=radio_tx_pin, rx=radio_rx_pin, rxbuf=rxbuf)
    radio_uart.init(bits=bits, parity=parity, stop=stop)
    
    radio_poll_obj = select.poll()
    radio_poll_obj.register(radio_uart,select.POLLIN)

    i2c = I2C(scl=display_scl_pin, sda=display_sda_pin, freq=400000)
    
    # display is 128x64 giving 8 lines of 16 characters
    display = sh1106.SH1106_I2C(128, 64, i2c, None, 0x3c)
    display.sleep(False)
    display.rotate(True)

def display_line(x):
    return x * 8
