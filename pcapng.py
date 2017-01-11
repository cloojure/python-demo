#!/usr/bin/python
import struct;
import time;
import math;

def section_header_block(data):
    type = 0x0A0D0D0A
    byte_order_magic = 0x1A2B3C4D
    major_version = 1
    major_version = 0
    section_length = -1     #todo set to actual (incl padding)

    total_len =
