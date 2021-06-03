from TodoUser import TodoUser
from flask import Flask, render_template, request, redirect, url_for
from pymongo.client_options import _parse_ssl_options
import items as mongoDB
from viewmodel import ViewModel
import pymongo
import certifi
import os
from flask_login import (current_user, login_required,
                            login_user, logout_user,
                            confirm_login, fresh_login_required)
from auth import init_auth, github_login

def get_collection():
    db_username = os.getenv('MONGO_USERNAME')
    db_password = os.getenv('MONGO_PW')
    client = pymongo.MongoClient(
        "mongodb+srv://{}:{}@cluster0.huksc.mongodb.net/todoDB?retryWrites=true&w=majority".format(db_username, db_password), 
        tlsCAFile=certifi.where()
    )
    db = client.todoDB
    return db.todos

def create_app():
    app = Flask(__name__)

    if os.getenv('LOGIN_DISABLED') is None:
        app.config['LOGIN_DISABLED'] = False
    else:
        app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED')
    init_auth(app)

    app.config.from_object('flask_config.Config')
    board_id = os.getenv('BOARD_ID')
    collection = get_collection()

    @app.route('/')
    @login_required
    def index():
        if (current_user.is_reader()):
            items = mongoDB.get_items(collection, board_id)
            item_view_model = ViewModel(items[0], items[1], items[2])
        else:
            item_view_model = ViewModel([], [], [])
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    @login_required
    def add():
        if (current_user.is_writer()):
            name = request.form.get('new_item_name')
            description = request.form.get('new_item_description')
            mongoDB.create_item(collection, board_id, name, description)
        return redirect(url_for('index'))

    @app.route('/start/<item_id>', methods=['POST'])
    @login_required
    def start_item(item_id):
        if (current_user.is_writer()):
            mongoDB.start_item(collection, board_id, item_id)
        return redirect(url_for('index'))            

    @app.route('/complete/<item_id>', methods=['POST'])
    @login_required
    def complete_item(item_id):
        if (current_user.is_writer()):
            mongoDB.complete_item(collection, board_id, item_id)
        return redirect(url_for('index'))


    @app.route('/undo/<item_id>', methods=['POST'])
    @login_required
    def undo_item(item_id):
        if (current_user.is_writer()):
            mongoDB.undo_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/stop/<item_id>', methods=['POST'])
    @login_required
    def stop_item(item_id):
        if (current_user.is_writer()):
            mongoDB.stop_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/login/callback', methods=['GET'])
    @login_required
    def login_callback():
        auth_code = request.args.get('code')
        auth_state = request.args.get('state')
        github_login(auth_code, auth_state)
        return redirect(url_for('index'))

    return app
