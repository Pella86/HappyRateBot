# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 20:44:58 2018

@author: Mauro
"""
__version__ = "0.0.1"


# import sys to access the src folder
import sys
sys.path.append("./src")

#==============================================================================
# Imports
#==============================================================================

#py imports
import time
import logging
import datetime

# telepot imports
import telepot
from telepot.loop import MessageLoop

# my imports
import BotDataReader
import MessageParser
import PersonDB
import ChatsDB
import UsersDB
import Handle

#==============================================================================
# Logging
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
# handle
#==============================================================================

def handle(raw_msg):
    msg = MessageParser.Message(raw_msg)
    
    persondb.addPerson(msg.mfrom) # logs every person!
    
    if msg.chat.type == "private":
        log.debug("private message received")
        
        chatsdb.addChat(msg.chat)
        chatid = msg.chat.id
#        lang_tag = msg.mfrom.language_code
        
        # add the user 
        usersdb.addUser(msg.mfrom, chatid)
        
        user = usersdb.getUser(msg.mfrom)
        
        log.debug("handle privacy policy")
        Handle.handle_privacy_policy(bot, usersdb, user, msg.content)
        
        if user.accepted_terms == True:
            log.debug("handle rest")
            if msg.content.type == "text":
                Handle.handle_private_text(msg.content.text, bot, user)
        
        chatsdb.update()
        usersdb.update()
    
    persondb.update()
    
    
    

#==============================================================================
# query
#==============================================================================

def query(msg):
    pass

#==============================================================================
# Main
#==============================================================================

if __name__ == "__main__":
    log.info("\n---Happy rate bot---")
    
    bot_data = BotDataReader.BotDataReader("./botdata/bot_data.tbot")
    bot_data.prepareServerRouting()    
    
    bot = telepot.Bot(bot_data.token)
    
    bot_data.updateDataFile(bot)
    
    log.info("Bot data read, bot ready")
    
    persondb = PersonDB.PersonDB()
    chatsdb = ChatsDB.ChatsDB()
    usersdb = UsersDB.UsersDB()
    
    
    log.info("Loaded databases")
    
    response = {
            'chat': handle,
            'callback_query': query
            #'inline_query': inline_query,
            #'chosen_inline_result' : chosen_inline
            }
    
    MessageLoop(bot, response).run_as_thread()
    
    log.info("Message loop started")
    while 1:
        time.sleep(10)    