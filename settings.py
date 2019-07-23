# Discord
discord_api_key = ''

# 8ball
_8ball_aliases = ['eightball', 'ball']
_8ball_responses = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes - definitely.',
    'You may rely on it.',
    'As I see it, yes.',
    'Most likely.',
    'Outlook good.',
    'Yes.',
    'Signs point to yes.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Better not tell you now.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.',
    ]


# Status
statuses = ['Sometimes', 'I', 'Think', 'Of', 'World of Warcraft']

# Greetings
greetings = {
    'polish': ['cześć', 'czesc', 'cze', 'siema', 'hej', 'witaj'],
    'english': ['hi', 'hey', 'hello', 'morning']
    }

# Youtube
ytdl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s_%(id)s_%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}
