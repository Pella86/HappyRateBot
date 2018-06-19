# -*- coding: utf-8 -*-
"""
Created on Tue Jun 19 18:28:37 2018

@author: Mauro
"""

class UserProfile:
    
    
    def __init__(self, hash_id, display_id):
        # hash the tg id
        # 
        self.hash_id = hash_id
        self.display_id = display_id 
        
        self.banned = False
        self.accepted_terms = False
        