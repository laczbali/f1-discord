import discord

from helpers import Helpers

class ClientWrapper:

    client = discord.Client()

    @client.event
    async def on_ready():
        await ClientWrapper.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/F1"))
        print(f'Client is ready')

    @client.event
    async def on_message(message):
        try:
            
            # Ignore messages from self
            if message.author == ClientWrapper.client.user:
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
                        "**/f1 about** - Show information about the bot \n"
                        "**/f1 config [setting] [value]** - Configure the bot \n"
                        "\t The **setting** can be: \n"
                        "\t   *channel* - Which channel should the bot send the schedule to \n"
                        "**/f1 next** - Show the next upcoming race \n"
                    )

                case 'about':
                    await message.channel.send("https://github.com/laczbali/f1-discord")

                case 'config':
                    if len(content_arr) < 3:
                        await message.channel.send('Please provide a setting and a value')
                        return

                    if content_arr[1] not in ['channel', 'stream-url', 'alert', 'drivers']:
                        await message.channel.send('Please provide a valid setting')
                        return

                    Helpers.update_user_config(message.guild.id, content_arr[1], content_arr[2])
                    await message.channel.send('Saved')

                    if content_arr[1] == 'channel':
                        # Channel changed, update it right away
                        Helpers.force_race_reminder()

                case 'next':
                    next_event = Helpers.get_next_event()
                    next_event_datetime = Helpers.get_event_utc_datetime(next_event)
                    message = f"The next race is **{next_event['raceName']}** on **{next_event_datetime.date()}** at **{next_event_datetime.time()}**"
                    await message.channel.send(message)

                case _:
                    await message.channel.send("Unknown command, type **/f1 help** for more information.")

        except:
            await message.channel.send("Something went wrong")
        
    def run():
        ClientWrapper.client.run(Helpers.get_env_var('bot_token'))