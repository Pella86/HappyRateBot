# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 00:08:09 2018

@author: Mauro
"""

import os
import struct

class BannedItem:
    
    def __init__(self, id):
        self.id = id
        



class BannedItems:
    
    
    def __init__(self, file, file_type):
        self.file = file
        self.ids = []
        self.file_type = file_type
    
    def loadFile(self):
        co = 0
        with open(self.file, "rb") as f:
            nitems = struct.unpack('i', f.read(4))[0]
            co += 4
            f.seek(co)
            
            for i in range(nitems):
                byte_size = int(struct.unpack("B", f.read(1))[0])
                co += 1
                f.seek(co)
                if self.file_type == "c":
                    id = struct.unpack(self.type, f.read(byte_size))
                    id = "".join(id)
                elif self.file_type == "x":
                    id = struct.unpack(self.type, f.read(byte_size))[0]
                self.ids.append(id)
                co += byte_size
                f.seek(co)
    
    def addItem(self, item):
        with open(self.file, "ab") as f:
            #write size
            if self.file_type == "c":
                s = len(item)
            # how do i calculte the bit lengths?
            f.write()
                
                
                
            
        
        
    
    def addItem(self, )