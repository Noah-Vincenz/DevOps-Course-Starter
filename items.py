from flask import session
import requests
import os
from card import Card
import sys
import uuid
from datetime import date
from pprint import pprint

def get_items(collection, board_id):
    """
    Fetches all cards from mongoDB collection.

    Returns:
        list: The nested list of cards containing all cards constructed using the Card class.
    """
    todo_cards = []
    doing_cards = []
    done_cards = []
    for list_elem in get_board(collection, board_id)['lists']:
        for card in list_elem['cards']:
            list_name = list_elem['name']
            new_card = Card(card['card_id'], card['name'], card['desc'], list_name, card['dateLastActivity'])
            if list_name == "todo":
                todo_cards.append(new_card)
            elif list_name == "doing":
                doing_cards.append(new_card)
            else:
                done_cards.append(new_card)
    return [todo_cards, doing_cards, done_cards]


def get_board(collection, board_id):
    """
    Fetches a given board by id from the DB.

    Returns:
        board: The board with the given id.
    """
    return collection.find_one({ 'board_id': board_id })


def insert(collection, board_id, list_index, item_id, title, description):
    """
    Creates a card in the TO DO list of the board.
    """
    collection.update_one(
        { 'board_id': board_id },
        { '$push': {
            'lists.{}.cards'.format(list_index): {
                'card_id': item_id,
                'name': title,
                'desc': description,
                'dateLastActivity': str(date.today())
            }
        }}
    )


def delete(collection, board_id, list_index, item_id):
    """
    Removes a card from the given list (by index) of the board.
    """
    collection.update_one(
        { 'board_id': board_id },
        { '$pull': {
            'lists.{}.cards'.format(list_index): {
                'card_id': item_id
            }
        }}
    )


def create_item(collection, board_id, title, description):
    """
    Creates a card in the TO DO list of the board.
    """
    insert(collection, board_id, 0, str(uuid.uuid4()), title, description)

    
def start_item(collection, board_id, item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    # get todo items
    todo_cards = get_board(collection, board_id)['lists'][0]['cards']
    # filter with list comprehension
    filtered_list = [x for x in todo_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from todo list
    delete(collection, board_id, 0, item_id)
    # insert item in doing list
    insert(collection, board_id, 1, item_id, item['name'], item['desc'])


def complete_item(collection, board_id, item_id):
    """
    Moves a card to the 'DONE' list of the board.
    """
    # get doing items
    doing_cards = get_board(collection, board_id)['lists'][1]['cards']
    # filter with list comprehension
    filtered_list = [x for x in doing_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from doing list
    delete(collection, board_id, 1, item_id)
    # insert item in done list
    insert(collection, board_id, 2, item_id, item['name'], item['desc'])


def undo_item(collection, board_id, item_id):
    """
    Moves a card to the 'DOING' list of the board.
    """
    # get done items
    done_cards = get_board(collection, board_id)['lists'][2]['cards']
    # filter with list comprehension
    filtered_list = [x for x in done_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from done list
    delete(collection, board_id, 2, item_id)
    # insert item in doing list
    insert(collection, board_id, 1, item_id, item['name'], item['desc'])


def stop_item(collection, board_id, item_id):
    """
    Moves a card to the 'To Do' list of the board.
    """
    # get doing items
    doing_cards = get_board(collection, board_id)['lists'][1]['cards']
    # filter with list comprehension
    filtered_list = [x for x in doing_cards if x['card_id'] == item_id]
    item = filtered_list[0]
    # remove item from doing list
    delete(collection, board_id, 1, item_id)
    # insert item in todo list
    insert(collection, board_id, 0, item_id, item['name'], item['desc'])

