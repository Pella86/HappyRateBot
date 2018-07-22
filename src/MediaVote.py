# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 10:18:11 2018

@author: Mauro
"""
import datetime

import BotWrappers
import NumberFormatter
import EmojiTable

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
        tot_votes = 1 if tot_votes == 0 else tot_votes
        days_up = datetime.datetime.now() - self.creation_date
        days_up = 1 if days_up.days < 1 else days_up.days
        return ((karma / tot_votes) * 500) / days_up
    
    def generateHideReportButtons(self):
        
        cb = "hide_" + str(self.uid)
        b_hide = BotWrappers.Button("Hide " + EmojiTable.hidemedia_emoji, cb)
        
        cb = "report_" + str(self.uid)
        b_report = BotWrappers.Button("Report " + EmojiTable.report_emoji, cb)
        
        return [b_hide, b_report]
    
    def generateDeleteButton(self, user):        
        price = 100 + self.calculateScore()
        cb = "delete_{uid}_{price}".format(uid=self.uid, price=price)
        emdel = EmojiTable.report_emoji 
        price_fmt = NumberFormatter.PellaCoins(price)
        text = "Delete {} {}".format(emdel, price_fmt)
        return BotWrappers.Button(text, cb)
    
    def showPrivate(self, bot, user, userdb, catdb):
        caption = "Uploader: {display_id}\n"
        caption += "Category: {category}\n"
        caption += "{upvotes} - {downvotes} | Score: {score}\n"
        caption += "/main_menu || /show_{category}"
        
        sdb = {}
        sdb["display_id"] = userdb.hGetUser(self.creator_hash_id).getDisplayName()
        sdb["category"] = catdb.getCategory(self.cat_name).display_name
        sdb["upvotes"] = str(self.upvotes) + " " + EmojiTable.upvote_emoji
        sdb["downvotes"] = str(self.downvotes) + " " + EmojiTable.downvote_emoji
        sdb["score"] = NumberFormatter.FormatNumber(self.calculateScore(), 0)
        
        keyboard = BotWrappers.ReplyKeyboard()
        buttons = self.generateHideReportButtons()
        keyboard.addButtonLine(buttons)
        if user.hash_id == self.creator_hash_id:
            d_button = [self.generateDeleteButton(user)]
            keyboard.addButtonLine(d_button)
        
        
        rmk = keyboard.getKeyboard()
        
        if self.content.type == "text":
            original_message = self.content.text + "\n"
            original_message += "---------------------\n"
            original_message += caption
            
            BotWrappers.sendMessage(bot, user, original_message, sdb, reply_markup = rmk)                        
        
        else:
            BotWrappers.sendMedia(bot, user, self.content, caption, sdb, reply_markup = rmk)
            caption = caption.format(**sdb)
    
    def votePrivate(self, bot, user, usersdb, catdb):
        caption = "Uploader: {display_id}\n"
        caption += "Category: {category}\n"
        caption += "Score: {score}\n"
        caption += "/main_menu || /vote_{category}"
        
        sdb = {}
        sdb["display_id"] = usersdb.hGetUser(self.creator_hash_id).getDisplayName()
        sdb["category"] = catdb.getCategory(self.cat_name).display_name
        sdb["score"] = NumberFormatter.FormatNumber(self.calculateScore(), 0)
        
        uid_tag = "_" + str(self.uid)
        vote_up = BotWrappers.Button(EmojiTable.upvote_emoji + " " + str(self.upvotes), "vote_up" + uid_tag)
        vote_down = BotWrappers.Button(EmojiTable.downvote_emoji + " " + str(self.downvotes), "vote_down" + uid_tag)
        
        keyboard = BotWrappers.ReplyKeyboard()
        keyboard.addButtonLine([vote_up, vote_down])
        buttons = self.generateHideReportButtons()
        keyboard.addButtonLine(buttons)
        if user.hash_id == self.creator_hash_id:
            d_button = [self.generateDeleteButton(user)]
            keyboard.addButtonLine(d_button)
        
        rmk = keyboard.getKeyboard()
        
        if self.content.type == "text":
            original_message = self.content.text + "\n"
            original_message += "---------------------\n"
            original_message += caption
            
            BotWrappers.sendMessage(bot, user, original_message, sdb, reply_markup = rmk)                        
        
        else:
            BotWrappers.sendMedia(bot, user, self.content, caption, sdb, reply_markup = rmk)
            caption = caption.format(**sdb)
            
            
            
            
            
            
            
        
        
        