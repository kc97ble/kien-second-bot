#!/usr/bin/env python3

import datetime

from tinydb import TinyDB, Query, operations as op, where

def hasAuthor(author):
    return where('author') == author

def hasAction(action):
    return where('action') == action

def hasItem(item):
    return where('item') == item

class Backend:
    
    def __init__(self):
        self.db = TinyDB('./db.json')
        self.movements = self.db.table('movements')
        self.stages = self.db.table('stages')
    
    def get_movements(self):
        return self.movements.all()
    
    def del_movements(self):
        return self.movements.purge()
    
    def get_stages(self, author, action):
        return self.stages.search(hasAuthor(author) & hasAction(action))
    
    def post_stages_operate(self, author, action, operation, text):
        assert operation in ['insert', 'remove']
        if operation == 'insert':
            self.stages.insert({
                'author': author,
                'action': action,
                'item': text,
                'date': str(datetime.datetime.now())
            })
        else:
            self.stages.remove(hasAuthor(author) & hasAction(action) & hasItem(text))
    
    def post_movement_proceed(self, author, action):
        stages = self.stages.search(hasAuthor(author) & hasAction(action))
        for item in stages:
            item.date = str(datetime.datetime.now())
        self.movements.insert_multiple(stages)
        self.stages.remove(hasAuthor(author) & hasAction(action))
    
    def post_clear_stages(self, author, action):
        self.stages.remove(hasAuthor(author) & hasAction(action))

    def get_unreturned_movements(self, author=None):
        m_list = self.movements.all()
        m_list.sort(key = lambda m : m['date'])
        
        latest = {}
        for m in m_list:
            if m['action'] == 'borrow':
                latest[m['item']] = m
            else:
                latest.pop(m['item'], None)

        result = sorted(latest.values(), key = lambda m : m['date'])
        if author != None:
            result = filter(lambda m : m['author'] == author, result)
            
        return list(result)
