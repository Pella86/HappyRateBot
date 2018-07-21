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
import BannedItems

#==============================================================================
# logging
#==============================================================================
# create logger
log = Logging.get_logger(__name__, "WARNING")

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
        
        self.banned_categories = BannedItems.BannedItems("./databases/banned_categories.bic", "string")
    
    def getKeys(self):
        return list(self.database.keys())
        
    def deleteCategory(self, cat_name):
        dcat = self.database[cat_name]
        self.database.deleteItem(dcat)
    
    def banCategory(self, cat_name):
        #move the category from the database to the banned database
        self.banned_categories.addItem(cat_name)
        
        dcat = self.database[cat_name]
        self.database.deleteItem(dcat)
        log.debug("category " + cat_name + " banned")
    
    def getValues(self):
        return self.database.getValues()

    def isPresent(self, catname):
        is_present_database = not self.database.isNew(catname.lower())
        is_present_banned_database = catname in self.banned_categories.ids
        return is_present_database or is_present_banned_database
    
    def getCategory(self, cat_name):
        return self.database[cat_name].getData()
    
    
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
    
    def setCategory(self, category):
        self.database[category.name_id].setData(category)
    
    def addCategory(self, category):
        if not self.isPresent(category.name_id):
            data = Databases.Data(category.name_id, category)
            self.database.addData(data)
            return True
        return False
    
    def update(self):
        log.info("updating database...")
        self.database.updateDB()

    def deleteCategoryUser(self, user, mediavotedb):
        # rimuovi tutti i files contenuti nella categoria?
        user_categories = []
        deleted_categories = 0
        for category in self.getValues():
            if category.creator == user.hash_id:
                user_categories.append(category.name_id)
                dcat = self.database[category.name_id]
                self.database.deleteItem(dcat)
                deleted_categories += 1
        log.debug("deleted {} categories".format(deleted_categories))
        
        log.debug("user categories:")
        log.debug(user_categories)
        
        log.debug("deleteing media in the user categories...")
        deleted_media = 0
        for media in mediavotedb.getValues():
            if media.cat_name in user_categories:
                dmedia = mediavotedb.database[media.uid]
                mediavotedb.database.deleteItem(dmedia)
                deleted_media += 1
        log.debug("deleted {} media".format(deleted_media))
                    
                