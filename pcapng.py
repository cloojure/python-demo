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

def assert_block32_size(data):
    assert type(data) == list
    assert (0 == len(data) % 4), "data must be 32-bit aligned"
    return True;


def section_header_block(data):
    data_pad = pad_to_block32(data)

    blk_type = 0x0A0D0D0A
    byte_order_magic = 0x1A2B3C4D
    major_version = 1
    major_version = 0
    section_length = -1     #todo set to actual (incl padding)
    options_bytes=[]        #todo none at present
    options_str = util.bytearray_to_str( options_bytes )
    blk_total_len = ( 4 +       # block type
                      4 +       # block total length
                      4 +       # byte order magic
                      2 + 2 +   # major version + minor version
                      8 +       # section length
                      len(options_bytes) +
                      4 )       # block total length
    header = ( struct.pack( '!LlLhhq', blk_type, blk_total_len, byte_order_magic,
                                       major_version, minor_version, section_len ) +
               options_str + struct.pack( '!l', blk_total_len ))

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
    assert_block32_size( options_bytes )
    block_len_total = ( 4 +       # block type
                        4 +       # block total length
                        2 + 2 +   # linktype + reserved
                        4 +       # snaplen
                        len(options_bytes) +
                        4 )       # block total length



