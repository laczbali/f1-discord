import discord
import json
import sys
import requests
from datetime import date

if sys.version_info < (3, 10):
    print('Please upgrade your Python version to 3.10 or higher')
    sys.exit()

# Load ENV variables
env_file = open("env.json", "r")
env_data = json.load(env_file)

# Load Discord client
client = discord.Client()

# Init schedule objects
schedule_info = {
    'data': None,
    'last_successfull_sync': None,
    'last_sync_ok' : None
}

# -----------------------------------------------------------------------------

@client.event
async def on_ready():
    print(f'Client is ready')

@client.event
async def on_message(message):
    try:

        if message.author == client.user:
            return

        if not message.content.startswith('/f1'):
            return

        content = message.content.replace('/f1 ', '')
        content_arr = content.split(' ')
        command = content_arr[0]

        match command:
            case 'help':
                await message.channel.send(
                "**/f1 help** - Show this help message \n"
                "**/f1 about** - Show information about the bot \n"
                "**/f1 config [* channel] [* pin] [stream-url]** - Configure the bot \n"
                    "\t * channel - Which channel should the bot send the schedule to \n"
                    "\t * pin - true\\false - Should the bot pin the message \n"
                    "\t stream-url - The url where the race can be streamed \n"
                "**/f1 status** - Provides the status of the synced data"
                )

            case 'about':
                await message.channel.send('made by **blaczko#0134**')
        
            case 'config':
                if len(content_arr) < 3:
                    await message.channel.send('Please provide all necessary parameters. See **/f1 help** for more information**')
                    return

                channel_to_use = content_arr[1]
                should_pin = (content_arr[2] == 'True' or content_arr[2] == 'true')
                stream_url = None

                if len(content_arr) > 3:
                    stream_url = content_arr[3]

                # TODO save config

                await message.channel.send('Config saved')

            case 'status':
                await message.channel.send(
                    'Last sync status: **' +  ("OK" if schedule_info['last_sync_ok'] else "FAIL") + '**\n'
                    'Last succesful sync: **' + str(schedule_info['last_successfull_sync']) + "**"
                )

            case _:
                await message.channel.send('Unknown command. Type **/f1 help** for more information.')

    except Exception as e:
        #TODO log error
        await message.channel.send('Something went wrong :worried:\n')

# -----------------------------------------------------------------------------

# Runs the discord client
def run():
    client.run(env_data["auth"]["bot_token"])

# Gets the schedule from the API
def get_schedule():
    # HTTP request to API
    try:
        response = requests.get(env_data["f1_api"]["base_url"] + env_data["f1_api"]["schedule"])
        schedule = response.json()['MRData']['RaceTable'].asd
        schedule_info['data'] = schedule

        schedule_info['last_sync_ok'] = True
        schedule_info['last_successfull_sync'] = date.today().strftime("%Y-%m-%d")
    except Exception as e:
        #TODO log error
        schedule_info['last_sync_ok'] = False
        return None

# Periodically gets the data from the API & posts messages
def init_scheduling():
    #TODO implement
    pass

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    get_schedule()
    init_scheduling()
    run()