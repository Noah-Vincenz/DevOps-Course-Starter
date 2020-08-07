from flask import session
import requests
import config
import os

def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    url1 = "https://api.trello.com/1/members/me/boards"
    query = {
        'key': config.key,
        'token': config.token
    }
    boards = requests.request(
        "GET",
        url1,
        params=query
    )
    all_cards = []
    for board in boards.json():
        board_id = board['id']
        print(board_id)
        url2 = "https://api.trello.com/1/boards/{}/cards".format(board_id)
        cards = requests.request(
            "GET",
            url2,
            params=query
        )
        for card in cards.json():
            all_cards.append(Card(card['pos'], card['name'], get_list(card['id'])))
    return all_cards


def get_list(card_id):
    url = "https://api.trello.com/1/cards/{}/list".format(card_id)
    query = {
        'key': config.key,
        'token': config.token
    }
    list = requests.request(
        "GET",
        url,
        params=query
    )
    return list.json()['name']


def get_lists_map(board_id):
    url1 = "https://api.trello.com/1/boards/{}/lists".format(board_id)
    query = {
        'key': config.key,
        'token': config.token
    }
    lists = requests.request(
        "GET",
        url1,
        params=query
    )
    dict = {}
    print(lists)
    print(lists.json())
    for list in lists.json():
        dict[list.id] = list.name
    return dict


def create_item(title):
    """
    Creates a card in the TO DO list of the board.
    """
    print(get_lists_on_board("5f2977346edfad5675e78f48"))
    url = "https://api.trello.com/1/cards"
    query = {
        'key': config.key,
        'token': config.token,
        'name': title, 
        'desc': "CARD_DESC",
        'pos': "top", 
        'idList': "TRELLO_BOARD_LIST_ID"
    }
    item = requests.request(
        "PUT",
        url,
        params=query
    )
    return item


class Card:
    def __init__(self, position, name, status):
        self.position = position
        self.name = name
        self.status = status