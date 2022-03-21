# f1-bot

## Purpose
- Gets the [schedule](https://ergast.com/api/f1/2022.json) for the current F1 season from [ergast](http://ergast.com/mrd/)  
- In a message, on a selected channel, it displays the time and place of the next event

## Usage
- [Set up a Discord bot](https://discord.com/developers/applications)
- Invite the bot to a server (you can invite it to multiple). Bot should have permission to:
  - Send messages
  - Read messages
- Clone repo
- Create env.json in the root folder
- Use the env.schema.json file as a schema for env.json
- Fill out env.json
- Start main.py
- Configure which channel the bot should post in, by calling `/F1 config channel YOUR_CHANNEL_NAME`