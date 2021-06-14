import discord
from discord import member, channel
import time
import os
import random
# from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
# client = commands.Bot(command_prefix="-")


RULES = "Gentlemen, welcome to Fight Club. \nThe first rule of Fight Club is: You do not talk about Fight Club. \nThe second rule of Fight Club is: You do not talk about Fight Club. \nThird rule of Fight Club: Someone yells \"Stop!\", goes limp, taps out, the fight is over. \nFourth rule: Only two guys to a fight. Fifth rule: One fight at a time, fellas. \nSixth rule: No shirts, no shoes. \nSeventh rule: Fights will go on as long as they have to. \nAnd the eighth and final rule: If this is your first night at Fight Club, you have to fight."

reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]


@client.event
async def on_ready():
    print("hello there")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("-poll"):
        nxt = message.split(" ")[1]

        print(nxt)


@client.event
async def on_member_join(member):
    print("joined")
    await member.edit(nick="tylerDurden")
    print("rule sent")
    await member.send(content=RULES)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    emojis_to_add = []

    if message.content.startswith("!poll"):
        nxt = message.content.split(",")
        msg = "Add Reactions:\n"
        opt1 = nxt[0].split(" ")
        opt = opt1[1]
        nxt.insert(1, opt)
        nxt.pop(0)

        print(nxt)
        options = []

        for i in range(0, len(nxt)):
            options.append(nxt[i].strip())
            msg += str(i+1) + ". " + nxt[i].strip() + "\n"
            emojis_to_add.append(reactions[i])

        print(msg)
        print("options...", options)

        message_ = await message.channel.send(msg)
        id = message_.id
        for emoji in emojis_to_add:
            await message_.add_reaction(emoji)

        time.sleep(45)

        _message = await message.channel.fetch_message(id)
        reactions_ = _message.reactions
        print(_message.content)
        max = 1
        tie = False
        winner = ""
        winners = []
        j = 0
        for reaction in reactions_:
            if reaction.count > max:
                print("winning reaction:", reaction)
                winner = options[j]
                # winners.append(winner)
            elif reaction.count == max:
                tie = True
                winners.append(winner)
                
            j += 1

        congrats = "And the winner is: " + winner

        if winner == "":
            congrats = "Nobody won!"
        
        if tie:
            congrats = "Tie between"
            for win in winners:
                congrats += " "+win
            
            congrats += "."    
            

        await message.channel.send(congrats)

token = os.environ["TOKEN"]

client.run(token)
