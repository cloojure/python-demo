#!/usr/bin/python
import struct;
import time;
import math;

print;
print('-------------------------------------------------------');

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

print( 'x10  first=%d second=%f' % (123, 45.6));
frac, whole = math.modf(3.1415);
print( 'x40  curr_utc_time_tuple() ', curr_utc_time_tuple());
print( 'UTC time:  ', time.time() );


fmt_pcap_hdr(1,2,3,4);

print;
data = [
     0xa4, 0x77, 0x33, 0xf1, 0x98, 0xcc, 0x80, 0x3f, 0x5d, 0x22, 0x05, 0x1b, 0x08, 0x00, 0x45, 0x00, 0x00, 0x34, 0x54, 0x93
   , 0x40, 0x00, 0x40, 0x06, 0x61, 0xc2, 0xc0, 0xa8, 0x01, 0x8e, 0xc0, 0xa8, 0x01, 0x90, 0xaf, 0xea, 0x1f, 0x49, 0xbd, 0xcf
   , 0x7a, 0xc1, 0x03, 0x6f, 0x8c, 0xb1, 0x80, 0x10, 0x01, 0x62, 0x67, 0xc9, 0x00, 0x00, 0x01, 0x01, 0x08, 0x0a, 0x00, 0x50
   , 0x36, 0xaa, 0x00, 0x3b, 0xba, 0x08 ];
print( 'len(data)  %d' % len(data) );
print( data );

dd = [97, 98, 99];
print('dd', type(dd), dd);
print('for c in dd')
for c in dd: print(c)

