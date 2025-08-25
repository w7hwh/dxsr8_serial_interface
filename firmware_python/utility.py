"""
utility.py

 Various common routines

 last edit: 20250725 1050 hrs by hwh

 edit history:


 todo:
    add clr_bit(bytes, offset)
    add set_bit(bytes, offset, value)
    add set_byte(bytes, offset, value)
    
"""
def get_bit(bytes, offset):
    i = int(offset)//8
    j = offset % 8

    if (bytes[i] & (1<<j)) != 0:
        return 1
    return 0

def set_bit(bytes, offset):
    i = int(offset)//8
    j = offset % 8

    bytes[i] |= (1<<j);
    return bytes

# ---------------------

# returns a string of hex values separated by spaces
def hexBytes(b):
    return ''.join(['{:02x} '.format(i) for i in b])
    
# returns a string of hex values separated by spaces
# but with printable characters not in hex
# to avoid confusion space is still printed as hex
def hexBytes2(b):
    ret = ''
    for i in b:
        if i > 32 and i < 127:
            ret += chr(i) + '  '
        else:
            ret += '{:02x} '.format(i)
    return ret
    
    
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



def print_bit_header(spaces, length):
    
    print(' '*spaces, end = '')
    print('-'*((length*3)-1))
    
    print(' '*spaces, end = '')
    for i in range(length):
        print("%2d" % ((i*8)//100), end = ' ')
    print()
    
    print(' '*spaces, end = '')
    for i in range(length):
        print("%02d" % ((i*8)%100), end = ' ')
    print()

    print(' '*spaces, end = '')
    print('-'*((length*3)-1))
