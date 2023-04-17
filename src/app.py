import discord

from discord.ext import commands
from src.history import ChainedList
from src.functions import *

class app:
    "class bot"
    def __init__(self) -> None:
        logPath()
        intents = discord.Intents.all()
        client = commands.Bot(command_prefix='!', intents=intents)
        now = datetime.datetime.now()
        jsonD = loadJson()

        self.history = ChainedList({"id": 0, "user": "SYSTEM", "day": now.strftime("%d/%m/%Y"), "hours": now.strftime("%H:%M:%S"), "reason": "REBOOT"})
        
        @client.command()
        async def history(ctx):
            self.log("cheking history",ctx)
            await ctx.send(self.history)
    
        @client.command()
        async def save(ctx):
            self.log("Shut down",ctx)
            self.history.to_json(jsonD['path'])
            await ctx.send("I'm sleeping")

        client.run(jsonD['token'])

    def log(self, reason, ctx):
        now = datetime.datetime.now()
        self.history.append({"id": ctx.author.id, "user": str(ctx.author), "day": now.strftime("%d/%m/%Y"), "hours": now.strftime("%H:%M:%S"), "reason": reason})
