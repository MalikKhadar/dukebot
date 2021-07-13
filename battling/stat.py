class Stat:
    def __init__(self, wins=0,
                 loss=0, draw=0):
        self.wins = wins
        self.loss = loss
        self.draw = draw

    def stat_string(self, outcome=0):
        '''return row in stats'''
        s = ""
        #highlight wins if won
        if outcome == 1:
            s += "\b" + str(self.wins) + "\b\t\t"
        else:
            s += str(self.wins) + "\t\t"
        #highlight loss if loss
        if outcome == -1:
            s += "\b" + str(self.loss) + "\b\t\t"
        else:
            s += str(self.loss) + "\t\t"
        #a draw is a draw
        s += str(self.draw) + "\n"
        return s