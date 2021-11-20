import json


# -----------------------------------------------------------------------------

env_file = open("env.json", "r")
env_data = json.load(env_file)

# -----------------------------------------------------------------------------

schedule_info = {
    'data': None,
    'last_successfull_sync': None,
    'last_sync_ok' : None
}