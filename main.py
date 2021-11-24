import discord
import sys
from threading import Thread
import tasks, data
import asyncio

if sys.version_info < (3, 10):
    print('Please upgrade your Python version to 3.10 or higher')
    sys.exit()



# -----------------------------------------------------------------------------

# Load Discord client
client = discord.Client()


# Bot is logged-in
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/F1"))
    print(f'Client is ready')
    init_scheduling()



# Handle new messages on server
@client.event
async def on_message(message):
    try:

        # Ignore messages from self
        if message.author == client.user:
            return

        # Ignore messages not to the bot
        if not (message.content.startswith('/f1') or message.content.startswith('/F1')):
            return

        # First pass of message parsing
        content = message.content.replace('/f1 ', '')
        content = content.replace('/F1 ', '')
        content_arr = content.split(' ')
        command = content_arr[0]

        # Handle commands
        match command:
            case 'help':
                await message.channel.send(
                "**/f1 help** - Show this help message \n"
                "**/f1 about** - Show information about the bot \n"
                "**/f1 config [setting] [value]** - Configure the bot \n"
                    "\t The **setting** can be: \n"
                    "\t   *channel* - Which channel should the bot send the schedule to \n"
                    "\t   *stream-url* - The url where the race can be streamed \n"
                    "\t   *drivers* - List of drivers-of-interest (eg: BOT,PER) \n"
                "**/f1 current-config** - Shows the currently saved configuration"
                "**/f1 status** - Provides the status of the synced data"
                )

            case 'about':
                await message.channel.send(
                    "made by **blaczko**\n"
                    "https://github.com/laczbali/f1-discord"
                )
        
            case 'config':
                if len(content_arr) < 3:
                    await message.channel.send('Please provide a setting and a value')
                    return

                if content_arr[1] not in ['channel', 'stream-url', 'alert', 'drivers']:
                    await message.channel.send('Please provide a valid setting')
                    return

                data_cont.update_server_config(message.guild.id, content_arr[1], content_arr[2])
                await message.channel.send('Saved')

            case 'current-config':
                current_config = data_cont.get_server_config(message.guild.id)
                await message.channel.send(current_config if current_config else 'No configuration found')
            
            case 'status':
                # TODO should return a more general status (eg other tasks, uptime, config values)
                await message.channel.send(
                    'Last sync status: **' +  ("OK" if data_cont.schedule_info['last_sync_ok'] else "FAIL") + '**\n'
                    'Last succesful sync: **' + str(data_cont.schedule_info['last_successfull_sync']) + "**"
                )

            case _:
                await message.channel.send('Unknown command. Type **/f1 help** for more information.')

    except Exception as e:
        #TODO log error
        print("Error handling message\n" + str(e))
        await message.channel.send('Something went wrong :worried:\n')


# -----------------------------------------------------------------------------

def run():
    """
    Runs the discord client
    """

    client.run(data_cont.env_data["auth"]["bot_token"])



def init_scheduling():
    """
    Starts the scheduling process, which will periodically get the data from the API, and run relevant functions
    """
    Thread(target=tasks.get_event_schedule, name="EventSchedule", daemon=True, args=[data_cont]).start()
    Thread(target=tasks.get_driver_standings, name="DriverStandings", daemon=True).start()
    Thread(target=tasks.get_race_results, name="RaceResults", daemon=True).start()
    
    client.loop.create_task(tasks.post_messages(data_cont, client))



# -----------------------------------------------------------------------------

data_cont = data.Data()

if __name__ == "__main__":
    run()