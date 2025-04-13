from datetime import *
from unidecode import unidecode
import description_llm

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
                self.fail(1, "Inconsistent casing/accents.")
            else:
                self.fail(2, "Inconsistent fields.")

            return False
    
    def fail(self, level, reason):
        self.discrepancy_level = level
        self.model._handler(self, reason)

    def _check_impl(self, postulate, val):
        return postulate == val


# val is (year, month, day) number
class DateField(ConsistencyField):
    def _check_impl(self, postulate, val: datetime):        
        return postulate == val
    
class ContainsField(ConsistencyField):
    def _check_impl(self, postulate, val):        
        return postulate in val or val in postulate

class LLMField(ConsistencyField):
    def _check_impl(self, postulate, val):       
        result = description_llm.compare_fields(postulate, val)
        print(result)

        return result == "consistent"        