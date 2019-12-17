import requests
from src.data import Data


class ApiHelper:

    def authentification(self):
        LOGIN_URL = Data.BASE_URL + Data.read_credentials()
        response = requests.post(LOGIN_URL, headers=Data.basic_authorization_header)
        body = response.json()
        authorization_header = {'authorization': 'bearer ' + body['access_token']}
        return authorization_header

    def get_user_info(self):
        response = requests.get(Data.BASE_API_PATH + 'user', headers=ApiHelper.authentification(self))
        body = response.json()
        return body

    def get_project_name(self):
        body = ApiHelper.get_user_info(self)
        project = body['default_project']
        return project

    def get_dashboards(self):
        content = []
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard'
        response = requests.get(project_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        response = response[0]
        content.append(response)
        return content

    def get_dashboard_id(self):
        dashboard = ApiHelper.get_dashboards(self)
        json = dashboard[1]
        dashboard_id = json['id']
        return dashboard_id

    def create_new_dashboard(self):
        content = []
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard'
        response = requests.post(project_url, headers=ApiHelper.authentification(self),
                                 json=Data.json_for_create_dashboard())
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    def get_shared_dashboards(self):
        content = []
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard/shared'
        response = requests.get(project_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    def delete_dashboard(self, new_dashboard_id):
        content = []
        project = ApiHelper.get_project_name(self)
        dashboard_url = Data.BASE_API_PATH + project + '/dashboard/' + new_dashboard_id
        response = requests.delete(dashboard_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    @staticmethod
    def return_status_code(content):
        status_code = content[0]
        return status_code

    @staticmethod
    def return_json_from_list(content):
        json_response = content[1]
        json = json_response["content"]
        json = json[-1]
        json = json["id"]
        return json

    def get_activities(self):
        content = []
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/activity'
        response = requests.get(project_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

# print(ApiHelper.get_user_info())

# response = ApiHelper()
