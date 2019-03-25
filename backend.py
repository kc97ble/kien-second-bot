#!/usr/bin/python3

import datetime

from tinydb import TinyDB, Query, operations as op

class Backend:
    
    def __init__(self):
        self.db = TinyDB('./db.json')
        self.movements = self.db.table('movements')
        self.stages = self.db.table('stages');
    
    def get_stages(self, author):
        return self.stages.search(Query().author == author)
    
    def post_borrow_add(self, author, text):
        self.stages.insert({
            'author': author,
            'action': 'borrow',
            'item': text,
            'date': str(datetime.datetime.now())
        })
        
