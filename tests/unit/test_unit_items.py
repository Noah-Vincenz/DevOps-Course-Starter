import items as mongoDB
from card import Card
import pymongo
import mongomock
import uuid
import certifi


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


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_get_items(monkeypatch):
    id1 = 'cardId1'
    id2 = 'cardId2'
    name1 = 'Clean flat'
    name2 = 'Clean room'
    desc1 = 'You need to clean the entire flat'
    desc2 = 'You need to clean the entire room'
    date1 = '2020-09-08'
    date2 = '2020-09-01'
    card1 = {'card_id': id1, 'card_name': name1, 'card_desc': desc1, 'card_dateLastActivity': date1}
    card2 = {'card_id': id2, 'card_name': name2, 'card_desc': desc2, 'card_dateLastActivity': date2}
    
    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection

    monkeypatch.setattr(collection, 'find_one', lambda obj: mock_find_one(obj))

    expected_result = [
        [Card(id1, name1, desc1, 'todo', date1)], 
        [Card(id2, name2, desc2, 'doing', date2)], 
        []
    ]
    actual_result = mongoDB.get_items(collection, 'board_id')
    same_items(expected_result, actual_result)


# @mongomock.patch(servers=(('cluster0.huksc.mongodb.net')))
# def test_insert(monkeypatch):
#     client = pymongo.MongoClient('cluster0.huksc.mongodb.net')
#     collection = client.db.collection
#     populate_collection(collection)

#     mongoDB.insert(collection, 'boardId1', 1, 'cardId3', 'title3', 'description3')
#     board_lists = collection.find_one({ 'board_id': 'boardId1' })['lists']
#     assert len(board_lists[0]['cards']) == 1
#     assert len(board_lists[1]['cards']) == 2
#     assert len(board_lists[2]['cards']) == 0


# @mongomock.patch(servers=(('cluster0.huksc.mongodb.net')))
# def test_delete(monkeypatch):
#     db_username = 'nnoeh'
#     db_password = 'nnoehPassword1996'
#     client = pymongo.MongoClient('cluster0.huksc.mongodb.net')
#     collection = client.db.collection
#     populate_collection(collection)

#     mongoDB.delete(collection, 'boardId1', 1, 'cardId2')
#     board_lists = collection.find_one({ 'board_id': 'boardId1' })['lists']
#     print(board_lists)
#     assert len(board_lists[0]['cards']) == 1
#     assert len(board_lists[1]['cards']) == 0
#     assert len(board_lists[2]['cards']) == 0