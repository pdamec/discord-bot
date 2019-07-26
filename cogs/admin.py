from bot import load_cogs
import discord
from discord.ext import commands


class Admin(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def load(self, ctx, extension):
        """Loads the given module."""
        extension = extension.lower()
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Extension {extension} has been loaded.')
    
    @commands.command()
    async def unload(self, ctx, extension):
        """Unloads the given module."""
        extension = extension.lower()
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Extension {extension} has been unloaded.')

    @commands.command()
    async def reload(self, ctx, extension):
        """Reloads the given module."""
        extension = extension.lower()
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Extension {extension} has been reloaded.')
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """Kicks the user from server."""
        await member.kick(reason=reason)
        await ctx.send(f'User {member.mention} has been kicked.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """Bans the user from server."""
        await member.ban(reason=reason)
        await ctx.send(f'User {member.mention} has been banned.')

    @commands.command()
    async def unban(self, ctx, *, member):
        """Unbans the user."""
        banned_entries = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_entries:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'User {user.name}#{user.discriminator} has been unbanned.')  # or user.mention
                return

def setup(bot):
    bot.add_cog(Admin(bot))
