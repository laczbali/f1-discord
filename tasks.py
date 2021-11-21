import requests
import datetime
from datetime import date
import time
from data import Data
import typing

# TODO change next run dates to be json based

# ------------------------------------------------------------------------------

def post_messages(data: Data):
    """
    Task for posting pinned and personalized messages
    It runs on the tuesday of race week, and an hour before & after each event
    """
    # Wait with first run, so the schedule has time to load
    next_run_datetime = datetime.datetime.now() + datetime.timedelta(minutes=1)
    next_run_type = 'week_start'

    while 1:
        if next_run_datetime != None and next_run_datetime <= datetime.datetime.now():
            _post_messages(next_run_type)

            # set next run time
            match next_run_type:
                case ('week_start' | 'after_event'):
                    # set next run time to earlier of: before next event, next tuesday
                    nextevent = data.get_next_event()
                    pass

                case 'before_event':
                    # set next run time to after next event
                    next_run_type = 'after_event'

                case _:
                    # unknown type, set to next Tuesday
                    next_run_datetime = datetime.datetime.now() + datetime.timedelta(days=8-datetime.datetime.now().weekday())
                    next_run_type = 'week_start'                  

        time.sleep(10)



def _post_messages(run_type):
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