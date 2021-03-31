from flask import session
import requests
import os
from card import Card
import sys
import uuid
from datetime import date

def get_items(collection):
    """
    Fetches all cards from mongoDB collection.

    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    todo_cards = []
    doing_cards = []
    done_cards = []
    board_id = os.getenv('BOARD_ID')
    for list_elem in get_board(collection, board_id)['lists']:
        for card in list_elem['cards']:
            list_name = list_elem['name']
            new_card = Card(card['id'], card['name'], card['desc'], list_name, card['dateLastActivity'])
            if list_name == "todo":
                todo_cards.append(new_card)
            elif list_name == "doing":
                doing_cards.append(new_card)
            else:
                done_cards.append(new_card)
    return [todo_cards, doing_cards, done_cards]


def get_board(collection, boardId):
    """
    Fetches a given board by id from the DB.

    Returns:
        board: The board with the given id.
    """
    return collection.find_one({'board_id': boardId})


def create_item(collection, title, description):
    """
    Creates a card in the TO DO list of the board.

    Returns:
        Response object from requests.request representing a Card.
    """
    board_id = os.getenv('BOARD_ID')
    collection.update_one(
        { 'board_id': board_id },
        { '$push': {
            'lists.0.cards': {
                'id': str(uuid.uuid4()),
                'name': title,
                'desc': description,
                'dateLastActivity': str(date.today())
            }
        }}
    )


def start_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('DOING_LIST_ID')
    }
    return requests.request("PUT", url, params=query)


def complete_item(item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('DONE_LIST_ID')
    }
    return requests.request("PUT", url, params=query)


def undo_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('DOING_LIST_ID')
    }
    return requests.request("PUT", url, params=query)


def stop_item(item_id):
    """
    Moves a card to the 'To Do' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('TODO_LIST_ID')
    }
    return requests.request("PUT", url, params=query)
