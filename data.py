import json

class Data():

    # -----------------------------------------------------------------------------

    env_file = open("env.json", "r")
    env_data = json.load(env_file)

    # -----------------------------------------------------------------------------

    schedule_info = {
        'data': None,
        'last_successfull_sync': None,
        'last_sync_ok' : None
    }

    # -----------------------------------------------------------------------------

    user_configfile = open("user_config.json", "r")
    user_config_all = json.load(user_configfile)

    def get_server_config(self, server_id):
        try:
            return list(filter(lambda x: x['server_id'] == server_id, self.user_config_all))[0]
        except:
            return None


    def set_server_config(self, server_id, config):
        # filter out server from list
        new_config_list = list(filter(lambda x: x['server_id'] != server_id, self.user_config_all))
        # add new server config
        new_config_list.append(config)
        # write new config to file
        with open("user_config.json", "w") as f:
            json.dump(new_config_list, f)
        # update config in memory
        self.user_config_all = new_config_list


    def update_server_config(self, server_id, key, value):
        config = self.get_server_config(server_id)

        if config is None:
            config = { 'server_id': server_id }

        config[key] = value
        self.set_server_config(server_id, config)