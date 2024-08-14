from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Variáveis globais para armazenar os dados do sensor
sensor_data = {"X": 0, "Y": 0, "Z": 0, "Gx": 0, "Gy": 0, "Gz": 0}

@app.route('/', methods=['POST'])
def receive_data():
    global sensor_data
    sensor_data['X'] = request.form['X']
    sensor_data['Y'] = request.form['Y']
    sensor_data['Z'] = request.form['Z']
    sensor_data['Gx'] = request.form['Gx']
    sensor_data['Gy'] = request.form['Gy']
    sensor_data['Gz'] = request.form['Gz']
    return jsonify(sensor_data)

@app.route('/')
def index():
    return render_template('mpudados2.html')

@app.route('/sensor_data')
def get_sensor_data():
    return jsonify(sensor_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
