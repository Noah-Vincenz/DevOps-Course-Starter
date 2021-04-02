from flask import session
import requests
import os
from card import Card
import sys
import uuid
from datetime import date

board_id = os.getenv('BOARD_ID')
todo_list_id = os.getenv('TODO_LIST_ID')
doing_list_id = os.getenv('DOING_LIST_ID')
done_list_id = os.getenv('DONE_LIST_ID')

def get_items(collection):
    """
    Fetches all cards from mongoDB collection.

    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    todo_cards = []
    doing_cards = []
    done_cards = []
    for list_id in [todo_list_id, doing_list_id, done_list_id]:
        dbList = get_list(collection, list_id)
        for card in dbList['cards']:
            list_name = dbList['list_name']
            new_card = Card(card['card_id'], card['card_name'], card['card_desc'], list_name, card['card_dateLastActivity'])
            if list_name == "todo":
                todo_cards.append(new_card)
            elif list_name == "doing":
                doing_cards.append(new_card)
            else:
                done_cards.append(new_card)
    return [todo_cards, doing_cards, done_cards]


def get_list(collection, list_id):
    """
    Fetches a given list by board id and list id from the DB.

    Returns:
        board: The list with the given id.
    """
    return collection.find_one(
        { 
            'board_id': board_id,
            'list_id': list_id
        }
    )


def insert(collection, list_id, item_id, title, description):
    """
    Creates a card in a given list of the board.
    """
    collection.update_one(
        { 
            'board_id': board_id,
            'list_id': list_id
        },
        { '$push': {
            'cards': {
                'card_id': item_id,
                'card_name': title,
                'card_desc': description,
                'card_dateLastActivity': str(date.today())
            }
        }}
    )


def delete(collection, list_id, item_id):
    """
    Removes a card from the given list (by index) of the board.
    """
    collection.update_one(
        { 
            'board_id': board_id,
            'list_id': list_id
        },
        { '$pull': {
            'cards': {
                'card_id': item_id
            }
        }}
    )


def create_item(collection, title, description):
    """
    Creates a card in the TO DO list of the board.
    """
    insert(collection, todo_list_id, str(uuid.uuid4()), title, description)

    
def start_item(collection, item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    # get todo items
    todo_cards = get_list(collection, todo_list_id)['cards']
    # filter with list comprehension
    filtered_list = [x for x in todo_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from todo list
    delete(collection, todo_list_id, item_id)
    # insert item in doing list
    insert(collection, doing_list_id, item_id, item['card_name'], item['card_desc'])


def complete_item(collection, item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    # get doing items
    doing_cards = get_list(collection, doing_list_id)['cards']
    # filter with list comprehension
    filtered_list = [x for x in doing_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from doing list
    delete(collection, doing_list_id, item_id)
    # insert item in done list
    insert(collection, done_list_id, item_id, item['card_name'], item['card_desc'])


def undo_item(collection, item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    # get done items
    done_cards = get_list(collection, done_list_id)['cards']
    # filter with list comprehension
    filtered_list = [x for x in done_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from done list
    delete(collection, done_list_id, item_id)
    # insert item in doing list
    insert(collection, doing_list_id, item_id, item['card_name'], item['card_desc'])


def stop_item(collection, item_id):
    """
    Moves a card to the 'To Do' list of the board.
    """
    # get doing items
    doing_cards = get_list(collection, doing_list_id)['cards']
    # filter with list comprehension
    filtered_list = [x for x in doing_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from doing list
    delete(collection, doing_list_id, item_id)
    # insert item in todo list
    insert(collection, todo_list_id, item_id, item['card_name'], item['card_desc'])

