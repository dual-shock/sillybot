import dotenv
import os
import datetime
from pathlib import Path
from interactions import (
    Client, 
    listen, 
    Intents, 
    slash_command,
    SlashContext,
    check,
    is_owner,
    Permissions,
    slash_option,
    OptionType,
    SlashCommandChoice
)
#c:/Users/nokken/Desktop/repos/sillybot/.venv/Scripts/python.exe -m pip install discord-py-interactions --upgrade



dotenv.load_dotenv(Path(__file__).with_name("bot-token.env"))
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
print(BOT_TOKEN)
class Silly(Client):
    def __init__(self):
        super().__init__(
            intents=Intents.ALL,
            sync_interactions=True,
            asyncio_debug=True,
            send_command_tracebacks=False,
            basic_logging=True

        )
        #default cogs other than startup loaded
        self.cogs_set = [
            'startup',
            'utility',
            'baseCmds',
            'vcReq',
            'misc',
            'funStuff'
        ]
        
    async def log(self, content):
        time = datetime.datetime.now().strftime('%H:%M:%S')
        await self.get_channel(1318190826458714214).send(f"```fix\n{time} | LOG: {content}```")
    
    async def load_cogs(self):
        await self.log("attempting to load cogs")
        print('\nLoading extention cogs!')
        for filename in self.cogs_set:
            try:
                print(f'- Loading cogs.{filename}')
                self.load_extension(f"cogs.{filename}")
            except Exception as e:
                await self.log(f"error loading cog {filename} with error: {e}")
                print(f'Failed to load cogs.{filename} with error: {e}')
        await self.log(f"cogs loading over")

    async def reload_cogs(self):
        await self.log("attempting to reload cogs")
        print('\nReloading extension cogs!')
        for filename in self.cogs_set:
            try:
                print(f'- Reloading cogs.{filename}')
                self.reload_extension(f"cogs.{filename}")
            except Exception as e:
                await self.log(f"error reloading cog {filename} with error: {e}")
                print(f'Failed to reload cogs.{filename} with error: {e}')
        await self.log(f"cogs reloading over")



Silly = Silly()

@listen()
async def on_ready():
    print(f'Silly activated as {Silly.user}! loading cogs now...')
    await Silly.log("silly has been turned on, loading its cogs :3")
    await Silly.load_cogs()

@slash_command(
    name="shutdown",
    description="Shuts down the bot")
@check(is_owner())
async def shutdown(ctx: SlashContext):
    await Silly.log("shutting down")
    await ctx.send("shutting down Nora<3", ephemeral=True)
    await Silly.stop()

@slash_command(
    name="reload_cogs",
    description="Reloads the bot without restarting")
@check(is_owner())
async def reload_cogs(ctx: SlashContext):
    await Silly.log("reloading cogs")
    await Silly.reload_cogs()
    await ctx.send("reloaded cogs Nora<3", ephemeral=True)

@slash_command(
    name="reload_cog",
    description="Reloads the bot without restarting")
@slash_option(
    name="cog",
    description="The cog to reload",
    required=True,
    opt_type=OptionType.STRING,
    choices=[
        SlashCommandChoice(name="utility", value="utility"),
        SlashCommandChoice(name="baseCmds", value="baseCmds"),
        SlashCommandChoice(name="vcReq", value="vcReq"),
        SlashCommandChoice(name="misc", value="misc"),
        SlashCommandChoice(name="funStuff", value="funStuff"), 
        SlashCommandChoice(name="startup", value="startup")
    ]
)
@check(is_owner())
async def reload_cog(ctx: SlashContext, cog: str):
    await Silly.log(f"reloading {cog}")
    try:
        Silly.reload_extension(f"cogs.{cog}")
        await ctx.send(f"reloaded {cog} Nora<3", ephemeral=True)
    except Exception as e:
        await ctx.send(f"Failed to reload {cog} with error: {e}", ephemeral=True)

Silly.start(BOT_TOKEN)

