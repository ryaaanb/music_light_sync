# 🎵 Music Light Sync – Home Assistant Add-on

**Sync your smart lights to music in real time using your browser’s microphone.**  
This add-on detects beats and audio energy to create light effects that match the rhythm of your music — all from inside Home Assistant.

> ⚠️ **Work in Progress**  
> This is an early prototype and still very basic. Expect rough edges and limited functionality for now. Contributions and feedback are welcome!

---

## ✨ Features

- 🎙 Uses your **browser’s microphone** (no extra software or hardware needed)
- 🥁 Live **beat detection** from audio input
- 💡 Flashes lights on each beat
- 🧠 Smart light behaviour:
  - Fades out when music gets quiet
  - Strobes when beat rate gets high
- 🌈 Preview mode to test colour cycling
- 📊 Displays current BPM (beats per minute)
- 🖱 Select lights to use via built-in web interface
- ⚡ All runs locally in your Home Assistant instance

---

## 🔐 HTTPS Required for Microphone Access

Because the browser uses the Web Audio API and `getUserMedia`, you **must access Home Assistant over HTTPS** for the microphone to work.

### ✅ Works with:
- `https://homeassistant.local:8123`
- `https://your-nabu-casa-url.ui.nabu.casa`

### ❌ Does **not** work with:
- `http://` (non-secure)
- IP addresses over HTTP

---

## 🛠 Installation

1. **Add this repository to Home Assistant**:

   Go to **Settings → Add-ons → Add-on Store**  
   Click the three dots (⋮) in the top right → **Repositories**  
   Add the following URL: `https://github.com/ryaaanb/music_light_sync`


2. **Install the add-on**

Find **Music Light Sync** in the list and click **Install**.

3. **Start the add-on**

Enable "Start on boot" and optionally "Watchdog".

4. **Open the Web UI**

- Choose your lights  
- Click **🎙 Start Mic Beat**  
- Watch your lights react in real time!

---

## ⚙️ How It Works

- A small Flask server hosts a web interface inside Home Assistant (via Ingress)
- The browser uses `getUserMedia()` to capture your microphone
- JavaScript performs beat detection using live audio analysis
- Beats trigger `light.turn_on` commands via the Home Assistant API
- "Smart" modes (fade/strobe) adjust based on BPM and volume

---

## 🔧 Requirements

- Home Assistant OS, Supervised, or Container
- Smart lights integrated into Home Assistant
- A computer with a microphone
- Access to HA over **HTTPS**

---

## 📥 Contributing

Pull requests and suggestions are welcome!  
If you find bugs or have ideas, feel free to open an issue or start a discussion.

---

## 🙌 Credits

Inspired by ILightShow and Hue Sync — rebuilt as a local-first, privacy-friendly, Home Assistant-native solution using Python, JavaScript, and creativity.

---
