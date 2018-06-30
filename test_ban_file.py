# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 13:17:09 2018

@author: Mauro
"""
import struct

with open("./databases/banned_categories.bic", "rb") as f:
    
    b = f.read()
print(b)
    
l = struct.unpack("I", b[0:4])
print(l)


l = struct.unpack("I", b[4:8])
print(l)