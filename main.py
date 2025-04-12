from ConsistencyModel import *

import passport_reader
import pdf_decoder

import api
import base64
import io

def inconsistent_handler(field: ConsistencyField, reason: str):
    print(f"Inconsistent field: {field.name}, reason: {reason}")

cm = InconsistencyCounterModel(inconsistent_handler)

game = api.start_game()

passport_reader.read_passport(cm, game['client_data']['passport'])

print(api.submit_decision(cm.inconsistencies == 0, game['session_id'], game['client_id']))



