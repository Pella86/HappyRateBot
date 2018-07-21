# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 01:58:59 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import telepot
from telepot import Bot
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

import Logging
from language_support.LanguageSupport import _

#==============================================================================
# logging
#==============================================================================

log = Logging.get_logger(__name__, "INFO")

#==============================================================================
# bot functions
#==============================================================================

sendMethods = {
    "photo": (true, Bot.sendPhoto),
    "video": (true, Bot.sendVideo),
    "document": (true, Bot.sendDocument),
    "sticker": (false, Bot.sendSticker),
    "audio": (true, Bot.sendAudio),
    "voice": (true, Bot.sendVoice),
    "video_note": (false, Bot.sendVideoNote),
}

def Button(text, cb):    
    return InlineKeyboardButton(text=text, callback_data=cb)

class ReplyKeyboard:
    
    def __init__(self):
        self.keyboard = []
        
    def addButtonLine(self, line):
        self.keyboard.append(line)
    
    def getKeyboard(self):
        return InlineKeyboardMarkup(inline_keyboard=self.keyboard)


def checkUserActivity(func):
    def function_wrapper(bot, user, *args, **kwargs):
        if user.isActive:
            try:
               func(bot, user, *args, **kwargs)
            except telepot.exception.BotWasBlockedError:
                log.info("bot was blocked by user")
                user.isActive = False
            except Exception as e:
                print(e)
                raise Exception
        else:
            log.info("user is inactive")
    return function_wrapper



@checkUserActivity
def sendMessage(bot, user, text, sdb = None, translation = True, *args, **kwargs):
    
    if sdb:
        text = text.format(**sdb)
    
    if translation:
        text = _(text, user.lang_tag)
    
    bot.sendMessage(user.chatid, text, *args, **kwargs)
 
@checkUserActivity
def editMessage(bot, user, msgchatid, text, sdb = None, translation=True, *args, **kwargs ):
    if sdb:
        text = text.format(**sdb)
    
    if translation:
        text = _(text, user.lang_tag) 
    
    bot.editMessageText(msgchatid, text, *args, **kwargs) 

@checkUserActivity
def sendMedia(bot, user, content, caption = None, sdb = None, translation = True, *args, **kwargs):
    if caption and translation:
        caption = _(caption, user.lang_tag)
    
    if sdb:
        caption = caption.format(**sdb)
    

    file_id = content.file_id
    if file_id in sendMethods:
        if sendMethods[file_id][0] == True:
            sendMethods[file_id][1](bot, user.chatid, file_id, caption=caption, *args, **kwargs)
        else:
            sendMethods[file_id][1](bot, user.chatid, file_id, *args, **kwargs)
            if caption:
                sendMessage(bot, user, caption, translation=False)
