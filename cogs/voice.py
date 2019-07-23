import os
import discord
import youtube_dl
from discord.ext import commands
from discord.utils import get
from settings import ytdl_opts


class Voice(commands.Cog):
    
    SONG = 'song.mp3'

    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        
    @commands.command(aliases=['sum', 'summ', 'sm'])
    async def summon(self, ctx, *, channel: discord.VoiceChannel=None):
        """Summons bot to the given voice channel."""
        if channel is None: 
            channel = ctx.message.author.voice.channel
            
        if ctx.voice_client is not None:
            print(f'{self.bot.user.name} was summoned to {channel} by {ctx.message.author}')
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()
        
    @commands.command(aliases=['bani', 'bn'])
    async def banish(self, ctx):
        """Stops and disconnects the bot from a voice channel."""
        channel = ctx.message.author.voice.channel
        print(f'{self.bot.user.name} was banished from {channel} by {ctx.message.author}')
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def play(self, ctx, url : str):
        """Plays music from YT."""

        await ctx.send(f'Getting everything ready...')
        voice = get(self.bot.voice_clients, guild=ctx.guild)  # option to have it declared once?

        # Validate song file
        is_song = os.path.isfile(self.SONG)

        try:
            if is_song:
                os.remove(self.SONG)
                print(f'Removed old {self.SONG} file.')
        except PermissionError as e:
            await ctx.send('Music is already scheduled. Adding to queue.')
            return

        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            ydl.download([url])
            print('Song downloaded.')

        for filename in os.listdir('./'):
            if filename.endswith(self.SONG.split('.')[-1]):
                song_name = filename
                os.rename(song_name, self.SONG)
                print(f'Renamed {song_name} to {self.SONG}')

        # play music
        player = discord.FFmpegPCMAudio(self.SONG)
        voice.play(player, after=lambda e: print(f'{song_name} has finished playing.'))
        song_name = song_name.split('_')[2]
        await ctx.send(f'Now playing: {song_name}')

    @commands.command(aliases=['pau', 'ps', 'pa'])
    async def pause(self, ctx):
        """Pauses the music."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send('Music has been paused.')
        else:
            await ctx.send('Music is not playing currently.')

    @commands.command(aliases=['res', 're', 'rs'])
    async def resume(self, ctx):
        """Resumes the music."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send('Music has been resumed.')
        else:
            await ctx.send('Music is not paused.')

    @commands.command(aliases=['sto', 'st'])
    async def stop(self, ctx):
        """Stops the music."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Music has been stopped.')
        else:
            await ctx.send('Music is not playing.')

    @commands.command(aliases=['que', 'qu'])
    async def queue(self, ctx, url : str):
        """Queues the music."""
        pass

    @commands.command(aliases=['vol', 'vl'])
    async def volume(self, ctx):
        """Changes volume of the music"""
        pass


def setup(bot):
    bot.add_cog(Voice(bot))
