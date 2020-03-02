from locust import HttpLocust, TaskSet, task, between
from src.authorization import Authorization
from src.data import Data

def login():
    auth = Authorization()
    return auth.authentification_with_admin_role()

# def logout(l):
#     l.client.post("/logout", {"username":"ellen_key", "password":"education"})

def index(l):
    l.client.get("/")

def profile(l):
    l.client.get("/profile")

class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    def on_start(self):
        self.client.headers.update(login())

    def on_stop(self):
        self.client.delete('/uat/sso/me')

class MyTaskSet(UserBehavior):

    @task
    def get_user_info(self):
        self.client.get('api/v1/user')

    @task
    def upload_photo(self):
        photo = '\pickle.jpg'
        self.client.post('api/v1/data/photo', files=Data.return_photo(photo))

    @task
    def get_photo(self):
        self.client.get('api/v1/data/photo', headers=login())

    @task
    def delete_photo(self):
        self.client.delete('api/v1/data/photo', headers=login())

class WebsiteUser(HttpLocust):
    task_set = MyTaskSet
    wait_time = between(900, 1100)
    host = "http://10.20.12.203:8080/"

