import requests
import random
import socket
import time
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
URL = os.getenv("CRIBL_URL") 
BEARER_TOKEN = os.getenv("CRIBL_BEARER")
BATCH_SIZE = 5
SLEEP_SECONDS = 5

# HTTP headers
headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Content-Type": "text/plain"  
}

# Random data sources
levels = ["INFO", "WARN", "ERROR", "DEBUG"]
users = [f"user{i}" for i in range(1, 50)]
services = [f"service{i}" for i in range(1, 10)]
messages = [
    "User login successful", "Disk space low", "Service stopped",
    "Memory usage normal", "CPU usage high"
]

# Event generator
def generate_event():
    ts = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    level = random.choice(levels)
    msg = random.choice(messages)
    user = random.choice(users)
    service = random.choice(services)
    return f"{ts} {level} {msg} - {user} - {service}"

# Main loop
try:
    while True:
        batch_events = [generate_event() for _ in range(BATCH_SIZE)]
        payload = "\n".join(batch_events)
        response = requests.post(URL, headers=headers, data=payload)

        print(f"[Batch] Sent {BATCH_SIZE} events → Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response Text: {response.text}")

        print(f"Sleeping {SLEEP_SECONDS}s...\n")
        time.sleep(SLEEP_SECONDS)

except KeyboardInterrupt:
    print("Stream stopped by user.")
