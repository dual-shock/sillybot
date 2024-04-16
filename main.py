import discord
from discord.ext import commands 
import logging
import json
import random
import dotenv
import os

dotenv.load_dotenv("bot-token.env")
BOT_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

class Silly(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="",
            case_insensetive=True,
            intents=discord.Intents.all()
        )
        self.cogs_list = [
            'game_commands',
            'events'
        ]

    async def load_cogs(self):
        print('\nLoading extention cogs!')
        for filename in os.listdir("./cogs"):
            if filename[:-3] in self.cogs_list:
                print(f'- Loading cogs.{filename[:-3]}')
                await self.load_extension(f"cogs.{filename[:-3]}")
        print(f'Loaded extention cogs!\n')

    async def reload_cogs(self):
        print('\nReloading extension cogs!')
        for filename in os.listdir("./cogs"):
            if filename[:-3] in self.cogs_list:
                print(f"- Reloading cogs.{filename[:-3]}!")
                await self.reload_extension(f"cogs.{filename[:-3]}")
        print(f'Reloaded extention cogs!\n')

Silly = Silly()

@Silly.event
async def on_ready():
    await Silly.load_cogs()
    print(f'Silly activated as {Silly.user}')

@Silly.command(aliases=['ReloadCogs'], hidden=True)
@commands.is_owner()
async def _reload_cogs(ctx):
    await Silly.reload_cogs()


Silly.run(BOT_TOKEN, 
    #log_handler=logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
)