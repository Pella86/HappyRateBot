# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 23:34:20 2018

@author: Mauro
"""
#==============================================================================
# Imports
#==============================================================================

#pyimports
import os
import string

# my imports
import Databases
import Logging

#==============================================================================
# logging
#==============================================================================
# create logger
log = Logging.get_logger(__name__, "DEBUG")

#==============================================================================
# Categories Database
#==============================================================================
class CategoriesDB:
    
    def __init__(self):
        self.folder = "./databases/categories_db"
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        
        self.database = Databases.Database(self.folder, "category_")
        self.database.loadDB() 
        self.database.update_uid()
        log.info("loaded db") 
    
    def getValues(self):
        return self.database.getValues()
    
    def isPresent(self, catname):
        return not self.database.isNew(catname.lower())
    
    
    def checkName(self, text):
        error_message = True
        
        alphanumeric = string.ascii_letters + string.digits
        
        if len(text) < 3:
            error_message = "too short"
        elif len(text) >= 15:
            error_message = "too long"
        
        elif not all(c in alphanumeric for c in text):
            error_message = "invalid character"
        
        return error_message
    
    def addCategory(self, category):
        if self.database.isNew(category.name_id):
            data = Databases.Data(category.name_id, category)
            self.database.addData(data)
            return True
        return False
    
    def update(self):
        log.info("updating database...")
        self.database.updateDB()
        