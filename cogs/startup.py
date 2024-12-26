
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
    Activity,
    ActivityType
)
from interactions.api.events import Component


class startup(Extension):
    def __init__(self, client):
        self.Silly = client
        asyncio.create_task(self.async_init())
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()
    async def async_init(self): 
        print(f"- {self.__class__.__name__} loaded!")
        await self.Silly.change_presence(
            status="online",
            activity=Activity.create(
                type=ActivityType.PLAYING,
                name="with your heart<3",
                state="flying through cyberspace.,.",
                url="https://www.youtube.com/watch?v=SZQc4YCxjNY"
            )
        )
        
    async def async_drop(self): print(f"- {self.__class__.__name__} unloaded!")





def setup(client):
    startup(client)
