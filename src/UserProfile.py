# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 18:28:37 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================
import datetime

import NumberFormatter
import BotWrappers

#==============================================================================
# User class
#==============================================================================
class UserProfile:
    
    
    def __init__(self, hash_id, display_id, chatid, lang_tag):
        # ids and stuff
        self.hash_id = hash_id
        self.display_id = display_id 
        self.chatid = chatid
        
        # points and karma
        self.pella_coins = 0
        self.karma = None
        self.rep_points = 1
        
        # various flags
        self.banned = False
        self.accepted_terms = False
        self.isActive = True
        
        # temporary uploads
        self.tmp_display_id = ""
        self.tmp_upload_content = None
        self.tmp_upload_category = None
        self.tmp_create_category = None
        
        # upload limits
        self.uploads_day = 0
        self.last_upload_time = datetime.datetime.now()
        
        # hidden pics
        self.no_show_ids = []
        
        # notifications
        #   notification tag : true, false
        self.notifications = {}
        
        # language tag
        self.lang_tag = lang_tag
        
    def calculateKarma(self, mediavotedb):
        self.karma = 0
        for media in mediavotedb.getValues():
            if media.creator_hash_id == self.hash_id:
                self.karma += media.calculateScore()
    
    def getReputation(self):
        if self.karma > 0:
            return self.karma * self.rep_points
        else:
            return 0
    
        
    def getDisplayName(self):
        return str(self.display_id) + " (" + str(NumberFormatter.Reputation(self.getReputation())) + ")"
    
    def getPoints(self):
        return str(NumberFormatter.PellaCoins(self.pella_coins))
    
    def countVoted(self, cat_name, mediavotedb):
        voted = 0
        total = 0
        for media in mediavotedb.getValues():
            media_visible = not (media.deleted or media.uid in self.no_show_ids)
            if media.cat_name == cat_name and media_visible:
                if self.hash_id in media.voters_id:
                    voted += 1
                total += 1
        return voted, total

    def sendUserProfile(self, bot, commands):
        s = "<b>User Profile </b>\n"
        s += "<i>Your anonymous id is: {anon_id}</i>\n"
        s += "<i>Change nickname</i> "
        s += commands["/set_nickname"].name + "\n"
        s += "\n"
        s += "Coins: {pella_coins}\n"
        s += "Karma: {karma}\n"
        s += "Shield points: {rep_points}\n"
        s += "Repuation: {reputation}\n"
        s += "\n"
        s += "<b>--- Create category ---</b>\n"
        s += "<i> You can create your own categories </i>\n"
        s += "/create_category\n"
        s += "\n"
        s += "<b>--- User Top ---</b>\n"
        s += "<i> The bot top chart </i>\n"
        s += "/user_top\n"
        s += "\n"
        s += "<b>--- Uploaded media ---</b>\n"
        s += "<i> The media you uploaded to the bot </i>\n"
        s += "/uploaded_media\n"
        s += "\n"
        s += "<b>--- delete profile ---</b>\n"
        s += "<i> this action will delete every file you uploaded and reset all scores </i>\n"
        s += commands["/remove_account"].name
    
        sdb = {}
        sdb["anon_id"] = self.display_id
        sdb["pella_coins"] = self.getPoints()
        sdb["karma"] = NumberFormatter.Karma(self.karma if self.karma else 0)        
        sdb["rep_points"] = NumberFormatter.RepPoints(self.rep_points)
        sdb["reputation"] = NumberFormatter.Reputation(self.getReputation())
                
    
        BotWrappers.sendMessage(bot, self, s, sdb, parse_mode = "HTML")
                    
        

        