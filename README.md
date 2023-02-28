# Disctweet

Disctweet is a Python script that monitors Twitter accounts and sends new tweets to designated Discord channels.

## How to Use

To use Disctweet, follow these steps:

1. Fill in the necessary tokens in the `tokens.txt` file in the following order: Discord bot token, Twitter API key, Twitter API secret key, Twitter access token, and Twitter access token secret.
2. In the `users.txt` file, add the users you want to monitor in the following format: `username:channel_id`. For example, `vrilya:123456789`.
3. Run the Python script by typing `python disctweet.py` in the terminal.

## users.txt Format

The `users.txt` file should be formatted as follows:

username1:channel_id1
username2:channel_id2
username3:channel_id3

## tokens.txt Format

The `tokens.txt` file should be formatted as follows:

DISCORD_BOT_TOKEN
TWITTER_API_KEY
TWITTER_API_SECRET_KEY
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET

Make sure to replace each token with your own values.

## Contact

If you have any questions or issues, please feel free to contact on our Discord server at https://discord.gg/nRYSSkfbHD. Thanks for using Disctweet!