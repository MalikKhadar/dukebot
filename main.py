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

if "dict" not in db.keys():
  db["dict"] = {}

if not os.path.isfile("battle.pkl"):
  b = Battle()
  save_battle(b, "battle.pkl")
  
#gotta keep track of user on each battle event, if they're the one that added the emoji, on_reaction_add, do the stuff
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
        s = b.champ_string()
        s += "\nClear battle history with $battle_clear. Goodbye."
        await message.channel.send(s)

    if msg.startswith('$battle_clear'):
        b = Battle()
        save_battle(b, "battle.pkl")
        db["dict"] = {}
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
        db["dict"][m.id] = [sender, r_num]
        
        # #move following to reaction handler
        # response += b.stats_string()


keep_alive()
client.run(os.getenv('TOKEN'))