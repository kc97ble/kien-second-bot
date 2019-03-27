#!/usr/bin/env python3

import logging
import textwrap

from backend import Backend
from talker import Talker
from formatter import format_stages

QUESTION_FMT = """\
You are trying to %s equipment.
Press Insert to add items to the list.

Current list: %d item(s)

%s
"""

class MovementOperationTalker(Talker):
    
    def __init__(self, backend, action, operation, next_talker):
        assert action in ['borrow', 'return']
        assert operation in ['insert', 'remove']
        
        self.backend = backend
        self.action = action
        self.operation = operation
        self.next_talker = next_talker

    def ask(self, bot, update):
        question = "What do you want to %s?" % self.operation
        return self.ask_text(bot, update, question)

    def ans(self, bot, update):
        req = update.message.text
        self.backend.post_stages_operate(update.message.from_user.id, self.action, self.operation, req)
        return self.next_talker.ask(bot, update)

class MovementTalker(Talker):
    
    def __init__(self, backend, action, next_talker):
        self.backend = backend
        self.action = action
        self.next_talker = next_talker
        self.insert_talker = MovementOperationTalker(backend, action, 'insert', self)
        self.remove_talker = MovementOperationTalker(backend, action, 'remove', self)
    
    def ask(self, bot, update):
        stages = self.backend.get_stages(update.message.from_user.id, self.action)
        res = QUESTION_FMT % (self.action, len(stages), format_stages(stages))
        buttons = [["Insert", "Remove"], ["Proceed", "Cancel"]]
        return self.ask_buttons(bot, update, res, buttons)

    def ans(self, bot, update):
        req = update.message.text
        if req == "Insert":
            return self.insert_talker.ask(bot, update)
        elif req == "Remove":
            return self.remove_talker.ask(bot, update)
        elif req == "Proceed":
            return self.proceed_ask(bot, update)
        else:
            update.message.reply_text("Unknown request: `%s`" % req)
            return self.ask(bot, update)
    
    def proceed_ask(self, bot, update):
        self.backend.post_movement_proceed(update.message.from_user.id, self.action)
        update.message.reply_text("OK")
        return self.next_talker.ask(bot, update)
    
