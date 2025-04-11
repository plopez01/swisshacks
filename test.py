from ConsistencyModel import ConsistencyModel
from ConsistencyModel import ConsistencyField


def inconsistent_handler(field: ConsistencyField):
    print("Inconsistency detected!")

cm = ConsistencyModel(inconsistent_handler)

