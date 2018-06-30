# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 23:02:01 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import datetime

import BotWrappers
from CreatorID import creator_hash_id

#==============================================================================
# Category class
#==============================================================================

class Category:
    
    def __init__(self, name, creator):
        
        # name
        self.name_id = name.lower()
        self.display_name = name
        
        # creation stuff
        self.creation_date = datetime.datetime.now()
        self.creator = creator
        
        # score
        self.score = 0
        
        # other proprieties
        self.deleted = False
        self.reported_by = []
        
        # eventuals 
        self.description = ""
    
    def show(self, bot, user):
        ## can be used only by the creator_id        
        if user.hash_id == creator_hash_id:        
            s = self.display_name + "\n"
            s += self.creation_date.strftime("%D-%M-%Y") + "\n"
            s += "Score: " + str(self.score) + "\n"
            s +=  "Reported by: " + str(len(self.reported_by)) + "\n"

            text = "delete"
            query_tag = "remcat_{}".format(self.name_id)
            b_del = BotWrappers.Button(text, query_tag)

            text = "ban"
            query_tag = "bancat_{}".format(self.name_id)
            b_ban = BotWrappers.Button(text, query_tag)
            
            buttons1 = [b_del]
            buttons2 = [b_ban]
            
            keyboard = BotWrappers.ReplyKeyboard()
            keyboard.addButtonLine(buttons1)
            keyboard.addButtonLine(buttons2)
            
            rmk = keyboard.getKeyboard()
            
            BotWrappers.sendMessage(bot, user, s ,translation=False, reply_markup=rmk)
        else:
            BotWrappers.sendMessage(bot, user, "no permission")
        
    
    
class BannedCategory:
    
    def __init__(self, category):
        self.name_id = category.name_id
        
        