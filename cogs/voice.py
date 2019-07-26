import os
import asyncio
import discord
import youtube_dl
from discord.ext import commands, tasks
from discord.utils import get
from settings import ytdl_opts, ffmpeg_options
from datetime import datetime


ytdl = youtube_dl.YoutubeDL(ytdl_opts)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data

        self.title = data.get('title', None)
        self.url = data.get('url', None)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Voice(commands.Cog):
    
    SONG_DIR = 'music'
    SONG_FORMAT = 'webm'

    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        
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
    async def yt(self, ctx, *, url):
        """Plays music from youtube"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command(aliases=['vol', 'vo', 'vl'])
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(aliases=['sto', 'st'])
    async def stop(self, ctx):
        """Stops the music."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send('Music has been stopped.')
        else:
            await ctx.send('Music is not playing.')

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

    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        ytdl.params['outtmpl'] = self.SONG_DIR + '/%(extractor)s-%(id)s-%(title)s.%(ext)s'
        is_dir = os.path.isdir(f'./{self.SONG_DIR}')
        if is_dir is False:
            os.mkdir(f'./{self.SONG_DIR}')
        
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            # TBD: add queue 

    @tasks.loop(minutes=30)
    async def clear_songs(self):
        songs = os.listdir(f'./{self.SONG_DIR}')
        if len(songs) > 15:
            for item in songs:
                if item.endswith(self.SONG_FORMAT):
                    os.remove(item)


def setup(bot):
    bot.add_cog(Voice(bot))
