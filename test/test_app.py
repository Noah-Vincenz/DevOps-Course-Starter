import trello_items as trello
import pytest
import requests
from app import app
from dotenv import load_dotenv, find_dotenv
from card import Card
import os
from threading import Thread

@pytest.fixture(scope='module')
def test_app():
    # Create the new board & update the board id environment variable 
    board_id = trello.create_trello_board('Test Board')
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
    trello.delete_trello_board(board_id)

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = app
    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@pytest.mark.parametrize("items", [
    [[],[],[]], 
    [[Card("id", "Fix wifi", "Restart router to fix the wifi.", "To Do", "2019-10-03 12:16:26.061713")], [], []],
    [[], [Card("id", "Fix wifi", "Restart router to fix the wifi.", "Doing", "2019-10-03 12:16:26.061713")], []],
    [[], [], [Card("id", "Fix wifi", "Restart router to fix the wifi.", "Done", "2019-10-03 12:16:26.061713")]],
    [[Card("id", "Fix wifi", "Restart router to fix the wifi.", "To Do", "2019-10-03 12:16:26.061713")], [Card("id", "Fix wifi", "Restart router to fix the wifi.", "Doing", "2019-10-03 12:16:26.061713")], [Card("id", "Fix wifi", "Restart router to fix the wifi.", "Done", "2019-10-03 12:16:26.061713")]],
    [[Card("id", "Fix wifi", "Restart router to fix the wifi.", "To Do", "2019-10-03 12:16:26.061713"), Card("id", "Fix wifi", "Restart router to fix the wifi.", "To Do", "2019-10-03 12:16:26.061713")], [], []]
])
def test_index(client, monkeypatch, items):
    monkeypatch.setattr(trello, 'get_items', lambda: items)
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == "text/html; charset=utf-8"
  