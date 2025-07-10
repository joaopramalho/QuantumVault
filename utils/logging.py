from datetime import datetime

def log_message(message = "Teste", step = "cryptography", message_type = "info"):
    prefix = f"[{message_type}]"
    entry_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp = datetime.now().strftime('%Y-%m-%d')
    entry = f"{timestamp} {prefix} @ {step}: {message}\n"

    with open(f"{timestamp}.txt", "a") as file:
        file.write(entry)
        file.close()