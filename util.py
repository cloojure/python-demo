#!/usr/bin/python
import struct;
import time;
import math;

def fmt_pcap_hdr( ts_sec, ts_usec, incl_len, orig_len ):
    print( (ts_sec, ts_usec, incl_len, orig_len) );
    packed = struct.pack( '>LLLL', ts_sec, ts_usec, incl_len, orig_len);
    print( 'packed:  %r' % packed );
    return packed;

def split_float( fval ):
    frac, whole = math.modf( fval );
    micros = int( round( frac * 1000000 ));
    return int(whole), micros

def curr_utc_time_tuple():
    utc_secs = time.time();
    secs, usecs = split_float( utc_secs );
    return secs, usecs;

def timetup_to_float( secs, usecs ):
    return secs + (usecs / 1000000.0)

def timetup_subtract( ts1, ts2 ):
    (s1, us1) = ts1
    (s2, us2) = ts2
    t1 = timetup_to_float( s1, us1 );
    t2 = timetup_to_float( s2, us2 );
    delta = t2 - t1;
    return delta;

def str_to_bytearray( arg ):
    bytearr = map( int, bytearray(arg) );
    return bytearr;

def bytearray_to_chrarray( arg ):
  charArray = map( chr, arg );
  return charArray;

def chrarray_to_str( arg ):
  strval = ''.join( arg );
  return strval;

def bytearray_to_str( arg ):
  strval = chrarray_to_str( bytearray_to_chrarray(arg) );
  return strval;

