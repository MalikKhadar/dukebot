import os, random
from battling.battler import Battler

class Battler_Pool:
    def __init__(self, chunk_dir=
                 "midi/chunks/",
                 battlers=None, 
                 retired=None, size=4):
        #folder holding chunks
        self.chunk_dir = chunk_dir
        #chunks in play
        if battlers == None:
            self.battlers = []
        else:
            self.battlers = battlers
        #chunks no longer in play
        if retired == None:
            self.retired = []
        else:
            self.retired = retired
        #maximum number of chunks
        self.size = size

    def taken_chunks(self):
        '''returns list of chunks in use'''
        return [b.midi for b in self.battlers]

    def get_new_chunk(self):
        '''returns random chunk from chunk_dir'''
        taken = self.taken_chunks()
        chunk_list = os.listdir(self.chunk_dir)
        chunk = random.choice(chunk_list)
        #random choice until chunk isn't taken
        while chunk in taken:
            chunk = random.choice(chunk_list)
        return self.chunk_dir + chunk

    def should_grow(self):
        '''is true if growth check passes'''
        #minus 1 because >=2 battlers needed
        b_len = len(self.battlers) - 1
        #chance based on pool fullness
        fullness = b_len/(self.size-1)
        thresh = 1 - fullness
        check = random.uniform(0, 1)
        return True if check < thresh else False

    def draw_battler(self, exclude=None):
        '''draw a chunk for battle'''
        #make/return new battler if should grow
        if self.should_grow():
            chunk = self.get_new_chunk()
            new_battler = Battler(chunk)
            self.battlers.append(new_battler)
            return new_battler
        #or use existing battler if not
        else:
            b = random.choice(self.battlers)
            #choose non-excluded battler
            while b == exclude:
                b = random.choice(self.battlers)
            return b
    
    def retire_check(self, b, loss_cap=3):
        '''if b.loss > loss_cap, retire'''
        if b in self.retired:
            #stop if b already retired
            return
        if b.stat.loss >= loss_cap:
            self.battlers.remove(b)
            self.retired.append(b)

    def stats_string(self):
        '''string with stats'''
        s = "\t~Battlers~\n"
        s += "who\twins\tloss\tdraw\n"
        for b in self.battlers:
            s += b.stat_string()
        #if no retired, stop
        if len(self.retired) == 0:
            return s
        #else, display retired
        s += "\t-RETIRED-\n"
        s += "who\twins\tloss\tdraw\n"
        for r in self.retired:
            s += r.stat_string()
        return s

    def get_champ(self, standing=True):
        '''battler with most wins'''
        contenders = self.battlers
        #if considering retired as well
        if standing == False:
            contenders += self.retired
        champ = contenders[0]
        for c in contenders:
            if c.get_wins() > champ.get_wins():
                champ = c