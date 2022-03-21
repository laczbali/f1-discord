from threading import Thread
from client_wrapper import ClientWrapper
from tasks.get_schedule import task_get_schedule
from tasks.race_reminder import task_race_reminder

def main():
    # set up tasks
    Thread(target=task_get_schedule, name="get_schedule", daemon=True).start()
    # bot-related tasks need to be handled by the bot itself
    ClientWrapper.client.loop.create_task(task_race_reminder(ClientWrapper.client))

    # BLOCK CALL, start the discord bot
    ClientWrapper.run()

if __name__ == "__main__":
    main()