import discord
import time
import os
from bs4 import BeautifulSoup
import requests
# from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
# client = commands.Bot(command_prefix="-")


RULES = "Gentlemen, welcome to Fight Club. \nThe first rule of Fight Club is: You do not talk about Fight Club. \nThe second rule of Fight Club is: You do not talk about Fight Club. \nThird rule of Fight Club: Someone yells \"Stop!\", goes limp, taps out, the fight is over. \nFourth rule: Only two guys to a fight. Fifth rule: One fight at a time, fellas. \nSixth rule: No shirts, no shoes. \nSeventh rule: Fights will go on as long as they have to. \nAnd the eighth and final rule: If this is your first night at Fight Club, you have to fight."

reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

categories = ['cars', 'animals-nature', 'anime-manga', 'art-creative', 'celebrities', 'gaming',
            'girls', 'internet', 'memes', 'movies', 'other', 'science-tech', 'sports', 'tv-shows']
lengths = ['day', 'week', 'month', 'year']


def get_media(link):
    sources = requests.get(link).text

    soup = BeautifulSoup(sources, 'lxml')

    post_m = soup.find('div', class_="post__media")

    img = post_m.a['href']
    img_ = img.split('/')
    print(img_)
    if(img_[1] == 'video'):
        link = 'https://ifunny.co'+img
        print('link:', link)
        src = requests.get(link).text

        souper = BeautifulSoup(src, 'lxml')

        vid = souper.find(
            'div', class_='media media_fun js-media js-playlist-media')['data-source']

        print(vid)
        return vid
        # print('way down: ', vid_)
    elif (img_[1] == 'picture'):
        img_p = post_m.a.img['data-src']
        print('Here', img_p)
        return img_p


def get_top(length):
    return get_media('https://ifunny.co/top-memes/'+length)


def get_cat(cat):
    return get_media('https://ifunny.co/'+cat)


def get_query(query):
    return get_media('https://ifunny.co/tags/'+query)


@client.event
async def on_ready():
    print("hello there")


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

    if message.content.startswith("!funny"):
        print('gotcha')
        h = message.content.split(' ')
        if(h[1] == 'help' and len(h) <= 2):
            msg_ = "Here's how to use the bot:\n!funny <type>:<parameter>\n\nThe three types are: \n1. 'category'\n2. 'top'\n3. 'tags'\n\n use !funny help <type> for help with parameters"
            await message.channel.send(msg_)
        elif(h[1] == 'help' and len(h) == 3):
            par = h[2]

            if(par == 'category'):
                msg_ = "The categories are: \n"
                for i in range(len(categories)):
                    msg_ += str(i+1)+". "+categories[i]+"\n"

                msg_ += "\n\n Use this as:\n!funny category:memes"
                await message.channel.send(msg_)
            elif(par == 'top'):
                msg_ = 'You can get top memes of the day, week, month or year.\n Use this as:\n!funny top:day'
                await message.channel.send(msg_)
            elif(par == 'tags'):
                msg_ = 'This acts like a search bar, simply type in your query as this:\n!funny tags:<query>'
                await message.channel.send(msg_)
        h1 = h[1].split(':')

        print('h', h)
        print('h1 -', h1)

        type_ = h1[0].strip()
        try:
            if(type_ == 'category'):
                print("it's category")
                cat = h1[1].strip()
                print('category:', cat)
                if cat in categories:
                    msg = get_cat(cat)
                    print('link: ', msg)
                    await message.channel.send(msg)
            elif(type_ == 'top'):
                print("it's top")
                _len = h1[1].strip()
                print('length:', _len)
                if(_len == ''):
                    _len = 'day'
                if _len in lengths:
                    msg = get_top(_len)
                    print('link: ', msg)
                    await message.channel.send(msg)
            elif(type_ == 'tags'):
                print("it's tag")
                tag = h1[1].strip()
                print('tag:', tag)
                if(tag == ''):
                    await message.channel.send("Don't do this")
                msg = get_query(tag)
                print('link: ', msg)
                await message.channel.send(msg)
        except:
            await message.channel.send('Error :(')

    elif message.content.startswith("!poll"):
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
                tie = False
                winners.clear()
                print("winning reaction:", reaction)
                winner = options[j]
                winners.append(winner)
                max = reaction.count
            elif reaction.count == max:
                tie = True
                winners.append(options[j])

            j += 1

        congrats = "And the winner is: " + winner

        if winner == "":
            congrats = "Nobody won!"

        if tie:
            congrats = "Tie between"
            for win in winners:
                congrats += " "+win+","

            congrats = congrats[:-1]
            congrats += "."

        await message.channel.send(congrats)

token = os.environ["TOKEN"]

client.run(token)
