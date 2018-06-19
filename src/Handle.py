# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 23:32:03 2018

@author: Mauro
"""

from language_support.LanguageSupport import _

command_list = ["/categories",
                ]

def send_main_menu(bot, chatid, lang_tag):
    s = "<b> Main Menu </b>\n"
    s += "<i> Chose a category to vote or see the media in it</i>\n"
    s += "\n"
    s += "<b>--- Categories ---</b>\n"
    s += "<i> start here </i>"
    s += "/categories"
    
    s = _(s, lang_tag)

    bot.sendMessage(chatid, s, parse_mode = "HTML")
    
    

def handle_private_text(text, bot, chatid, lang_tag):
    
    if text == "/categories" or text == "/categories@pellascarpbot":
        pass
        # give the category page
    
    
    send_main_menu(bot, chatid, lang_tag)