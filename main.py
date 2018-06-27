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
import pprint

# telepot imports
import telepot
from telepot.loop import MessageLoop

# my imports
import BotDataReader
import MessageParser
import PersonDB
#import ChatsDB
import UsersDB
import CategoriesDB
import MediaVoteDB
import Handle
import Logging
import Pages
from src.language_support.LanguageSupport import _

import BotWrappers

#==============================================================================
# Logging
#==============================================================================

# create logger
log = Logging.get_logger(__name__, "DEBUG")

#==============================================================================
# handle
#==============================================================================


def LogBigMistakes(func):
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            log.exception(func.__name__ + ": Big mistake")
    return func_wrapper

@LogBigMistakes
def handle(raw_msg):
    log.debug("Message:\n" + pprint.pformat(raw_msg, indent = 2))

    msg = MessageParser.Message(raw_msg)
    
    persondb.addPerson(msg.mfrom) # logs every person!
    
    
    
    if msg.chat.type == "private":
        log.debug("private message received")
        
        
        
        #chatsdb.addChat(msg.chat)
        chatid = msg.chat.id

        # add the user 
        usersdb.addUser(msg.mfrom, chatid)
        user = usersdb.getUser(msg.mfrom)

        
        # received a message user is supposedly active
        user.isActive = True

        if user.accepted_terms == False:
            log.debug("handle privacy policy")
            Handle.handle_privacy_policy(bot, usersdb, user, msg.content)        
        else:
            
            # flag to send main menu
            send_main_menu = True
            
            # check the content if there is piped some request
            send_main_menu = Handle.handle_content(msg.content, bot, user, categoriesdb, mediavotedb)
            
            # analyize content
            if msg.content.type == "text" and send_main_menu:
                # log the messages to the bot 
                text = msg.content.text
                log_msg = text if len(text) < 244 else text[:241] + "..."
                log_msg = log_msg.encode("utf-8").decode("utf-8", "backslashreplace")
                log.debug("Message: " + log_msg)
                
                # handle the requests
                send_main_menu = Handle.handle_private_text(msg.content.text, bot, user, usersdb, categoriesdb, mediavotedb)
            
            if send_main_menu:
                Handle.send_main_menu(bot, user)
                
        #chatsdb.update()
        usersdb.update()
        categoriesdb.update()
        mediavotedb.update()
    
    persondb.update()
    
    
    

#==============================================================================
# query
#==============================================================================
@LogBigMistakes
def query(raw_msg):
    query = MessageParser.CbkQuery(raw_msg, False)
    
    query.initOptionals()
    
    user = usersdb.getUser(query.person)
    
    log.debug(query.data)
    
    if query.data.startswith("rmacc"):
        
        scmd = query.data.split("_")
        ans = scmd[1]

        if ans == "yes":
            
            categoriesdb.deleteCategoryUser(user, mediavotedb)
            log.info("deleted categories")
            
            mediavotedb.deleteUserMedia(user)
            log.info("deleted media")
            
            usersdb.deleteUser(user)
            log.info("deleted user")
            
            BotWrappers.sendMessage(bot, user, "All data removed")
            bot.answerCallbackQuery(query.id, text='Removed')
        else:
            Handle.send_main_menu(bot, user)
            bot.answerCallbackQuery(query.id, text='Not removed')
        
        usersdb.update()
    
    elif query.data.startswith("remcat_"):
        st = query.data.split("_")
        
        if len(st) == 2:
            categoriesdb.deleteCategory(st[1])
            bot.answerCallbackQuery(query.id, text='Deleted {}'.format(st[1]))
        else:
            bot.answerCallbackQuery(query.id, text='Delete cat somethings fucky')
    
    elif query.data.startswith("bancat_"):
        st = query.data.split("_")
        
        if len(st) == 2:
            categoriesdb.banCategory(st[1])
            bot.answerCallbackQuery(query.id, text='Banned {}'.format(st[1]))
        else:
            bot.answerCallbackQuery(query.id, text='Ban cat somethings fucky')
    
    elif query.data.startswith("cp_"):
        # change page
        cmd_list = query.data.split("_")
        
        if len(cmd_list) < 4:
            raise Exception("list too short")

        page_n = int(cmd_list[2])
        prev = True if cmd_list[3] == "prev" else False        

        if cmd_list[1] == "cat":
            Handle.answer_categories_page(bot, user, categoriesdb, query, prev, page_n, mediavotedb)
        elif cmd_list[1] == "shortcat":
            Handle.answer_short_categories(bot, user, categoriesdb, query, prev, page_n)
        
        elif cmd_list[1] == "catlist":
            cat_list = categoriesdb.getValues()
            p = Pages.CategoryList(page_n, cat_list, query)
            p.check_answer(bot, user, prev)  
    else:
        bot.answerCallbackQuery(query.id, text='what?')

@LogBigMistakes
def inline_query(msg):
    log.debug("inline query")
    print(msg)

@LogBigMistakes
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
    usersdb = UsersDB.UsersDB()
    categoriesdb = CategoriesDB.CategoriesDB()
    mediavotedb = MediaVoteDB.MediaVoteDB()
    
    # clean up mess
    
    for category in categoriesdb.getValues():
        if category.creator not in usersdb.database.keys():
            print("found stray category")
    

    log.info("Loaded databases")
    try:
        response = {
                'chat': handle,
                'callback_query': query,
                'inline_query': inline_query,
                'chosen_inline_result' : chosen_inline
                }
    
        MessageLoop(bot, response).run_as_thread()
    except Exception as e:
        log.exception("main: Big mistake")
    
    log.info("Message loop started")
    while 1:
        time.sleep(10)    