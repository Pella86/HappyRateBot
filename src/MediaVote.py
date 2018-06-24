# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 10:18:11 2018

@author: Mauro
"""
import datetime

from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

import BotWrappers
import NumberFormatter

def Button(text, cb):    
    return InlineKeyboardButton(text=text, callback_data=cb)

class MediaVote:
    
    
    def __init__(self, uid, content, cat_name, hash_id):
        
        self.uid = uid
        self.content = content
        self.cat_name = cat_name
        self.creator_hash_id = hash_id
        
        self.upvotes = 0
        self.downvotes = 0
        self.voters_id = []
        
        self.deleted = False
        self.reported_by = []
        
        self.creation_date = datetime.datetime.now()
    
    def calculateScore(self):
        karma = self.upvotes - self.downvotes
        tot_votes = self.upvotes + self.downvotes
        days_up = datetime.datetime.now() - self.creation_date
        days_up = 1 if days_up.days < 1 else days_up.days
        return (karma * tot_votes) / days_up
    
    def showPrivate(self, bot, user, userdb, catdb):
        
            
        caption = "Uploader: {display_id}\n"
        caption += "Category: {category}\n"
        caption += "{upvotes} up - {downvotes} down | Score: {score}\n"
        caption += "/main_menu"
        
        sdb = {}
        sdb["display_id"] = userdb.hGetUser(self.creator_hash_id).display_id
        sdb["category"] = catdb.getCategory(self.cat_name).display_name
        sdb["upvotes"] = self.upvotes
        sdb["downvotes"] = self.downvotes
        sdb["score"] = NumberFormatter.FormatNumber(self.calculateScore(), 0)

        file_id = self.content.file_id
        
        rmk =InlineKeyboardMarkup(inline_keyboard=[[Button("under construction", "lol")]])
        
        if self.content.type == "photo":
            bot.sendPhoto(user.chatid, file_id, caption = caption, reply_markup = rmk)
        elif self.content.type == "video":
            bot.sendVideo(user.chatid, file_id, caption = caption, reply_markup = rmk)
        elif self.content.type == "document":
            bot.sendDocument(user.chatid, file_id, caption = caption, reply_markup = rmk)  
        elif self.content.type == "text":
            original_message = self.content.text + "\n"
            original_message += "---------------------\n"
            original_message += caption
            
            BotWrappers.sendMessage(bot, user, original_message, sdb, reply_markup = rmk)            
            
            
            
            
            
            
        
        
        