from selenium import webdriver
import os
from threading import Thread
import pytest
import requests
import items as mongoDB
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
    os.environ['BOARD_ID'] = 'board_id'
    os.environ['LOGIN_DISABLED'] = 'True'
    application = app.create_app()
    collection = app.get_collection()
    create_board(collection)
    # start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False)) 
    thread.daemon = True
    thread.start()
    yield app
    # Tear Down
    thread.join(1) 
    delete_board(collection)

# THIS IS USED TO RUN THE E2E TESTS IN DOCKER CONTAINER
@pytest.fixture(scope='module') 
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless') 
    opts.add_argument('--no-sandbox') 
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver

# UNCOMMENT THIS TO RUN THE E2E TESTS LOCALLY - COMMENT THE ABOVE
# @pytest.fixture(scope='module') 
# def driver():
#     with webdriver.Firefox() as driver:
#         driver.implicitly_wait(2)
#         yield driver

def test_task_journey(driver, test_app): 
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'
    #Create new item
    driver.find_element_by_id("title-input").send_keys("Clean room")
    driver.find_element_by_id("description-input").send_keys("Tidy room and wipe desk")
    driver.find_element_by_id("create-btn").click()
    els = driver.find_elements_by_tag_name("td")
    assert len(els) == 5
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "todo"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Start item
    driver.find_element_by_class_name("start-btn").click()
    time.sleep(3) # sleep for 3 seconds
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "doing"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Complete item
    driver.find_element_by_class_name("complete-btn").click()
    time.sleep(3) # sleep for 3 seconds
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "done"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Undo item
    driver.find_element_by_class_name("undo-btn").click()
    time.sleep(3) # sleep for 3 seconds
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "doing"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"
    #Stop item
    driver.find_element_by_class_name("stop-btn").click()
    time.sleep(3) # sleep for 3 seconds
    assert driver.find_element_by_xpath("//td[2]").text == "Clean room"
    assert driver.find_element_by_xpath("//td[3]").text == "todo"
    assert driver.find_element_by_xpath("//td[4]").text == "Tidy room and wipe desk"


def create_board(collection):
    """
    Creates documents representing our lists and inserts these into our collection.
    """
    collection.insert_one(
        {
            'board_id': 'board_id',
            'list_id': 'todo_list_id',
            'list_name': 'todo',
            'cards': []
        }
    )
    collection.insert_one(
        {
            'board_id': 'board_id',
            'list_id': 'doing_list_id',
            'list_name': 'doing',
            'cards': []
        }
    )
    collection.insert_one(
        {
            'board_id': 'board_id',
            'list_id': 'done_list_id',
            'list_name': 'done',
            'cards': []
        }
    )


def delete_board(collection):
    """
    Deletes all document that have been created for the test. Returns nothing.
    """
    collection.delete_many( { 'board_id': 'board_id' } )