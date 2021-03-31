import requests
import trello_items as trello
import os
import pytest

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

def test_get_all_lists_on_board(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/boards/1/lists' and 'key' in params and 'token' in params:
            return MockResponse({"name": "todo_list"}, "200")
        elif url == 'https://api.trello.com/1/boards/2/lists' and 'key' in params and 'token' in params:
            return MockResponse({"name": "doing_list"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.get_all_lists_on_board('1') == MockResponse({"name": "todo_list"}, "200").json_data
    assert trello.get_all_lists_on_board('2') == MockResponse({"name": "doing_list"}, "200").json_data
    assert trello.get_all_lists_on_board('3') == MockResponse({}, "404").json_data


def test_stop_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('TODO_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('TODO_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.stop_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert trello.stop_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert trello.stop_item('3').json_data == {} and trello.stop_item('3').status_code == "404"


def test_undo_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.undo_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert trello.undo_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert trello.undo_item('3').json_data == {} and trello.undo_item('3').status_code == "404"


def test_complete_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DONE_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DONE_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.complete_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert trello.complete_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert trello.complete_item('3').json_data == {} and trello.complete_item('3').status_code == "404"


def test_start_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        elif url == 'https://api.trello.com/1/cards/2' and 'key' in params and 'token' in params and 'idList' in params and params['idList'] == os.getenv('DOING_LIST_ID'):
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.start_item('1').json_data == MockResponse({"name": "clean room"}, "200").json_data
    assert trello.start_item('2').json_data == MockResponse({"name": "tidy room"}, "200").json_data
    assert trello.start_item('3').json_data == {} and trello.start_item('3').status_code == "404"


def test_create_item(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards' and 'key' in params and 'token' in params and 'name' in params and 'desc' in params and 'idList' in params and params['idList'] == os.getenv('TODO_LIST_ID'):
            return MockResponse({"name": "clean room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.create_item('clean room', 'tidy room and wipe surfaces').json_data == MockResponse({"name": "clean room"}, "200").json_data


def test_get_list_name(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/cards/1/list' and 'key' in params and 'token' in params:
            return MockResponse({"name": "todo list"}, "200")
        elif url == 'https://api.trello.com/1/cards/2/list' and 'key' in params and 'token' in params:
            return MockResponse({"name": "doing list"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.get_list_name('1') == "todo list"
    assert trello.get_list_name('2') == "doing list"
    with pytest.raises(KeyError):
        trello.get_list_name('3')


def test_get_all_boards(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/members/me/boards' and 'key' in params and 'token' in params:
            return MockResponse({"name": "todo list board"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.get_all_boards() == MockResponse({"name": "todo list board"}, "200").json_data
