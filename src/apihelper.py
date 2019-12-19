import requests
from src.data import Data


class ApiHelper:

    def authentification(self):
        auth_path = Data.read_credentials()
        login_url = Data.BASE_URL + auth_path[0]
        response = requests.post(login_url, headers=Data.basic_authorization_header)
        body = response.json()
        authorization_header = {'authorization': 'bearer ' + body['access_token']}
        return authorization_header

    def authentification_with_new_password(self):
        auth_path = Data.read_credentials()
        login_url = Data.BASE_URL + auth_path[3]
        response = requests.post(login_url, headers=Data.basic_authorization_header)
        body = response.json()
        authorization_header = {'authorization': 'bearer ' + body['access_token']}
        return authorization_header

    def get_user_info(self, *args):
        content = []
        if not args:
            response = requests.get(Data.BASE_API_PATH + 'user', headers=ApiHelper.authentification(self))
        else:
            response = requests.get(Data.BASE_API_PATH + 'user/' + args[0], headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        json = response.json()
        content.append(json)
        return content

    def get_project_name(self):
        content = ApiHelper.get_user_info(self)
        json = content[1]
        project = json['default_project']
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

    def get_specified_dashboard_for_project(self, new_dashboard_id):
        content = []
        project = ApiHelper.get_project_name(self)
        dashboard_url = Data.BASE_API_PATH + project + '/dashboard/' + new_dashboard_id
        response = requests.get(dashboard_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    def update_dashboard(self, dashboard_id):
        content = []
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard/' + dashboard_id
        response = requests.put(project_url, headers=ApiHelper.authentification(self),
                                json=Data.json_for_update_dashboard())
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
        activity_url = Data.BASE_API_PATH + project + '/activity'
        response = requests.get(activity_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    def upload_photo(self, photo):
        content = []
        data_url = Data.BASE_API_PATH + '/data/photo'
        response = requests.post(data_url, headers=ApiHelper.authentification(self), files=Data.return_photo(photo))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    def get_photo(self):
        data_url = Data.BASE_API_PATH + '/data/photo'
        response = requests.get(data_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        return status_code

    def delete_photo(self):
        content = []
        data_url = Data.BASE_API_PATH + '/data/photo'
        response = requests.delete(data_url, headers=ApiHelper.authentification(self))
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content

    def create_user(self):
        content = []
        user_url = Data.BASE_API_PATH + '/user'
        response = requests.post(user_url, headers=ApiHelper.authentification(self), json=Data.json_for_create_user())
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        content.append(Data.json_for_create_user())
        return content

    def change_password(self):
        content = []
        user_url = Data.BASE_API_PATH + '/user/password/change'
        json = Data.json_for_update_password(Data.read_credentials()[2], Data.read_credentials()[1])
        response = requests.post(user_url, headers=ApiHelper.authentification(self), json=json)
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        content.append(Data.json_for_create_user())
        return content

    def revert_password(self):
        user_url = Data.BASE_API_PATH + '/user/password/change'
        json = Data.json_for_update_password(Data.read_credentials()[1], Data.read_credentials()[2])
        response = requests.post(user_url, headers=ApiHelper.authentification_with_new_password(self), json=json)
        status_code = response.status_code
        return status_code

    def edit_user(self):
        pass
        # needs to create new project
