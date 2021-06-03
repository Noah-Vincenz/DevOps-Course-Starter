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

    def is_reader(self):
        if ('reader' not in self.roles):
            print('User does not have required role: reader')
            return False
        return True

    def is_writer(self):
        if ('writer' not in self.roles):
            print('User does not have required role: writer')
            return False
        return True