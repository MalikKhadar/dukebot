# powered by Curtis Hawthorne, Andriy Stasyuk, Adam Roberts, Ian Simon, Cheng-Zhi Anna Huang,
#   Sander Dieleman, Erich Elsen, Jesse Engel, and Douglas Eck. "Enabling
#   Factorized Piano Music Modeling and Generation with the MAESTRO Dataset."
#   In International Conference on Learning Representations, 2019.

import pretty_midi
from midi import chunk_midi
from battle import battle
from keep_alive import keep_alive
import discord
import os
from replit import db


# b = battle.Battle()
# while(True):
#     b.host_battle()

client = discord.Client()

if "active" not in db.keys():
  db["active"] = False

if "battle" not in db.keys():
  db["battle"] = battle.Battle()

#gotta keep track of user on each battle event, if they're the one that added the emoji, on_reaction_add, do the stuff
#when battle_end, display standing champion and the overall champion
#make it save 1.midi, 2.midi

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
        #TODO print standing champ, all-time champ
        db["active"] = False
        s = "" # db["battle"].champs()
        s += "Clear battle history with $battle_reset. Goodbye."
        await message.channel.send(s)

    if msg.startswith('$battle_reset'):
        db["battle"] = battle.Battle()
        s = "Battle history has been cleared."
        await message.channel.send(s)

    if msg.startswith('$challenge'):
        db["battle"].host_battle()

keep_alive()
client.run(os.getenv('TOKEN'))