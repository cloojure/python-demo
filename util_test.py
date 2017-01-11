#!/usr/bin/python
import struct;
import time;
import math;
import util;

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4

def test_xxx():
    xx1 = struct.pack( '>hhl', 1, 2, 3 );  # h='short', l='long'
    xx2 = struct.unpack( '>hhl', xx1 )
    assert xx1 == '\x00\x01\x00\x02\x00\x00\x00\x03'
    assert xx2 == ( 1, 2, 3 );

    assert 3 == len( [ 1, 2, 3] );
    assert (3, 140000) == util.split_float(3.14);
    assert (3, 141593) == util.split_float(3.141592654);

    assert [97, 98, 99]      == util.str_to_bytearray(       'abc'           )
    assert ['a', 'b', 'c']   == util.bytearray_to_chrarray(  [97, 98, 99]    )
    assert 'abc'             == util.bytearray_to_str(       [97, 98, 99]    )
    assert 'abc'             == util.chrarray_to_str(        ['a', 'b', 'c'] )

    ts1 = util.curr_utc_time_tuple();
    time.sleep(0.1);
    delta = util.timetup_subtract( ts1, util.curr_utc_time_tuple() );
    assert ((0.09 < delta) and (delta < 0.11))
