from battling import record

class Battle:
    def __init__(self, rm= None):
        if rm == None:
            self.rm = record.Record_Manager()
        else:
            self.rm = rm

    def host_battle(self, record_num=None):
        '''create new battle if new record'''
        #host existing record if specified
        if record_num != None:
            rec = self.rm.records[record_num]
        #or just make a new record
        else:
            self.rm.make_record()
            #use latest (just created)
            rec = self.rm.records[-1]

    def battle_msg(self, record_num=None):
        '''string: battler stats, talk'''
        #host existing record if specified
        if record_num != None:
            rec = self.rm.records[record_num]
        #or use latest record
        else:
            rec = self.rm.records[-1]
        #display stats of contenders
        s = "\t\t~Contenders~\n"
        s += "who\twins\tloss\tdraw\n"
        s += rec.b1.stat_string()
        s += rec.b2.stat_string()
        #increase draw num AFTER text
        rec.b1.stat.draw += 1
        rec.b2.stat.draw += 1
        return s
    
    def stats_string(self, w=None, l=None):
        '''stat string from pool'''
        return self.rm.pool.stats_string(w=None, l=None)

    def champ_stat(self):
        '''stats of standing/retired champ'''
        #standing champ
        s = "\t\t~Standing Champ~\n"
        s += "who\twins\tloss\tdraw\n"
        standing = self.rm.pool.get_champ()
        if standing == None:
            return ""
        s += standing.stat_string()
        #ultimate champ
        s += "\t\t~Ultimate Champ~\n"
        s += "who\twins\tloss\tdraw\n"
        #False param for non-standing champ
        ult = self.rm.pool.get_champ(False)
        s += ult.stat_string()
        return s
        
        # choice = input("1 or 2: ")
        # if choice == "1":
        #     rec.winner = rec.b1
        #     rec.b1.add_stat(won=True)
        #     rec.b2.add_stat(won=False)
        # else:
        #     rec.winner = rec.b2
        #     rec.b1.add_stat(won=False)
        #     rec.b2.add_stat(won=True)

        # #retire battler if lost too much
        # self.rm.pool.retire_check(rec.b1)
        # self.rm.pool.retire_check(rec.b2)

        # self.rm.pool.print_stats()