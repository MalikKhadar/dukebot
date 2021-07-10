from os import truncate
from battle.battler_pool import Battler_Pool
from midi import midi_tools

class Battle_Record:
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
        self.winner = None

    def render(self, d1="1.wav", 
               d2="2.wav"):
        '''writes battlers to 2 dests'''
        wav = self.b1.generate_wav()
        midi_tools.save_wav(wav, d1)
        wav = self.b2.generate_wav()
        midi_tools.save_wav(wav, d2)

class History:
    def __init__(self, balance=0,
                 history=0):
        self.balance = balance
        self.history = history

class Record_Manager:
    def __init__(self, records=None, 
                 pool=None):
        #list of battle records
        if records == None:
            self.records = []
        else:
            self.records = records
        #pool of chunks
        if pool == None:
            self.pool = Battler_Pool()
        else:
            self.pool = pool

    def make_record(self):
        '''use repl db stuff later'''
        #db["records"].append(brec(blah))
        b1 = self.pool.draw_battler()
        b2 = self.pool.draw_battler(b1)
        record = Battle_Record(b1, b2)
        self.records.append(record)

def is_history(record, b1, b2):
    '''true if b1 & b2 in record'''
    if record.b1 == b1:
        if record.b2 == b2:
            return True
    #check both orders
    if record.b1 == b2:
        if record.b2 == b1:
            return True
    return False

def get_history(records, b1, b2):
    '''return b1 to b2 history'''
    balance = 0
    history = 0
    for r in records:
        #check if b1/b2 in record
        if is_history(r, b1, b2):
            history += 1
            #winner shifts balance
            if r.winner == b1:
                balance += 1
            elif r.winner == b2:
                balance -= 1
    h = History(balance, history)
    return h