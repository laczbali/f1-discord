from discord import guild
from discord.abc import GuildChannel
from discord.channel import TextChannel
import requests
import datetime
from datetime import date
import time
from data import Data
import typing
import discord
from discord import Client
import asyncio

# TODO change next run dates to be json based

# ------------------------------------------------------------------------------

async def post_messages(data: Data, client: Client):
    """
    Task for posting pinned and personalized messages
    It runs on the tuesday of race week, and an hour before & after each event
    """
    # Wait with first run, so the schedule has time to load
    next_run_datetime = datetime.datetime.now() + datetime.timedelta(seconds=10)
    next_run_type = 'week_start'

    while 1:
        if next_run_datetime != None and next_run_datetime <= datetime.datetime.now():
            await _post_messages(data, client, next_run_type)

            # set next run time
            match next_run_type:
                case ('week_start' | 'after_event'):
                    # set next run time to earlier of: before next event, next tuesday
                    nextevent = data.get_next_event()
                    before_next_event = datetime.datetime.fromisoformat(nextevent['date'] + 'T' + nextevent['time'][:-1]) - datetime.timedelta(hours=1)
                    next_tuesday = datetime.datetime.now() + datetime.timedelta(days=8-datetime.datetime.now().weekday())

                    next_run_datetime = min(before_next_event, next_tuesday)
                    next_run_type = 'week_start' if next_tuesday < before_next_event else 'before_event'
                    pass

                case 'before_event':
                    # set next run time to after next event
                    next_run_type = 'after_event'
                    nextevent = data.get_next_event()
                    next_run_datetime = datetime.datetime.fromisoformat(nextevent['date'] + 'T' + nextevent['time'][:-1]) + datetime.timedelta(hours=1)

                case _:
                    # unknown type, set to next Tuesday
                    next_run_datetime = datetime.datetime.now() + datetime.timedelta(days=8-datetime.datetime.now().weekday())
                    next_run_type = 'week_start'                  

        await asyncio.sleep(10)



async def _post_messages(data: Data, client: Client, run_type):
    configs = data.user_config_all
    for conf in configs:
        try:
            server : guild.Guild = client.get_guild(conf['server_id'])
            channel : TextChannel = discord.utils.get(server.text_channels, name=conf['channel'])

            message = ''

            # Message stucture is:
            #   if BEFORE_EVENT or WEEK_START:
            #      No events this week. Next event is: [location] on [date] at [time]
            #      /
            #      This week is: [location] on [date] at [time]
            #      Qualyfing resutls are (if BEFORE EVENT)
            #      1. [driver]
            #      2. [driver]
            #      3. [driver]
            #
            #   all cases:
            #      Results of [event] on [date]:
            #      1. [driver]
            #      2. [driver]
            #      3. [driver]
            #
            #  @alertuser1 @alertuser2 (if BEFORE_EVENT)

            if run_type == 'week_start' or run_type == 'before_event':
                # display next event date and time
                nextevent = data.get_next_event()
                nextevent_date = datetime.datetime.fromisoformat(nextevent['date'] + 'T' + nextevent['time'][:-1])
                if datetime.datetime.now()+datetime.timedelta(days=7) < nextevent_date:
                    message = f"**No events this week.** Next event is {nextevent['raceName']} on {nextevent['date']} at {nextevent['time'][:-4]}\n\n"
                else:
                    message = f"This week is **{nextevent['raceName']}** on **{nextevent['date']}** at **{nextevent['time'][:-4]}**\n\n"
                # display qualifying results
                if run_type == 'before_event':
                    # TODO
                    pass

            # display results of previous event
            # TODO

            await channel.send(message)
            pass
            
        except Exception as e:
            print('error\n'+str(e))
            pass
    pass



# ------------------------------------------------------------------------------

def get_event_schedule(data: Data):
    """
    Task for getting the race schedule from the API
    It runs on every monday
    """
    next_run_datetime = datetime.datetime.now()
    
    while 1:
        if next_run_datetime != None and next_run_datetime <= datetime.datetime.now():
            _get_event_schedule(data)
            # set next run time to next monday
            next_run_datetime = datetime.datetime.now() + datetime.timedelta(days=7-datetime.datetime.now().weekday())

        time.sleep(10)

    

def _get_event_schedule(data: Data):
    """
    Gets the race schedule from the API
    """
    schedule = data.schedule_info

    # HTTP request to API
    try:
        response = requests.get(data.env_data["f1_api"]["base_url"] + data.env_data["f1_api"]["schedule"])
        schedule = response.json()['MRData']['RaceTable']
        schedule['data'] = schedule

        schedule['last_sync_ok'] = True
        schedule['last_successfull_sync'] = date.today().strftime("%Y-%m-%d")

        data.schedule_info = schedule
    except Exception as e:
        #TODO log error
        print("Error getting event schedule\n" + str(e))
        schedule['last_sync_ok'] = False


# ------------------------------------------------------------------------------

def get_race_results():
    pass



def _get_race_results():
    pass



# ------------------------------------------------------------------------------

def get_driver_standings():
    pass



def _get_driver_standings():
    pass