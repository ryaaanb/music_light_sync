import json
import os
import requests
import time

CONFIG_PATH = "/data/options.json"
HA_API_URL = "http://supervisor/core/api"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('SUPERVISOR_TOKEN')}",
    "Content-Type": "application/json"
}

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def get_all_lights():
    url = f"{HA_API_URL}/states"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        entities = response.json()
        lights = [entity for entity in entities if entity["entity_id"].startswith("light.")]
        print(f"Discovered {len(lights)} light entities:")
        for light in lights:
            print(f" - {light['entity_id']}")
        return lights
    except Exception as e:
        print(f"Error fetching lights: {e}")
        return []

def main():
    print("🔊 Starting Music Light Sync Add-on...")

    config = load_config()
    selected_lights = config.get("selected_lights", [])

    all_lights = get_all_lights()
    all_light_ids = [light["entity_id"] for light in all_lights]

    if not selected_lights:
        print("⚠️ No lights selected in config. Using all available lights.")
        selected_lights = all_light_ids
    else:
        print("✅ Selected lights from config:")
        for light in selected_lights:
            if light in all_light_ids:
                print(f" - {light}")
            else:
                print(f" ⚠️ Warning: {light} not found in Home Assistant")

    # Simulate music-light sync logic
    print("\n🎵 Music Light Sync is running... (add your sync logic here)")
    while True:
        time.sleep(5)

if __name__ == "__main__":
    main()
