#!/usr/bin/python
import pytest;
import struct;
import time;
import math;
import util;
import pcapng;

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
    result = pcapng.section_header_block( [1,2,3] )
    assert type( result )  == str
    assert 28              == len(result)
    assert 0x0A0D0D0A      == util.first( struct.unpack( '=l', result[0:4]   ))
    assert 32              == util.first( struct.unpack( '=l', result[4:8]   ))
    assert 0x1A2B3C4D      == util.first( struct.unpack( '=L', result[8:12]  ))
    assert 1               == util.first( struct.unpack( '=h', result[12:14] ))
    assert 0               == util.first( struct.unpack( '=h', result[14:16] ))
    assert -1              == util.first( struct.unpack( '=q', result[16:24] ))
    assert 32              == util.first( struct.unpack( '=l', result[24:28] ))

def test_interface_desc_block():
    result = pcapng.interface_desc_block()
    assert type( result )   == str
    assert 20               == len(result)
    assert 0x00000001       == util.first( struct.unpack( '=L', result[0:4]   ))
    assert 20               == util.first( struct.unpack( '=l', result[4:8]   ))
    assert 1                == util.first( struct.unpack( '=H', result[8:10]  ))
    assert 0                == util.first( struct.unpack( '=H', result[10:12] ))
    assert 0                == util.first( struct.unpack( '=l', result[12:16] ))
    assert 20               == util.first( struct.unpack( '=l', result[16:20] ))

def decode_simple_pkt_block( block ):
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

def test_simple_pkt_block():
    block_str = pcapng.simple_pkt_block( [1,2,3] )
    block_data = decode_simple_pkt_block( block_str )
    assert type( block_str )                == str
    assert type( block_data )               == dict
    assert block_data['block_type']         == 0x00000003
    assert block_data['blk_tot_len']        == 20
    assert block_data['blk_tot_len']        == block_data['blk_tot_len_end']
    assert block_data['blk_tot_len']        == len(block_str)
    assert block_data['blk_tot_len']        == 16 + block_data['pkt_data_pad_len']
    assert block_data['original_pkt_len']   == 3
    assert block_data['pkt_data']           == util.byte_list_to_str( [1,2,3] )


