import items as mongoDB
from card import Card
import pymongo
import mongomock
import uuid
import certifi

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

@mongomock.patch(servers=(('cluster0.huksc.mongodb.net')))
def test_get_items(monkeypatch):
    id1 = '1'
    id2 = '2'
    name1 = 'Clean flat'
    name2 = 'Clean room'
    desc1 = 'You need to clean the entire flat'
    desc2 = 'You need to clean the entire room'
    date1 = '2020-09-08'
    date2 = '2020-09-01'
    card1 = {'id':id1, 'name':name1, 'desc':desc1, 'dateLastActivity':date1}
    card2 = {'id':id2, 'name':name2, 'desc':desc2, 'dateLastActivity':date2}

    def mock_get_board(collection, board_id):
       return {
            'board_id': board_id,
            'lists': [
                {
                    'list_id': str(uuid.uuid4()),
                    'name': 'todo',
                    'cards': [
                        {
                            'card_id': id1,
                            'name': name1,
                            'desc': desc1,
                            'dateLastActivity': date1
                        }
                    ]
                },
                {
                    'list_id': str(uuid.uuid4()),
                    'name': 'doing',
                    'cards': [
                        {
                            'card_id': id2,
                            'name': name2,
                            'desc': desc2,
                            'dateLastActivity': date2
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
        }
    
    client = pymongo.MongoClient('cluster0.huksc.mongodb.net')
    collection = client.db.collection

    monkeypatch.setattr(mongoDB, 'get_board', lambda collection, board_id: mock_get_board(collection, board_id))

    expected_result = [
        [Card(id1, name1, desc1, '', date1)], 
        [Card(id2, name2, desc2, '', date2)], 
        []
    ]
    actual_result = mongoDB.get_items(collection, 'board1')
    same_items(expected_result, actual_result)


@mongomock.patch(servers=(('cluster0.huksc.mongodb.net')))
def test_insert(monkeypatch):
    client = pymongo.MongoClient('cluster0.huksc.mongodb.net')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.insert(collection, 'boardId1', 1, 'cardId3', 'title3', 'description3')
    board_lists = collection.find_one({ 'board_id': 'boardId1' })['lists']
    assert len(board_lists[0]['cards']) == 1
    assert len(board_lists[1]['cards']) == 2
    assert len(board_lists[2]['cards']) == 0


@mongomock.patch(servers=(('cluster0.huksc.mongodb.net')))
def test_delete(monkeypatch):
    db_username = 'nnoeh'
    db_password = 'nnoehPassword1996'
    client = pymongo.MongoClient('cluster0.huksc.mongodb.net')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.delete(collection, 'boardId1', 1, 'cardId2')
    board_lists = collection.find_one({ 'board_id': 'boardId1' })['lists']
    print(board_lists)
    assert len(board_lists[0]['cards']) == 1
    assert len(board_lists[1]['cards']) == 0
    assert len(board_lists[2]['cards']) == 0