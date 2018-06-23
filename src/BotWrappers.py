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

def sendMessage(bot, user, text, sdb = None, translation = True, *args, **kwargs):
    
    if sdb:
        text = text.format(*sdb)
    
    if translation:
        text = _(text, user.lang_tag)
        
    
    if user.isActive:
        try:
            bot.sendMessage(user.chatid, text, *args, **kwargs)
        
        except telepot.exception.BotWasBlockedError:
            log.info("bot was blocked by user")
            user.isActive = False
    else:
        log.info("user is inactive") 

def editMessage(bot, user, msgchatid, text, sdb = None, translation=True, *args, **kwargs ):
    if sdb:
        text = text.format(*sdb)
    
    if translation:
        text = _(text, user.lang_tag) 
    
    if user.isActive:
        try:    
            bot.editMessageText(msgchatid, text, *args, **kwargs) 
        except telepot.exception.BotWasBlockedError:
            log.info("bot was blocked by user")
            user.isActive = False
    else:
        log.info("user is inactive") 