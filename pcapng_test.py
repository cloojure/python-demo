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

# def test_section_header_block():

result = pcapng.section_header_block( [1,2,3] )
print( ':len()    %r' % len(result) )
print( ':[ 0: 4]  %s' % util.str_to_bytearray( result[0:4] ))
print
for ch in result[4:8]: print( ord(ch) )
print
print( ':[ 4: 8]  %r' % result[4:8] )
print( ':[ 8:12]  %r' % result[8:12] )
print( ':[12:14]  %r' % result[12:14] )
print( ':[14:16]  %r' % result[14:16] )
print( ':[16:24]  %r' % result[16:24] )
print( ':[24:28]  %r' % result[24:28] )

assert 28 == len(result)
# assert ('\n\r\r\n',) == struct.unpack( '!l', result[0:4] )
assert (32,) == struct.unpack( '!l', result[4:8] )
xx = struct.unpack( '!L', result[8:12] )
yy = 0x1A2B3C4D
assert (yy,) == xx
# assert xxx == result[12:14]
# assert xxx == result[14:16]
# assert xxx == result[16:24]
# assert xxx == result[24:28]


