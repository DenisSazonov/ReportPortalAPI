import os
import json
import time

class Data:
    BASE_URL = 'https://web.demo.reportportal.io'
    BASE_API_PATH = BASE_URL + '/api/v1/'
    basic_authorization_header = {"authorization": "Basic dWk6dWltYW4="}

    @staticmethod
    def read_credentials():
        current_dir = os.path.abspath(os.path.dirname(__file__))
        with open(current_dir + '\credentials.json', 'r') as f:
            credentials = json.load(f)
        user_name = (credentials['user']['user_name'])
        password = (credentials['user']['password'])
        auth_string = f'/uat/sso/oauth/token?grant_type=password&password={password}&username={user_name}'
        return auth_string

    @staticmethod
    def json_for_create_dashboard():
        json_for_create_dashboard = {
            "description": "My dashboard created at " + str(time.time()),
            "name": "New dashboard created at " + str(time.time()),
            "share": "true"
        }
        return json_for_create_dashboard
