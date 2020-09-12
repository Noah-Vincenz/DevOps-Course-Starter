from flask import session
import requests
import os
from card import Card

def get_items():
    """
    Fetches all cards from our Trello board.

    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    todo_cards = []
    doing_cards = []
    done_cards = []
    board_id = os.getenv('TRELLO_BOARD_ID')
    cards = get_cards_from_board(board_id)
    for card in cards:
        list_name = get_list_name(card['id'])
        new_card = Card(card['id'], card['name'], card['desc'], list_name, card['dateLastActivity'])
        if list_name == "To Do":
            todo_cards.append(new_card)
        elif list_name == "Doing":
            doing_cards.append(new_card)
        else:
            done_cards.append(new_card)
    return [todo_cards, doing_cards, done_cards]


def get_cards_from_board(board_id):
    """
    Fetches all cards from a specific Trello board.

    Returns:
        list: The list of cards.
    """
    url = "https://api.trello.com/1/boards/{}/cards".format(board_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN')
    }
    return requests.request("GET", url, params=query).json()


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
    print(requests.request("GET", url, params=query).json())
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
        'pos': len(get_items()) + 1, 
        'idList': os.getenv('TODO_LIST_ID') # this is the id for the 'To Do' list
    }
    card = requests.request("POST", url, params=query)
    return card


def start_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('DOING_LIST_ID') # this is the id for the 'Doing' list
    }
    requests.request("PUT", url, params=query)


def complete_item(item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('DONE_LIST_ID') # this is the id for the 'Done' list
    }
    requests.request("PUT", url, params=query)


def undo_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('DOING_LIST_ID') # this is the id for the 'Doing' list
    }
    requests.request("PUT", url, params=query)


def stop_item(item_id):
    """
    Moves a card to the 'To Do' list of the board.
    """
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'idList': os.getenv('TODO_LIST_ID') # this is the id for the 'To Do' list
    }
    requests.request("PUT", url, params=query)
