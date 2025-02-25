import network
import urequests
import time
import machine
import dht

# === Konfigurasi WiFi ===
ssid = 'hade'
password = 'N4ntidulu'

# === Konfigurasi Server ===
API_URL = "http://147.93.107.208:5000/sensor"  # Ganti dengan endpoint server kamu

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Menghubungkan ke jaringan {}...'.format(ssid))
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Koneksi berhasil, alamat IP:', wlan.ifconfig()[0])

def send_data_to_server(temperature, humidity, motion):
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "temperature": temperature,
        "humidity": humidity,
        "motion": motion
    }
    try:
        response = urequests.post(API_URL, json=payload, headers=headers)
        print("Data terkirim. Respon dari server:", response.text)
        response.close()
    except Exception as e:
        print("Gagal mengirim data:", e)

def main():
    # Menghubungkan ke WiFi
    connect_wifi()

    # === Setup Sensor ===
    dht_pin = machine.Pin(14)  # Sesuaikan dengan GPIO DHT22
    dht_sensor = dht.DHT22(dht_pin)
    
    pir_pin = machine.Pin(27, machine.Pin.IN)  # Sesuaikan dengan GPIO PIR
    
    # Loop utama
    while True:
        try:
            # Baca data DHT22
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
        except Exception as e:
            print("Gagal membaca sensor DHT22:", e)
            temperature = None
            humidity = None
        
        # Baca sensor PIR
        motion = pir_pin.value()
        
        # Tampilkan data di serial monitor
        print("Suhu: {}°C, Kelembapan: {}%, Gerakan: {}".format(temperature, humidity, motion))
        
        # Kirim data ke server jika pembacaan sensor valid
        if temperature is not None and humidity is not None:
            send_data_to_server(temperature, humidity, motion)
        
        # Delay 10 detik
        time.sleep(10)

if __name__ == '__main__':
    main()
