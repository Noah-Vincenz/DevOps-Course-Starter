import trello_items as trello

def test_answer():
    assert len(trello.get_items()) == 3