from flask import Flask, render_template, request, redirect, url_for
import items as mongoDB
from viewmodel import ViewModel
import pymongo
import certifi
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_config.Config')
    board_id = os.getenv('BOARD_ID')
    db_username = os.getenv('MONGO_USERNAME')
    db_password = os.getenv('MONGO_PW')
    client = pymongo.MongoClient(
        "mongodb+srv://{}:{}@cluster0.huksc.mongodb.net/todoDB?retryWrites=true&w=majority".format(db_username, db_password), 
        tlsCAFile=certifi.where()
    )
    db = client.todoDB
    collection = db.todos

    @app.route('/')
    def index():
        items = mongoDB.get_items(collection, board_id)
        item_view_model = ViewModel(items[0], items[1], items[2])
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    def add():
        name = request.form.get('new_item_name')
        description = request.form.get('new_item_description')
        mongoDB.create_item(collection, board_id, name, description)
        return redirect(url_for('index'))

    @app.route('/start/<item_id>', methods=['POST'])
    def start_item(item_id):
        mongoDB.start_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/complete/<item_id>', methods=['POST'])
    def complete_item(item_id):
        mongoDB.complete_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/undo/<item_id>', methods=['POST'])
    def undo_item(item_id):
        mongoDB.undo_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/stop/<item_id>', methods=['POST'])
    def stop_item(item_id):
        mongoDB.stop_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    return app, collection
