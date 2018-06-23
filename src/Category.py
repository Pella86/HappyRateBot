# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 23:02:01 2018

@author: Mauro
"""

#==============================================================================
# Imports
#==============================================================================

import datetime

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
        