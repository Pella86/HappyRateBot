# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 11:54:27 2018

@author: Mauro
"""

import os

import Databases
import Logging
import MediaVote

#==============================================================================
# Logging
#==============================================================================

log = Logging.get_logger(__name__, "DEBUG")

#==============================================================================
# Media vote database
#==============================================================================
class MediaVoteDB:
    
    def __init__(self):
        self.folder = "./databases/media_db"
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        
        self.database = Databases.Database(self.folder, "media_")
        self.database.loadDB()
        self.database.update_uid()
        log.info("database loaded")
    
    def getMediaCategory(self, cat_name):
        
        all_media = self.getValues()
        print(all_media)
        
        medias_category = []
        for media in all_media:
            if media.cat_name == cat_name:
                medias_category.append(media)
        return medias_category
    
    def addContent(self, content, cat_name, hash_id):
        
        uid = self.database.short_uid
        
        media = MediaVote.MediaVote(uid, content, cat_name, hash_id)
        
        data = Databases.Data(self.database.short_uid, media)
        
        if self.database.isNew(data.id):
            self.database.addData(data)
    
    def getValues(self):
        return self.database.getValues()
    
    def update(self):
        self.database.updateDB()
        