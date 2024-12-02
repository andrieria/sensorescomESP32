from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Variáveis globais para armazenar os valores do MPU6050
accX, accY, accZ, gyroX, gyroY, gyroZ = 0, 0, 0, 0, 0, 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update', methods=['POST'])
def update_data():
    global accX, accY, accZ, gyroX, gyroY, gyroZ
    if request.method == 'POST':
        # Receber os dados do MPU6050 do ESP32
        data = request.form
        
        # Atualizar os valores globais
        accX = float(data['accX'])
        accY = float(data['accY'])
        accZ = float(data['accZ'])
        gyroX = float(data['gyroX'])
        gyroY = float(data['gyroY'])
        gyroZ = float(data['gyroZ'])
        
        print(f"Dados Recebidos - AccX: {accX}, AccY: {accY}, AccZ: {accZ}, GyroX: {gyroX}, GyroY: {gyroY}, GyroZ: {gyroZ}")
        
        return jsonify({"status": "success"})

@app.route('/get_data')
def get_data():
    global accX, accY, accZ, gyroX, gyroY, gyroZ
    # Enviar os dados para o cliente em tempo real
    return jsonify({'accX': accX, 'accY': accY, 'accZ': accZ, 'gyroX': gyroX, 'gyroY': gyroY, 'gyroZ': gyroZ})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
