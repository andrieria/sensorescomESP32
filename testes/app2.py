from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import matplotlib.pyplot as plt
import io
import base64
from threading import Lock
from geopy.geocoders import Nominatim

app = Flask(__name__)
socketio = SocketIO(app)
temperatura = []
umidade = []
latitude = 0.0
longitude = 0.0
altitude = 0.0
velocidade = 0.0
satelites = 0.0
precisao = 0.0
acelerometro_x = []
acelerometro_y = []
acelerometro_z = []
giroscopio_x = []
giroscopio_y = []
giroscopio_z = []
thread = None
thread_lock = Lock()

geolocator = Nominatim(user_agent="gps_app")

@app.route('/', methods=['POST'])
def receive_data():
    global latitude, longitude, altitude, velocidade, satelites, precisao

    temperature = request.form['temperature']
    humidity = request.form['humidity']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    altitude = float(request.form['altitude'])
    velocidade = float(request.form['velocidade'])
    satelites = float(request.form['satelites'])
    precisao = float(request.form['precisao'])

    # MPU6050 data
    accel_x = float(request.form['accel_x'])
    accel_y = float(request.form['accel_y'])
    accel_z = float(request.form['accel_z'])
    gyro_x = float(request.form['gyro_x'])
    gyro_y = float(request.form['gyro_y'])
    gyro_z = float(request.form['gyro_z'])

    temperatura.append(float(temperature))
    umidade.append(float(humidity))
    
    # Append MPU6050 data
    acelerometro_x.append(accel_x)
    acelerometro_y.append(accel_y)
    acelerometro_z.append(accel_z)
    giroscopio_x.append(gyro_x)
    giroscopio_y.append(gyro_y)
    giroscopio_z.append(gyro_z)

    location = geolocator.reverse(f"{latitude}, {longitude}")
    address = location.address

    socketio.emit('update_data', {
        'temperature': temperature,
        'humidity': humidity,
        'latitude': latitude,
        'longitude': longitude,
        'altitude': altitude,
        'velocidade': velocidade,
        'satelites': satelites,
        'precisao': precisao,
        'address': address
    })

    return 'Data received', 200

def generate_chart():
    # Função para gerar os gráficos de temperatura, umidade, eixos do acelerômetro e giroscópio
    while True:
        with thread_lock:
            if temperatura and umidade:
                plt.figure(figsize=(15, 10))

                # Gráfico de temperatura
                plt.subplot(3, 3, 1)
                plt.plot(temperatura, label='Temperatura')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Temperatura (°C)')
                plt.legend()

                # Gráfico de umidade
                plt.subplot(3, 3, 2)
                plt.plot(umidade, label='Umidade')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Umidade (%)')
                plt.legend()

                # Gráficos do acelerômetro
                plt.subplot(3, 3, 3)
                plt.plot(acelerometro_x, label='Accel X')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Acelerômetro X')
                plt.legend()

                plt.subplot(3, 3, 4)
                plt.plot(acelerometro_y, label='Accel Y')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Acelerômetro Y')
                plt.legend()

                plt.subplot(3, 3, 5)
                plt.plot(acelerometro_z, label='Accel Z')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Acelerômetro Z')
                plt.legend()

                # Gráficos do giroscópio
                plt.subplot(3, 3, 6)
                plt.plot(giroscopio_x, label='Gyro X')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Giroscópio X')
                plt.legend()

                plt.subplot(3, 3, 7)
                plt.plot(giroscopio_y, label='Gyro Y')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Giroscópio Y')
                plt.legend()

                plt.subplot(3, 3, 8)
                plt.plot(giroscopio_z, label='Gyro Z')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Giroscópio Z')
                plt.legend()

                # Convertendo os gráficos para imagens base64
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                buf.close()

                socketio.emit('update_chart', {'chart': chart_base64})

        socketio.sleep(1)

@socketio.on('connect')
def handle_connect():
    # Inicia a geração dos gráficos quando um cliente se conecta
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=generate_chart)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
