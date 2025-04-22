import threading
import time
from web.app import start_flask_server

def main():
    print("🟢 Starting Music Light Sync Add-on...")

    # Start Flask server in background
    threading.Thread(target=start_flask_server, daemon=True).start()

    while True:
        time.sleep(10)

if __name__ == "__main__":
    main()
