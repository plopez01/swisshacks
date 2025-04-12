from datetime import *

class ConsistencyField:
    def __init__(self, name, inconsistent_handler):
        self.truth = None
        self.name = name
        self._inconsistent_handler = inconsistent_handler

    def check(self, val):
        if self.truth == None:
            self.truth = val
            return True

        if self._check_impl(val):
            return True
        else:
            self.fail(self, "Inconsistent fields.")
            return False
    
    def fail(self, reason: str):
        self._inconsistent_handler(self, reason)

    def _check_impl(self, val):
        return self.truth == val


class DateField(ConsistencyField):
    def check(self, val: datetime):        
        return self.truth == val
        