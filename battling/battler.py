from midi import midi_tools
from battling.rand_emoji import random_emoji
from battling.stat import Stat
import battling.talk as b_talk
from shutil import copyfile

class Battler:
    def __init__(self, midi, stat=None, 
                 emoji=None):
        self.midi = midi
        if stat == None:
            self.stat = Stat()
        else:
            self.stat = stat
        if emoji == None:
            self.emoji = random_emoji()
        else:
            self.emoji = emoji

    def generate_wav(self):
        '''returns midi as wav'''
        m = midi_tools.make_midi(self.midi)
        return midi_tools.make_wav(m)

    def write_midi(self, dest):
        '''write midi to dest'''
        copyfile(self.midi, dest)

    def stat_string(self):
        '''return row in stats'''
        s = self.emoji + ":\t"
        s += self.stat.stat_string()
        return s

    def add_stat(self, won=True, cap=3):
        '''update stat from battle'''
        if won:
            self.stat.wins += 1
        else:
            self.stat.loss += 1

    def get_age(self):
        '''return total num of battles'''
        w = self.stat.wins
        l = self.stat.loss
        d = self.stat.draw
        #sum battle outcomes
        return w + l + d

    def get_ratio(self):
        '''return wins - loss'''
        w = self.stat.wins
        l = self.stat.loss
        #ignore draws
        return w - l

    def get_wins(self):
        '''return stat.wins'''
        return self.stat.wins

    def get_loss(self):
        '''returns stat.loss'''
        return self.stat.loss

    def talk(self, topics=None):
        '''battle dialogue'''
        #assign topics object
        t = topics
        if t == None:
            t = b_talk.Topics()
        #say emoji, then phrase
        say = self.emoji + ": "
        say += b_talk.talk(t)
        return say