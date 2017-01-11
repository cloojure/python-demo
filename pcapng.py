#!/usr/bin/python
import struct;
import time;
import math;

#todo options (for all)

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

def verify_block32(data):
    assert type(data) == list
    assert 0 == len(data) % 4


def section_header_block(data):
    blk_type = 0x0A0D0D0A
    blk_byte_order_magic = 0x1A2B3C4D
    major_version = 1
    major_version = 0
    section_length = -1     #todo set to actual (incl padding)
    data_pad = pad_to_block32(data)
    options_bytes=[]        #todo none at present
#   blk_total_len =

#todo
# http://www.tcpdump.org/linktypes.html
LINKTYPE_ETHERNET   =     1
LINKTYPE_IPV4       =   228
LINKTYPE_IPV6       =   229

def interface_desc_block():
    blk_type = 0x00000001
    link_type = LINKTYPE_ETHERNET   # todo how determine?
    reserved = 0
    snaplen = 0                     # 0 => no limit
    options_bytes=[]                #todo none at present
    block_len_total = ( 4 +       # block type
                        4 +       # block total length
                        2 + 2 +   # linktype + reserved
                        4 +       # snaplen
                        len(options_bytes) +
                        4 )       # block total length
    return None


