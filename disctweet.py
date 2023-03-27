import subprocess
import sys
try:
    import discord
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "discord"])
    import discord
try:
    import tweepy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tweepy"])
    import tweepy
import asyncio
import os

# Get the path to the directory where the script is running
dir_path = os.path.dirname(os.path.abspath(__file__))

# Read tokens from the tokens.txt file
with open(os.path.join(dir_path, 'tokens.txt'), 'r') as f:
    TOKEN = f.readline().strip()
    API_KEY = f.readline().strip()
    API_SECRET_KEY = f.readline().strip()
    ACCESS_TOKEN = f.readline().strip()
    ACCESS_TOKEN_SECRET = f.readline().strip()

# Read channel_ids from the users.txt file
CHANNEL_IDS = {}
with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
    for line in f:
        user, channel_id = line.strip().split(':')
        CHANNEL_IDS[user] = int(channel_id)

# Read the users to be monitored from the users.txt file
USERS_TO_TRACK = []
with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
    for line in f:
        user, channel_id = line.strip().split(':')
        USERS_TO_TRACK.append(user)

# Create an authentication for Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create a Tweepy API client
api = tweepy.API(auth)

# Create a Discord client
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('The bot is connected to Discord')
    latest_tweets = {user: None for user in USERS_TO_TRACK}
    while True:
        for user in USERS_TO_TRACK:
            if latest_tweets[user] is None:
                try:
                    latest_tweet = api.user_timeline(screen_name=user, count=1, include_rts=False, exclude_replies=True)[0]
                    latest_tweets[user] = latest_tweet
                except IndexError:
                    print(f"No tweets found for {user}")
            else:
                latest_tweet = api.user_timeline(screen_name=user, count=1, since_id=latest_tweets[user].id, include_rts=False, exclude_replies=True)
                if len(latest_tweet) > 0:
                    latest_tweet = latest_tweet[0]
                    latest_tweets[user] = latest_tweet
                    channel = client.get_channel(CHANNEL_IDS[user])
                    if channel:
                        tweet_url = 'https://twitter.com/{}/status/{}'.format(user, latest_tweet.id)
                        await channel.send("\u200B\n" + tweet_url)
        await asyncio.sleep(60)

# Run the client using the token
client.run(TOKEN)
