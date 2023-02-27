import discord
import tweepy
import time
import os

# Hämta sökvägen till mappen där skriptet körs
dir_path = os.path.dirname(os.path.abspath(__file__))

# Läs in tokens från tokens.txt filen
with open(os.path.join(dir_path, 'tokens.txt'), 'r') as f:
    TOKEN = f.readline().strip()
    API_KEY = f.readline().strip()
    API_SECRET_KEY = f.readline().strip()
    ACCESS_TOKEN = f.readline().strip()
    ACCESS_TOKEN_SECRET = f.readline().strip()

# Läs in channel_ids från users.txt filen
CHANNEL_IDS = {}
with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
    for line in f:
        user, channel_id = line.strip().split(':')
        CHANNEL_IDS[user] = int(channel_id)

# Läs in användarna som ska bevakas från users.txt filen
USERS_TO_TRACK = []
with open(os.path.join(dir_path, 'users.txt'), 'r') as f:
    for line in f:
        user, channel_id = line.strip().split(':')
        USERS_TO_TRACK.append(user)

# Skapa en autentisering för Twitter API
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Skapa en Tweepy API-klient
api = tweepy.API(auth)

# Skapa en Discord-klient
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Bot är ansluten till Discord')
    latest_tweets = {user: None for user in USERS_TO_TRACK}
    while True:
        for user in USERS_TO_TRACK:
            if latest_tweets[user] is None:
                latest_tweet = api.user_timeline(screen_name=user, count=1, include_rts=False, exclude_replies=True)[0]
                latest_tweets[user] = latest_tweet
            else:
                latest_tweet = api.user_timeline(screen_name=user, count=1, since_id=latest_tweets[user].id, include_rts=False, exclude_replies=True)
                if len(latest_tweet) > 0:
                    latest_tweet = latest_tweet[0]
                    latest_tweets[user] = latest_tweet
                    channel = client.get_channel(CHANNEL_IDS[user])
                    if channel:
                        tweet_url = 'https://twitter.com/{}/status/{}'.format(user, latest_tweet.id)
                        await channel.send("\u200B\n" + tweet_url)
        time.sleep(60)

# Kör klienten med hjälp av token
client.run(TOKEN)
