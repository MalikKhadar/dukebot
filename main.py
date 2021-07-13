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

def save_battle(battle, dest):
    with open(dest, 'wb') as output:
        pickle.dump(battle, output, pickle.HIGHEST_PROTOCOL)

def load_battle(dest):
    with open(dest, 'rb') as input_file:
        return pickle.load(input_file)

def monospace(text):
    return "```" + text + "```"

client = discord.Client()

if "active" not in db.keys():
  db["active"] = False

if "dict" not in db.keys():
  db["dict"] = {}

if not os.path.isfile("battle.pkl"):
  b = Battle()
  save_battle(b, "battle.pkl")

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
        db["dict"] = {}
        s = "Battle history has been cleared."
        await message.channel.send(s)

    if msg.startswith('$challenge') and db["active"]:
        sender = message.author.id
        b = load_battle("battle.pkl")
        b.host_battle()
        response = b.battle_msg()
        response = monospace(response)
        save_battle(b, "battle.pkl")
        c = message.channel
        rec = b.rm.records[-1]
        #get the emoji options
        e1 = rec.b1.emoji
        e2 = rec.b2.emoji
        #post message with emoji
        m = await c.send(response)
        await m.add_reaction(e1)
        await m.add_reaction(e2)
        #file the messageid
        r_num = len(b.rm.records) - 1
        db["dict"][m.id] = [sender, r_num]
        #send the battler's talk/wav
        t1 = b.rm.get_topics(rec.b1, rec.b2)
        t2 = b.rm.get_topics(rec.b2, rec.b1)
        t1 = rec.b1.talk(t1)
        t2 = rec.b2.talk(t2)
        rec.render()
        w1 = discord.File("1.wav")
        w2 = discord.File("2.wav")
        await c.send(file=w1, content=t1)
        await c.send(file=w2, content=t2)


@client.event
async def on_reaction_add(reaction, user):
    msgid = str(reaction.message.id)
    #stop if reaction to normal message
    if str(msgid) not in db["dict"].keys() or not db["active"]:
        return
    b = load_battle("battle.pkl")
    userid = db["dict"][msgid][0]
    r_num = db["dict"][msgid][1]
    #stop if reacter didn't initiate challenge
    if user.id != userid:
        return
    #stop if a winner was already determined
    rec = b.rm.records[r_num]
    if rec.winner != None:
        return

    file = ""
    b.rm.records[r_num].save_midi()
    if rec.b1.emoji == reaction.emoji:
        rec.winner = rec.b1
        rec.b1.add_stat(won=True)
        rec.b2.add_stat(won=False)
        file = discord.File("1.mid")
    elif rec.b2.emoji == reaction.emoji:
        rec.winner = rec.b2
        rec.b1.add_stat(won=False)
        rec.b2.add_stat(won=True)
        file = discord.File("2.mid")
    else:
        #stop if emoji is irrelevent
        return
    
    #retire battler if lost too much
    b.rm.pool.retire_check(rec.b1)
    b.rm.pool.retire_check(rec.b2)

    save_battle(b, "battle.pkl")
    
    #reply to the user's challenge
    c = reaction.message.channel
    challege_msg = c.fetch_message(int(msgid))

    response = "The battle has been decided. The victor's midi is attached.\n\n"
    response += b.stats_string()
    response = monospace(response)
    await challege_msg.reply(file=file, content=response)
    
keep_alive()
client.run(os.getenv('TOKEN'))