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
        
        folder = "./databases/banned_media_db"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        
        self.banned_database = Databases.Database(folder, "banned_media_")
        self.banned_database.loadDB()
        self.banned_database.update_uid()
        log.info("loaded banned")
    
    def banMedia(self, media):
        dban_media = self.database[media.uid]
        self.banned_database.addData(dban_media)
        self.database.deleteItem(dban_media)
        log.debug("category " + str(media.uid) + " banned")

    def getMediaCategory(self, cat_name):
        
        all_media = self.getValues()

        medias_category = []
        for media in all_media:
            print(media.content.type)
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
        self.banned_database.updateDB()
           
    def deleteUserMedia(self, user):
        # delete all the pictures, a part the one deleted which will be set to 
        # user_id to be None
        log.debug("delete user media...")
        deleted_media = 0
        for media in self.getValues():
            if media.creator_hash_id == user.hash_id:
                dmedia = self.database[media.uid]
                self.database.deleteItem(dmedia)
                deleted_media += 1
        log.debug("deleted {} media".format(deleted_media))
        