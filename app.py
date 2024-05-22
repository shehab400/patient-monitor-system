from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Store heart rate data
heart_rate_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heart_rate', methods=['POST'])
def receive_heart_rate():
    data = request.get_json()
    if all(key in data for key in ("patient_id", "heart_rate", "timestamp")):
        try:
            data["timestamp"] = datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            heart_rate_data.append(data)
            print(f"Received data: {data}\n")
            return jsonify({"status": "success"}), 200
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid timestamp format"}), 400
    else:
        return jsonify({"status": "error", "message": "Invalid data format"}), 400

@app.route('/heart_rate', methods=['GET'])
def get_heart_rate():
    return jsonify(heart_rate_data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
