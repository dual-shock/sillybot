import interactions
#import importlib
import asyncio

class vcReq(interactions.Extension):
    def __init__(self, client):
        self.client = client
        print(self.extension_checks)
        asyncio.create_task(self.async_init())
    def drop(self):
        asyncio.create_task(self.async_drop())
        super().drop()

    # doing something when the cog gets loaded
    async def async_init(self):
        print(f"- {self.__class__.__name__} loaded!")
        
        vc = self.bot.get_channel(1233254546340581416)
        print(vc.members)
        

    # # doing something when the cog gets unloaded
    async def async_drop(self):
        print(f"- {self.__class__.__name__} unloaded!")
        
        pass


def setup(client):
    # finally, adding the cog to the bot
    vcReq(client)