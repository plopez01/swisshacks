from ConsistencyModel import *

import passport_reader
import pdf_decoder
import description_extracter
import description_llm

from description_extracter import extract_docx_text_from_base64
from docx_extracter import docx_extracter

import api
import time
from colors import *

def inconsistent_handler(field: ConsistencyField, reason: str):
    if field.discrepancy_level == 1:
        print(colors.WARNING, end='')
    else:
        print(colors.FAIL, end='')

    print(f"Inconsistent field: {field.name}, reason: {reason} \"{field.postulate}\" ({field.postulate_source}) differs from \"{field.discrepancy}\" ({field.discrepancy_source}){colors.ENDC}")

def debug():
    passport_reader.decode_passport(gamedata['client_data']['passport']).save('error_passport.png')


gamedata = api.start_game()
session = gamedata['session_id']

status = "active"

while status != "gameover":
    try:
        debug()
        cm = InconsistencyCounterModel(inconsistent_handler)
        #cm.set_document("passport")
        #passport_reader.read_passport(cm, gamedata['client_data']['passport'])

        cm.set_document("account")
        pdf_decoder.decode(cm, gamedata['client_data']['account'])

        cm.set_document("profile")
        docx_extracter(cm, gamedata['client_data']['profile'])

        description = description_extracter.extract_docx_text_from_base64(gamedata['client_data']['description'])
        llm_out = description_llm.check_consistency(cm, cm.to_string(), description)

        if llm_out != "[]":
            print(llm_out)
            cm.llm_description.fail("LLM Found inconsistencies")
            print(f"INCONSITENCIAS ARE {cm.inconsistencies}")

        print("Accepting" if cm.inconsistencies == 0 else "Rejecting")
        gamedata = api.submit_decision(cm.inconsistencies == 0, session, gamedata['client_id'])

        status = gamedata['status']

        if (status == "gameover"):
            cm.print()

        print(f"Status: {status}")
        print(f"Score: {gamedata['score']}")

        print()
        time.sleep(3)
    except Exception as e:
        print(e.with_traceback())
        print("ERROR DETECTED, STOPPING")
        passport_reader.decode_passport(gamedata['client_data']['passport']).save('error_passport.png')
        break



