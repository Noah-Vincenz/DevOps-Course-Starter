class ViewModel:

    def __init__(self, todo_items, doing_items, done_items):
        self._todo_items = todo_items
        self._doing_items = doing_items
        self._done_items = done_items

    @property
    def todo_items(self):
        return self._todo_items

    @property
    def doing_items(self):
        return self._doing_items

    @property
    def done_items(self):
        return self._done_items