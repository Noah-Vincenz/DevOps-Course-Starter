from viewmodel import ViewModel

vm = ViewModel(["some todo items"], ["some doing items"], ["some done items"])

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