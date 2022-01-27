from datetime import datetime
import json

class Data():

    # -----------------------------------------------------------------------------

    def get_env_variable(self, key):
        env_file = open("env.json", "r")
        env_data = json.load(env_file)
        env_file.close()

        try:
            return env_data[key]
        except:
            return None


    # -----------------------------------------------------------------------------

    schedule_info = {
        'data': None,
        'last_successfull_sync': None,
        'last_sync_ok' : None
    }

    def get_next_event(self):
        try:
            events = self.schedule_info['data']['Races']
            # filter out past events
            upcoming = list(filter(lambda e: datetime.fromisoformat(e['date'] + 'T' + e['time'][:-1]) >= datetime.now(), events))
            return upcoming[0] if len(upcoming) > 1 else None
        except:
            return None

    # -----------------------------------------------------------------------------

    user_configfile = open("user_config.json", "r")
    user_config_all = json.load(user_configfile)

    def get_user_config(self, server_id):
        try:
            return list(filter(lambda x: x['server_id'] == server_id, self.user_config_all))[0]
        except:
            return None


    def set_user_config(self, server_id, config):
        # filter out server from list
        new_config_list = list(filter(lambda x: x['server_id'] != server_id, self.user_config_all))
        # add new server config
        new_config_list.append(config)
        # write new config to file
        with open("user_config.json", "w") as f:
            json.dump(new_config_list, f)
        # update config in memory
        self.user_config_all = new_config_list


    def update_user_config(self, server_id, key, value):
        config = self.get_user_config(server_id)

        if config is None:
            config = { 'server_id': server_id }

        config[key] = value
        self.set_user_config(server_id, config)

    # -----------------------------------------------------------------------------

    try:
        task_file = open("tasks.json", "r")
        task_file.close()
    except FileNotFoundError:
        with open("tasks.json", "w") as f:
            json.dump({}, f)


    def get_task_next_run(self, task_name):
        task_file = open("tasks.json", "r")
        task_data = json.load(task_file)
        task_file.close()

        try:
            return datetime.fromisoformat(task_data[task_name]['next_run'])
        except:
            return None


    def get_task_arg(self, task_name, arg_name):
        task_file = open("tasks.json", "r")
        task_data = json.load(task_file)
        task_file.close()

        try:
            return task_data[task_name]['args'][arg_name]
        except:
            return None


    def set_task_next_run(self, task_name, next_run, args={}):
        task_file = open("tasks.json", "r")
        task_data = json.load(task_file)
        task_file.close()

        task_data[task_name] = { 'next_run': next_run.isoformat(), 'args': args }

        with open("tasks.json", "w") as f:
            json.dump(task_data, f)


    def force_task_next_run(self, task_name):
        task_file = open("tasks.json", "r")
        task_data = json.load(task_file)
        task_file.close()

        task_data[task_name]['next_run'] = datetime.now().isoformat()

        with open("tasks.json", "w") as f:
            json.dump(task_data, f)