import trello_items as trello
import pytest
import requests
from app import create_app
from dotenv import load_dotenv, find_dotenv
from card import Card

@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version 
    file_path = find_dotenv('tests/unit_integration/.env.test')
    load_dotenv(file_path, override=True)
    # Create the new app.
    test_app = create_app()
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