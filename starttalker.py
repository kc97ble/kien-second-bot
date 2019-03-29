#!/usr/bin/env python3

import logging
import textwrap

from backend import Backend
from talker import Talker
from formatter import format_stages, format_movement_list
from movementtalker import MovementTalker

class StartTalker(Talker):
    
    def __init__(self, backend):
        self.backend = backend
        self.borrow_talker = MovementTalker(backend, 'borrow', self)
        self.return_talker = MovementTalker(backend, 'return', self)
    
    def ask(self, bot, update):
        return self.ask_buttons(bot, update, "Hi! How can I help you?",
            [["Borrow", "Return", "Status"]])
    
    def ans(self, bot, update):
        req = update.message.text
        if req == "Borrow":
            return self.borrow_talker.ask(bot, update)
        elif req == "Return":
            return self.return_talker.ask(bot, update)
        elif req == "Status":
            return self.status_ask(bot, update)
        else:
            update.message.reply_text("Unknown request: `%s`" % req)
            return self.ask(bot, update)
    
    def status_ask(self, bot, update):
        m_list = self.backend.get_unreturned_movements(update.message.from_user.id)
        update.message.reply_text(format_movement_list(m_list))
        return self.ask(bot, update)
