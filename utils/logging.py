import os
from datetime import datetime

def log_message(message = "Teste", step = "cryptography", message_type = "info"):
    prefix = f"[{message_type.upper()}]"
    entry_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = datetime.now().strftime('%Y-%m-%d')
    entry = f"{entry_timestamp} {prefix} @ {step}: {message}\n"

    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, f"{timestamp}.txt")
    
    try:
        with open(log_file, "a", encoding="utf-8") as file:
            file.write(entry)
    except Exception as e:
        print(f"Error when trying to write logs: {e}")