from ConsistencyModel import ConsistencyModel
from ConsistencyModel import ConsistencyField

import passport_reader
import game_starter
import base64
import io




def inconsistent_handler(field: ConsistencyField):
    print("Inconsistency detected!")

cm = ConsistencyModel(inconsistent_handler)


data = game_starter.game_starter()

image = io.BytesIO(base64.b64decode(data['client_data']['passport'], validate=True))

passport_reader.read_passport(cm, image)
