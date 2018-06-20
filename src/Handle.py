# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:32:03 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================
import logging
import datetime
from language_support.LanguageSupport import _

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
# Handle
#==============================================================================
command_list = ["/categories",
                "/accept",
                "/decline",
                "/privacy_policy"
                ]



def send_main_menu(bot, user):
    s = "<b> Main Menu </b>\n"
    s += "<i> Chose a category to vote or see the media in it</i>\n"
    s += "\n"
    s += "<b>--- Categories ---</b>\n"
    s += "<i> start here </i>"
    s += "/categories"
    
    s = _(s, user.lang_tag)

    bot.sendMessage(user.chatid, s, parse_mode = "HTML")
    
    

def handle_private_text(text, bot, user):
    
    if text == "/categories" or text == "/categories@pellascarpbot":
        pass
        # give the category page

    send_main_menu(bot, user)

def handle_privacy_policy(bot, userdb, user, msg_content):
    if msg_content.type == "text" and msg_content.text in command_list[1:4]:
        log.debug("working on function {}".format(msg_content.text))
        command_function[msg_content.text](bot, userdb, user)
        
    if user.accepted_terms == False:
        s = _("Accept term and conditions. /privacy_policy\n /accept /decline", user.lang_tag)
        bot.sendMessage(user.chatid, s)

def accept_policy(bot, userdb, user):
    user.accepted_terms = True
    userdb.setUser(user)
    bot.sendMessage(user.chatid, "accepted")

def decline_policy(bot, userdb, user):
    user.accepted_terms = False
    # delete all users
    bot.sendMessage(user.chatid, "declined")

def privacy_policy(bot, userdb, user):
    bot.sendMessage(user.chatid, "privacy policy")
    


command_function = { command_list[1] : accept_policy,
                     command_list[2] : decline_policy,
                     command_list[3] : privacy_policy
                    
                    }    

