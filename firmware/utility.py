"""
utilities.py

some utility routines

 original written by Josh, AJ9BM
 see https://github.com/jbm9/dxsr8_serial

 last edit: 20250710 1641 hrs by hwh


 edit history:

"""

def _get_bit(bytes, offset):
    i = int(offset)/8
    j = offset % 8

    if (bytes[i] & (1<<j)) != 0:
        return 1
    return 0
    