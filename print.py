#!/usr/bin/python
import struct;
import time;
import math;
import sam;

print;
print('-------------------------------------------------------');

packed = struct.pack( '>hhl', 1, 2, 3);
print( ':10  packed:   %s   %r   ' % (packed, packed) );
print( ':20  ', packed );

print( ':10  first=%d second=%f' % (123, 45.6));
print( ':20  first=%s second=%s' % (123, 45.6));
print( ':30  first={} second={}'.format( 123, 45.6) );
print( ':40  curr_utc_time_tuple() ', sam.curr_utc_time_tuple());

print( 'UTC time:  ', time.time() );

dd = [97, 98, 99];
print('dd', type(dd), dd);
print('for c in dd')
for c in dd: print(c)

