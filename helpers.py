import datetime
from dateutil import tz
import json

class Helpers:

    def get_env_var(key):
        env_file = open("env.json", "r")
        env_data = json.load(env_file)
        env_file.close()

        try:
            return env_data[key]
        except:
            print("Error with getting the environment variable")
            return None

    def set_task_next_run(task_name, next_run, args={}):
        try:
            task_file = open("tasks.json", "r")
            task_data = json.load(task_file)
            task_file.close()
        except:
            task_data = {}

        task_data[task_name] = { 'next_run': next_run.isoformat(), 'args': args }

        with open("tasks.json", "w") as f:
            json.dump(task_data, f)

    def get_task_next_run(task_name):
        task_file = open("tasks.json", "r")
        task_data = json.load(task_file)
        task_file.close()

        try:
            return datetime.datetime.fromisoformat(task_data[task_name]['next_run'])
        except:
            return None

    def get_next_event():
        try:
            events = json.load(open("schedule.json", "r"))
            # filter out past events
            upcoming = list(
                filter(lambda e:
                    Helpers.get_event_utc_datetime(e) >= datetime.datetime.now(), events
                )
            )
            return upcoming[0] if len(upcoming) > 1 else None
        except:
            return None

    def get_event_utc_datetime(event, adjust_timezone=True, as_naive=True):
        event_datetime = datetime.datetime.fromisoformat(event['date'] + 'T' + event['time'][:-1])
        if adjust_timezone:
            event_datetime = Helpers.adjust_date_timezone(event_datetime)
        if as_naive:
            ev_date = event_datetime.isoformat().split("T")[0]
            ev_time = event_datetime.isoformat().split("T")[1].replace("-","+").split("+")[0]
            # ev_offset_h = event_datetime.isoformat().split("T")[1].replace("-","+").split("+")[1].split(":")[0]
            # ev_offset_m = event_datetime.isoformat().split("T")[1].replace("-","+").split("+")[1].split(":")[1]
            event_datetime = datetime.datetime.fromisoformat(f"{ev_date}T{ev_time}") #+datetime.timedelta(hours=int(ev_offset_h), minutes=int(ev_offset_m))
        return event_datetime

    def adjust_date_timezone(base_date_time):
        base_date_time = base_date_time.replace(tzinfo=tz.gettz('UTC'))
        target_time_zone = tz.gettz(Helpers.get_env_var('timezone'))
        adjusted_datetime = base_date_time.astimezone(target_time_zone)
        return adjusted_datetime

    def update_user_config(server_id, key, value):
        config = Helpers.get_user_config(server_id)

        if config is None:
            config = { 'server_id': server_id }

        config[key] = value
        Helpers.set_user_config(server_id, config)

    def get_user_config(server_id):
        try:
            configfile = open("user_config.json", "r")
            user_config_all = json.load(configfile)
            configfile.close()
            return list(filter(lambda x: x['server_id'] == server_id, user_config_all))[0]
        except:
            return None

    def set_user_config(server_id, config):
        try:
            configfile = open("user_config.json", "r")
            user_config_all = json.load(configfile)
            configfile.close()
        except:
            user_config_all = []

        # filter out server from list
        new_config_list = list(filter(lambda x: x['server_id'] != server_id, user_config_all))
        # add new server config
        new_config_list.append(config)
        # write new config to file
        with open("user_config.json", "w") as f:
            json.dump(new_config_list, f)

    def force_race_reminder():
        task_file = open("tasks.json", "r")
        task_data = json.load(task_file)
        task_file.close()

        task_data["race_reminder"]['next_run'] = datetime.datetime.now().isoformat()

        with open("tasks.json", "w") as f:
            json.dump(task_data, f)