import json
import os
import time

CONFIG_PATH = "/data/options.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def main():
    config = load_config()
    selected_lights = config.get("lights", [])
    
    print("Selected lights:")
    for light in selected_lights:
        print(f" - {light}")

    # Example: you could flash the lights here or just print every 5 seconds
    while True:
        print("Sync loop running... (add your music logic here)")
        time.sleep(5)

if __name__ == "__main__":
    main()