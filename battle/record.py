from os import truncate
from battle.battler_pool import Battler_Pool
from midi import midi_tools
from battle.talk import Topics

class Battle_Record:
    def __init__(self, b1, b2):
        self.b1 = b1
        self.b2 = b2
        self.winner = None

    def render(self, d1="1.wav", 
               d2="2.wav"):
        '''writes battlers to wav'''
        wav = self.b1.generate_wav()
        midi_tools.save_wav(wav, d1)
        wav = self.b2.generate_wav()
        midi_tools.save_wav(wav, d2)

    def save_midi(self, d1="1.mid",
                  d2="2.mid"):
        '''write battlers to midi'''
        self.b1.write_midi(d1)
        self.b2.write_midi(d2)

    def in_record(self, b):
        '''true if b in record'''
        if self.b1 == b:
            return True
        if self.b2 == b:
            return True
        #b isn't in record
        return False

    def outcome(self, b1, b2):
        '''b1 won: 1, lost: -1, else 0'''
        if self.winner == b1:
            #make sure b1 beat b2
            if self.in_record(b2):
                return 1
        elif self.winner == b2:
            #make sure b2 beat b1
            if self.in_record(b1):
                return -1
        return 0

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

    def get_history(self, b1, b2):
        '''return b1 to b2 history'''
        hist = 0
        for r in self.records:
            hist += r.outcome(b1, b2)
        return hist

    def get_topics(self, b1, b2):
        '''return topics from b1 to b2'''
        #get ages, calculate diff
        a1 = b1.get_age()
        a2 = b2.get_age()
        a_diff = a1 - a2
        #same for ratios
        r1 = b1.get_ratio()
        r2 = b2.get_ratio()
        r_diff = r1 - r2
        #get history of b1 vs b2
        hist = self.get_history(b1, b2)
        #create topics object
        return Topics(a_diff, r_diff, hist)