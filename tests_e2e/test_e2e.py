from selenium import webdriver
import os
from threading import Thread
import pytest
import requests
import trello_items as trello
from dotenv import load_dotenv, find_dotenv
import app
import time
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable 
    # Use our test e2e config instead of the 'real' version 
    file_path = find_dotenv('/.env')
    load_dotenv(file_path, override=True)
    board_id = create_trello_board('Test Board')
    update_env_vars(board_id)
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

def update_env_vars(board_id):
    os.environ['TRELLO_BOARD_ID'] = board_id
    lists = trello.get_all_lists_on_board(board_id)
    for list in lists:
        if list['name'] == 'To Do':
            os.environ['TODO_LIST_ID'] = list['id']
        elif list['name'] == 'Doing':
            os.environ['DOING_LIST_ID'] = list['id']
        else:
            os.environ['DONE_LIST_ID'] = list['id']


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver, test_app): 
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    #Create new item
    els = driver.find_elements_by_tag_name("td")
    assert len(els) == 0
    driver.find_element_by_id("title-input").send_keys("Clean room")
    driver.find_element_by_id("description-input").send_keys("Tidy room and wipe desk")
    driver.find_element_by_id("create-btn").click()
    time.sleep(1)
    els = driver.find_elements_by_tag_name("td")
    assert len(els) == 5
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "To Do"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Start item
    driver.find_element_by_id("start-btn").click()
    time.sleep(1)
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "Doing"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Complete item
    driver.find_element_by_id("complete-btn").click()
    time.sleep(1)
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "Done"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Undo item
    driver.find_element_by_id("undo-btn").click()
    time.sleep(1)
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "Doing"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"


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
