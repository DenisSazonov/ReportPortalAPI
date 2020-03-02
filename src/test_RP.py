from .apihelper import ApiHelper
from .data import Data


class TestActivityController:
    def test_get_activities_for_project(self):
        get_activity = ApiHelper()
        content = get_activity.get_activities()
        assert 200 == content[0]


class TestDashboardController:
    def test_get_dashboard_resources_for_project(self):
        get_dashboard = ApiHelper()
        content = get_dashboard.get_dashboards()
        assert content[1]["owner"] == "default"
        assert 200 == content[0]

    def test_create_dashboard_for_project(self):
        post_dashboard = ApiHelper()
        content = post_dashboard.create_new_dashboard()
        assert "id" in content[1]
        assert 201 == content[0]

    def test_get_shared_dashboards_from_project(self):
        post_dashboard = ApiHelper()
        create_new_dashboard_response = post_dashboard.create_new_dashboard()
        new_dashboard_id = create_new_dashboard_response[1]["id"]
        get_shared_dashboards = ApiHelper()
        content = get_shared_dashboards.get_shared_dashboards()
        json = ApiHelper.return_json_from_list(content)
        status_code = ApiHelper.return_status_code(content)
        assert new_dashboard_id in json
        assert 200 == status_code

    def test_delete_project_dashboard(self):
        post_dashboard = ApiHelper()
        create_new_dashboard_response = post_dashboard.create_new_dashboard()
        json = create_new_dashboard_response[1]
        new_dashboard_id = json["id"]
        delete_dashboard = ApiHelper()
        content = delete_dashboard.delete_dashboard(new_dashboard_id)
        assert content[1] == {'msg': "Dashboard with ID = '" + new_dashboard_id + "' successfully deleted."}
        assert 200 == content[0]

    def test_get_specified_dashboard_for_specified_project(self):
        post_dashboard = ApiHelper()
        create_new_dashboard_response = post_dashboard.create_new_dashboard()
        json = create_new_dashboard_response[1]
        new_dashboard_id = json["id"]
        get_shared_dashboards = ApiHelper()
        content = get_shared_dashboards.get_shared_dashboards()
        json = ApiHelper.return_json_from_list(content)
        status_code = ApiHelper.return_status_code(content)
        assert new_dashboard_id in json
        assert 200 == status_code

    def test_update_dashboard_for_project(self):
        post_dashboard = ApiHelper()
        create_new_dashboard_response = post_dashboard.create_new_dashboard()
        json = create_new_dashboard_response[1]
        new_dashboard_id = json["id"]
        update_dashboard = ApiHelper()
        content = update_dashboard.update_dashboard(new_dashboard_id)
        assert content[1] == {'msg': "Dashboard with ID = '" + new_dashboard_id + "' successfully updated."}
        assert 200 == content[0]
        ApiHelper().delete_dashboard(new_dashboard_id)


class TestFileStorageController:
    def test_upload_user_photo(self):
        photo = '\pickle.jpg'
        upload_photo_response = ApiHelper().upload_photo(photo)
        assert upload_photo_response[1] == {"msg": "Profile photo has been uploaded successfully"}
        assert 200 == upload_photo_response[0]

    def test_get_photo(self):
        get_photo = ApiHelper()
        get_photo_status_code = get_photo.get_photo()
        assert 200 == get_photo_status_code

    def test_delete_photo(self):
        delete_photo = ApiHelper()
        delete_photo_response = delete_photo.delete_photo()
        assert delete_photo_response[1] == {"msg": "Profile photo has been deleted successfully"}
        assert 200 == delete_photo_response[0]

    def test_upload_large_photo(self):
        photo = '\large.jpg'
        upload_photo = ApiHelper()
        upload_photo_response = upload_photo.upload_photo(photo)
        assert upload_photo_response[1] == {
            "error_code": 4002,
            "message": "Binary data cannot be saved. Image size should be 300x500px or less"
        }
        assert 400 == upload_photo_response[0]


class TestUserController:
    def test_get_info_about_current_user(self):
        get_user_info = ApiHelper()
        get_user_info_response = get_user_info.get_current_user_info()
        assert get_user_info_response[1]['userId'] == 'default'
        assert 200 == get_user_info_response[0]

    def test_create_specified_user(self):
        create_user = ApiHelper().create_user()
        assert create_user[2]["login"] == create_user[1]["login"]
        assert 201 == create_user[0]

    def test_create_user_without_enough_permissions(self):
        role = 'user'
        create_user = ApiHelper().create_user(role)
        # assert create_user[1] == Data.no_permissions_json()
        assert 409 == create_user[0]

    def test_get_info_about_all_users(self):
        get_user_info = ApiHelper()
        all_users = '/all'
        get_user_info_response = get_user_info.get_info_about_all_users(all_users)
        assert 200 == get_user_info_response[0]

    def test_get_info_about_all_users_without_enough_permissions(self):
        role = 'user'
        get_user_info = ApiHelper()
        get_user_info_response = get_user_info.get_info_about_all_users(role)
        assert 403 == get_user_info_response[0]
        assert get_user_info_response[1] == Data.no_permissions_json()

    def test_change_password(self):
        change_password = ApiHelper()
        change_password_response = change_password.change_password()
        assert 200 == change_password_response[0]
        assert change_password_response[1] == {"msg": "Password has been changed successfully"}
        assert 200 == change_password.revert_password()

    def test_delete_user(self):
        create_user = ApiHelper().create_user('test_delete_user')
        json_for_create_user = create_user[2]
        user = json_for_create_user["login"]
        delete_user = ApiHelper().delete_user(user)
        assert delete_user[1] == {'msg': "User with ID = '" + user + "' successfully deleted."}
        assert 200 == delete_user[0]

    def test_return_info_about_specified_user(self):
        specified_user = ApiHelper()
        get_username = specified_user.get_current_user_info()
        get_specified_user_json = get_username[1]
        get_specified_user_name = get_specified_user_json["userId"]
        get_info_about_specified_user_response = specified_user.get_info_about_all_users(get_specified_user_name)
        assert "userId" in get_info_about_specified_user_response[1]
        assert 200 == get_info_about_specified_user_response[0]

    def test_edit_specified_user(self):
        pass


class TestProjectController:

    def test_create_new_project(self):
        create_project = ApiHelper()
        admin = True
        create_project_response = create_project.create_project(admin)
        assert create_project_response[1]["id"] == create_project_response[2]
        assert 201 == create_project_response[0]
        ApiHelper().delete_project(create_project_response[1]["id"])

    def test_create_new_project_without_enough_permissions(self):
        create_project = ApiHelper()
        create_project_response = create_project.create_project()
        assert create_project_response[1] == Data.no_permissions_json()
        assert 403 == create_project_response[0]

    def test_delete_project(self):
        create_project = ApiHelper()
        admin = True
        create_project_response = create_project.create_project(admin)
        new_project_id = create_project_response[2]
        delete_project = ApiHelper()
        delete_project_response = delete_project.delete_project(new_project_id)
        assert delete_project_response[0] == 200
        assert delete_project_response[1] == {"msg": "Project with name = '" + new_project_id + "' is successfully deleted."}

    def test_get_information_about_project(self):
        get_info = ApiHelper()
        get_info_response = get_info.get_project_info()
        assert get_info_response[0] == 200
        assert get_info_response[1]["projectId"] == 'default_personal'

    def test_update_project(self):
        create_project = ApiHelper()
        admin = True
        create_project_response = create_project.create_project(admin)
        new_project_id = create_project_response[2]
        update_project = ApiHelper()
        update_project_response = update_project.update_project(new_project_id)
        assert update_project_response[0] == 200
        assert update_project_response[1] == {"msg": "Project with name = '" + new_project_id + "' is successfully updated."}
        get_updated_info = ApiHelper()
        get_updated_info_response = get_updated_info.get_project_info(new_project_id)
        assert get_updated_info_response[1]["addInfo"] == "Updated_project"
        ApiHelper().delete_project(new_project_id)

    def test_assign_user_on_project(self):
        create_project = ApiHelper()
        admin = True
        create_project_response = create_project.create_project(admin)
        new_project_id = create_project_response[2]
        create_user = ApiHelper().create_user('user_for_assignee')
        user_response = create_user[1]
        user = user_response['login']
        assign_user = ApiHelper()
        assign_user_response = assign_user.assign_user_on_project(new_project_id)
        assert assign_user_response[1] == {
            "msg": "User(s) with username='[" + user + "]' was successfully assigned to project='" + new_project_id + "'"
        }
        assert assign_user_response[0] == 200
        ApiHelper().delete_project(new_project_id)
        ApiHelper().delete_user(user)

    def test_get_assigned_users_on_project(self):
        project = ApiHelper().create_project('test_assigned_users')[1]
        project_id = project['id']
        user_json = ApiHelper().create_user('user_for_getting_assigned_user')[1]
        user = user_json['login']
        ApiHelper().assign_user_on_project(project_id)
        get_assigned_users_response = ApiHelper().get_users_who_can_be_assigned_on_project(project_id)
        json = get_assigned_users_response[1]
        assigned_users = json['content']
        new_assigned_user = assigned_users[-1]
        assert user == new_assigned_user['userId']
        assert 200 == get_assigned_users_response[0]
        ApiHelper().delete_user(user)
        ApiHelper().delete_project(project_id)

    def test_un_assign_user(self):
        admin = True
        project = ApiHelper().create_project(admin)[1]
        project_id = project['id']
        user_json = ApiHelper().create_user('user_for_assignee')[1]
        user = user_json['login']
        ApiHelper().assign_user_on_project(project_id)
        un_assign_user = ApiHelper().un_assign_user(project_id, user)
        assert un_assign_user[1] == {
            "msg": "User(s) with username(s)='[" + user + "]' was successfully un-assigned from project='" + project_id + "'"
        }
        assert 200 == un_assign_user[0]
        ApiHelper().delete_user(user)
        ApiHelper().delete_project(project_id)

    def test_get_users_from_project(self):
        pass
