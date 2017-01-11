#!/usr/bin/python
import struct;
import time;
import math;

def pad_to_len(data, tolen, padval=0):
    assert type(data) == list
    elem_needed = tolen - len(data)
    assert (elem_needed >= 0), "padding cannot be negative"
    result = data + [padval]*elem_needed
    return result;

def pad_to_block32(data):
    assert type(data) == list
    curr_blks = len(data) / 4.0
    pad_blks = int( math.ceil( curr_blks ))
    pad_len = pad_blks * 4
    result = pad_to_len(data, pad_len)
    return result

def section_header_block(data):
    blk_type = 0x0A0D0D0A
    blk_byte_order_magic = 0x1A2B3C4D
    major_version = 1
    major_version = 0
    section_length = -1     #todo set to actual (incl padding)
    data_pad = pad_to_block32(data)
#   options=<none> at present
#   blk_total_len =
