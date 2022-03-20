import datetime
import json
import time
from helpers import Helpers
import requests


def task_get_schedule():
    # guaranteed run at startup
    Helpers.set_task_next_run(
        task_name='get_event_schedule',
        next_run=datetime.datetime.now()
    )

    while 1:
        next_run_datetime = Helpers.get_task_next_run('get_event_schedule')

        if next_run_datetime != None and next_run_datetime <= datetime.datetime.now():
            _get_schedule()            

            # set next run time to next monday
            next_run_datetime = datetime.datetime.now() + datetime.timedelta(days=7-datetime.datetime.now().weekday())
            Helpers.set_task_next_run(
                task_name='get_event_schedule',
                next_run=next_run_datetime
            )

        time.sleep(10)

def _get_schedule():
    try:
        request_url = Helpers.get_env_var("api_base_url") + Helpers.get_env_var("api_schedule_endpoint")
        response = requests.get(request_url)
        schedule = response.json()['MRData']['RaceTable']["Races"]

        with open("schedule.json", "w") as f:
            json.dump(schedule, f)

    except:
        print("Error with getting the schedule")
        pass