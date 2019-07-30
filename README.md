# discord-bot

Bot based on [discord.py](https://github.com/Rapptz/discord.py).

Bot acts as a client to discord server to which user is connected.

## Configuration

In ./settings.py set following variables:

- discord API key

```python
discord_api_key = 'your_discord_api_key'
```

For more information, refer to discord [documentation](https://discordapp.com/developers/docs/intro).

- bot prefix. All available command starts with it, i.e. _**.help**_

```python
bot_prefix = '.'
```

## Setup

```bash
pip install requirements.txt
python bot.py
```

Alternatively with docker:

```bash
docker run -it --rm --name dibot -v "$PWD":/usr/src/dibot -w /usr/src/dibot python:3-alpine python bot.py
```

or

```bash
docker image build . -it dibot
docker run --name dibot -d dibot
```

## Commands

```text
Admin:
  ban    Bans the user from server.
  kick   Kicks the user from server.
  load   Loads the given module.
  reload Reloads the given module.
  unban  Unbans the user.
  unload Unloads the given module.
Misc:
  8ball  Returns randomly generated answer to the question.
  clear  Clears given amount of messages from text channel.
  ping   Checks bot's latency.
Voice:
  banish Stops and disconnects the bot from a voice channel.
  pause  Pauses the music.
  resume Resumes the music.
  stop   Stops the music.
  stream Streams from a url (same as yt, but doesn't predownload)
  summon Summons bot to the given voice channel.
  volume Changes the player's volume
  yt     Plays music from youtube
​No Category:
  help   Shows this message

Type .help command for more info on a command.
You can also type .help category for more info on a category.
```
