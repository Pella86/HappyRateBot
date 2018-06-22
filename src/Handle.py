# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:32:03 2018

@author: Mauro
"""

#==============================================================================
# TO DO
#==============================================================================

# organze better the command factory

#==============================================================================
# Imports
#==============================================================================
import logging
import datetime

from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

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

def send_main_menu(bot, user):
    s = "<b>Main Menu </b>\n"
    s += "<i>Chose a category to vote or see the media in it</i>\n"
    s += "\n"
    s += "<b>--- Categories ---</b>\n"
    s += "<i> start here </i>\n"
    s += "/categories\n"
    s += "\n"
    s += "<b>--- Profile ---</b>\n"
    s += "<i> Your profile </i>\n"
    s += "/profile\n"
    s += "\n"
    
    
    s = _(s, user.lang_tag)

    bot.sendMessage(user.chatid, s, parse_mode = "HTML")

def categories(bot, user):
    bot.sendMessage(user.chatid, "feature not implemented, yet")


def handle_private_text(text, bot, user, usersdb):
    
    if user.tmp_display_id:
        set_nickname_result(text, bot, user, usersdb)

    if text in commands:
        commands[text].func(bot, user)
    else:
        send_main_menu(bot, user)
        
def user_profile(bot, user):
    s = "<b>User Profile </b>\n"
    s += "<i>Your anonymous id is: {anon_id}</i>\n"
    s += "<i>Change nickname</i> "
    s += commands["/set_nickname"].name + "\n"
    s += "\n"
    s += "<b>--- delete profile ---</b>\n"
    s += "<i> this action will delete every file you uploaded and reset all scores </i>\n"
    s += commands["/remove_account"].name
    
    
    s = _(s, user.lang_tag)
    
    sdb = {}
    sdb["anon_id"] = user.display_id
    s = s.format(**sdb)

    bot.sendMessage(user.chatid, s, parse_mode = "HTML")


def set_nickname(bot, user):
    # create a delegator bot and starts its own message loop?
    user.tmp_display_id = True
    
    s = "Send a new nickname. The nickname has to be between 3 and 15 characters. And can contain only alphanumeric values (a-z, A-Z, 0-9)."
    
    s = _(s, user.lang_tag)
    
    bot.sendMessage(user.chatid, s)

def set_nickname_result(text, bot, user, usersdb):
    result = usersdb.check_nickname(user, text)
    
    if result == True:
        s = _("Nickname changed successfully", user.lang_tag)
        bot.sendMessage(user.chatid, s)
    else:
        s = "Nickname error: " + result 
        s = _(s, user.lang_tag)
        bot.sendMessage(user.chatid, s)
    user.tmp_display_id = False
        

    

#==============================================================================
# Privacy policy stuff (boooring)
#==============================================================================

privacy_policy_text = None
with open("./src/privacy/Privacy_policy.txt", "r") as f:
    privacy_policy_text = f.read()

def handle_privacy_policy(bot, userdb, user, msg_content):
    accpt_cmd = [commands["/accept"].name, commands["/decline"].name, commands["/privacy_policy"].name]
    if msg_content.type == "text" and msg_content.text in accpt_cmd:
        log.debug("working on function {}".format(msg_content.text))
        commands[msg_content.text].func(bot, userdb, user)
        
    if user.accepted_terms == False:
        s = "<b> Welcome to the Happy Rate Bot </b>\n"
        s += "In this bot you can upload your content and let the other users in the bot community to rate the content. The bot is subdivided in categories (which you can create). The bot will not disclose who is using it, you will be masked by an anonymous id.\n"
        s += "\n"
        s += "Accept terms and conditions:\nFor more information you can read the /privacy_policy\n"
        s += "\n"
        s += "/accept       /decline"
        s = _(s, user.lang_tag)
        bot.sendMessage(user.chatid, s, parse_mode="HTML")

def accept_policy(bot, userdb, user):
    user.accepted_terms = True
    userdb.setUser(user)
    bot.sendMessage(user.chatid, "accepted")
    send_main_menu(bot, user)

def decline_policy(bot, userdb, user):
    if user.accepted_terms == False:
        bot.sendMessage(user.chatid, "declined")
        userdb.deleteUser(user)
    else:
        s = _("Already accepted, if you want to delete your data, refer to /remove_account", user.lang_tag)
        bot.sendMessage(user.chatid, s)
    

def privacy_policy(bot, userdb, user):
    s = privacy_policy_text
    s = _(s, user.lang_tag)
    bot.sendMessage(user.chatid, s)


def remove_account(bot, user):
    s = _("Are you sure you want to remove your data?", user.lang_tag)
    b_no = InlineKeyboardButton(
            text='no',
            callback_data='rmacc_no'
            )
    b_yes = InlineKeyboardButton(
            text='yes',
            callback_data='rmacc_yes'
            )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[b_yes, b_no]])
    
    bot.sendMessage(user.chatid, s, reply_markup=keyboard)



#==============================================================================
# Commands functions
#==============================================================================

# read form file

class Command:
    
    def __init__(self, name, func):
        
        self.name = name
        
        if func:
            self.func = globals()[func]
        else:
            self.func = None

commands = {}
with open("./src/utils/command_factory.txt", "r") as f:
    cl = f.readlines()

for line in cl:
    sl = [s.strip() for s in line.split(" ")]
    if len(sl) == 2:
        cmd = Command(sl[0], sl[1])
    else:
        cmd = Command(sl[0], None)
    
    commands[cmd.name] = cmd    

