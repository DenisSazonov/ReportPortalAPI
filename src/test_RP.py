from .apihelper import ApiHelper
import time

class TestActivityController:
    def test_get_activities_for_project(self):
        get_activity = ApiHelper()
        content = get_activity.get_activities()
        status_code = content[0]
        assert 200 == status_code

    def test_get_activities_for_test_item(self):
        pass


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
        pass

    def test_update_dashboard_for_project(self):
        pass