
import asyncio
from pathlib import Path
from typing import Union
from interactions import (
    Extension,
    SlashContext,
    slash_command,
    check,
    is_owner,
    Permissions,
    slash_option,
    OptionType, 
    listen,
    Member,
    User,
    ActionRow, 
    Button, 
    ButtonStyle, 
    is_owner, 
    check,
    user_context_menu,
    ContextMenuContext,
    Message,
    ChannelType
)
from interactions.api.events import Component


class funStuff(Extension):
    def __init__(self, client):
        self.Silly = client
        asyncio.create_task(self.async_init())
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()
    async def async_init(self): print(f"- {self.__class__.__name__} loaded!")   
    async def async_drop(self): print(f"- {self.__class__.__name__} unloaded!")

    @slash_command(
        name="s",
        description="mmdfhm",
    )
    @slash_option(
        name="content",
        description="content",
        required=True,
        opt_type=OptionType.STRING
    )
    @slash_option(
        name="channel",
        description="channel",
        required=True,
        opt_type=OptionType.CHANNEL,
        channel_types=[ChannelType.GUILD_TEXT],
    )
    @slash_option(
        name="reply_id",
        description="msg id of smth to reply to",
        required=False,
        opt_type=OptionType.STRING,
    )
    @check(is_owner())
    
    async def s(self, ctx: SlashContext, content: str, channel, reply_id: Union[str, None] = None):
        if reply_id is not None:
            try:
                msg = await channel.fetch_message(int(reply_id))
                print(msg)
                
            except Exception as e:
                print(e)
            await msg.reply(content)
            await ctx.send("reply sent", ephemeral=True)
            return
        await channel.send(content)
        await ctx.send("sent", ephemeral=True)

def setup(client):
    funStuff(client)