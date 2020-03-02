import requests
from src.data import Data
from .authorization import Authorization


class ApiHelper:
    def __init__(self):
        self.user_access_token = Authorization().authentification()
        self.admin_token = Authorization().authentification_with_admin_role()

    def get_current_user_info(self):
        response = requests.get(Data.BASE_API_PATH + 'user', headers=self.user_access_token)
        content = ApiHelper.content(response)
        return content

    def get_info_about_all_users(self, *args):
        if args[0] == 'user':
            response = requests.get(Data.BASE_API_PATH + 'user/all', headers=self.user_access_token)
        elif not args:
            response = requests.get(Data.BASE_API_PATH + 'user/all', headers=self.admin_token)
        else:
            response = requests.get(Data.BASE_API_PATH + 'user/' + args[0],
                                    headers=self.admin_token)
        content = ApiHelper.content(response)
        return content

    def get_project_name(self):
        content = ApiHelper.get_current_user_info(self)
        json = content[1]
        project = json['default_project']
        return project

    def get_dashboards(self):
        content = []
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard'
        response = requests.get(project_url, headers=self.user_access_token)
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
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard'
        response = requests.post(project_url, headers=self.user_access_token,
                                 json=Data.json_for_create_dashboard())
        content = ApiHelper.content(response)
        return content

    def get_shared_dashboards(self):
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard/shared'
        response = requests.get(project_url, headers=self.user_access_token)
        content = ApiHelper.content(response)
        return content

    def delete_dashboard(self, new_dashboard_id):
        project = ApiHelper.get_project_name(self)
        dashboard_url = Data.BASE_API_PATH + project + '/dashboard/' + new_dashboard_id
        response = requests.delete(dashboard_url, headers=self.user_access_token)
        content = ApiHelper.content(response)
        return content

    def get_specified_dashboard_for_project(self, new_dashboard_id):
        project = ApiHelper.get_project_name(self)
        dashboard_url = Data.BASE_API_PATH + project + '/dashboard/' + new_dashboard_id
        response = requests.get(dashboard_url, headers=self.user_access_token)
        content = ApiHelper.content(response)
        return content

    def update_dashboard(self, dashboard_id):
        project = ApiHelper.get_project_name(self)
        project_url = Data.BASE_API_PATH + project + '/dashboard/' + dashboard_id
        response = requests.put(project_url, headers=self.user_access_token,
                                json=Data.json_for_update_dashboard())
        content = ApiHelper.content(response)
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
        project = ApiHelper.get_project_name(self)
        activity_url = Data.BASE_API_PATH + project + '/activity'
        response = requests.get(activity_url, headers=self.user_access_token)
        content = ApiHelper.content(response)
        return content

    def upload_photo(self, photo):
        data_url = Data.BASE_API_PATH + '/data/photo'
        response = requests.post(data_url, headers=self.user_access_token,
                                 files=Data.return_photo(photo))
        content = ApiHelper.content(response)
        return content

    def get_photo(self):
        data_url = Data.BASE_API_PATH + '/data/photo'
        response = requests.get(data_url, headers=self.user_access_token)
        status_code = response.status_code
        return status_code

    def delete_photo(self):
        data_url = Data.BASE_API_PATH + '/data/photo'
        response = requests.delete(data_url, headers=self.user_access_token)
        content = ApiHelper.content(response)
        return content

    def create_user(self, *args):
        content = []
        user_url = Data.BASE_API_PATH + '/user'
        if args:
            json = Data.json_for_create_user(args)
            response = requests.post(user_url, headers=self.admin_token, json=json)
        else:
            json = Data.json_for_create_user()
            response = requests.post(user_url, headers=self.admin_token, json=json)
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        content.append(json)
        return content

    def change_password(self):
        content = []
        user_url = Data.BASE_API_PATH + '/user/password/change'
        json = Data.json_for_update_password(Data.read_credentials()[2], Data.read_credentials()[1])
        response = requests.post(user_url, headers=self.user_access_token, json=json)
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        content.append(Data.json_for_create_user())
        return content

    @staticmethod
    def revert_password():
        user_url = Data.BASE_API_PATH + '/user/password/change'
        json = Data.json_for_update_password(Data.read_credentials()[1], Data.read_credentials()[2])
        response = requests.post(user_url, headers=Authorization().authentification_with_new_password(), json=json)
        status_code = response.status_code
        return status_code

    def edit_user(self):
        pass
        # needs to create new project

    def create_project(self, *args):
        content = []
        request_json = Data.json_for_create_new_project()
        project_url = Data.BASE_API_PATH + 'project'
        if args:
            response = requests.post(project_url, headers=self.admin_token, json=request_json)
        else:
            response = requests.post(project_url, headers=self.user_access_token, json=request_json)
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        content.append(request_json["projectName"])
        return content

    def delete_project(self, new_project):
        project_url = Data.BASE_API_PATH + 'project/' + new_project
        response = requests.delete(project_url, headers=self.admin_token)
        content = ApiHelper.content(response)
        return content

    def get_project_info(self, *args):
        if args:
            project_url = Data.BASE_API_PATH + 'project/' + args[0]
        else:
            project_id = self.get_project_name()
            project_url = Data.BASE_API_PATH + 'project/' + project_id
        response = requests.get(project_url, headers=self.admin_token)
        content = ApiHelper.content(response)
        return content

    def update_project(self, project):
        project_url = Data.BASE_API_PATH + 'project/' + project
        response = requests.put(project_url, headers=self.admin_token, json=Data.json_for_update_project())
        content = ApiHelper.content(response)
        return content

    def assign_user_on_project(self, project):
        project_url = Data.BASE_API_PATH + 'project/' + project + '/assign'
        response = requests.put(project_url, headers=self.admin_token,
                                json=Data.json_for_assign_user('user_for_assignee'))
        content = ApiHelper.content(response)
        return content

    def delete_user(self, user):
        user_url = Data.BASE_API_PATH + 'user/' + user
        response = requests.delete(user_url, headers=self.admin_token)
        content = ApiHelper.content(response)
        return content

    def get_users_who_can_be_assigned_on_project(self, project):
        project_url = Data.BASE_API_PATH + 'project/' + project + '/assignable'
        response = requests.get(project_url, headers=self.admin_token)
        content = ApiHelper.content(response)
        return content

    def get_assigned_on_project_users(self, project):
        project_url = Data.BASE_API_PATH + 'project/' + project + '/users'
        response = requests.get(project_url, headers=self.admin_token)
        content = ApiHelper.content(response)
        return content

    def un_assign_user(self, project, user):
        project_url = Data.BASE_API_PATH + 'project/' + project + '/unassign'
        response = requests.put(project_url, headers=self.admin_token, json={"userNames": [user]})
        content = ApiHelper.content(response)
        return content

    @staticmethod
    def content(response):
        content = []
        status_code = response.status_code
        content.append(status_code)
        response = response.json()
        content.append(response)
        return content
