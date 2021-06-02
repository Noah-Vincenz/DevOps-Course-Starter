from flask_login import UserMixin

class TodoUser(UserMixin):

    def __init__(self, github_id):
        self.id = github_id
        self.set_roles(github_id)

    def set_roles(self, github_id):
        if (github_id == '16804823'):
            self.roles = ['writer', 'reader']
        else:
            self.roles = ['reader']