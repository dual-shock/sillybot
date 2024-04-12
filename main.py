import discord
from discord.ext import commands 
import logging
import json
import random
from utils import get_env_var

BOT_TOKEN = get_env_var("bot-token.env", "DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

log_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

bot = commands.Bot(command_prefix="",case_insensitive=True, intents=intents)
data = {}
with open("data.json","r") as data_file:
    data = json.load(data_file)
    print(data)

@bot.event
async def on_ready():
    print(f'Bot activated as {bot.user}')

@bot.event
async def on_message(message):

    if message.author == bot.user:
        return

    # if someone sends 20-30 consecutive messages, or a
    # >1000 character message, respond "yapper alert!"    

    if len(message.content) > 256:
        await message.channel.send("yapper alert!")
    if 'ban' in message.content.lower():
        await message.channel.send("mods, ban him")    
    if 'chat' in message.content.lower():
        await message.channel.send(random.choice(data['responses']['chat']))
    if message.content.lower() in ['itsyou','its you', "it's you","it'syou"]:
        await message.channel.send("Despite everything, it's still you.")
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
        if True:
            await ctx.send(f'silly removed {arguments} from the list of games!')
        else:
            await ctx.send(f'silly failed to remove {arguments} from the list of games! did you spell it correctly?')
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