from ConsistencyModel import ConsistencyField
from datetime import *

class DateField(ConsistencyField):
    def check(self, val: datetime):        
        return self.truth == val
        