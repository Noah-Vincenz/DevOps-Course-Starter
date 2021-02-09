import trello_items as trello
import pytest
import requests
from app import create_app
from dotenv import load_dotenv, find_dotenv
from card import Card
import json 

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

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

def test_index(client, monkeypatch):
    mocked_cards_from_board = [
        {'id': 'card_id1', 'dateLastActivity': 'some_date1', 'idBoard': 'board_id', 'idList': 'id_list', 'name': 'Book flights', 'desc': 'book your flights home', 'pos': 1, 'badges': {}, 'dueComplete': False, 'due': None, 'idChecklists': ['id_checklists'], 'shortUrl': 'short_url1', 'url': 'url1', 'cover': {}},
        {'id': 'card_id2', 'dateLastActivity': 'some_date2', 'idBoard': 'board_id', 'idList': 'id_list', 'name': 'Book dinner', 'desc': 'dinner for Friday night', 'pos': 2, 'badges': {}, 'dueComplete': False, 'due': None, 'idChecklists': ['id_checklists'], 'shortUrl': 'short_url2', 'url': 'url2', 'cover': {}}
    ]
    mocked_list_name_todo = {'id': 'list_id1', 'name': 'To Do', 'closed': False, 'pos': 1, 'idBoard': 'board_id', 'limits': {}, 'subscribed': False}
    mocked_list_name_done = {'id': 'list_id2', 'name': 'Done', 'closed': False, 'pos': 2, 'idBoard': 'board_id', 'limits': {}, 'subscribed': False}

    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/boards/board_id/cards' and 'key' in params and 'token' in params:
            return MockResponse(mocked_cards_from_board, "200")
        elif url == 'https://api.trello.com/1/cards/card_id1/list' and 'key' in params and 'token' in params:
            return MockResponse(mocked_list_name_todo, "200")
        elif url == 'https://api.trello.com/1/cards/card_id2/list' and 'key' in params and 'token' in params:
            return MockResponse(mocked_list_name_done, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))

    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "text/html; charset=utf-8"