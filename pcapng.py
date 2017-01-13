#!/usr/bin/python
import struct;
import time;
import math;
import linktype;
import util;

#todo options (for all)

def section_header_block_create():    #todo data_len, options
    blk_type = 0x0A0D0D0A
    byte_order_magic = 0x1A2B3C4D
    major_version = 1
    minor_version = 0
    section_len = -1        #todo set to actual (incl padding)
    options_bytes=[]        #todo none at present
    options_str = util.byte_list_to_str(options_bytes)
    blk_total_len =  ( 4 +      # block type
                       4 +      # block total length
                       4 +      # byte order magic
                       2 + 2 +  # major version + minor version
                       8 +      # section length
                       len(options_bytes) +
                       4 )      # block total length
    header = ( struct.pack( '=LlLhhq', blk_type, blk_total_len, byte_order_magic,
                                       major_version, minor_version, section_len ) +
               options_str + 
               struct.pack( '=l', blk_total_len ))
    return header

def section_header_block_decode(block):
    assert type( block ) == str
    block_type          = util.first( struct.unpack( '=l', block[0:4]   ))
    blk_total_len       = util.first( struct.unpack( '=l', block[4:8]   ))
    byte_order_magic    = util.first( struct.unpack( '=L', block[8:12]  ))
    major_version       = util.first( struct.unpack( '=h', block[12:14] ))
    minor_version       = util.first( struct.unpack( '=h', block[14:16] ))
    section_len         = util.first( struct.unpack( '=q', block[16:24] ))
    blk_total_len_end   = util.first( struct.unpack( '=l', block[24:28] ))

    block_data = {  'block_type'          : block_type ,
                    'blk_total_len'       : blk_total_len ,
                    'byte_order_magic'    : byte_order_magic ,
                    'major_version'       : major_version ,
                    'minor_version'       : minor_version ,
                    'section_len'         : section_len ,
                    'blk_total_len_end'   : blk_total_len_end }
    return block_data

def interface_desc_block_create():
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

def interface_desc_block_decode(block):
    assert type( block ) == str
    block_type              = struct.unpack( '=L', block[0:4]   )[0]
    block_total_len         = struct.unpack( '=l', block[4:8]   )[0]
    link_type               = struct.unpack( '=H', block[8:10]  )[0]
    reserved                = struct.unpack( '=H', block[10:12] )[0]
    snaplen                 = struct.unpack( '=l', block[12:16] )[0]
  # options_str  #todo
    block_total_len_end     = struct.unpack( '=l', block[-4:]   )[0]
    block_data = { 'block_type'              : block_type ,
                   'block_total_len'         : block_total_len ,
                   'link_type'               : link_type ,
                   'reserved'                : reserved ,
                   'snaplen'                 : snaplen ,
                   # options_str  #todo
                   'block_total_len_end'     : block_total_len_end }
    return block_data


def simple_pkt_block_create(pkt_data):
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

def simple_pkt_block_decode(block):
    assert type( block ) == str
    block_type          = util.first( struct.unpack( '=L', block[0:4]  ))
    blk_tot_len         = util.first( struct.unpack( '=L', block[4:8]  ))
    original_pkt_len    = util.first( struct.unpack( '=L', block[8:12] ))
    pkt_data_pad_len    = util.block32_pad_len( original_pkt_len )
    pkt_data            = block[ 12 : (12+original_pkt_len)  ]
    blk_tot_len_end     = util.first( struct.unpack( '=L', block[ -4:blk_tot_len] ))
    result = {  'block_type'          : block_type ,
                'blk_tot_len'         : blk_tot_len ,
                'original_pkt_len'    : original_pkt_len ,
                'pkt_data_pad_len'    : pkt_data_pad_len ,
                'pkt_data'            : pkt_data ,
                'blk_tot_len_end'     : blk_tot_len_end }
    return result

