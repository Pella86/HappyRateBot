# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 23:26:12 2018

@author: Mauro
"""
#==============================================================================
# Imports
#==============================================================================
from telepot.namedtuple import InlineKeyboardButton, InlineKeyboardMarkup

import BotWrappers
import NumberFormatter

#==============================================================================
# helpers
#==============================================================================
def Button(text, cb):    
    return InlineKeyboardButton(text=text, callback_data=cb)

#==============================================================================
# Pages base class
#==============================================================================
class Pages:
    
    def __init__(self, title, page, max_per_page, query_tag, query = None):
        self.title = title
        self.page = page
        self.max_per_page = max_per_page
        self.query_tag = query_tag
        self.query = query

    def get_page_list_indexes(self):
        start = self.page * self.max_per_page
        end = start + self.max_per_page
        return (start, end)     
    
    def calcTotPages(self, org_list):
        return int(len(org_list) / self.max_per_page)
    
    def sendPage(self, bot, user, list_of_elements,  tot_pages):
        s = "<b>" + self.title + "</b>\n"
        s += "\n"
        
        for i in range(0, self.max_per_page):
            if i >= len(list_of_elements):
                break
            else:
                s += list_of_elements[i] + "\n"
                s += "\n"
        s += "\n"     
        
        s += "/main_menu      {}/{}".format(self.page, tot_pages)
        
        text = "<"
        callback_data = self.query_tag  + str(self.page)  + "_" + "prev"
        b_prev = Button(text, callback_data)

        text = ">"
        callback_data = self.query_tag  + str(self.page) + "_" + "succ"
        b_succ = Button(text, callback_data)

        keyboard = [[b_prev, b_succ]]
        
        rmk = InlineKeyboardMarkup(inline_keyboard=keyboard)

        if self.query is not None:
            BotWrappers.editMessage(bot, user, self.query.getChatMsgID(), s, translation = False, reply_markup=rmk, parse_mode="HTML")
        else:
            BotWrappers.sendMessage(bot, user, s, translation=False, reply_markup=rmk, parse_mode="HTML")        
        
#==============================================================================
# Categories
#==============================================================================
class CategoryPages(Pages):
    
    def __init__(self, page, cat_list, query = None):
        super().__init__("Categories", page, 3, "cp_cat_", query)
        
        self.cat_list = cat_list

    def create_element(self, cat_list, i, user, mediavotedb):
        s = "~~~~ " + cat_list[i].display_name + " ~~~~" + "\n"
        n_voted, total = user.countVoted(cat_list[i].name_id, mediavotedb)
        if total == 0:
            s += "Empty\n"
        else:
            s += "Voted: {} / {}\n".format(n_voted, total)
        s += "Category score: " + str(NumberFormatter.FormatNumber(cat_list[i].score, 0)) + "\n"
        #user_voted_all = get media if user in  already voted
        #calc tot for media in media list if not hide nor ban
        # if voted == tot -> show
        # else -> vote
        s += "/show_" + cat_list[i].display_name
        return s  
    
    def create_element_list(self, user, mediavotedb):
        elements = []
        
        for i in range(*self.get_page_list_indexes()):
            if i < len(self.cat_list):
                s = self.create_element(self.cat_list, i, user, mediavotedb)
                elements.append(s)
            else:
                break
        return elements

    
    def check_answer(self, bot, user, prev, mediavotedb):
        if prev:
            self.page -= 1
            if self.page < 0:
                bot.answerCallbackQuery(self.query.id, "Reached first page")
                return
        else:
            self.page += 1
            if self.page > self.calcTotPages(self.cat_list):
                bot.answerCallbackQuery(self.query.id, "Reached last page")
                return

        self.sendPage(bot, user, mediavotedb)         

    def sendPage(self, bot, user, mediavotedb):
        list_of_elements = self.create_element_list(user, mediavotedb)
        tot_pages = self.calcTotPages(self.cat_list)
        super().sendPage(bot, user, list_of_elements, tot_pages)

#==============================================================================
# Categories condensed
#==============================================================================

class CategoryPagesShort(Pages):
    
    def __init__(self, page, cat_list, query = None):
        super().__init__("Categories", page, 6, "cp_shortcat_", query)
        
        self.cat_list = cat_list   

    def create_element(self, cat_list, i):
        s = "<b>-- " + cat_list[i].display_name + " --</b>" + "\n"
        s += "Score: " + str(NumberFormatter.FormatNumber(cat_list[i].score, 0))
        return s  
    
    def create_element_list(self):
        elements = []
        
        for i in range(*self.get_page_list_indexes()):
            if i < len(self.cat_list):
                s = self.create_element(self.cat_list, i)
                elements.append(s)
            else:
                break
        return elements

    
    def check_answer(self, bot, user, prev):
        if prev:
            self.page -= 1
            if self.page < 0:
                bot.answerCallbackQuery(self.query.id, "Reached first page")
                return
        else:
            self.page += 1
            if self.page > self.calcTotPages(self.cat_list):
                bot.answerCallbackQuery(self.query.id, "Reached last page")
                return
        
        self.sendPage(bot, user)
    
    def sendPage(self, bot, user):
        list_of_elements = self.create_element_list()
        tot_pages = self.calcTotPages(self.cat_list)
        super().sendPage(bot, user, list_of_elements, tot_pages)
    
    