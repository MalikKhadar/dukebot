from midi import midi_tools
from battle.rand_emoji import random_emoji
from battle.stat import Stat

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

    def print_stat(self):
        '''print row in stats'''
        print(self.emoji, end="\t")
        self.stat.print_stat()

    def add_stat(self, won=True, cap=3):
        '''update stat from battle'''
        if won:
            self.stat.wins += 1
        else:
            self.stat.loss += 1

    def talk(self, history=None):
        '''battle dialogue'''
        say = self.emoji + ":\t"
        #say += talk(history)
        return say