import requests
import items as mongoDB
import os
import pytest
import pymongo
import mongomock
import uuid
import sys
import time

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def populate_collection(collection):
    collection.insert_one({
        'board_id': 'boardId1',
        'lists': [
            {
                'list_id': str(uuid.uuid4()),
                'name': 'todo',
                'cards': [
                    {
                        'card_id': 'cardId1',
                        'name': 'name1',
                        'desc': 'desc1',
                        'dateLastActivity': 'date1'
                    }
                ]
            },
            {
                'list_id': str(uuid.uuid4()),
                'name': 'doing',
                'cards': [
                    {
                        'card_id': 'cardId2',
                        'name': 'name2',
                        'desc': 'desc2',
                        'dateLastActivity': 'date2'
                    }
                ]
            },
            {
                'list_id': str(uuid.uuid4()),
                'name': 'done',
                'cards': [
                ]
            }
        ] 
    })

@mongomock.patch(servers=(('server.example.com', 27017),))
def test_delete(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.delete(collection, 'boardId1', 1, 'cardId2')
    board_lists = collection.find_one({ 'board_id': 'boardId1' })['lists']
    print(board_lists)
    assert len(board_lists[0]['cards']) == 1
    assert len(board_lists[1]['cards']) == 0
    assert len(board_lists[2]['cards']) == 0


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_stop_item(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    # monkeypatch.setattr(mongoDB, 'get_board', lambda collection, board_id: mock_get_board(collection, board_id))

    mongoDB.stop_item(collection, 'boardId1', 'cardId2')
    board_lists = collection.find_one({ 'board_id': 'boardId1' })['lists']
    print(board_lists)
    assert len(board_lists[0]['cards']) == 2
    assert len(board_lists[1]['cards']) == 0
    assert len(board_lists[2]['cards']) == 0


def test_undo_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert mongoDB.undo_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert mongoDB.undo_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert mongoDB.undo_item('3').json_data == {} and mongoDB.undo_item('3').status_code == "404"


def test_complete_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DONE_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DONE_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert mongoDB.complete_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert mongoDB.complete_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert mongoDB.complete_item('3').json_data == {} and mongoDB.complete_item('3').status_code == "404"


def test_start_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert mongoDB.start_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert mongoDB.start_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert mongoDB.start_item('3').json_data == {} and mongoDB.start_item('3').status_code == "404"


def test_create_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards' and 'key' in params and 'token' in params and 'name' in params and 'desc' in params and 'idList' in params and params['idList'] == os.getenv('TODO_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert mongoDB.create_item('clean room', 'tidy room and wipe surfaces').json_data == MockResponse({"name": "clean room"}, "200").json_data


def test_get_list_name(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1/list' and 'key' in params and 'token' in params:
            return MockResponse({"name": "todo list"}, "200")
        elif url == 'https://api.trello.com/1/cards/2/list' and 'key' in params and 'token' in params:
            return MockResponse({"name": "doing list"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert mongoDB.get_list_name('1') == "todo list"
    assert mongoDB.get_list_name('2') == "doing list"
    with pytest.raises(KeyError):
        mongoDB.get_list_name('3')


def test_get_all_boards(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/members/me/boards' and 'key' in params and 'token' in params:
            return MockResponse({"name": "todo list board"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert mongoDB.get_all_boards() == MockResponse({"name": "todo list board"}, "200").json_data
