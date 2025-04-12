import requests
import os
from pathlib import Path
import json

with open('config.json') as f:
    config = json.load(f)

def start_game():
    endpoint = f"{config['api']['host']}/game/start"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{config['api']['key']}",
    }
    body = {
        "player_name": config['player_name'],
    }
    
    try:
        response = requests.post(endpoint, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()
        return result

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def submit_decision(veredict, session_id, client_id):
    endpoint = f"{config['api']['host']}/game/decision"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": f"{config['api']['key']}",
    }
    body = {
        "decision": "Accept" if veredict else "Reject",
        "session_id": session_id,
        "client_id": client_id
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
    print(start_game())

