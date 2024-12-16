#import discord
#from discord.ext import commands 
import dotenv
import os
from pathlib import Path

from interactions import Client, listen, Intents
import interactions.ext.prefixed_commands as pre



#X:/Desktop/repos/sillybot/.venv/Scripts/python.exe -m pip install discord-py-interactions --upgrade



dotenv.load_dotenv(Path(__file__).with_name("bot-token.env"))
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

#intents = discord.Intents.default()
#intents.message_content = True

class Silly(Client):
    def __init__(self):
        super().__init__(
            # command_prefix="",
            # case_insensetive=True,
            intents=Intents.ALL
        )
        self.cogs_list = [
            #'game_commands',
            #'events'
            'vcReq'
        ]
    

    def load_cogs(self):
        print('\nLoading extention cogs!')
        for filename in os.listdir(Path(__file__).parent / "./cogs"):
            if filename[:-3] in self.cogs_list:
                print(f'- Loading cogs.{filename[:-3]}')
                self.load_extension(f"cogs.{filename[:-3]}")
        print(f'Loaded extention cogs!\n')

    def reload_cogs(self):
        print('\nReloading extension cogs!')
        for filename in os.listdir(Path(__file__).parent / "./cogs"):
            if filename[:-3] in self.cogs_list:
                print(f"- Reloading cogs.{filename[:-3]}!")
                self.reload_extension(f"cogs.{filename[:-3]}")
        print(f'Reloaded extention cogs!\n')



Silly = Silly()
pre.setup(Silly, default_prefix="-")

@listen()
async def on_ready():
    Silly.load_cogs()
    print(f'Silly activated as {Silly.user}')
    

@pre.prefixed_command(name='ReloadCogs')
async def _reload_cogs(ctx: pre.PrefixedContext):
    if ctx.author != Silly.owner:
        await ctx.send("You're not Silly's owner...")
    else:
        Silly.reload_cogs()
        await ctx.send("Reloaded cogs Nora<3")

Silly.start(BOT_TOKEN)
    #log_handler=logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
