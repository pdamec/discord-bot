from itertools import cycle
import settings as st
import discord
from discord.ext import commands, tasks


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.statuses = cycle(st.statuses)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} is ready.')
        self.change_status.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send('Hello!')

    # Member join/leave
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member} has joined the server.')
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left the server.')
    
    # Errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Invalid command used.')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You lack permissions, Lad.')
        else:
            print(f'{error}')

    # Reactions
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(f'{user.name} has added {reaction.emoji} to the message: {reaction.message.content}')
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        channel = reaction.message.channel
        await channel.send(f'{user.name} has removed {reaction.emoji} from the message: {reaction.message.content}')

    #-------------- TASKS ---------------------

    @tasks.loop(seconds=2)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.statuses)))

def setup(bot):
    bot.add_cog(Events(bot))
