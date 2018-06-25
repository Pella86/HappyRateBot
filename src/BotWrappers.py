# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 01:58:59 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import telepot
import Logging

from language_support.LanguageSupport import _

#==============================================================================
# logging
#==============================================================================

log = Logging.get_logger(__name__, "DEBUG")

#==============================================================================
# bot functions
#==============================================================================


def checkUserActivity(func):
    def function_wrapper(bot, user, *args, **kwargs):
        if user.isActive:
            try:
               func(bot, user, *args, **kwargs)
            except telepot.exception.BotWasBlockedError:
                log.info("bot was blocked by user")
                user.isActive = False
            except Exception:
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
    if content.type == "photo":
        bot.sendPhoto(user.chatid, file_id, caption = caption, *args, **kwargs)
    elif content.type == "video":
        bot.sendVideo(user.chatid, file_id, caption = caption, *args, **kwargs)
    elif content.type == "document":
        bot.sendDocument(user.chatid, file_id, caption = caption, *args, **kwargs) 
    elif content.type == "sticker":
        bot.sendSticker(user.chatid, file_id, *args, **kwargs)
        if caption:
            sendMessage(bot, user, caption, translation=False)
    elif content.type == "audio":
        bot.sendAudio(user.chatid, file_id, caption=caption, *args, **kwargs)
    elif content.type == "voice":
        bot.sendVoice(user.chatid, file_id, caption=caption, *args, **kwargs)
    elif content.type == "voice_note":
        bot.sendVideoNote(user.chatid, file_id, *args, **kwargs)
        if caption:
            sendMessage(bot, user, caption, translation=False)
