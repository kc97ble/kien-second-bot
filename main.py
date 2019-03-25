#!/usr/bin/python3

import logging
import textwrap

from backend import Backend

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

backend = Backend()

"""
Start
"""

def start_ask(bot, update):
    reply_markup = ReplyKeyboardMarkup(
        [["Borrow"], ["Return"], ["Status"]],
        one_time_keyboard=True
    )
    res = "Hello! How can I help you?"
    update.message.reply_text(res, reply_markup=reply_markup)
    return start_ans

def start_handlers():
    return [MessageHandler(Filters.text, start_ans)]

def start_ans(bot, update):
    req = update.message.text
    if req == "Borrow":
        return borrow_ask(bot, update)
    else:
        update.message.reply_text("Unknown request: `%s`" % req)
        return start_ask(bot, update)

"""
Borrow
"""

def borrow_ask(bot, update):
    stages = backend.get_stages(update.message.from_user.id)
    print(update.message.from_user.id)
    
    res = textwrap.dedent(
        """
        You are trying to borrow equipment.
        Press Add to add items to the list.
        
        Current list: %d item(s)
        
        %s
        """ % (len(stages), '\n'.join(map(str, stages)))
    )

    buttons = [["Add", "Remove"], ["Proceed"], ["Cancel"]]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    update.message.reply_text(res, reply_markup=reply_markup)
    return borrow_ans

def borrow_handlers():
    return [
        MessageHandler(Filters.text, borrow_ans)
    ]

def borrow_ans(bot, update):
    req = update.message.text
    if req == "Add":
        return borrow_add_ask(bot, update)
    elif req == "Proceed":
        pass
    else:
        update.message.reply_text("Unknown request: `%s`" % req)
        return borrow_ask(bot, update)

"""
Borrow > Add
"""

def borrow_add_ask(bot, update):
    res = "What do you want to add?"
    reply_markup = ReplyKeyboardRemove()
    update.message.reply_text(res, reply_markup=reply_markup)
    return borrow_add_ans

def borrow_add_handlers():
    return [
        MessageHandler(Filters.text, borrow_add_ans)
    ]

def borrow_add_ans(bot, update):
    req = update.message.text
    backend.post_borrow_add(update.message.from_user.id, req)
    return borrow_ask(bot, update)

"""
Done
"""

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    
    updater = Updater('639582450:AAEAHQ_VapSVqpcEiYLz6pxVGWchHAlTvS8')

    conversation_handler = ConversationHandler(
        entry_points = [
            RegexHandler('.*', start_ask)
        ],
        states = {
            start_ans: start_handlers(),
            borrow_ans: borrow_handlers(),
            borrow_add_ans: borrow_add_handlers()
        },
        fallbacks = [],
    )
    
    updater.dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
