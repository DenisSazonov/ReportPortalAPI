from .data import Data
import requests


class Authorization(Data):
    def __init__(self):
        self.auth_path = Data.read_credentials()

    def authentification(self):
        login_url = Data.BASE_URL + self.auth_path[0]
        response = requests.post(login_url, headers=Data.basic_authorization_header)
        body = response.json()
        authorization_header = {'authorization': 'bearer ' + body['access_token']}
        return authorization_header

    def authentification_with_new_password(self):
        login_url = Data.BASE_URL + self.auth_path[3]
        response = requests.post(login_url, headers=Data.basic_authorization_header)
        body = response.json()
        authorization_header = {'authorization': 'bearer ' + body['access_token']}
        return authorization_header

    def authentification_with_admin_role(self):
        login_url = Data.BASE_URL + self.auth_path[4]
        response = requests.post(login_url, headers=Data.basic_authorization_header)
        body = response.json()
        authorization_header = {'authorization': 'bearer ' + body['access_token']}
        return authorization_header
