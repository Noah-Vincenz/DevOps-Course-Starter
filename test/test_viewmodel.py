from viewmodel import ViewModel
import dateutil.parser
from card import Card

vm = ViewModel(["some todo items"], ["some doing items"], ["some done items"])
today_mock = dateutil.parser.parse('2020-09-02 00:16:26.061713')

def test_todo_items():
    assert vm.todo_items == ["some todo items"]
    vm.todo_items = ["some other todo items"]
    assert vm.todo_items == ["some other todo items"]

def test_doing_items():
    assert vm.doing_items == ["some doing items"]
    vm.doing_items = ["some other doing items"]
    assert vm.doing_items == ["some other doing items"]

def test_done_items():
    assert vm.done_items == ["some done items"]
    vm.done_items = ["some other done items"]
    assert vm.done_items == ["some other done items"]

def test_same_date_same():
    last_modified = '2020-09-02 12:16:26.061713'
    assert vm.same_date(last_modified, today_mock)

def test_same_date_same_day():
    last_modified = '2020-09-02 12:16:26.061713'
    assert vm.same_date(last_modified, today_mock)

def test_same_date_different_day():
    last_modified = '2020-09-01 12:16:26.061713'
    assert not vm.same_date(last_modified, today_mock)

def test_older_date_same():
    last_modified = '2020-09-02 12:16:26.061713'
    assert not vm.older_date(last_modified, today_mock)

def test_older_date_same_day():
    last_modified = '2020-09-02 12:16:26.061713'
    assert not vm.older_date(last_modified, today_mock)

def test_older_date_different_day():
    last_modified = '2020-08-30 12:16:26.061713'
    assert vm.older_date(last_modified, today_mock)

def test_recent_done_items_empty_list(monkeypatch):
    items = []
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.recent_done_items(items)
    assert result_list == []

def test_recent_done_items_empty(monkeypatch):
    card1 = Card("id", "name", "description", "status", "2020-09-01 12:16:26.061713")
    card2 = Card("id", "name", "description", "status", "2020-09-01 11:16:26.061713")
    card3 = Card("id", "name", "description", "status", "2020-09-01 12:16:26.061713")
    items = [card1, card2, card3]
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.recent_done_items(items)
    assert result_list == []

def test_recent_done_items_single(monkeypatch):
    card1 = Card("id", "name", "description", "status", "2020-09-01 12:16:26.061713")
    card2 = Card("id", "name", "description", "status", "2020-09-01 11:16:26.061713")
    card3 = Card("id", "name", "description", "status", "2020-09-02 12:16:26.061713")
    items = [card1, card2, card3]
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.recent_done_items(items)
    assert result_list == [card3]

def test_recent_done_items_double(monkeypatch):
    card1 = Card("id", "name", "description", "status", "2020-09-01 12:16:26.061713")
    card2 = Card("id", "name", "description", "status", "2020-09-02 11:16:26.061713")
    card3 = Card("id", "name", "description", "status", "2020-09-02 12:16:26.061713")
    items = [card1, card2, card3]
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.recent_done_items(items)
    assert result_list == [card2, card3]

def test_old_done_items_empty_list(monkeypatch):
    items = []
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.old_done_items(items)
    assert result_list == []

def test_old_done_items_empty(monkeypatch):
    card1 = Card("id", "name", "description", "status", "2020-09-03 12:16:26.061713")
    card2 = Card("id", "name", "description", "status", "2020-09-03 11:16:26.061713")
    card3 = Card("id", "name", "description", "status", "2020-09-03 12:16:26.061713")
    items = [card1, card2, card3]
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.old_done_items(items)
    assert result_list == []

def test_old_done_items_single(monkeypatch):
    card1 = Card("id", "name", "description", "status", "2020-09-01 12:16:26.061713")
    card2 = Card("id", "name", "description", "status", "2020-09-02 11:16:26.061713")
    card3 = Card("id", "name", "description", "status", "2020-09-02 12:16:26.061713")
    items = [card1, card2, card3]
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.old_done_items(items)
    assert result_list == [card1]

def test_old_done_items_double(monkeypatch):
    card1 = Card("id", "name", "description", "status", "2020-09-01 12:16:26.061713")
    card2 = Card("id", "name", "description", "status", "2020-09-01 11:16:26.061713")
    card3 = Card("id", "name", "description", "status", "2020-09-02 12:16:26.061713")
    items = [card1, card2, card3]
    monkeypatch.setattr(ViewModel, 'today', lambda self: today_mock)
    result_list = vm.old_done_items(items)
    assert result_list == [card1, card2]