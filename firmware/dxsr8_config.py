"""
dxsr8_config.py

 This class stores the project pin settings, etc.
 
 last edit: 20250715 1000 hrs by hwh

 edit history:


 todo:


"""
from machine import Pin

class dxsr8_config():
    
    led=Pin("LED", Pin.OUT)
    
    baud_rate=38400
    bits=8
    parity=None
    stop=1
    rxbuf=512
    
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

