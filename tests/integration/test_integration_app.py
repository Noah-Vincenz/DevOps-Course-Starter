import items as mongoDB
import pytest
import requests
from app import create_app
from dotenv import load_dotenv, find_dotenv
from card import Card
import json 
import pymongo
import mongomock

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_find_one(obj):
    if obj['list_name'] == 'todo':
        return {
            'board_id': 'board_id',
            'list_id': 'todo_list_id',
            'list_name': 'todo',
            'cards': [
                {
                    'card_id': 'cardId1',
                    'card_name': 'Clean flat',
                    'card_desc': 'You need to clean the entire flat',
                    'card_dateLastActivity': '2020-09-08'
                }
            ]
        }
    elif obj['list_name'] == 'doing':
       return {
            'board_id': 'board_id',
            'list_id': 'doing_list_id',
            'list_name': 'doing',
            'cards': [
                {
                    'card_id': 'cardId2',
                    'card_name': 'Clean room',
                    'card_desc': 'You need to clean the entire room',
                    'card_dateLastActivity': '2020-09-01'
                }
            ]
        }
    elif obj['list_name'] == 'done':
        return {
            'board_id': 'board_id',
            'list_id': 'done_list_id',
            'list_name': 'done',
            'cards': []
        }
    else:
        raise Exception('No document found')
    

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_index(client, monkeypatch):
    pymongo_client = pymongo.MongoClient('server.example.com')
    collection = pymongo_client.db.collection
    
    monkeypatch.setattr(collection, 'find_one', lambda obj: mock_find_one(obj))

    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "text/html; charset=utf-8"