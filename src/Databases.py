# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 21:12:18 2018

@author: Mauro
"""
#==============================================================================
# Imports
#==============================================================================
import logging
import os
import pickle
import datetime

#==============================================================================
# logging
#==============================================================================
# create logger
log = logging.getLogger(__name__)

# set logger level
log.setLevel(logging.INFO)

# create a file handler
fh = logging.FileHandler("./log_files/log_" + datetime.datetime.now().strftime("%y%m%d") + ".log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# create console and file handler
log.addHandler(fh)
log.addHandler(logging.StreamHandler())

#==============================================================================
# Helper functions
#==============================================================================

def get_pathname(path):
    ''' Little function to split the path in path, name, extension'''
    path, nameext = os.path.split(path)
    name, ext = os.path.splitext(nameext)
    return path, name, ext

#==============================================================================
# Data class
#==============================================================================
class Data:
    
    def __init__(self, id, content, filename):
        self.id = id
        self.content = content
        self.filename = filename
        self.hasChanged = True
    
    def getData(self):
        return self.content
    
    def setData(self, content):
        self.content = content
        self.hasChanged = True
    
    def setId(self, id):
        self.id = id
        self.hasChanged = True

#==============================================================================
# Database class
#==============================================================================
class Database:
    
    
    def __init__(self, folder):
        self.folder = folder
        self.db = {}
    
    
    def loadDB(self):
        log.debug("loading db...")
        files = [os.path.join(self.folder, f) for f in os.listdir(self.folder)]
        
        data_loaded = 0
        for file_name in files:
            _, _, ext = get_pathname(file_name)
            if ext == ".pickle" and os.path.isfile(file_name):
                with open(file_name, 'rb') as f:
                    data = pickle.load(f)
                self.db[data.id] = data
                data_loaded += 1
        log.debug("Loaded {} data".format(data_loaded))
    
    def writeData(self, data):
        filename = self.folder + "/"+ data.filename + ".pickle"
        with open(filename, "wb") as f:
            pickle.dump(data, f)   
            
    def saveDB(self):
        for data in self.db.values():
            self.writeData(data)
    
    def updateDB(self):
        for data in self.db.values():
            if data.hasChanged:
                data.hasChanged = False
                self.writeData(data)
                log.debug("database update!")
                
                
            
        
        
        
        
        