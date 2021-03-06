import asyncio
import datetime
import json
from dateutil import tz
import discord
from discord import Client
from discord import guild
from discord.channel import TextChannel

from helpers import Helpers

async def task_race_reminder(client: Client):
    """
    Posts a message about upcoming races.

    Runs every tuesday, and a few hours before every race.
    """

    # Wait with first run, so the schedule has time to load
    await asyncio.sleep(5)

    # guaranteed run at startup
    Helpers.set_task_next_run(
        'race_reminder',
        next_run = datetime.datetime.now()
    )

    while 1:
        next_run_datetime = Helpers.get_task_next_run('race_reminder')

        if next_run_datetime != None and next_run_datetime <= datetime.datetime.now():
            next_event = Helpers.get_next_event()

            await _race_remidner(client, next_event)

            # set next status to earlier of: next tuesday, next sunday (before the next event)
            before_next_event = Helpers.get_event_utc_datetime(next_event) - datetime.timedelta(hours=Helpers.get_env_var("reminder_hours_before_event"))
            next_tuesday = datetime.datetime.now() + datetime.timedelta(days=(7 - datetime.datetime.now().weekday()) % 7 + 1)

            if before_next_event < datetime.datetime.now():
                next_run_datetime = next_tuesday
            else:
                next_run_datetime = min(before_next_event, next_tuesday)
                
            Helpers.set_task_next_run(
                task_name='race_reminder',
                next_run=next_run_datetime
            )
            
        await asyncio.sleep(10)

async def _race_remidner(client: Client, next_event):
    try:
        configfile = open("user_config.json", "r")
        configs = json.load(configfile)
        configfile.close()

        # if the bot is configured for multiple servers, itarate through them
        for conf in configs:
            server : guild.Guild = client.get_guild(conf['server_id'])
            channel : TextChannel = discord.utils.get(server.text_channels, name=conf['channel'])

            next_event_date = Helpers.get_event_utc_datetime(next_event)

            if datetime.datetime.now()+datetime.timedelta(days=7) < next_event_date:
                # no events in the next 7 days
                message = f"**No events this week.** Next event is {next_event['raceName']} on {next_event_date.date()} at {next_event_date.time()}\n\n"
            else:
                # there is an event in the next 7 days
                message = f"This week is **{next_event['raceName']}** on **{next_event_date.date()}** at **{next_event_date.time()}**\n\n"
                stream_url = Helpers.get_env_var("stream_url")
                message += f"Watch at {stream_url}\n\n"

            await channel.send(message)
        
    except:
        print("error posting message")