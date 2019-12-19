from .apihelper import ApiHelper


class TestActivityController:
    def test_get_activities_for_project(self):
        get_activity = ApiHelper()
        content = get_activity.get_activities()
        status_code = content[0]
        assert 200 == status_code


class TestDashboardController:
    def test_get_dashboard_resources_for_project(self):
        get_dashboard = ApiHelper()
        content = get_dashboard.get_dashboards()
        json = content[1]
        status_code = content[0]
        assert json["owner"] == "default"
        assert 200 == status_code

    def test_create_dashboard_for_project(self):
        post_dashboard = ApiHelper()
        content = post_dashboard.create_new_dashboard()
        json = content[1]
        status_code = content[0]
        assert "id" in json
        assert 201 == status_code

    def test_get_shared_dashboards_from_project(self):
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

    def test_delete_project_dashboard(self):
        post_dashboard = ApiHelper()
        create_new_dashboard_response = post_dashboard.create_new_dashboard()
        json = create_new_dashboard_response[1]
        new_dashboard_id = json["id"]
        delete_dashboard = ApiHelper()
        content = delete_dashboard.delete_dashboard(new_dashboard_id)
        json = content[1]
        status_code = content[0]
        print(json)
        assert json == {'msg': "Dashboard with ID = '" + new_dashboard_id + "' successfully deleted."}
        assert 200 == status_code

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
        json = content[1]
        status_code = content[0]
        assert json == {'msg': "Dashboard with ID = '" + new_dashboard_id + "' successfully updated."}
        assert 200 == status_code


class TestFileStorageController:
    def test_upload_user_photo(self):
        photo = '\pickle.jpg'
        upload_photo = ApiHelper()
        upload_photo_response = upload_photo.upload_photo(photo)
        json = upload_photo_response[1]
        status_code = upload_photo_response[0]
        assert json == {"msg": "Profile photo has been uploaded successfully"}
        assert 200 == status_code

    def test_get_photo(self):
        get_photo = ApiHelper()
        get_photo_status_code = get_photo.get_photo()
        assert 200 == get_photo_status_code

    def test_delete_photo(self):
        delete_photo = ApiHelper()
        delete_photo_response = delete_photo.delete_photo()
        json = delete_photo_response[1]
        status_code = delete_photo_response[0]
        assert json == {"msg": "Profile photo has been deleted successfully"}
        assert 200 == status_code

    def test_upload_large_photo(self):
        photo = '\large.jpg'
        upload_photo = ApiHelper()
        upload_photo_response = upload_photo.upload_photo(photo)
        json = upload_photo_response[1]
        status_code = upload_photo_response[0]
        assert json == {
            "error_code": 4002,
            "message": "Binary data cannot be saved. Image size should be 300x500px or less"
        }
        assert 400 == status_code


class TestUserController:
    def test_get_info_about_current_user(self):
        get_user_info = ApiHelper()
        get_user_info_response = get_user_info.get_user_info()
        json = get_user_info_response[1]
        status_code = get_user_info_response[0]
        assert json['userId'] == 'default'
        assert 200 == status_code

    def test_create_specified_user(self):
        create_user = ApiHelper().create_user()
        json = create_user[1]
        status_code = create_user[0]
        json_for_create_user = create_user[2]
        assert {"login": json_for_create_user["login"]} in json
        assert 200 == status_code

    def test_create_user_without_enough_permissions(self):
        create_user = ApiHelper().create_user()
        json = create_user[1]
        status_code = create_user[0]
        assert json == {
            "error_code": 4003,
            "message": "You do not have enough permissions. Access is denied"
        }
        assert 403 == status_code

    def test_get_info_about_all_users(self):
        get_user_info = ApiHelper()
        all_users = '/all'
        get_user_info_response = get_user_info.get_user_info(all_users)
        # json = get_user_info_response[1]
        status_code = get_user_info_response[0]
        print(get_user_info_response)
        assert 200 == status_code

    def test_get_info_about_all_users_without_enough_permissions(self):
        get_user_info = ApiHelper()
        all_users = '/all'
        get_user_info_response = get_user_info.get_user_info(all_users)
        json = get_user_info_response[1]
        status_code = get_user_info_response[0]
        assert 403 == status_code
        assert json == {
            "error_code": 4003,
            "message": "You do not have enough permissions. Access is denied"
        }

    def test_register_invitation_for_user_who_will_be_created(self):
        pass

    def test_change_password(self):
        change_password = ApiHelper()
        change_password_response = change_password.change_password()
        json = change_password_response[1]
        status_code = change_password_response[0]
        assert 200 == status_code
        assert json == {"msg": "Password has been changed successfully"}
        status_code = change_password.revert_password()
        assert 200 == status_code

    def test_reset_password(self):
        pass

    def test_check_if_restore_password_bid_exists(self):
        pass

    def test_create_restore_password_request(self):
        pass

    def test_activate_invitation_and_create_user_in_system(self):
        pass

    def test_delete_user(self):
        pass

    def test_return_info_about_specified_user(self):
        specified_user = ApiHelper()
        get_username = specified_user.get_user_info()
        get_specified_user_json = get_username[1]
        get_specified_user_name = get_specified_user_json["userId"]
        get_info_about_specified_user_response = specified_user.get_user_info(get_specified_user_name)
        json = get_info_about_specified_user_response[1]
        status_code = get_info_about_specified_user_response[0]
        assert "userId" in json
        assert 200 == status_code

    def test_edit_specified_user(self):
        pass


class TestProjectController:

    def test_create_new_project(self):
        pass

    def test_delete_project(self):
        pass

    def test_get_information_about_project(self):
        pass

    def test_update_project(self):
        pass

    def test_assign_user_on_project(self):
        pass

    def test_get_assigned_users_on_project(self):
        pass

    def test_update_project_email_configuration(self):
        pass

    def test_delete_project_index_from_ml(self):
        pass

    def test_start_reindex_all_project_data_in_ml(self):
        pass

    def test_get_user_preferences(self):
        pass

    def test_un_assign_user(self):
        pass

    def test_load_project_users_by_filter(self):
        pass

    def test_get_users_from_project(self):
        pass