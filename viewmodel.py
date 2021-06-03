from datetime import datetime
import dateutil.parser

class ViewModel:

    def __init__(self, roles, todo_items, doing_items, done_items):
        self._roles = roles
        self._todo_items = todo_items
        self._doing_items = doing_items
        self._done_items = done_items

    @property
    def roles(self):
        return self._roles

    @property
    def todo_items(self):
        return self._todo_items

    @property
    def doing_items(self):
        return self._doing_items

    @property
    def done_items(self):
        return self._done_items

    def recent_done_items(self, items):
        list_to_return = []
        for item in items:
            if self.same_date(item.last_modified, self.today()):
                list_to_return.append(item)
        return list_to_return
    
    def old_done_items(self, items):
        list_to_return = []
        for item in items:
            if self.older_date(item.last_modified, self.today()):
                list_to_return.append(item)
        return list_to_return

    def same_date(self, last_modified, today):
        date_obj = dateutil.parser.parse(last_modified)
        return date_obj.date() == today.date()

    def older_date(self, last_modified, today):
        date_obj = dateutil.parser.parse(last_modified)
        return date_obj.date() < today.date()

    def today(self):
        return datetime.today()