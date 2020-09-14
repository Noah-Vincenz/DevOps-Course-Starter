import pytest
import trello_items as trello
from flask import jsonify
from card import Card
import os
import requests

def same_items(arr1, arr2):
    assert len(arr1) == len(arr2)
    todo_items1 = arr1[0]
    todo_items2 = arr2[0]
    doing_items1 = arr1[1]
    doing_items2 = arr2[1]
    done_items1 = arr1[2]
    done_items2 = arr2[2]
    assert len(todo_items1) == len(todo_items2)
    for index in range(len(todo_items1)):
        assert todo_items1[index].name == todo_items2[index].name
        assert todo_items1[index].id == todo_items2[index].id
        assert todo_items1[index].description == todo_items2[index].description
        assert todo_items1[index].last_modified == todo_items2[index].last_modified
    assert len(doing_items1) == len(doing_items2)
    for index in range(len(doing_items1)):
        assert doing_items1[index].name == doing_items2[index].name
        assert doing_items1[index].id == doing_items2[index].id
        assert doing_items1[index].description == doing_items2[index].description
        assert doing_items1[index].last_modified == doing_items2[index].last_modified
    assert len(done_items1) == len(done_items2)
    for index in range(len(done_items1)):
        assert done_items1[index].name == done_items2[index].name
        assert done_items1[index].id == done_items2[index].id
        assert done_items1[index].description == done_items2[index].description
        assert done_items1[index].last_modified == done_items2[index].last_modified

def test_get_items(monkeypatch):
    def mock_get_list_name(card_id):
        if card_id == "1":
            return "To Do"
        elif card_id == "2":
            return "Doing"
        elif card_id == "3":
            return "Done"

    id1 = '1'
    id2 = '2'
    name1 = 'Clean flat'
    name2 = 'Clean room'
    desc1 = 'You need to clean the entire flat'
    desc2 = 'You need to clean the entire room'
    date1 = '2020-09-08T10:17:08.247Z'
    date2 = '2020-09-01T00:00:00'
    card1 = {'id':id1, 'name':name1, 'desc':desc1, 'dateLastActivity':date1}
    card2 = {'id':id2, 'name':name2, 'desc':desc2, 'dateLastActivity':date2}
    
    monkeypatch.setattr(trello, 'get_cards_from_board', lambda board_id: [card1, card2])
    monkeypatch.setattr(trello, 'get_list_name', lambda card_id: mock_get_list_name(card_id))

    expected_result = [
        [Card(id1, name1, desc1, '', date1)], 
        [Card(id2, name2, desc2, '', date2)], 
        []
    ]
    actual_result = trello.get_items()
    same_items(expected_result, actual_result)


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


def test_get_cards_from_board(monkeypatch):
    def mocked_requests_get(url, params):
        if url == 'https://api.trello.com/1/boards/1/cards' and 'key' in params and 'token' in params:
            return MockResponse({"name": "clean room"}, "200")
        if url == 'https://api.trello.com/1/boards/2/cards' and 'key' in params and 'token' in params:
            return MockResponse({"name": "tidy room"}, "200")
        return MockResponse({}, "404")

    monkeypatch.setattr(requests, 'request', lambda type, url, params: mocked_requests_get(url, params))
    assert trello.get_cards_from_board('1') == MockResponse({"name": "clean room"}, "200").json_data
    assert trello.get_cards_from_board('2') == MockResponse({"name": "tidy room"}, "200").json_data
    assert trello.get_cards_from_board('3') == {}

