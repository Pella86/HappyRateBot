# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 20:44:56 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import urllib3
import logging
import datetime

import telepot

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
log.addHandler(logging.StreamHandler())

#==============================================================================
# Bot Data Reader
#==============================================================================

class BotDataReader:
    ''' The class reads the tbot file and provides the data to the bot'''
    
    def __init__(self, bot_data_file):
        self.bot_data_file = bot_data_file
        self.id = None
        self.tag = None
        self.token = None
        self.isOnServer = None
        self.read_file()
    
    def read_file(self):
        ''' Reads the bot data file and stores the component in the approriate
        members. The file doesnt have to contain all the members
        '''
        
        # read file
        lines = None
        with open(self.bot_data_file, "r") as f:
            lines = f.readlines()
        
        # parse the lines
        named_data = {}
        for line in lines:
            lparts = line.split("=")
            
            if len(lparts) != 2: raise Exception("Bot reader: wrong fileparts")
            
            value = lparts[1].strip()
            named_data[lparts[0].strip()] =  value if value else None
        
        # assigns the parsed data
        self.id = named_data.get("id")
        self.tag = named_data.get("tag")            
        self.token = named_data.get("token")
        self.isOnServer = True if named_data.get("isOnServer") == "True" else False  
    
    
    def prepareServerRouting(self):
        if self.isOnServer:
            proxy_url = "http://proxy.server:3128"
            telepot.api._pools = {
                'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
            }
            telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

    def createDataFile(self):
        ''' creates the tbot data file with the data given '''
        
        s = ""
        s += "{} = {}\n".format("id", self.id)
        s += "{} = {}\n".format("tag", self.tag)
        s += "{} = {}\n".format("token", self.token)
        s += "{} = {}\n".format("isOnServer", self.isOnServer)    
        
        with open(self.bot_data_file, "w") as f:
            f.write(s)
    
    def updateDataFile(self, bot):
        ''' updates the file with the telegram get me which provide some data 
        given the token'''
        
        updated = False
        
        if self.id is None or self.tag is None:
            data_dict = bot.getMe()
        
        
        if self.id is None:
            self.id = data_dict["id"]
            updated = True
        
        if self.tag is None:
            self.tag = data_dict["username"]
            updated = True
        
        if updated:
            log.info("Updated bot data")
            self.createDataFile()
    