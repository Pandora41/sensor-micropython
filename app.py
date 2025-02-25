from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Koneksi ke MongoDB (default port 27017)
client = MongoClient("mongodb://localhost:27017/")
db = client["iot_database"]  # Nama database
collection = db["sensor_data"]  # Nama koleksi (table)

@app.route('/sensor', methods=['POST'])
def receive_sensor_data():
    try:
        # Ambil data JSON dari request
        data = request.json
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Tambahkan timestamp
        data["timestamp"] = datetime.now()

        # Simpan ke MongoDB
        collection.insert_one(data)

        return jsonify({"message": "Data received", "data": data}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route untuk cek data yang tersimpan
@app.route('/sensor', methods=['GET'])
def get_sensor_data():
    data = list(collection.find({}, {"_id": 0}))  # Ambil semua data kecuali _id
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
