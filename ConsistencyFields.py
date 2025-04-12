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
            self.fail(val, "Inconsistent fields.")
            return False
    
    def fail(self, value, reason: str):
        self._inconsistent_handler(self, f"{reason} \"{self.truth}\" differs from \"{value}\"")

    def _check_impl(self, val):
        return self.truth == val


# val is (year, month, day) number
class DateField(ConsistencyField):
    def check(self, val: datetime):        
        return self.truth == val
        