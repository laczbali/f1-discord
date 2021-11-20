import requests
import datetime
from datetime import date
import data
import time



# ------------------------------------------------------------------------------

def post_messages():
    pass



def _post_messages():
    pass


# ------------------------------------------------------------------------------

def get_event_schedule():
    """
    Task for getting the race schedule from the API
    It runs immediately after the startup, and then on every monday
    """
    next_run_datetime = datetime.datetime.now()
    
    while 1:
        if next_run_datetime != None and next_run_datetime <= datetime.datetime.now():
            _get_event_schedule()
            # set next run time to next monday
            next_run_datetime = datetime.datetime.now() + datetime.timedelta(days=7-datetime.datetime.now().weekday())

        time.sleep(10)

    

def _get_event_schedule():
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