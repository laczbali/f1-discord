import discord
import sys
import threading
from threading import Thread
import tasks, data

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
        content = message.content.replace('/F1 ', '')
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
                    "\t   *pin* - Should the bot pin the message (true or false) \n"
                    "\t   *stream-url* - The url where the race can be streamed \n"
                    "\t   *alert* - Users to alert about upcoming events (eg: user1,user2) \n"
                    "\t   *drivers* - List of drivers-of-interest (eg: BOT,PER) \n"
                "**/f1 status** - Provides the status of the synced data"
                )

            case 'about':
                await message.channel.send('made by **blaczko#0134**')
        
            case 'config':
                # TODO parse and save config
                await message.channel.send('Saved')

            case 'status':
                # TODO should return a more general status (eg other tasks, uptime, config values)
                await message.channel.send(
                    'Last sync status: **' +  ("OK" if data.schedule_info['last_sync_ok'] else "FAIL") + '**\n'
                    'Last succesful sync: **' + str(data.schedule_info['last_successfull_sync']) + "**"
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

    client.run(data.env_data["auth"]["bot_token"])



def init_scheduling():
    """
    Starts the scheduling process, which will periodically get the data from the API, and run relevant functions
    """
    
    Thread(target=tasks.get_event_schedule, name="EventSchedule", daemon=True).start()
    Thread(target=tasks.get_driver_standings, name="DriverStandings", daemon=True).start()
    Thread(target=tasks.get_race_results, name="RaceResults", daemon=True).start()
    Thread(target=tasks.post_messages, name="PostMessages", daemon=True).start()



# -----------------------------------------------------------------------------

if __name__ == "__main__":
    #TODO load server-config
    init_scheduling()
    run()