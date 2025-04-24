from flask import Flask, render_template, request, redirect, url_for
import os, json, requests, time
import threading
import sounddevice as sd
import numpy as np
import threading

preview_thread = None
preview_running = False

app = Flask(__name__, template_folder="./templates")

HA_API_URL = "http://supervisor/core/api"
SELECTION_FILE = "./web/selected_lights.json"

def get_all_lights():
    token = os.getenv('SUPERVISOR_TOKEN')
    debug_output = []

    if not token:
        debug_output.append("❌ SUPERVISOR_TOKEN is missing!")
        return {}, debug_output
    else:
        debug_output.append(f"🔑 SUPERVISOR_TOKEN begins with: {token[:10]}...")

    try:
        r = requests.get(f"{HA_API_URL}/states", headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        r.raise_for_status()
        entities = r.json()
        debug_output.append(f"✅ Found {len(entities)} entities total.")

        room_map = {}

        for entity in entities:
            if entity["entity_id"].startswith("light."):
                entity_id = entity["entity_id"]
                attrs = entity.get("attributes", {})
                room = attrs.get("room", attrs.get("friendly_name", "Ungrouped")).split()[0]
                name = attrs.get("friendly_name", entity_id)
                room_map.setdefault(room, []).append((entity_id, name))

        debug_output.append(f"🏠 Grouped into {len(room_map)} room(s).")
        return room_map, debug_output

    except Exception as e:
        debug_output.append(f"❌ Error fetching lights: {e}")
        return {}, debug_output

def flash_light(light_id):
    print(f"⚡ Simulating flash for: {light_id}")
    
    token = os.getenv('SUPERVISOR_TOKEN')
    if not token:
        print("❌ No SUPERVISOR_TOKEN for flashing!")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        requests.post("http://supervisor/core/api/services/light/turn_off", headers=headers, json={
            "entity_id": light_id
        })
        time.sleep(0.3)
        requests.post("http://supervisor/core/api/services/light/turn_on", headers=headers, json={
            "entity_id": light_id
        })
        print("✅ Flash simulated.")
    except Exception as e:
        print(f"❌ Simulated flash failed for {light_id}: {e}")

@app.route("/preview", methods=["POST"])
def preview():
    global preview_thread, preview_running
    selected = request.json.get("lights", [])
    print(f"🌈 Starting preview on: {selected}")

    def cycle_colors():
        global preview_running
        preview_running = True
        token = os.getenv("SUPERVISOR_TOKEN")
        if not token:
            print("❌ No token for preview.")
            return

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        hue = 0
        while preview_running:
            for light in selected:
                hs_color = [hue % 360, 100]
                requests.post("http://supervisor/core/api/services/light/turn_on", headers=headers, json={
                    "entity_id": light,
                    "hs_color": hs_color,
                    "brightness": 200
                })
            hue += 30
            time.sleep(1)

    if preview_thread and preview_thread.is_alive():
        preview_running = False
        preview_thread.join()

    preview_thread = threading.Thread(target=cycle_colors, daemon=True)
    preview_thread.start()
    return ("", 204)

        
@app.route("/flash/<light_id>", methods=["POST"])
def flash(light_id):
    flash_light(light_id)
    return ("", 204)

@app.route("/beat", methods=["POST"])
def beat():
    token = os.getenv("SUPERVISOR_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        with open(SELECTION_FILE, "r") as f:
            selected = json.load(f).get("lights", [])
    except:
        selected = []

    hue = int(time.time() * 1000) % 360

    for light in selected:
        requests.post("http://supervisor/core/api/services/light/turn_on", headers=headers, json={
            "entity_id": light,
            "hs_color": [hue, 100],
            "brightness": 255
        })

    return ("", 204)

@app.route("/smart", methods=["POST"])
def smart_mode():
    mode = request.json.get("mode")
    print(f"🤖 Smart mode: {mode}")

    token = os.getenv("SUPERVISOR_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        with open(SELECTION_FILE, "r") as f:
            selected = json.load(f).get("lights", [])
    except:
        selected = []

    if mode == "fade":
        for light in selected:
            requests.post("http://supervisor/core/api/services/light/turn_on", headers=headers, json={
                "entity_id": light,
                "brightness": 0,
                "transition": 2
            })

    elif mode == "strobe":
        for light in selected:
            requests.post("http://supervisor/core/api/services/light/turn_on", headers=headers, json={
                "entity_id": light,
                "brightness": 255,
                "hs_color": [int(time.time() * 1000) % 360, 100]
            })

    return ("", 204)


@app.route("/stop_all", methods=["POST"])
def stop_all():
    global preview_running, media_running
    print("🛑 Stopping all effects...")
    preview_running = False
    media_running = False
    return ("", 204)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    lights = {}
    current = []
    debug_output = []

    if request.method == "POST":
        if "fetch" in request.form:
            lights, debug_output = get_all_lights()
        elif "save" in request.form:
            selected = request.form.getlist("lights")
            with open(SELECTION_FILE, "w") as f:
                json.dump({"lights": selected}, f)
            message = "✅ Lights saved!"
            current = selected
        elif "load" in request.form:
            message = "📦 Loaded previous selection."
        else:
            message = "⚠️ Unknown action."

    try:
        with open(SELECTION_FILE, "r") as f:
            current = json.load(f).get("lights", [])
    except:
        pass

    if not lights:
        lights, debug_output = get_all_lights()

    return render_template("index.html", lights=lights, current=current, message=message, debug_output=debug_output)

def start_flask_server():
    print("✅ Flask server starting...")
    app.run(host="0.0.0.0", port=5000)

