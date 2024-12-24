from discord.ext import commands
import random
import re
import json 
#import cogs.responses as rs
import importlib

wordle_message_regex = re.compile('^Wordle\s\d,\d\d\d\s\d/6$')

async def check_message(message):
    for response in rs.responses:
        for input_string in response.inputs:
            if response.anySubstring and input_string.lower() in message.content.lower():
                if len(response.responses) > 1:
                    await message.channel.send(random.choice(response.responses))
                else:
                    await message.channel.send(response.reponses[0])
                return
            elif response.startsWith and message.content.lower().startswith(input_string.lower()):
                if len(response.responses) > 1:
                    await message.channel.send(random.choice(response.responses))
                else:
                    await message.channel.send(response.reponses[0])
                return
    return

async def handle_wordle(message):
    with open("data.json","r") as data_file:
        data = json.load(data_file)
        wordle_number = message.content.split(' ')[1].replace(',','')
        print(wordle_number)
        username = message.author.name
        print(data["userdata"])
        print(username)
        print(data["userdata"]["africansalvationunite"]["wordles"])  
        print(bool(username in data["userdata"]))
        if username not in data["userdata"]:
            data["userdata"][username] = {
                "wordles":[{}],
                "total_wordle_score":0
            }
        if f'{wordle_number}' not in data["userdata"][username]["wordles"]:
            data["userdata"][username]["wordles"].append({
                "number":wordle_number,
                "score":message.content.split(' ')[2].split('/')[0]
            })
            message.channel.send(f"Added wordle {wordle_number} to {username}'s wordle list!")

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:return
        # ? If someone mentions the bot:
        if self.bot.user.mentioned_in(message):
            pass
            #await message.channel.send("hi! i'm silly, a bot made by @noranixi. i can help you with a few things, like picking games or responding to certain messages. try saying 'pick game' or 'show games'!")

        # ? Check if message contains any of the inputs that trigger responses
        await check_message(message) 
            
        
        if random.randint(1, 1000) == 1:
            await message.channel.send(random.choice(["You found a butterscoth-cinnamon pie."]))

        # ? If message contains "Wordle"
        if wordle_message_regex.match( message.content.split('\n')[0] ) is not None:
            await handle_wordle(message)
            
        # ? If message is long
        if len(message.content) > 256:
            await message.channel.send("yapper alert!")

        # ? Boob getting told to lock in every 100th ish msg
        if message.author.name == "balogna":
            if random.randint(1, 25) == 1:
                await message.channel.send(f"time to lock in {message.author.mention}")

    # doing something when the cog gets loaded
    async def cog_load(self):
        print(f'- loading responses module for {self.__class__.__name__}')
        importlib.reload(rs)
        print(f"- {self.__class__.__name__} loaded!")

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        print(f"- {self.__class__.__name__} unloaded!")
    


async def setup(bot):
    # finally, adding the cog to the bot
    await bot.add_cog(EventsCog(bot=bot))