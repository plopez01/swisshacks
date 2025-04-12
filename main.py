from ConsistencyModel import *

import passport_reader
import pdf_decoder
from description_extracter import extract_docx_text_from_base64
from docx_extracter import docx_extracter

import api

import time

def inconsistent_handler(old_document: str, document: str, htruth: ConsistencyField, new_val: str, reason: str):
    print(f"Inconsistent field: {htruth.name}, reason: {reason} \"{htruth.truth}\" ({old_document}) differs from \"{new_val}\" ({document})")

cm = InconsistencyCounterModel(inconsistent_handler)

gamedata = api.start_game()
session = gamedata['session_id']

status = "active"

while status != "gameover":
    try:
        cm.set_document("passport")
        passport_reader.read_passport(cm, gamedata['client_data']['passport'])

        cm.set_document("profile")
        docx_extracter(cm, gamedata['client_data']['profile'])


        gamedata = api.submit_decision(cm.inconsistencies == 0, session, gamedata['client_id'])
        
        status = gamedata['status']

        print(f"Status: {status}")
        print(f"Score: {gamedata['score']}")

        time.sleep(0.5)
    except Exception as e:
        print(e.with_traceback())
        print("ERROR DETECTED, STOPPING")
        passport_reader.decode_passport(gamedata['client_data']['passport']).save('error_passport.png')
        break



