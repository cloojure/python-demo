#!/usr/bin/python
import pytest;
import struct;

import linktype;
import pcapng;
import util;
import pcapng


def test_block32_pad_len():
    assert 0 == util.block32_pad_len(  0 )

    assert 4 == util.block32_pad_len(  1 )
    assert 4 == util.block32_pad_len(  2 )
    assert 4 == util.block32_pad_len(  3 )
    assert 4 == util.block32_pad_len(  4 )

    assert 8 == util.block32_pad_len(  5 )
    assert 8 == util.block32_pad_len(  6 )
    assert 8 == util.block32_pad_len(  7 )
    assert 8 == util.block32_pad_len(  8 )

def test_pad_to_len():
    with pytest.raises(AssertionError):
        util.pad_to_len( [1, 2, 3, 4], 3 )
    with pytest.raises(AssertionError):
        util.pad_to_len( 5, 3 )

    assert [0, 0, 0, 0] == util.pad_to_len( [          ], 4 )
    assert [1, 0, 0, 0] == util.pad_to_len( [1,        ], 4 )
    assert [1, 2, 0, 0] == util.pad_to_len( [1, 2      ], 4 )
    assert [1, 2, 3, 0] == util.pad_to_len( [1, 2, 3   ], 4 )
    assert [1, 2, 3, 4] == util.pad_to_len( [1, 2, 3, 4], 4 )

    assert [9, 9, 9, 9] == util.pad_to_len( [          ], 4, 9)
    assert [1, 9, 9, 9] == util.pad_to_len( [1,        ], 4, 9)
    assert [1, 2, 9, 9] == util.pad_to_len( [1, 2      ], 4, 9)
    assert [1, 2, 3, 9] == util.pad_to_len( [1, 2, 3   ], 4, 9)
    assert [1, 2, 3, 4] == util.pad_to_len( [1, 2, 3, 4], 4, 9)

def test_pad_to_block32():
    assert [                      ] == util.pad_to_block32( [                      ] )
    assert [1, 0, 0, 0            ] == util.pad_to_block32( [1                     ] )
    assert [1, 2, 0, 0            ] == util.pad_to_block32( [1, 2                  ] )
    assert [1, 2, 3, 0            ] == util.pad_to_block32( [1, 2, 3               ] )
    assert [1, 2, 3, 4            ] == util.pad_to_block32( [1, 2, 3, 4            ] )
    assert [1, 2, 3, 4, 5, 0, 0, 0] == util.pad_to_block32( [1, 2, 3, 4, 5         ] )
    assert [1, 2, 3, 4, 5, 6, 0, 0] == util.pad_to_block32( [1, 2, 3, 4, 5, 6      ] )
    assert [1, 2, 3, 4, 5, 6, 7, 0] == util.pad_to_block32( [1, 2, 3, 4, 5, 6, 7   ] )
    assert [1, 2, 3, 4, 5, 6, 7, 8] == util.pad_to_block32( [1, 2, 3, 4, 5, 6, 7, 8] )
    
    util.assert_block32_size( [                      ] )
    util.assert_block32_size( [1, 2, 3, 4            ] )
    util.assert_block32_size( [1, 2, 3, 4, 5, 6, 7, 8] )
    with pytest.raises(AssertionError):
      util.assert_block32_size( [1        ] )
    with pytest.raises(AssertionError):
      util.assert_block32_size( [1, 2     ] )
    with pytest.raises(AssertionError):
      util.assert_block32_size( [1, 2, 3  ] )

def test_section_header_block():
    block_str     = pcapng.section_header_block_create()
    block_data    = pcapng.section_header_block_decode(block_str)
    assert type( block_str  )  == str
    assert type( block_data )  == dict

    assert block_data['block_type']           == 0x0A0D0D0A
    assert block_data['blk_total_len']        == 28
    assert block_data['blk_total_len']        == len( block_str )
    assert block_data['blk_total_len']        == block_data['blk_total_len_end']
    assert block_data['byte_order_magic']     == 0x1A2B3C4D
    assert block_data['major_version']        == 1
    assert block_data['minor_version']        == 0
    assert block_data['section_len']          == -1


def test_interface_desc_block():
    block_str    = pcapng.interface_desc_block_create()
    block_data   = pcapng.interface_desc_block_decode(block_str)
    assert type( block_str )     == str
    assert type( block_data )    == dict

    assert block_data['block_type']          == 0x00000001
    assert block_data['block_total_len']     == 20
    assert block_data['block_total_len']     == block_data['block_total_len_end']
    assert block_data['block_total_len']     == len(block_str)
    assert block_data['link_type']           == linktype.LINKTYPE_ETHERNET
    assert block_data['reserved']            == 0
    assert block_data['snaplen']             == 0


def test_simple_pkt_block():
    block_str   = pcapng.simple_pkt_block_create([1, 2, 3])
    block_data  = pcapng.simple_pkt_block_decode(block_str)
    assert type( block_str )                == str
    assert type( block_data )               == dict
    assert block_data['block_type']         == 0x00000003
    assert block_data['blk_tot_len']        == 20
    assert block_data['blk_tot_len']        == block_data['blk_tot_len_end']
    assert block_data['blk_tot_len']        == len(block_str)
    assert block_data['blk_tot_len']        == 16 + block_data['pkt_data_pad_len']
    assert block_data['original_pkt_len']   == 3
    assert block_data['pkt_data']           == util.byte_list_to_str( [1,2,3] )


