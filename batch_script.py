import requests
import random
import time
import os
import json
from datetime import datetime, timezone
from dotenv import load_dotenv
import socket

load_dotenv()

URL = os.getenv("CRIBL_URL")
HEC_TOKEN = os.getenv("CRIBL_BEARER")
BATCH_SIZE = 5
SLEEP_SECONDS = 5

headers = {
    "Authorization": f"Bearer {HEC_TOKEN}",
    "Content-Type": "application/json"
}

levels = ["INFO", "WARN", "ERROR", "DEBUG"]
users = [f"user{i}" for i in range(1, 51)]
services = [f"service{i}" for i in range(1, 10)]
messages = [
    "User login successful", "Disk space low", "Service stopped",
    "Memory usage normal", "CPU usage high", "Database connection established",
    "Cache miss occurred", "API request processed",
    "File uploaded successfully", "Network timeout detected"
]

def generate_log_line():
    ts = datetime.now(timezone.utc).isoformat()
    return f"{ts} {random.choice(levels)} {random.choice(messages)} - {random.choice(users)} - {random.choice(services)}"

def send_log_batch():
    logs = [generate_log_line() for _ in range(BATCH_SIZE)]
    events = [{
        "time": int(datetime.now(timezone.utc).timestamp()),
        "host": socket.gethostname(),
        "source": "python_batch_generator",
        "sourcetype": "random_logs",
        "event": log
    } for log in logs]

    payload = "\n".join(json.dumps(e) for e in events)

    try:
        r = requests.post(URL, headers=headers, data=payload, timeout=5)
        if r.ok:
            print(f"Sent {BATCH_SIZE} logs | Sample: {logs[0]}")
            return True
        else:
            print(f"Error {r.status_code}: {r.text.strip()[:100]}")
    except Exception as e:
        print(f"Request error: {e}")

    return False

if __name__ == "__main__":
    print("Starting log generator (Ctrl+C to stop)")
    count = success = 0

    try:
        while True:
            count += 1
            if send_log_batch():
                success += 1
            time.sleep(SLEEP_SECONDS)
    except KeyboardInterrupt:
        print("\nStopped by user")
        print(f"Batches sent: {success}/{count}")
        print(f"Total logs: {success * BATCH_SIZE}")
