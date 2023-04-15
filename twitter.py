import tweepy
import discord
from discord.ext import commands, tasks
import asyncio

# Twitter API credentials
TWITTER_API_KEY = 'your_twitter_api_key'
TWITTER_API_SECRET_KEY = 'your_twitter_api_secret_key'
TWITTER_ACCESS_TOKEN = 'your_twitter_access_token'
TWITTER_ACCESS_TOKEN_SECRET = 'your_twitter_access_token_secret'

# Discord bot token
DISCORD_BOT_TOKEN = 'your_discord_bot_token'

# Twitter accounts to watch
tech_accounts = ['elonmusk', 'sundarpichai', 'tim_cook', 'satyanadella', 'jeffbezos', 'sherylsandberg', 'jack', 'ericschmidt', 'reidhoffman', 'ev']
ai_accounts = ['ylecun', 'goodfellow_ian', 'karpathy', 'AndrewYNg', 'drfeifei']
cloud_accounts = ['awscloud', 'Azure', 'GCPcloud']

watched_accounts = tech_accounts + ai_accounts + cloud_accounts

# Set up Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Set up Discord bot
bot = commands.Bot(command_prefix='!')

async def get_latest_tweet(screen_name):
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=1, tweet_mode='extended')
        return tweets[0].full_text
    except Exception as e:
        print(e)
        return None

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    tweet_watcher.start()

@tasks.loop(minutes=5.0)
async def tweet_watcher():
    channel = discord.utils.get(bot.get_all_channels(), name='tweets')
    if channel:
        for account in watched_accounts:
            tweet = await get_latest_tweet(account)
            if tweet:
                await channel.send(f'**{account}** just tweeted:\n{tweet}')
            await asyncio.sleep(1)

# Run the bot
bot.run(DISCORD_BOT_TOKEN)
