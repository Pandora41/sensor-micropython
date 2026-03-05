# sensor-micropython
================================================================================
IoT Sensor Monitor - MicroPython (ESP32/ESP8266)
================================================================================

[説明] Description
------------------
A simple IoT learning project that reads sensor data (DHT22 + PIR) and sends 
it to a server via WiFi using MicroPython.

Built for educational purposes (school project / self-learning).

[主な機能] Main Features
------------------------
• Read temperature & humidity from DHT22 sensor
• Detect motion using PIR (HC-SR501) sensor
• Connect to WiFi automatically
• Send JSON data to custom API endpoint or Ubidots cloud
• Basic error handling & serial logging
• Easy to modify for other sensors or platforms

[必要なもの] Requirements
-------------------------
Hardware:
• ESP32 or ESP8266 board
• DHT22 sensor (Temperature & Humidity)
• PIR motion sensor (HC-SR501)
• Jumper wires & breadboard
• 3.3V power supply

Software:
• MicroPython firmware (flashed to ESP32/ESP8266)
• Thonny IDE or ampy for code upload
• WiFi network with internet access

[配線] Wiring Guide
-------------------
ESP32/ESP8266 → Sensor
-----------------------------
GPIO 14      → DHT22 DATA
GPIO 27      → PIR OUT
3.3V         → VCC (both sensors)
GND          → GND (both sensors)

※ Pull-up resistor (10kΩ) recommended for DHT22 DATA line

[使い方] How to Use
-------------------
1. Edit configuration in the code:

   # WiFi settings
   ssid = "YOUR_WIFI_NAME"
   password = "YOUR_WIFI_PASSWORD"

   # Choose ONE output method:

   # Option A: Custom server
   API_URL = "http://xxx.xxx.xxx.xxx:5000/sensor"

   # Option B: Ubidots cloud
   UBIDOTS_TOKEN = "YOUR_UBIDOTS_TOKEN"
   DEVICE_LABEL = "your_device_name"

2. Upload main.py to your ESP board using Thonny or ampy.

3. Reset the board and open Serial Monitor (baud: 115200).

4. Expected output:
   > Connecting to network YOUR_WIFI_NAME...
   > Connection successful, IP address: ('192.168.1.100', ...)
   > Temperature: 28.5°C, Humidity: 65.2%, Motion: 0
   > Data sent. Server response: {"status":"ok"}

[データ形式] Data Payload Example
---------------------------------
{
  "temperature": 28.5,
  "humidity": 65.2,
  "motion": 0
}

[注意] Notes & Limitations
--------------------------
• This project is for EDUCATIONAL PURPOSES only (学習用プロジェクト).
• No deep-sleep mode implemented (not optimized for battery operation).
• No local data buffering if WiFi disconnects.
• Sensor readings may have slight delays (~10 sec interval).
• Always validate sensor data on the server side.

[開発のアイデア] Future Improvements
------------------------------------
□ Add deep-sleep mode for battery-powered use
□ Store data locally (SPIFFS/SD) when offline, sync later
□ Add more sensors: CO2, light, soil moisture, etc.
□ Create a simple dashboard (Grafana / custom web UI)
□ Add OTA (Over-The-Air) update support

[ライセンス] License
--------------------
MIT License - Feel free to use, modify, and share for learning purposes.
Please credit the original author if you build upon this work.

[連絡先] Contact
----------------
• GitHub: https://github.com/[your-username]
• HuggingFace: https://huggingface.co/spaces/mewton

Questions or suggestions? Feel free to open an issue! 🛠️

================================================================================
備考: This project was created as part of self-directed learning in IoT and 
embedded systems. Code quality reflects a learning journey - feedback welcome!
================================================================================
