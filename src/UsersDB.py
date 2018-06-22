# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:10:14 2018

@author: Mauro
"""
#==============================================================================
# Imports
#==============================================================================
# py imports
import os
import logging
import datetime
import hashlib
import string

# my imports
import Databases
import UserProfile
import random

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
sh = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(message)s')
sh.setFormatter(formatter)
log.addHandler(sh)

#==============================================================================
# Helpers
#==============================================================================
def get_hash_id(personid):
    pid = hashlib.sha256()
    pid.update(bytes(personid))
    
    return pid.digest()   

#==============================================================================
# User database
#==============================================================================
class UsersDB:
    
    def __init__(self):
        self.folder = "./databases/user_db"
        if not os.path.isdir(self.folder):
            os.mkdir(self.folder)
        
        self.database = Databases.Database(self.folder)
        self.database.loadDB()
        log.info("loaded users database")
        
        names = [data.filename for data in self.database.db.values() ]
        last_uid = 0
        if names:
            uids = [int(name.split("_")[1]) for name in names]
            uids = sorted(uids)
            last_uid = uids[-1]
            log.debug("last uid:{}".format(last_uid))
        
        self.short_uid = last_uid + 1 
    
    def check_nickname(self, user, text):
        
        error_message = None
        
        alphanumeric = string.ascii_letters + string.digits
        
        if len(text) < 3:
            error_message = "too short"
        elif len(text) >= 15:
            error_message = "too long"
        
        elif not all(c in alphanumeric for c in text):
            error_message = "invalid character"
        
        elif text in [u.display_id for u in self.database.getValues()]:
            error_message = "already present"
        
        if error_message is None:
            user.display_id = text
            self.database[user.hash_id].setData(user)
            return True
        else:
            return error_message
        

    def addUser(self, person, chatid):
        # hash the id

        hash_id = get_hash_id(person.id)
        
        if not ( hash_id in self.database.db ):
            log.info("added new user to database: {}".format(self.short_uid))
            # create a new user
            
            # create a unique display id
            start_number = 0x10000000
            stop_number = 0xFFFFFFFF
            display_id = random.randint(start_number,stop_number)
            log.debug("display id {}".format(display_id))
            display_id_list = [user.display_id for user in self.database.getValues()]
            while display_id in display_id_list:
                display_id = random.randint(start_number,stop_number)
                log.debug("new display id {}".format(display_id))                
            
            lang_tag = person.language_code if person.language_code else "en"

            user = UserProfile.UserProfile(hash_id, display_id, chatid, lang_tag)
            data = Databases.Data(hash_id, user, "user_" + str(self.short_uid))
            self.database.db[hash_id] = data
            self.short_uid += 1 
            return user
    
    def deleteUser(self, user):
        data = self.database[user.hash_id]
        os.remove(os.path.join(self.folder, data.filename + ".pickle"))
        self.database.deleteItem(user.hash_id)
        
        
    def getUser(self, person):
        log.debug("User already in database, got user")
        hash_id = get_hash_id(person.id)
        return self.database.db[hash_id].getData()
    
    def setUser(self, user):
        self.database.db[user.hash_id].setData(user)

    def update(self):
        log.info("updating database...")
        self.database.updateDB()
        
        