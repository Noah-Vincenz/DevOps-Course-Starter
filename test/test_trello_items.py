import pytest
import trello_items as trello
from flask import jsonify
from app import app
from card import Card

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
