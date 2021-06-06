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

reactions = [":hand_splayed:", ":hand_fist:", ":v:"]


@client.event
async def on_ready():
    print("hello there")


@client.event
async def on_member_join(member):
    print("joined")
    await member.edit(nick="tylerDurden")
    print("rule sent")
    await member.send(content=RULES)
    
token = os.environ["TOKEN"]

client.run(token)
