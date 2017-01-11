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
