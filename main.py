#!/usr/bin/env python3

import logging
import textwrap

from backend import Backend
from starttalker import StartTalker

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
start_talker = StartTalker(backend)

"""
Stateless commands
"""

def get_movements_execute(bot, update):
    update.message.reply_text(str(backend.get_movements()))

def del_movements_execute(bot, update):
    backend.del_movements()
    update.message.reply_text("OK")

"""
Main
"""

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    
    updater = Updater('639582450:AAEAHQ_VapSVqpcEiYLz6pxVGWchHAlTvS8')

    conversation_handler = ConversationHandler(
        entry_points = [
            CommandHandler('start', start_talker.ask)
        ],
        states = {
            start_talker.ans: start_talker.handlers(),
            start_talker.borrow_talker.ans: start_talker.borrow_talker.handlers(),
            start_talker.borrow_talker.insert_talker.ans: start_talker.borrow_talker.insert_talker.handlers(),
            start_talker.borrow_talker.remove_talker.ans: start_talker.borrow_talker.remove_talker.handlers(),
            start_talker.return_talker.ans: start_talker.return_talker.handlers(),
            start_talker.return_talker.insert_talker.ans: start_talker.return_talker.insert_talker.handlers(),
            start_talker.return_talker.remove_talker.ans: start_talker.return_talker.remove_talker.handlers(),
        },
        fallbacks = [],
    )
    
    updater.dispatcher.add_handler(conversation_handler)
    
    for callback in [get_movements_execute, del_movements_execute]:
        name = callback.__name__
        if name.endswith("_execute"):
            command = name[:-len("_execute")]
            updater.dispatcher.add_handler(CommandHandler(command, callback))
        else:
            raise Exception("Function name `%s` does not end with _execute")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
