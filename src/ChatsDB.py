# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 00:07:27 2018

@author: Mauro
"""

#==============================================================================
# imports
#==============================================================================

import logging
import datetime

import Databases


#==============================================================================
# logging
#==============================================================================
# create logger
log = logging.getLogger(__name__)

# set logger level
log.setLevel(logging.DEBUG)

# create a file handler
fh = logging.FileHandler("./log_files/log_" + datetime.datetime.now().strftime("%y%m%d") + ".log")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# create console and file handler
log.addHandler(fh)
sh = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(message)s')
sh.setFormatter(formatter)
log.addHandler(sh)


#==============================================================================
# ChatDB
#==============================================================================

class ChatsDB:
    
    def __init__(self):
        folder = "./databases/chats_db"
        self.database = Databases.Database(folder)
        self.database.loadDB()
        log.info("loaded chats db")
        
        names = [data.filename for data in self.database.db.values() ]
        last_uid = 0
        if names:
            uids = [int(name.split("_")[1]) for name in names]
            uids = sorted(uids)
            last_uid = uids[-1]
            log.info("last uid:{}".format(last_uid))
        
        self.short_uid = last_uid + 1
        
    def addChat(self, chat):

        chat_id = chat.id
        
        if not ( chat_id in self.database.db ):
            log.info("added new chat to database: {}".format(self.short_uid))
            data = Databases.Data(chat_id, chat, "chat_" + str(self.short_uid))
            self.database.db[chat_id] = data
            self.short_uid += 1
    
    def update(self):
        log.debug("updating database...")
        self.database.updateDB()