from flask_login import LoginManager, login_user
from flask import redirect
import requests
from TodoUser import TodoUser
from oauthlib.oauth2 import WebApplicationClient
import random, string
import os

client_id = os.getenv('OAUTH_CLIENT_ID')
client_secret = os.getenv('OAUTH_CLIENT_SECRET')
secret_key = os.getenv('SECRET_KEY')

def init_auth(app):
    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthorised():
        # Users are redirected to request their GitHub identity
        state = ''.join(random.choices(string.ascii_lowercase, k=16))
        auth_client = WebApplicationClient(client_id)
        auth_uri = auth_client.prepare_request_uri(
            'https://github.com/login/oauth/authorize',
            redirect_uri = 'http://localhost:5000/login/callback',
            state = state
        )
        return redirect(auth_uri)

    @login_manager.user_loader
    def load_user(user_id):
        return TodoUser(user_id)

    login_manager.init_app(app)


def github_login(code, state):
    access_token = get_access_token(code, state)
    user_request_headers = {'Authorization': 'bearer ' + access_token}
    user_id = requests.get('https://api.github.com/user', headers = user_request_headers).json()['id']
    user = TodoUser(user_id)
    login_user(user)


def get_access_token(code, state):
    auth_client = WebApplicationClient(client_id)
    token_request = auth_client.prepare_token_request(
        'https://github.com/login/oauth/access_token',
        client_id = client_id,
        client_secret = client_secret,
        code = code,
        state = state
    )
    token_request[1]['Accept'] = 'application/json'
    access_token_response = requests.post(token_request[0], data = token_request[2], headers = token_request[1]).content
    token_params = auth_client.parse_request_body_response(access_token_response)
    return token_params['access_token']