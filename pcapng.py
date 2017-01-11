#!/usr/bin/python
import struct;
import time;
import math;

def pad_to_len(data, tolen, padval=0):
    needed = tolen - len(data)
    assert (needed >= 0), "padding cannot be negative"
    result = data + [padval]*needed
    return result;



def section_header_block(data):
    blk_type = 0x0A0D0D0A
    blk_byte_order_magic = 0x1A2B3C4D
    major_version = 1
    major_version = 0
    section_length = -1     #todo set to actual (incl padding)
#   options=<none> at present
#   blk_total_len =
