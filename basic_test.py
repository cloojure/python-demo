#!/usr/bin/python
import struct;
import time;
import math;
import pytest;
import util;

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def thrower():
    assert False, 'forgetaboutit'

def test_pack():
    assert '\x00\x05\x00\x06' == struct.pack( '>hh', 5, 6)
    assert '\x00\x05\x00\x06' == bytearray( [0, 5, 0, 6] )

print( ':00  %r' % struct.pack( '>hh', 5, 6) )
print( ':10  %s' % r'\x00\x05\x00\x06' )
print(        r'\x00\x05\x00\x06' )
print( ':20  %s' %  '\x00\x05\x00\x06' )
print( ':30  %r' %  '\x00\x05\x00\x06' )
print( ':40  %r' %  bytearray( [0, 5, 0, 6] ) )

def test_concat():
    assert [1, 2, 3] == [1, 2] + [3]

def test_xxx():
    assert 3 == 2 + 1
    assert 0x0103 == (1*16**2 + 0*16 + 3)
    assert 3 == (7 % 4)

    assert 0x0103 == (1*16**2 + 0*16 + 3)
    assert 3 == (7 % 4)
    assert [0, 0, 0] == [0]*3
    with pytest.raises(ZeroDivisionError):
        1 / 0
    with pytest.raises(AssertionError):
        assert 1 == 0
    with pytest.raises(AssertionError):
        thrower()

    assert type( [1,2,3] ) == list
    assert type( 3 ) == int
    assert type( 3.14 ) == float
    assert type( "abc" ) == str
    assert 3 != 4

    assert 4 == math.ceil( 3.14 )
    assert 4 == math.ceil( 4.0 )
    x = (2 +    # demo line continuation
         3)
    assert 5 == x
    assert 0 == 4 % 4
    assert 1 == 5 % 4
    assert 2 == 6 % 4
    assert 3 == 7 % 4


