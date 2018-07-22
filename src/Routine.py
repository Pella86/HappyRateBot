# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 12:15:08 2018

@author: Mauro
"""

import threading
import time

import Logging

log = Logging.get_logger(__name__, "INFO")

class Routine:
    
    def __init__(self):
        pass
    
    def routine_func(self, usersdb, mediavotedb, catdb):
        log.info("routine function started")
        
        log.debug("Updating karma...")
        for user in usersdb.getUsersList():
            
            user.calculateKarma(mediavotedb)
            
            usersdb.setUser(user)
        usersdb.update()
       
        log.debug("Updating categories db...")
        for category in catdb.getValues():
            category.calculateScore(mediavotedb)
            
            catdb.setCategory(category)
        
        catdb.update()
        
        log.info("Maintenence done.")
    
    def run_routine_func(self, usersdb, mediavotedb, catdb):
        while 1:
            log.debug("\nstart daily mainenece thread\n")
            #t = threading.Thread(target=self.routine_func, args=(catManager,))
            t = threading.Thread(target=self.routine_func, args=(usersdb, mediavotedb, catdb) )
            t.start()
            time.sleep(60*60)