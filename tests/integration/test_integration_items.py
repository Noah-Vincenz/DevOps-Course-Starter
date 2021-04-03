import requests
import items as mongoDB
import os
import pytest
import pymongo
import mongomock
import uuid
import sys
import time


def populate_collection(collection):
    collection.insert_one(
        {
            'board_id': 'board_id',
            'list_id': 'todo_list_id',
            'list_name': 'todo',
            'cards': [
                {
                    'card_id': 'cardId1',
                    'card_name': 'name1',
                    'card_desc': 'desc1',
                    'card_dateLastActivity': 'date1'
                }
            ]
        }
    )
    collection.insert_one(
        {
            'board_id': 'board_id',
            'list_id': 'doing_list_id',
            'list_name': 'doing',
            'cards': [
                {
                    'card_id': 'cardId2',
                    'card_name': 'name2',
                    'card_desc': 'desc2',
                    'card_dateLastActivity': 'date2'
                }
            ]
        }
    )
    collection.insert_one(
        {
            'board_id': 'board_id',
            'list_id': 'done_list_id',
            'list_name': 'done',
            'cards': [
                {
                    'card_id': 'cardId3',
                    'card_name': 'name3',
                    'card_desc': 'desc3',
                    'card_dateLastActivity': 'date3'
                }
            ]
        }
    )


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_insert(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.insert(collection, 'board_id', 'todo', 'cardId4', 'name4', 'desc4')
    
    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 2
    assert len(doing_list) == 1
    assert len(done_list) == 1


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_delete_existing(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.delete(collection, 'board_id', 'doing', 'cardId2')

    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 1
    assert len(doing_list) == 0
    assert len(done_list) == 1


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_delete_non_existing(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.delete(collection, 'board_id', 'doing', 'cardId3')

    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 1
    assert len(doing_list) == 1
    assert len(done_list) == 1


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_stop_item(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.stop_item(collection, 'board_id', 'cardId2')

    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 2
    assert len(doing_list) == 0
    assert len(done_list) == 1


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_undo_item(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.undo_item(collection, 'board_id', 'cardId3')

    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 1
    assert len(doing_list) == 2
    assert len(done_list) == 0


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_complete_item(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.complete_item(collection, 'board_id', 'cardId2')

    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 1
    assert len(doing_list) == 0
    assert len(done_list) == 2


@mongomock.patch(servers=(('server.example.com', 27017),))
def test_start_item(monkeypatch):

    client = pymongo.MongoClient('server.example.com')
    collection = client.db.collection
    populate_collection(collection)

    mongoDB.start_item(collection, 'board_id', 'cardId1')

    todo_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'todo'})['cards']
    doing_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'doing'})['cards']
    done_list = collection.find_one({ 'board_id': 'board_id', 'list_name': 'done'})['cards']

    assert len(todo_list) == 0
    assert len(doing_list) == 2
    assert len(done_list) == 1