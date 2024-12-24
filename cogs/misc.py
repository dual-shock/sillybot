
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
    Message
)
from interactions.api.events import Component


class misc(Extension):
    def __init__(self, client):
        self.Silly = client
        asyncio.create_task(self.async_init())
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()
    async def async_init(self): print(f"- {self.__class__.__name__} loaded!")   
    async def async_drop(self): print(f"- {self.__class__.__name__} unloaded!")

def setup(client):
    misc(client)