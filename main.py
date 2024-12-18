import dotenv
import os
from pathlib import Path

from interactions import (
    Client, 
    listen, 
    Intents, 
    slash_command,
    SlashContext,
    check,
    is_owner)

dotenv.load_dotenv(Path(__file__).with_name("bot-token.env"))
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
class Silly(Client):
    def __init__(self):
        super().__init__(intents=Intents.ALL)
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

    def reload_cogs(self):
        print('\nReloading extension cogs!')
        for filename in os.listdir(Path(__file__).parent / "./cogs"):
            if filename[:-3] in self.cogs_list:
                print(f"- Reloading cogs.{filename[:-3]}!")
                self.reload_extension(f"cogs.{filename[:-3]}")

Silly = Silly()

@listen()
async def on_ready():
    print(f'Silly activated as {Silly.user}! loading cogs now...')
    Silly.load_cogs()
    

@slash_command(name="reload_cogs",
               description="Reloads the bot without restarting")
@check(is_owner())
async def reload_cogs(ctx: SlashContext):
    Silly.reload_cogs()
    await ctx.send("Reloaded cogs Nora<3", ephemeral=True)
@reload_cogs.error
async def req_error(ctx: SlashContext, error: Exception):
    pass
    #await ctx.send(error, "\n\nYou're not Silly's owner...")



Silly.start(BOT_TOKEN)
    #log_handler=logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
