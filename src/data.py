import os
import json
import time


class Data:
    BASE_URL = 'http://10.20.12.203:8080'
    BASE_API_PATH = BASE_URL + '/api/v1/'
    basic_authorization_header = {"authorization": "Basic dWk6dWltYW4="}

    @staticmethod
    def read_credentials():
        current_dir = os.path.abspath(os.path.dirname(__file__))
        with open(current_dir + '\credentials.json', 'r') as f:
            credentials = json.load(f)
        user_name = (credentials['user']['user_name'])
        password = (credentials['user']['password'])
        new_password = (credentials['user']['new_password'])
        admin_name = (credentials['superadmin']['user_name'])
        admin_password = (credentials['superadmin']['password'])
        auth_string = f'/uat/sso/oauth/token?grant_type=password&password={password}&username={user_name}'
        auth_string_after_password_changing = f'/uat/sso/oauth/token?grant_type=password&password={new_password}&username={user_name}'
        auth_string_for_admin = f'/uat/sso/oauth/token?grant_type=password&password={admin_password}&username={admin_name}'
        return auth_string, password, new_password, auth_string_after_password_changing, auth_string_for_admin

    @staticmethod
    def json_for_create_dashboard():
        json_for_create_dashboard = {
            "description": "My dashboard created at " + str(time.time()),
            "name": "New dashboard created at " + str(time.time()),
            "share": "true"
        }
        return json_for_create_dashboard

    @staticmethod
    def json_for_update_dashboard():
        json_for_update_dashboard = {
            "description": "My dashboard updated at " + str(time.time()),
            "name": "New dashboard updated at " + str(time.time()),
            "share": "true"
        }
        return json_for_update_dashboard

    @staticmethod
    def return_photo(photo):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        file = {'file': open(current_dir + photo, 'rb')}
        return file

    @staticmethod
    def json_for_create_user(*args):
        if args:
            args = args[0]
            json_for_create_user = {
                "accountRole": "USER",
                "default_project": "default_personal",
                "email": str(time.time()) + "@mail.com",
                "full_name": "Full Name",
                "login": args[0],
                "password": "default_password",
                "projectRole": "CUSTOMER"
            }
        else:
            json_for_create_user = {
                "accountRole": "USER",
                "default_project": "default_personal",
                "email": str(time.time()) + "@mail.com",
                "full_name": "Full Name",
                "login": "login" + str(time.time()),
                "password": "default_password",
                "projectRole": "CUSTOMER"
            }
        return json_for_create_user

    @staticmethod
    def json_for_update_password(new_password, old_password):
        json_for_update_password = {
            "newPassword": new_password,
            "oldPassword": old_password
        }
        return json_for_update_password

    @staticmethod
    def json_for_create_new_project():
        timestamp = str(time.time()).replace('.', '')
        json_for_create = {
            "addInfo": "Some information about project",
            "customer": "Test customer",
            "entryType": "INTERNAL",
            "projectName": "project_created_at_" + timestamp
        }
        return json_for_create

    @staticmethod
    def no_permissions_json():
        json = {
            "error_code": 4003,
            "message": "You do not have enough permissions. Access is denied"
        }
        return json

    @staticmethod
    def json_for_update_project():
        json = {"addInfo": "Updated_project"}
        return json

    @staticmethod
    def json_for_assign_user(login):
        json = {"userNames": {login: "MEMBER"}}
        return json
