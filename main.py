# powered by Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang,
#   Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling
#   Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."
#   In International Conference on Learning Representations, 2019.

import pretty_midi
import battling
from keep_alive import keep_alive
import discord
import os
from replit import db
import pickle

# b = battle.Battle()
# while(True):
#     b.host_battle()

def save_battle(battle, dest):
    with open('dest', 'wb') as output:
        pickle.dump(battle, output, pickle.HIGHEST_PROTOCOL)
        print("dumped")

def load_battle(dest):
    with open('dest', 'rb') as input_file:
        return pickle.load(input_file)
        print("loaded")

client = discord.Client()

if "active" not in db.keys():
  db["active"] = False

if "used" not in db.keys():
  b = battling.Battle()
  save_battle(b, "battle.pkl")
  db["used"] = True

# if "battle" not in db.keys():
#   db["battle"] = battling.peepee
  
#gotta keep track of user on each battle event, if they're the one that added the emoji, on_reaction_add, do the stuff
#when battle_end, display standing champion and the overall champion

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
        # if "battle" not in db.keys():
        #     db["battle"] = Battle()

    if msg.startswith('$battle_end'):
        #TODO print standing champ, all-time champ
        db["active"] = False
        s = "" # db["battle"].champs()
        s += "Clear battle history with $battle_reset. Goodbye."
        await message.channel.send(s)

    if msg.startswith('$battle_reset'):
        b = battling.Battle()
        save_battle(b, "battle.pkl")
        s = "Battle history has been cleared."
        await message.channel.send(s)

    if msg.startswith('$challenge'):
        b = load_battle("battle.pkl")
        b.host_battle()
        response = b.battle_msg()
        save_battle(b, "battle.pkl")
        await message.channel.send(response)

keep_alive()
client.run(os.getenv('TOKEN'))