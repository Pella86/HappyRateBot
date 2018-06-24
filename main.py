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

# telepot imports
import telepot
from telepot.loop import MessageLoop

# my imports
import BotDataReader
import MessageParser
import PersonDB
import ChatsDB
import UsersDB
import CategoriesDB
import MediaVoteDB
import Handle
import Logging
from src.language_support.LanguageSupport import _

#==============================================================================
# Logging
#==============================================================================

# create logger
log = Logging.get_logger(__name__, "DEBUG")

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

        # add the user 
        usersdb.addUser(msg.mfrom, chatid)
        
        user = usersdb.getUser(msg.mfrom)
        
        # check if user is active?
        user.isActive = True

        if user.accepted_terms == False:
            log.debug("handle privacy policy")
            Handle.handle_privacy_policy(bot, usersdb, user, msg.content)        
        else:
            
            send_main_menu = True
            send_main_menu = Handle.handle_content(msg.content, bot, user, categoriesdb, mediavotedb)
            
            
            if msg.content.type == "text" and send_main_menu:
                log.debug("Message: " + msg.content.text.encode("utf-8").decode("utf-8", "backslashreplace"))
                send_main_menu = Handle.handle_private_text(msg.content.text, bot, user, usersdb, categoriesdb, mediavotedb)
            
            if send_main_menu:
                Handle.send_main_menu(bot, user)
                
            
        

        
        chatsdb.update()
        usersdb.update()
        categoriesdb.update()
        mediavotedb.update()
    
    persondb.update()
    
    
    

#==============================================================================
# query
#==============================================================================

def query(raw_msg):
    query = MessageParser.CbkQuery(raw_msg, False)
    
    query.initOptionals()
    
    user = usersdb.getUser(query.person)
    
    log.debug(query.data)
    
    if query.data.startswith("rmacc"):
        
        scmd = query.data.split("_")
        ans = scmd[1]

        if ans == "yes":
            chatid = user.chatid
            lang_tag = user.lang_tag
            
            usersdb.deleteUser(user)
            
            s = "All data removed"
            s = _(s, lang_tag)
            bot.sendMessage(chatid, s)
            bot.answerCallbackQuery(query.id, text='Removed')
        else:
            Handle.send_main_menu(bot, user)
            bot.answerCallbackQuery(query.id, text='Not removed')
        
        usersdb.update()
    
    elif query.data.startswith("cp_"):
        # change page
        cmd_list = query.data.split("_")
        log.debug(str(cmd_list))
        
        if len(cmd_list) < 4:
            raise Exception("list too short")

        page_n = int(cmd_list[2])
        prev = True if cmd_list[3] == "prev" else False        

        if cmd_list[1] == "cat":
            Handle.answer_categories_page(bot, user, categoriesdb, query, prev, page_n, mediavotedb)
        elif cmd_list[1] == "shortcat":
            Handle.answer_short_categories(bot, user, categoriesdb, query, prev, page_n)
    
    else:
        bot.answerCallbackQuery(query.id, text='what?')


def inline_query(msg):
    log.debug("inline query")
    print(msg)

def chosen_inline(msg):
    log.debug("chosen inline result")
    print(msg)

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
    categoriesdb = CategoriesDB.CategoriesDB()
    mediavotedb = MediaVoteDB.MediaVoteDB()
    

    log.info("Loaded databases")
    
    response = {
            'chat': handle,
            'callback_query': query,
            'inline_query': inline_query,
            'chosen_inline_result' : chosen_inline
            }
    
    MessageLoop(bot, response).run_as_thread()
    
    log.info("Message loop started")
    while 1:
        time.sleep(10)    