#!/usr/bin/env python3

import logging
import textwrap

from backend import Backend
from formatter import format_stages

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    RegexHandler,
    Filters
)

class Talker:
    
    def ask_text(self, bot, update, question):
        reply_markup = ReplyKeyboardRemove()
        update.message.reply_text(question, reply_markup=reply_markup)
        return self.ans
    
    def ask_buttons(self, bot, update, question, buttons):
        reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
        update.message.reply_text(question, reply_markup=reply_markup)
        return self.ans
    
    def ask(self, bot, update):
        raise Exception("Override this method then call "
            "`ask_text` or `ask_buttons`")
    
    def handlers(self):
        return [MessageHandler(Filters.text, self.ans)]
    
    def ans(self, bot, update):
        pass
