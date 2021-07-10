from battle import record

class Battle:
    def __init__(self, rm= None):
        if rm == None:
            self.rm = record.Record_Manager()
        else:
            self.rm = rm

    def host_battle(self, record_num=None):
        '''make wav files, await choice'''
        #host existing record if specified
        if record_num != None:
            rec = self.rm.records[record_num]
        #or just make a new record
        else:
            self.rm.make_record()
            #use latest (just created)
            rec = self.rm.records[-1]
        #render, await choice
        rec.render()
        print("\nBattlers")
        rec.b1.print_stat()
        rec.b2.print_stat()
        t1 = self.rm.get_topics(rec.b1, rec.b2)
        t2 = self.rm.get_topics(rec.b2, rec.b1)
        print("1: " + rec.b1.talk(t1))
        print("2: " + rec.b2.talk(t2))
        choice = input("1 or 2: ")
        if choice == "1":
            rec.winner = rec.b1
            rec.b1.add_stat(won=True)
            rec.b2.add_stat(won=False)
        else:
            rec.winner = rec.b2
            rec.b1.add_stat(won=False)
            rec.b2.add_stat(won=True)

        #retire battler if lost too much
        self.rm.pool.retire_check(rec.b1)
        self.rm.pool.retire_check(rec.b2)

        self.rm.pool.print_stats()