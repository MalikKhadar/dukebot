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

if not os.path.isfile("battle.pkl"):
  b = Battle()
  save_battle(b, "battle.pkl")
  
#gotta keep track of user on each battle event, if they're the one that added the emoji, on_reaction_add, do the stuff

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
        s = "Battle history has been cleared."
        await message.channel.send(s)

    if msg.startswith('$challenge') and db["active"]:
        b = load_battle("battle.pkl")
        b.host_battle()
        response = b.battle_msg()
        save_battle(b, "battle.pkl")
        #move following to reaction handler
        response += b.stats_string()
        await message.channel.send(response)

keep_alive()
client.run(os.getenv('TOKEN'))