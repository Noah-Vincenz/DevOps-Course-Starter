from flask import session
import requests
import os
from card import Card
import sys

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
    board = collection.find_one({'board_id': '5f297733b15e708b16d0b400'})
    for list_elem in board['lists']:
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


def get_all_boards():
    """
    Fetches all boards from Trello.

    Returns:
        list: The list of boards.
    """
    url = "https://api.trello.com/1/members/me/boards"
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN')
    }
    return requests.request("GET", url, params=query).json()


def get_all_lists_on_board(board_id):
    """
    Fetches all lists from a Trello board.

    Returns:
        list: The lists on the boards
    """
    url = "https://api.trello.com/1/boards/{}/lists".format(board_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN')
    }
    return requests.request("GET", url, params=query).json()


def get_list_name(card_id):
    """
    Gets the list name a specific card is in, based on the card's id.

    Returns:
        string: The list's name.
    """
    url = "https://api.trello.com/1/cards/{}/list".format(card_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN')
    }
    list = requests.request("GET", url, params=query)
    return list.json()['name']


def create_item(title, description):
    """
    Creates a card in the TO DO list of the board.

    Returns:
        Response object from requests.request representing a Card.
    """
    url = "https://api.trello.com/1/cards"
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'name': title, 
        'desc': description,
        'idList': os.getenv('TODO_LIST_ID')
    }
    response = requests.request("POST", url, params=query)
    return response


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
