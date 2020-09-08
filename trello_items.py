from flask import session
import requests
import os
from card import Card

key = os.getenv('API_KEY')
token = os.getenv('API_TOKEN')
todo_list_id = os.getenv('TODO_LIST_ID')
doing_list_id = os.getenv('DOING_LIST_ID')
done_list_id = os.getenv('DONE_LIST_ID')

def get_items():
    """
    Fetches all cards from Trello.

    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    boards = get_all_boards()
    todo_cards = []
    doing_cards = []
    done_cards = []
    for board in boards:
        cards = get_cards_from_board(board['id'])
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
        'key': key,
        'token': token
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
        'key': key,
        'token': token
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
        'key': key,
        'token': token
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
        'key': key,
        'token': token,
        'name': title, 
        'desc': description,
        'pos': len(get_items()) + 1, 
        'idList': todo_list_id # this is the id for the 'To Do' list
    }
    card = requests.request("POST", url, params=query)
    return card


def start_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    id_list = doing_list_id # this is the id for the 'Doing' list
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': key,
        'token': token,
        'idList': id_list
    }
    requests.request("PUT", url, params=query)


def complete_item(item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    id_list = done_list_id # this is the id for the 'Done' list
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': key,
        'token': token,
        'idList': id_list
    }
    requests.request("PUT", url, params=query)


def undo_item(item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    id_list = doing_list_id # this is the id for the 'Doing' list
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': key,
        'token': token,
        'idList': id_list
    }
    requests.request("PUT", url, params=query)


def stop_item(item_id):
    """
    Moves a card to the 'To Do' list of the board.
    """
    id_list = todo_list_id # this is the id for the 'To Do' list
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': key,
        'token': token,
        'idList': id_list
    }
    requests.request("PUT", url, params=query)