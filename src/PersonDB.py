# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 21:37:49 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import hashlib
import logging
import datetime

import Databases

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
# Persons databases
#==============================================================================
class PersonDB:
    
    def __init__(self):
        folder = "./databases/persons_db"
        self.database = Databases.Database(folder)
        self.database.loadDB()
        log.info("loaded persons db")
        
        names = [data.filename for data in self.database.db.values() ]
        last_uid = 0
        if names:
            uids = [int(name.split("_")[1]) for name in names]
            uids = sorted(uids)
            last_uid = uids[-1]
            log.debug("last uid:{}".format(last_uid))
        
        self.short_uid = last_uid + 1
    
    def addPerson(self, person):
        # hash the id
        pid = hashlib.sha256()
        pid.update(bytes(person.id))
        
        hash_id = pid.digest()
        
        if not ( hash_id in self.database.db ):
            log.info("added new person to database: {}".format(self.short_uid))
            data = Databases.Data(hash_id, "place holder", "person_" + str(self.short_uid))
            self.database.db[hash_id] = data
            self.short_uid += 1
    
    def update(self):
        log.info("updating database...")
        self.database.updateDB()

if __name__ == "__main__":
    print("hi")