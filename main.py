import discord
from discord.ext import commands 
import logging
import json
import random
from responses import responses
from utils import get_env_var
import re


BOT_TOKEN = get_env_var("bot-token.env", "DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

log_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

bot = commands.Bot(command_prefix="",case_insensitive=True, intents=intents)
data = {}
with open("data.json","r") as data_file:
    data = json.load(data_file)

wordle_message_regex = re.compile('^Wordle\s\d,\d\d\d\s\d/6$')

async def check_message(message):
    for response in responses:
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

async def update_leaderboard():

    pass

@bot.event
async def on_ready():
    print(f'Bot activated as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:return

    # ? If someone mentions the bot:
    if bot.user.mentioned_in(message):
        await message.channel.send("hi! i'm silly, a bot made by @noranixi. i can help you with a few things, like picking games or responding to certain messages. try saying 'silly pick game' or 'silly show games'!")

    # ? Check if message contains any of the inputs that trigger responses
    await check_message(message) 
        
    # ? If message contains "Wordle"
    if random.randint(1, 1000) == 1:
        await message.channel.send(random.choice(["You found a butterscoth-cinnamon pie."]))

    if wordle_message_regex.match( message.content.split('\n')[0] ) is not None:
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
        


    # ? If message is long
    if len(message.content) > 256:
        await message.channel.send("yapper alert!")

    # ? Boob getting told to lock in every 100th ish msg
    if message.author.name == "balogna":
        if random.randint(1, 25) == 1:
            await message.channel.send(f"time to lock in @{message.author.mention}")

    # ? Process other commands that might be triggered by message
    await bot.process_commands(message)

@bot.command(aliases=['pick'])
async def _pick_game(ctx, word1):
    if(word1.lower()=="game"):
        await ctx.send(f'Silly picked { random.choice(data["chooseGames"]) }!')
    else:
        return

@bot.command(aliases=['add'])
async def _add_game(ctx, word1, *args):
    arguments = ' '.join(args)
    if(word1.lower()=="game"):
        data["chooseGames"].append(f'{arguments}')
        with open("data.json","r+") as data_file:
            json.dump(data, data_file, indent=4)
        await ctx.send(f'silly added {arguments} to the list of games!')
    else:
        return

@bot.command(aliases=['remove'])
async def _remove_game(ctx, word1, *args):
    arguments = ' '.join(args)
    if(word1.lower()=="game"):
        data["chooseGames"].remove(arguments)
        with open("data.json","r+") as data_file:
            json.dump(data, data_file, indent=4)
            await ctx.send(f'silly removed {arguments} from the list of games!')
    else:
        return
    
@bot.command(aliases=['show'])
async def _show_games(ctx, word1):
    if(word1.lower()=="games"):
        games_list = ""
        for game in data["chooseGames"]:
            games_list += f'- {game}\n'
        await ctx.send(f"these are the games currently in silly's list:\n{games_list}")
    else:
        return

bot.run(BOT_TOKEN, log_handler=log_handler)
