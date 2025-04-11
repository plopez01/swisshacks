import requests
import os
from pathlib import Path
import base64, binascii


URL = "https://hackathon-api.mlo.sehlat.io"  # API endpoint

def game_starter():
    api_key = "JQvqqf9xxi6vhpIuCt0klxSDofYj7xFwZ5e0EjVgqfQ"
    endpoint = f"{URL}/game/start"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{api_key}",
    }
    body = {
        "player_name": "Fibers",
    }

    
    try:
        response = requests.post(endpoint, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()

        print("Game started successfully!")
        #print(f"Response: {result}")
        passport_value = result['client_data']['passport']
        print(passport_value)

        try:
            image = base64.b64decode(passport_value, validate=True)

            file_to_save = "password_image.png"
            with open(file_to_save, "wb") as f:
                f.write(image)
        except binascii.Error as e:
            print(e)

        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    game_starter()
