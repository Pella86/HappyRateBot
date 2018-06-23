# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 02:27:02 2018

@author: Mauro
"""
import EmojiTable

def suffix_numbers(num, prec):
    magnitude = 0
    onum = num
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
        if magnitude >= 5:
            break

    if abs(onum) <= 999:
        return '{0}'.format(num)
    else:
        suffix_list = ('', 'K', 'M', 'G', 'T', 'P')
        format_pattern = '{0:.' + str(prec) + 'f}{1}'
        return format_pattern.format(num, suffix_list[magnitude])


class FormatNumber:
    
    def __init__(self, number, precision = 2, symbol = None, sufffixed = True):
        self.number = number
        self.suffixed = sufffixed
        self.precision = precision
        self.symbol = symbol
    
    
    def __str__(self):
        value = None
        
        if self.suffixed:
            value = suffix_numbers(self.number, self.precision)
        else:
            format_pattern = "{:." + str(self.precision) + "f}"
            value = format_pattern.format(self.number)
        
        if self.symbol:
            value += " " + self.symbol
        
        return value

class PellaCoins(FormatNumber):
    
    def __init__(self, number, precision = 0, suffixed = True):
        super().__init__(number, precision, EmojiTable.points_emoji, suffixed)