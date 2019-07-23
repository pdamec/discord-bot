import random
import settings as st
from discord.ext import commands


class Misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Checks bot's latency."""
        await ctx.send(f'Pong! My ping: {round(self.bot.latency * 1000)}ms')

    @commands.command(name='8ball', aliases=st._8ball_aliases)
    async def _8ball(self, ctx, *, question):
        """Returns randomly generated answer to the question."""
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(st._8ball_responses)}')

    @commands.command()
    async def clear(self, ctx, amount=5):
        """Clears given amount of messages from text channel."""
        await ctx.channel.purge(limit=amount + 1)


def setup(bot):
    bot.add_cog(Misc(bot))
