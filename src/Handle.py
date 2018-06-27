# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:32:03 2018

@author: Mauro
"""

#==============================================================================
# TO DO
#==============================================================================

# organze better the command factory
# delete chatid corresponding to user when deleteing
# make a delete_user function which accept chatdb, persondb e userid

#==============================================================================
# Imports
#==============================================================================

import random

from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

import Logging
import BotWrappers
import Category
import Pages

from CreatorID import creator_hash_id

#==============================================================================
# logging
#==============================================================================

log = Logging.get_logger(__name__, "DEBUG")

#==============================================================================
# helpers
#==============================================================================



#==============================================================================
# Handle
#==============================================================================

def handle_content(content, bot, user, catdb, mediavotedb):
        
    if user.tmp_upload_category == True:
        text_type = content.type == "text"
        user_prompted_upload = user.tmp_upload_content is not None
        user_has_valid_content = user.tmp_upload_content != True
        
        if text_type and user_prompted_upload and user_has_valid_content:
            error_message = None
            
            # check if category is present
            if catdb.isPresent(content.text.lower()):
                cat_name = content.text.lower()
            else:
                error_message = "category not found"
                BotWrappers.sendMessage(bot, user, "Category not found\n/upload    /main_menu")
    
            if error_message is None:
                mediavotedb.addContent(user.tmp_upload_content, cat_name, user.hash_id)
                BotWrappers.sendMessage(bot, user, "Content uploaded successfully\n/main_menu")
                log.debug("handle normal requests")
        
        user.tmp_upload_content = False
        user.tmp_upload_category = False
        
        return False

    if user.tmp_upload_content == True:
        error_message = None
        
        content_id = content.text if content.type == "text" else content.file_id
        
        file_ids = [v.content.text if v.content.type == "text" else v.content.file_id for v in mediavotedb.getValues()]

        if content_id in file_ids:
            error_message = "not original content"
        
        if content.type == "text" and content.text.startswith("/"):
            if content.text == commands["/cancel"].name:
                error_message = "cancel"
            else:
                error_message = "commands not allowed"
            
        if error_message is None:
            # read the content from the message
            user.tmp_upload_content = content
            
            short_categories(bot, user, catdb)

            s = "Please choose a category where to put the media\n/cancel"
            BotWrappers.sendMessage(bot, user, s)
            
            user.tmp_upload_category = True
        
        else:
            if error_message == "not original content":
                user.tmp_upload_content = None
                s = "Content already in database\n/main_maenu"
                BotWrappers.sendMessage(bot, user, s) 
            elif error_message ==  "cancel":
                return True
            elif error_message == "command not allowed":
                user.tmp_upload_content = None
                s = "Commands not allowed\n/main_maenu"
                BotWrappers.sendMessage(bot, user, s)                
        
        return False
    return True
        
def handle_private_text(text, bot, user, usersdb, catdb, mediavotedb):
    
    if user.tmp_display_id:
        set_nickname_result(text, bot, user, usersdb)
        return False
    
    if user.tmp_create_category:
        get_category(bot, user, text, catdb)
        return False
     
    if text.startswith("/show"):
        st = text.split("_")
        
        
        if len(st) == 1:
            #pick a random media in all the database and and show it
            medias = mediavotedb.getValues()
            media = random.choice(medias)
            
            media.showPrivate(bot, user, usersdb, catdb)
            
        elif len(st) == 2:
            # pick a random media and show
            cat_name = st[1].lower()
            medias = mediavotedb.getMediaCategory(cat_name)
            if medias:
                media = random.choice(medias)
                
                print(media.content.type)
               
                media.showPrivate(bot, user, usersdb, catdb)
            else:
                BotWrappers.sendMessage(bot, user, "Category is empty\n/main_menu")
        
        elif len(st) == 3:
            pass
        
        return False
    
    if text.startswith("/catinfo") and user.hash_id == creator_hash_id:
        
        st = text.split("_")
        
        if len(st) == 2:
            cat_name = st[1].lower()
            print(cat_name in catdb.getKeys())
            if cat_name in catdb.getKeys():
                cat = catdb.database[cat_name].getData()
                cat.show(bot, user)
                return False
            else:
                BotWrappers.sendMessage(bot, user, "category not in database")
    
    if text == "/catlist" and user.hash_id == creator_hash_id:
        cat_list = catdb.getValues()
        p = Pages.CategoryList(0, cat_list)
        p.sendPage(bot, user)
        return False

    if text in commands and commands[text].domain == "#general":
        
        if commands[text].name == commands["/privacy_policy"].name:
            commands[text].func()(bot, usersdb, user)
            return False
        elif commands[text].name == commands["/categories"].name:
            commands[text].func()(bot, user, catdb, mediavotedb)
            return False
        else:
            commands[text].func()(bot, user)
            return False
    return True


#==============================================================================
# Main menu
#==============================================================================

def send_main_menu(bot, user):
    s = "<b>Main Menu </b>\n"
    s += "<i>Chose a category to vote or see the media in it</i>\n"
    s += "\n"
    s += "<b>--- Categories ---</b>\n"
    s += "<i> start here </i>\n"
    s += "/categories\n"
    s += "\n"
    s += "<b>--- Upload ---</b>\n"
    s += "<i> upload your pictures, gifs, ... </i>\n"
    s += "/upload\n"
    s += "\n"
    s += "<b>--- Profile ---</b>\n"
    s += "<i> Your profile </i>\n"
    s += "/profile\n"
    s += "\n"
    

    BotWrappers.sendMessage(bot, user, s, parse_mode = "HTML")

#==============================================================================
# Upload
#==============================================================================

def upload(bot, user):
    # send a message requessting the user to post anything
    s = "You can post anything text, gif, pictures, ..."
    
    BotWrappers.sendMessage(bot, user, s)
    
    user.tmp_upload_content = True
    

#==============================================================================
#  User profile
#==============================================================================
        
def user_profile(bot, user):
    s = "<b>User Profile </b>\n"
    s += "<i>Your anonymous id is: {anon_id}</i>\n"
    s += "<i>Change nickname</i> "
    s += commands["/set_nickname"].name + "\n"
    s += "\n"
    s += "<b>--- Create category ---</b>\n"
    s += "<i> You can create your own categories </i>\n"
    s += "/create_category\n"
    s += "\n"
    s += "<b>--- delete profile ---</b>\n"
    s += "<i> this action will delete every file you uploaded and reset all scores </i>\n"
    s += commands["/remove_account"].name

    sdb = {}
    sdb["anon_id"] = user.display_id
    s = s.format(**sdb)

    BotWrappers.sendMessage(bot, user, s, sdb, parse_mode = "HTML")

#==============================================================================
# short categories
#==============================================================================

def short_categories(bot, user, catdb):
    cat_list = catdb.getValues()
    p = Pages.CategoryPagesShort(0, cat_list)
    p.sendPage(bot, user)

def answer_short_categories(bot, user, catdb, query, prev, page_n):
    cat_list = catdb.getValues()
    p = Pages.CategoryPagesShort(page_n, cat_list, query)
    p.check_answer(bot, user, prev)    

#==============================================================================
# Categories pages
#============================================================================== 

def categories(bot, user, catdb, mediavotedb):
    # get category list
    cat_list = catdb.getValues()
    
    # generate page elements
    p = Pages.CategoryPages(0, cat_list)
    
    p.sendPage(bot, user, mediavotedb)
    

def answer_categories_page(bot, user, catdb, query, prev, page_n, mediavotedb):
    cat_list = catdb.getValues()
    
    p = Pages.CategoryPages(page_n, cat_list, query)
    
    p.check_answer(bot, user, prev, mediavotedb)

#==============================================================================
# Category stuff
#==============================================================================

def create_category(bot, user):
    
    user.tmp_create_category = True
    
    s = "<b>Send a category name</b>\n"
    s += "<i>The name must be maximum 15 characters long and can contain only alphanumeric characters (a-z and A-Z and 1-10)</i>\n"

    s += "\n"
    s += "Create a category will cost {price} you have {points}\n"
    s += "/cancel\n"
    
    sdb = {}
    sdb["price"] = 0
    sdb["points"] = user.getPoints()
    
    s = s.format(**sdb)
    
    BotWrappers.sendMessage(bot, user, s, sdb, parse_mode = "HTML")

    
def get_category(bot, user, text, catdb):
    # check if category name is valid
    # must be alphanumeric
    valid = catdb.checkName(text)
    user.tmp_display_id = ""
    user.tmp_upload_content = None
    user.tmp_upload_category = None
    user.tmp_create_category = None
    
    if valid == True:
    
        category = Category.Category(text, user.hash_id)
        
        if catdb.addCategory(category):
            s = "Success: new category created"
            BotWrappers.sendMessage(bot, user, s)
            
            
        else:
            s = "Fail: category already present"
            BotWrappers.sendMessage(bot, user, s)
    else:
        user.tmp_create_category = False
        s = "Create category error: " + valid
        
        BotWrappers.sendMessage(bot, user, s)
        
def cancel(bot, user):
    user.tmp_display_id = ""
    user.tmp_upload_content = None
    user.tmp_upload_category = None
    user.tmp_create_category = None
    BotWrappers.sendMessage(bot, user, "cancelled!")
    send_main_menu(bot, user)

#==============================================================================
# Nickname stuff
#==============================================================================

def set_nickname(bot, user):
    # create a delegator bot and starts its own message loop?
    user.tmp_display_id = True
    
    s = "Send a new nickname. The nickname has to be between 3 and 15 characters. And can contain only alphanumeric values (a-z, A-Z, 0-9).\n/cancel"
    
    
    BotWrappers.sendMessage(bot, user, s)

def set_nickname_result(text, bot, user, usersdb):
    result = usersdb.check_nickname(user, text)
    
    if result == True:
        s = "Nickname changed successfully"
        BotWrappers.sendMessage(bot, user, s)
    else:
        s = "Nickname error: " + result 
        BotWrappers.sendMessage(bot, user, s)
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
        commands[msg_content.text].func()(bot, userdb, user)
        
    if user.accepted_terms == False:
        s = "<b> Welcome to the Happy Rate Bot </b>\n"
        s += "In this bot you can upload your content and let the other users in the bot community to rate the content. The bot is subdivided in categories (which you can create). The bot will not disclose who is using it, you will be masked by an anonymous id.\n"
        s += "\n"
        s += "Accept terms and conditions:\nFor more information you can read the /privacy_policy\n"
        s += "\n"
        s += "/accept       /decline"
        BotWrappers.sendMessage(bot, user, s, parse_mode="HTML")

def accept_policy(bot, userdb, user):
    user.accepted_terms = True
    userdb.setUser(user)
    BotWrappers.sendMessage(bot, user, "accepted")
    send_main_menu(bot, user)

def decline_policy(bot, userdb, user):
    if user.accepted_terms == False:
        BotWrappers.sendMessage(bot, user, "declined")
        userdb.deleteUser(user)
    else:
        s = "Already accepted, if you want to delete your data, refer to /remove_account"
        BotWrappers.sendMessage(bot, user, s)
    

def privacy_policy(bot, userdb, user):
    s = privacy_policy_text
    BotWrappers.sendMessage(bot, user, s)


def remove_account(bot, user):
    s = "Are you sure you want to remove your data?"
    b_no = InlineKeyboardButton(
            text='no',
            callback_data='rmacc_no'
            )
    b_yes = InlineKeyboardButton(
            text='yes',
            callback_data='rmacc_yes'
            )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[b_yes, b_no]])
    
    BotWrappers.sendMessage(bot, user, s, reply_markup=keyboard)



#==============================================================================
# Commands functions
#==============================================================================

# read form file

class Command:
    
    def __init__(self, name, func, domain):
        
        self.name = name
        self.func_name = func
        self.domain = domain
        
    def func(self):
        if self.func_name is not None:
            return globals()[self.func_name]
        else:
            return None

commands = {}
with open("./src/utils/command_factory.txt", "r") as f:
    cl = f.readlines()

for line in cl:
    
    if line.startswith("#"):
        domain = line.strip()
        continue
    
    sl = [s.strip() for s in line.split(" ")]
    
    if len(sl) == 2:
        cmd = Command(sl[0], sl[1], domain)
    else:
        cmd = Command(sl[0], None, domain)
    
    commands[cmd.name] = cmd    

