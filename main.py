import discord
import json

# Load ENV variables
env_file = open("env.json", "r")
env_data = json.load(env_file)

# Load Discord client
client = discord.Client()

# Set up events
@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/f1'):
        await message.channel.send('Hello there')

# Run bot
client.run(env_data["auth"]["bot_token"])