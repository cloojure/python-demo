#!/usr/bin/python
import pytest;
import struct;
import time;
import math;
import util;
import pcapng;

def test_pad_to_len():
    with pytest.raises(AssertionError):
        pcapng.pad_to_len( [1, 2, 3, 4], 3 )
    with pytest.raises(AssertionError):
        pcapng.pad_to_len( 5, 3 )

    assert [0, 0, 0, 0] == pcapng.pad_to_len( [          ], 4 )
    assert [1, 0, 0, 0] == pcapng.pad_to_len( [1,        ], 4 )
    assert [1, 2, 0, 0] == pcapng.pad_to_len( [1, 2      ], 4 )
    assert [1, 2, 3, 0] == pcapng.pad_to_len( [1, 2, 3   ], 4 )
    assert [1, 2, 3, 4] == pcapng.pad_to_len( [1, 2, 3, 4], 4 )

    assert [9, 9, 9, 9] == pcapng.pad_to_len( [          ], 4, 9)
    assert [1, 9, 9, 9] == pcapng.pad_to_len( [1,        ], 4, 9)
    assert [1, 2, 9, 9] == pcapng.pad_to_len( [1, 2      ], 4, 9)
    assert [1, 2, 3, 9] == pcapng.pad_to_len( [1, 2, 3   ], 4, 9)
    assert [1, 2, 3, 4] == pcapng.pad_to_len( [1, 2, 3, 4], 4, 9)

def test_pad_to_block32():
    assert [                      ] == pcapng.pad_to_block32( [                      ] )
    assert [1, 0, 0, 0            ] == pcapng.pad_to_block32( [1                     ] )
    assert [1, 2, 0, 0            ] == pcapng.pad_to_block32( [1, 2                  ] )
    assert [1, 2, 3, 0            ] == pcapng.pad_to_block32( [1, 2, 3               ] )
    assert [1, 2, 3, 4            ] == pcapng.pad_to_block32( [1, 2, 3, 4            ] )
    assert [1, 2, 3, 4, 5, 0, 0, 0] == pcapng.pad_to_block32( [1, 2, 3, 4, 5         ] )
    assert [1, 2, 3, 4, 5, 6, 0, 0] == pcapng.pad_to_block32( [1, 2, 3, 4, 5, 6      ] )
    assert [1, 2, 3, 4, 5, 6, 7, 0] == pcapng.pad_to_block32( [1, 2, 3, 4, 5, 6, 7   ] )
    assert [1, 2, 3, 4, 5, 6, 7, 8] == pcapng.pad_to_block32( [1, 2, 3, 4, 5, 6, 7, 8] )
    
    pcapng.assert_block32_size( [                      ] )
    pcapng.assert_block32_size( [1, 2, 3, 4            ] )
    pcapng.assert_block32_size( [1, 2, 3, 4, 5, 6, 7, 8] )
    with pytest.raises(AssertionError):
      pcapng.assert_block32_size( [1        ] )
    with pytest.raises(AssertionError):
      pcapng.assert_block32_size( [1, 2     ] )
    with pytest.raises(AssertionError):
      pcapng.assert_block32_size( [1, 2, 3  ] )

def test_section_header_block():
    result = pcapng.section_header_block( [1,2,3] )
    assert 28              == len(result)
    assert 0x0A0D0D0A      == util.first( struct.unpack( '=l', result[0:4] ))
    assert 32              == util.first( struct.unpack( '=l', result[4:8] ))
    assert 0x1A2B3C4D      == util.first( struct.unpack( '=L', result[8:12] ))
    assert 1               == util.first( struct.unpack( '=h', result[12:14] ))
    assert 0               == util.first( struct.unpack( '=h', result[14:16] ))
    assert -1              == util.first( struct.unpack( '=q', result[16:24] ))
    assert 32              == util.first( struct.unpack( '=l', result[24:28] ))

def test_interface_desc_block():
    result = pcapng.interface_desc_block()
    assert 20               == len(result)
    assert 0x00000001       == util.first( struct.unpack( '=L', result[0:4] ))
    assert 20               == util.first( struct.unpack( '=l', result[4:8] ))
    assert 1                == util.first( struct.unpack( '=H', result[8:10] ))
    assert 0                == util.first( struct.unpack( '=H', result[10:12] ))
    assert 0                == util.first( struct.unpack( '=l', result[12:16] ))
    assert 20               == util.first( struct.unpack( '=l', result[16:20] ))


