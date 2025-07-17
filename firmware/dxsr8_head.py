"""
dxsr8_head.py

 Decodes/Encodes the info sent from the head to the radio
    
    SWDV  decodes rit, ifshift, squelch, and volume
    SWDR  decodes the direction of rotation of the frequency dial
    SWDA  related to the frequency dial?
    SWDS  decodes the switches on the front panel
    
 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250715 2045 hrs by hwh


 edit history:

"""
class decode_head:
    
    def _get_bit(bytes, offset):
        i = int(offset)//8
        j = offset % 8

        if (bytes[i] & (1<<j)) != 0:
            return 1
        return 0

    def _set_bit(bytes, offset):
        i = int(offset)/8
        j = offset % 8

        bytes[i] |= (1<<j);
        return bytes

    """
        -------------------------------

        decode_SWDV()
        
        Decodes rit, ifshift, squelch, and volume
                
    """
    def decode_SWDV(b):
        rit = ifshift = squelch = vol = 0
        
        try:
            rit = int(b.decode('ascii')[4:6], 16)
        except:
            pass

        try:
            ifshift = int(b.decode('ascii')[6:8], 16)
        except:
            pass

        try:
            squelch = int(b.decode('ascii')[8:10], 16)
        except:
            pass

        try:
            vol = int(b.decode('ascii')[10:12], 16)
        except:
            pass
        
        return {'rit': rit, 'ifshift':ifshift, 'squelch':squelch, 'vol':vol}

    """
        -------------------------------
 
        decode_SWDR()
        
        This decodes the direction of rotation
        of the frequency dial.
        
        Returns:
            1 = clockwise
            0 = no rotation
           -1 = anticlockwise
            
    """
    def decode_SWDR(b):
        try:
            x = b.decode('ascii')[4:6]
            
            if x == '80':
                return 0    # stopped
            if x == '81':
                return 1    # clockwise
            if x == '7F':
                return -1   # anticlockwise
        except:
            pass
        
        return 0     # defaults to stopped

    """
        -------------------------------
 
        decode_SWDA
        
        This decodes ??? related to the frequency dial???
        
        example: b'SWDR81SWDA00000000818353SWDR810100\r\n'
        
                 SWDR81
                 SWDA00000000818353
                 SWDR810100

        Returns:
            
            
    """
    def decode_SWDA(b):

        return "not implemented yet"        # TODO:

    """
        -------------------------------
        
        decode_SWDS()
        
        This routine decodes the switches on the front panel
        
    """

    KEYS = {
        'MF': 72,
        '1': 34,
        '2': 33,
        '3': 32,
        '4': 43,
        '5': 42,
        '6': 41,
        '7': 40,
        '8': 51,
        '9': 50,
        '*': 49,
        '0': 35,
        'ENT': 48,
        'FUNC': 75,
        'RIT': 74,
        'KEY': 73,
        'MODE': 67,
        'V/M': 66,
        'M/KHz': 65,
        'RF': 64,
        'UP': 83,
        'DOWN': 82
        }


    def decode_SWDS(b):        
        retval = []

        try:
            for key,bit in decode_head.KEYS.items():
                if 1 == decode_head._get_bit(b, bit):
                    retval.append(key)
        except:
            pass
        
        return retval

'''
    def encode_SWDS(button):
        keyblank = "SWDS000000000100\r\n"

        if button == None:
            return keyblank
        
        blank_bytes = [ ord(c) for c in keyblank ]

        
        o = KEYS[button]
        bytes = _set_bit(blank_bytes, o)

        return "".join([chr(c) for c in bytes])
'''