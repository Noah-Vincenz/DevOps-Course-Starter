from flask_login import UserMixin

class TodoUser(UserMixin):
    def __init__(self, github_id):
        self.id = github_id