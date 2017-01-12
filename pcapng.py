#!/usr/bin/python
import struct;
import time;
import math;
import linktype;
import util;

#todo options (for all)

def section_header_block(data):
    assert type(data) == list
    data_pad = util.pad_to_block32(data)
    data_pad_len = len(data_pad)
    print( 'data_pad_len %r' % data_pad_len )

    blk_type = 0x0A0D0D0A
    byte_order_magic = 0x1A2B3C4D
    major_version = 1
    minor_version = 0
    section_len = -1        #todo set to actual (incl padding)
    options_bytes=[]        #todo none at present
    options_str = util.byte_list_to_str(options_bytes)
    header_len = ( 4 +      # block type
                   4 +      # block total length
                   4 +      # byte order magic
                   2 + 2 +  # major version + minor version
                   8 +      # section length
                   len(options_bytes) +
                   4 )      # block total length
    blk_total_len = header_len + data_pad_len
    header = ( struct.pack( '=LlLhhq', blk_type, blk_total_len, byte_order_magic,
                                       major_version, minor_version, section_len ) +
               options_str + 
               struct.pack( '=l', blk_total_len ))
    return header

def interface_desc_block():
    blk_type = 0x00000001
    link_type = linktype.LINKTYPE_ETHERNET   # todo how determine?
    reserved = 0
    snaplen = 0                     # 0 => no limit
    options_bytes=[]                #todo none at present
    options_str = util.byte_list_to_str(options_bytes)
    util.assert_block32_size( options_bytes )
    blk_total_len = (  4 +         # block type
                       4 +         # block total length
                       2 + 2 +     # linktype + reserved
                       4 +         # snaplen
                       len(options_bytes) +
                       4 )         # block total length
    header = ( struct.pack( '=LlHHl', blk_type, blk_total_len, link_type, reserved,
                                      snaplen ) +
               options_str + 
               struct.pack( '=l', blk_total_len ))
    return header

def simple_pkt_block(pkt_data):
    assert type(pkt_data) == list
    pkt_data_pad     = util.pad_to_block32(pkt_data)
    pkt_data_pad_str = util.byte_list_to_str( pkt_data_pad )
    blk_type = 0x00000003
    original_pkt_len = len(pkt_data)
    pkt_data_pad_len = len(pkt_data_pad)
    blk_total_len = ( 4 +      # block type
                      4 +      # block total length
                      4 +      # original packet length
                      pkt_data_pad_len +
                      4 )      # block total length
    block = ( struct.pack( '=LLL', blk_type, blk_total_len, original_pkt_len ) +
              pkt_data_pad_str + 
              struct.pack( '=L', blk_total_len ))
    return block


