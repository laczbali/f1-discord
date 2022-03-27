from threading import Thread
from client_wrapper import ClientWrapper
from tasks.get_schedule import task_get_schedule
from tasks.race_reminder import task_race_reminder

# TODO: stream_url, timezone and reminder_hours_before_event should be user configs, instead of env vars
# TODO: query and post quali results, after they are available
# TODO: only force-update the guild that has its channel changed
# TODO: get next event should convert the datetime by default
# TODO: ability to query previous race results
# TODO: ability to query driver / constructor standings

def main():
    # set up tasks
    Thread(target=task_get_schedule, name="get_schedule", daemon=True).start()
    # bot-related tasks need to be handled by the bot itself
    ClientWrapper.client.loop.create_task(task_race_reminder(ClientWrapper.client))

    # BLOCK CALL, start the discord bot
    ClientWrapper.run()

if __name__ == "__main__":
    main()