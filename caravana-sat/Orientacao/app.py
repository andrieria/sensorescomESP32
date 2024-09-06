from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random
import time
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def send_sensor_data():
    while True:
        # Simulando dados de sensores
        data = {
            'accel_x': random.uniform(-2, 2),
            'accel_y': random.uniform(-2, 2),
            'accel_z': random.uniform(-2, 2),
            'gyro_x': random.uniform(-250, 250),
            'gyro_y': random.uniform(-250, 250),
            'gyro_z': random.uniform(-250, 250)
        }
        socketio.emit('sensor_data', data)
        time.sleep(1)

if __name__ == '__main__':
    thread = threading.Thread(target=send_sensor_data)
    thread.daemon = True
    thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
