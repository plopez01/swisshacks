from datetime import *

class ConsistencyField:
    def __init__(self, name, model):
        self.truth = None
        self.truth_source = None

        self.name = name
        self._model = model

    def check(self, val):
        assert self._model._document != None
        if self.truth == None:
            self.truth = val
            self.truth_source = self._model._document
            return True

        if self._check_impl(val):
            return True
        else:
            self.fail(val, "Inconsistent fields.")
            return False
    
    def fail(self, value, reason: str):
        self._model._handler(self.truth_source, self, value, reason)

    def _check_impl(self, val):
        return self.truth == val


# val is (year, month, day) number
class DateField(ConsistencyField):
    def check(self, val: datetime):        
        return self.truth == val
        