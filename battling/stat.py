class Stat:
    def __init__(self, wins=0,
                 loss=0, draw=0):
        self.wins = wins
        self.loss = loss
        self.draw = draw

    def stat_string(self):
        '''return row in stats'''
        s = self.wins + "\t"
        s += self.loss + "\t"
        s += self.draw + "\n"
        return s