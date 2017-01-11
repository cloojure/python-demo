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

