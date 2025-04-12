from ConsistencyModel import *

import passport_reader
import pdf_decoder
from description_extracter import extract_docx_text_from_base64
from docx_extracter import docx_extracter

import api

import time

def inconsistent_handler(field: ConsistencyField, reason: str):
    print(f"Inconsistent field: {field.name}, reason: {reason}")

cm = InconsistencyCounterModel(inconsistent_handler)

gamedata = api.start_game()
session = gamedata['session_id']

status = "active"

while status != "gameover":
    try:
        passport_reader.read_passport(cm, gamedata['client_data']['passport'])
        docx_extracter(cm, gamedata['client_data']['profile'])

        gamedata = api.submit_decision(cm.inconsistencies == 0, session, gamedata['client_id'])
        
        status = gamedata['status']

        print(f"Status: {status}")
        print(f"Score: {gamedata['score']}")

        time.sleep(0.5)
    except Exception as e:
        print(e)
        print("ERROR DETECTED, STOPPING")
        passport_reader.decode_passport(gamedata['client_data']['passport']).save('./log/error_passport.png')
        break



