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
    
    def getPoints(self):
        return str(NumberFormatter.PellaCoins(self.pella_coins))
        

        