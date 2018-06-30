# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 00:08:09 2018

@author: Mauro
"""

import bfh
import io
import os

import Logging

#==============================================================================
# Logging
#==============================================================================

log = Logging.get_logger(__name__, "WARNING")

#==============================================================================
# Banned Items class
#==============================================================================
class BannedItems:
    
    
    def __init__(self, file, item_type):
        self.file = file
        
        if not os.path.isfile(self.file):        
            with open(self.file, "wb") as f:
                bf = bfh.BinaryFile(f)
                bf.write("I", 0)        
        
        self.ids = []
        self.item_type = item_type
        
        self.loadFile()
        

    
    def loadFile(self):
        
        with open(self.file, "rb") as f:
            bf = bfh.BinaryFile(f)
            
            nitems = bf.read('I')
            
            for i in range(nitems):
                if self.item_type == "string":
                    item = bf.read_string()
                elif self.item_type == "hash_id":
                    item = bf.read_256hash()
                else:
                    item = bf.read(self.item_type)
            self.ids.append(item)
        
        log.debug("read items:")
        for item in self.ids:
            log.debug("{}".format(item))
    
    def addItem(self, item):
        
        if item in self.ids:
            raise Exception("Banned items duplicate id")
        
        self.ids.append(item)
        
        with open(self.file, "wb") as f:
            # change the size
            co = 0
            bf = bfh.BinaryFile(f, co)
            bf.write('I', len(self.ids))
            
            # adjust offset
            co = bf.file.seek(0, io.SEEK_END)
            bf.co = co
            
            # write data
            if self.item_type == "string":
                bf.write_string(item)
            elif self.item_type == "hash_id":
                bf.write_256hash(item)
            else:
                bf.write(self.item_type, item)
        
        
