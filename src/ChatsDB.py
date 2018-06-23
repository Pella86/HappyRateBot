# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 00:07:27 2018

@author: Mauro
"""

#==============================================================================
# imports
#==============================================================================

import Databases
import Logging


#==============================================================================
# logging
#==============================================================================
# create logger
log = Logging.get_logger(__name__, "INFO")

#==============================================================================
# ChatDB
#==============================================================================

class ChatsDB:
    
    def __init__(self):
        folder = "./databases/chats_db"
        self.database = Databases.Database(folder, "chat_")
        self.database.loadDB()
        self.database.update_uid()
        log.info("loaded chats db")
        
    def addChat(self, chat):

        chat_id = chat.id
        
        if self.database.isNew(chat_id):
            log.info("added new chat to database: {}".format(self.database.short_uid))
            data = Databases.Data(chat_id, chat)
            self.database.addData(data)
    
    def update(self):
        log.info("updating database...")
        self.database.updateDB()