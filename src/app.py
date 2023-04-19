import discord, os

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
        self.history = ChainedList({"id": 0, "user": "SYSTEM", "day": now.strftime("%d/%m/%Y"), "hours": now.strftime("%H:%M:%S"), "reason": "START"})
        self.page = 1

        #Viewing last command
        @client.command()
        async def hlast(ctx):
            await ctx.send(self.generateHistory("hlast"))
            self.log("Display of the last order",ctx)

        #Viewing history
        @client.command()
        async def h(ctx):
            self.log("Viewing history",ctx)
            self.history.to_json(jsonD['path'])
            message = await ctx.send(self.generateHistory("h"))
            await message .add_reaction('⬆️')
            await message .add_reaction('⬇️')
        
        #Interact with "async def h" by emoji to scroll history
        @client.event
        async def on_reaction_add(reaction, user):
            if user.bot:
                return
            channel = reaction.message.channel
            
            #delete the last message of bot
            async for msg in channel.history():
                    if msg.author == client.user:
                        await msg.delete()
                        break

            if str(reaction.emoji) == '⬆️':
                self.page += 1
                print(self.page)
                message = await channel.send(self.generateHistory("hp"))
                await message .add_reaction('⬆️')
                if self.page > 1 : await message .add_reaction('⬇️')
            elif str(reaction.emoji) == '⬇️':
                self.page -= 1
                if self.page > 1 : 
                    message = await channel.send(self.generateHistory("hp"))
                    await message .add_reaction('⬆️')
                    await message .add_reaction('⬇️')
                else : await channel.send("There is no previous page to this one")

        #Viewing by name or id
        @client.command()
        async def hname(ctx):
            await ctx.send("About who you are looking for ? (id or username) example : username#1010")

            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            
            message = await client.wait_for('message', check=check)
            await ctx.send(self.generateHistory(str(message.content)))
            self.log("Viewing history of " + str(message.content),ctx)
    
        #Delete history
        @client.command()
        async def hdel(ctx):
            if os.path.isfile(jsonD['path']):
                os.remove(jsonD['path'])
                self.history = ChainedList({"id": str(ctx.author.id), ctx.author: "SYSTEM", "day": now.strftime("%d/%m/%Y"), "hours": now.strftime("%H:%M:%S"), "reason": "New history"})
                self.log("History deleted",ctx)
                await ctx.send("History deleted on path " + jsonD['path'])
            else:
                await ctx.send("History not found")

        #Save history               
        @client.command()
        async def s(ctx):
            self.log("Save history",ctx)
            self.history.to_json(jsonD['path'])
            await ctx.send("Save history successfully.")
        
        #When a new user joins the server
        @client.event
        async def on_member_join(ctx):
            self.log("New user : " + ctx.author + " name : " + ctx.author.id,ctx)
            await client.get_channel(1097370667646722058).send("Welcome to the server !"+ ctx.name)

        #When he launches
        @client.event
        async def on_ready():
            await client.get_channel(1097370667646722058).send("Navy bot is running !")

        client.run(jsonD['token'])

    #Save to json on node
    def log(self, reason, ctx):
        now = datetime.datetime.now()
        self.history.append({"id": ctx.author.id, "user": str(ctx.author), "day": now.strftime("%d/%m/%Y"), "hours": now.strftime("%H:%M:%S"), "reason": reason})

    #Return history data
    def generateHistory(self, search=None):
        current_node = self.history.first_node
        result = ""
        if search == "h":
            count = 0
            while current_node != None:
                if count >= 10: 
                    return result
                count += 1
                result += ("[+] - id : " + str(current_node.data['id']) + " | user : " + current_node.data['user'] + " | day : " + current_node.data['day'] + " | hours : " + current_node.data['hours'] + " | reason : " + current_node.data['reason'] + "\n")
                current_node = current_node.next_node
            return result 
        elif search == "hp":
            count = self.page * 10
            countL = self.page * 10
            line = 1
            while current_node != None:
                line += 1
                if count == 0: return result
                if count <= 10:
                    print(line, " a ", countL)
                    if line >= countL: return result; self.page = 1
                    result += ("[+] - id : " + str(current_node.data['id']) + " | user : " + current_node.data['user'] + " | day : " + current_node.data['day'] + " | hours : " + current_node.data['hours'] + " | reason : " + current_node.data['reason'] + "\n")
                    current_node = current_node.next_node
                    count -= 1
                else: 
                    current_node = current_node.next_node
                    count -= 1
            return result
        elif search == "hlast":
            while current_node != None:
                result = ("[+] - id : " + str(current_node.data['id']) + " | user : " + current_node.data['user'] + " | day : " + current_node.data['day'] + " | hours : " + current_node.data['hours'] + " | reason : " + current_node.data['reason'] + "\n")
                current_node = current_node.next_node
            return result
        else:
            while current_node != None:
                if current_node.data['user'] == search or str(current_node.data['id']) == search:
                    result += ("[+] - id : " + str(current_node.data['id']) + " | user : " + current_node.data['user'] + " | day : " + current_node.data['day'] + " | hours : " + current_node.data['hours'] + " | reason : " + current_node.data['reason'] + "\n")
                current_node = current_node.next_node
            return result
