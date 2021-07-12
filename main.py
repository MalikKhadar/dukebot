# powered by Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang,
#   Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling
#   Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."
#   In International Conference on Learning Representations, 2019.

import pretty_midi
from battling.battle import Battle
from keep_alive import keep_alive
import discord
import os
from replit import db
import pickle

# b = battle.Battle()
# while(True):
#     b.host_battle()

def save_battle(battle, dest):
    with open(dest, 'wb') as output:
        pickle.dump(battle, output, pickle.HIGHEST_PROTOCOL)
        print("dumped")

def load_battle(dest):
    with open(dest, 'rb') as input_file:
        print("loaded")
        return pickle.load(input_file)

client = discord.Client()

if "active" not in db.keys():
  db["active"] = False

if "msgs" not in db.keys():
  db["msgs"] = []
  db["user"] = []
  db["rnum"] = []

if not os.path.isfile("battle.pkl"):
  b = Battle()
  save_battle(b, "battle.pkl")
  
#First message show contenders/stats, have contenders' emoji on message
#2nd and third, contenders say their things, have their wave files attached
#4th, appears once choice is made, shows all stats, has winner's midi attached

# dict for messageid to record_num?

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$battle_begin'):
        await message.channel.send("It has begun.")
        db["active"] = True

    if msg.startswith('$battle_end'):
        db["active"] = False
        b = load_battle("battle.pkl")
        s = b.champ_stat()
        s += "\nClear battle history with $battle_clear."
        s += "\nGoodbye."
        await message.channel.send(s)

    if msg.startswith('$battle_clear'):
        b = Battle()
        save_battle(b, "battle.pkl")
        db["msgs"] = []
        db["user"] = []
        db["rnum"] = []
        s = "Battle history has been cleared."
        await message.channel.send(s)

    if msg.startswith('$challenge') and db["active"]:
        sender = message.author.id
        b = load_battle("battle.pkl")
        b.host_battle()
        response = b.battle_msg()
        save_battle(b, "battle.pkl")
        c = message.channel
        #get the emoji options
        e1 = b.rm.records[-1].b1.emoji
        e2 = b.rm.records[-1].b2.emoji
        #post message with emoji
        m = await c.send(response)
        await m.add_reaction(e1)
        await m.add_reaction(e2)
        #file the messageid
        r_num = len(b.rm.records) - 1
        d = db["dict"]
        d[m.id] = [sender, r_num]
        db["dict"] = d

@client.event
async def on_reaction_add(reaction, user):
    print("reaction noted")
    msgid = reaction.message.id
    print(msgid)
    d = db["dict"]
    print(d)
    print(d.keys())
    #stop if reaction to normal message
    if msgid not in d.keys() or not db["active"]:
        return
    print("special message")
    b = load_battle("battle.pkl")
    userid = d[msgid][0]
    r_num =d[msgid][1]
    #stop if reacter didn't initiate challenge
    if user.id != userid:
        return
    print("correct user")
    #stop if a winner was already determined
    rec = b.rm.records[r_num]
    if rec.winner != None:
        return
    print("undetermined winner")

    file = ""
    if rec.b1.emoji == reaction.emoji:
        rec.winner = rec.b1
        rec.b1.add_stat(won=True)
        rec.b2.add_stat(won=False)
    elif rec.b2.emoji == reaction.emoji:
        rec.winner = rec.b2
        rec.b1.add_stat(won=False)
        rec.b2.add_stat(won=True)
    else:
        #stop if emoji is irrelevent
        return
    
    #retire battler if lost too much
    b.rm.pool.retire_check(rec.b1)
    b.rm.pool.retire_check(rec.b2)

    print("relevent emoji")
    save_battle(b, "battle.pkl")
    
    response = "The battle has been decided. The victor's midi is attached.\n\n"
    response += b.stats_string()
    await reaction.message.channel.send(response)
    
keep_alive()
client.run(os.getenv('TOKEN'))