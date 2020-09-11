from selenium import webdriver
import os
from threading import Thread
import pytest
import requests
import trello_items as trello
from dotenv import load_dotenv, find_dotenv
import app
import time

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable 
    # Use our real config 
    file_path = find_dotenv('./.env')
    load_dotenv(file_path, override=True)
    board_id = create_trello_board('Test Board')
    os.environ['TRELLO_BOARD_ID'] = board_id
    # construct the new application
    application = app.create_app()
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False)) 
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1) 
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app): 
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    #Create new item
    # els = driver.find_elements_by_tag_name("td")
    # for el in els:
    #     print(el)
    # print(driver.page_source)
    # assert len(els) == 0
    input1 = driver.find_element_by_id("title-input")
    input2 = driver.find_element_by_id("description-input")
    # input1.text = "Clean room"
    # input2.text = "Tidy room and wipe desk"
    btn = driver.find_element_by_id("create-btn")
    btn.click()
    time.sleep(2)
    # print(driver.page_source)
    els = driver.find_elements_by_tag_name("td")
    # for el in els:
    #     print(el)
    # assert len(els) == 1
    # print(els[0])

def create_trello_board(name):
    """
    Creates a new board with given name.

    Returns:
        The id of the newly created board.
    """
    url = "https://api.trello.com/1/boards"
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN'),
        'name': name
    }
    response = requests.request("POST", url, params=query)
    return response.json()['id']


def delete_trello_board(board_id):
    """
    Deletes a board with given id. Returns nothing.
    """
    url = "https://api.trello.com/1/boards/{}".format(board_id)
    query = {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('API_TOKEN')
    }
    requests.request("DELETE", url, params=query)
