import requests
import os
from pathlib import Path

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
        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    game_starter()

