import network
import urequests
import time
import machine
import dht

# === Konfigurasi WiFi ===
ssid = 'hade'
password = 'N4ntidulu'

# === Konfigurasi Ubidots ===
UBIDOTS_TOKEN = 'BBUS-Ohai5LhrlRIe3fZgfktoZYhGCeBebg'  # Ganti dengan Ubidots Token kalian
DEVICE_LABEL = 'tugas'          # Label device di Ubidots
# Nama-nama variabel di Ubidots
DHT22_TEMP_VARIABLE = 'temperature'
DHT22_HUM_VARIABLE = 'humidity'
PIR_VARIABLE = 'motion'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Menghubungkan ke jaringan {}...'.format(ssid))
        wlan.connect(ssid, password)
        # Tunggu hingga koneksi berhasil
        while not wlan.isconnected():
            time.sleep(1)
    print('Koneksi berhasil, alamat IP:', wlan.ifconfig()[0])

def send_data_to_ubidots(temperature, humidity, motion):
    url = "http://industrial.api.ubidots.com/api/v1.6/devices/{}".format(DEVICE_LABEL)
    headers = {
        "X-Auth-Token": UBIDOTS_TOKEN,
        "Content-Type": "application/json"
    }
    # Format payload sesuai dengan Ubidots API
    payload = {
        DHT22_TEMP_VARIABLE: {"value": temperature},
        DHT22_HUM_VARIABLE: {"value": humidity},
        PIR_VARIABLE: {"value": motion}
    }
    try:
        response = urequests.post(url, json=payload, headers=headers)
        print("Data terkirim. Respon dari Ubidots:", response.text)
        response.close()
    except Exception as e:
        print("Gagal mengirim data:", e)

def main():
    # Menghubungkan ke WiFi
    connect_wifi()

    # === Setup Sensor ===
    # Sensor DHT22 dihubungkan ke GPIO14
    dht_pin = machine.Pin(14)
    dht_sensor = dht.DHT22(dht_pin)
    
    # Sensor PIR HC-SR501 dihubungkan ke GPIO27
    pir_pin = machine.Pin(27, machine.Pin.IN)
    
    # Loop utama: Baca sensor dan kirim data setiap 10 detik
    while True:
        try:
            # Baca data DHT22
            dht_sensor.measure()
            temperature = dht_sensor.temperature()  # Suhu dalam derajat Celsius
            humidity = dht_sensor.humidity()          # Kelembapan dalam persen
        except Exception as e:
            print("Gagal membaca sensor DHT22:", e)
            temperature = None
            humidity = None
        
        # Baca sensor PIR (nilai 1 jika gerakan terdeteksi, 0 jika tidak)
        motion = pir_pin.value()
        
        # Tampilkan data di serial monitor
        print("Suhu: {}°C, Kelembapan: {}%, Gerakan: {}".format(temperature, humidity, motion))
        
        # Kirim data ke Ubidots jika pembacaan sensor valid
        if temperature is not None and humidity is not None:
            send_data_to_ubidots(temperature, humidity, motion)
        
        # Tunda selama 10 detik sebelum pengukuran berikutnya
        time.sleep(10)

if __name__ == '__main__':
    main()

