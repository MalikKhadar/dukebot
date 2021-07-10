class Stat:
    def __init__(self, wins=0,
                 loss=0, draw=0):
        self.wins = wins
        self.loss = loss
        self.draw = draw

    def print_stat(self):
        '''print row in stats'''
        print(self.wins, end="\t")
        print(self.loss, end="\t")
        print(self.draw)