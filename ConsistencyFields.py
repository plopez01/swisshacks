from datetime import *
from unidecode import unidecode

class ConsistencyField:
    def __init__(self, name, model):
        self.postulate: str = None
        self.postulate_source = None
        
        self.discrepancy: str = None
        self.discrepancy_source = None
        self.discrepancy_level = 0

        self.name = name
        self.model = model

    def check(self, val: str):
        # Document source must be set
        assert self.model.document != None

        if self.postulate == None:
            self.postulate = val
            self.postulate_source = self.model.document
            return True

        if self._check_impl(self.postulate, val):
            return True
        else:
            self.discrepancy = val
            self.discrepancy_source = self.model.document

            if type(self.postulate) == str and self._check_impl(unidecode(self.postulate.lower().strip()), unidecode(val.lower().strip())):
                self.discrepancy_level = 1
                self.fail("Inconsistent casing/accents.")
            else:
                self.discrepancy_level = 2
                self.fail("Inconsistent fields.")

            return False
    
    def fail(self, reason):
        self.discrepancy_level = 2
        self.model._handler(self, reason)

    def _check_impl(self, postulate, val):
        return postulate == val


# val is (year, month, day) number
class DateField(ConsistencyField):
    def _check_impl(self, postulate, val: datetime):        
        return postulate == val
        