from ConsistencyModel import *

import passport_reader
import game_starter
import base64
import io




def inconsistent_handler(field: ConsistencyField, reason: str):
    print(f"Inconsistent field: {field.name}, reason: {reason}")

cm = ConsistencyModel(inconsistent_handler)

cm.name.check("Pau")
cm.name.check("Pau")
cm.name.fail("Wrong")

data = game_starter.game_starter()

image = io.BytesIO(base64.b64decode(data['client_data']['passport'], validate=True))

#passport_reader.read_passport(cm, image)
