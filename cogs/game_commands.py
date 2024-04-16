from discord.ext import commands
import random
import json


class GameCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=['pick'])
    async def _pick_game(self, ctx, word1):
        if(word1.lower()=="game"):
            with open("data.json","r") as data_file:
                data = json.load(data_file)
                await ctx.send(f'Silly picked { random.choice(data["chooseGames"]) }!')
        else:
            return

    @commands.command(aliases=['add'])
    async def _add_game(self, ctx, word1, *args):
        arguments = ' '.join(args)
        if(word1.lower()=="game"):
            with open("data.json","r+") as data_file:
                data = json.load(data_file)
                data["chooseGames"].append(f'{arguments}')
                json.dump(data, data_file, indent=4)
            await ctx.send(f'silly added {arguments} to the list of games!')
        else:
            return

    @commands.command(aliases=['remove'])
    async def _remove_game(self, ctx, word1, *args):
        arguments = ' '.join(args)
        if(word1.lower()=="game"):
            with open("data.json","r+") as data_file:
                data = json.load(data_file)
                data["chooseGames"].remove(arguments)
                json.dump(data, data_file, indent=4)
            await ctx.send(f'silly removed {arguments} from the list of games!')
        else:
            return
        
    @commands.command(aliases=['show'])
    async def _show_games(self, ctx, word1):
        if(word1.lower()=="games"):
            games_list = ""
            with open("data.json","r") as data_file:
                data = json.load(data_file)
                for game in data["chooseGames"]:
                    games_list += f'- {game}\n'
            await ctx.send(f"these are the games currently in silly's list:\n{games_list}")
        else:
            return


    async def cog_load(self):
        print(f"- {self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"- {self.__class__.__name__} unloaded!")



async def setup(bot):
    await bot.add_cog(GameCommandsCog(bot=bot))