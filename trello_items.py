from flask import session
import requests
import config
import os
from card import Card

key = config.key
token = config.token
todo_list_id = config.todo_list_id
done_list_id = config.done_list_id

def get_items():
    """
    Fetches all cards from Trello.

    Returns:
        list: The list of cards constructed using the Card class.
    """
    url1 = "https://api.trello.com/1/members/me/boards"
    query = {
        'key': key,
        'token': token
    }
    boards = requests.request("GET", url1, params=query)
    all_cards = []
    for board in boards.json():
        board_id = board['id']
        url2 = "https://api.trello.com/1/boards/{}/cards".format(board_id)
        cards = requests.request("GET", url2, params=query)
        for card in cards.json():
            all_cards.append(Card(card['id'], card['pos'], card['name'], card['desc'], get_list_name(card['id'])))
    return all_cards


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
    Moves a card to the 'TODO' list of the board.
    """
    id_list = todo_list_id # this is the id for the 'To Do' list
    url = "https://api.trello.com/1/cards/{}".format(item_id)
    query = {
        'key': key,
        'token': token,
        'idList': id_list
    }
    requests.request("PUT", url, params=query)