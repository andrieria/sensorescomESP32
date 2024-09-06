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
acc_x = []
acc_y = []
acc_z = []
gyro_x = []
gyro_y = []
gyro_z = []
latitude = 0.0
longitude = 0.0
altitude = 0.0
velocidade = 0.0
satelites = 0.0
precisao = 0.0
ssid = ""
ip = ""
rssi = ""
thread = None
thread_lock = Lock()

geolocator = Nominatim(user_agent="gps_app")

@app.route('/', methods=['POST'])
def receive_data():
    global latitude, longitude, altitude, velocidade, satelites, precisao, ssid, ip, rssi
    global acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z

    temperature = request.form['temperature']
    humidity = request.form['humidity']
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    altitude = float(request.form['altitude'])
    velocidade = float(request.form['velocidade'])
    satelites = float(request.form['satelites'])
    precisao = float(request.form['precisao'])
    ssid = request.form['ssid']
    ip = request.form['ip']
    rssi = request.form['rssi']
    ax = float(request.form['acc_x'])
    ay = float(request.form['acc_y'])
    az = float(request.form['acc_z'])
    gx = float(request.form['gyro_x'])
    gy = float(request.form['gyro_y'])
    gz = float(request.form['gyro_z'])

    print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")
    print(f"Temperatura: {temperature}, Umidade: {humidity}")
    print(f"Velocidade: {velocidade}, Satélites: {satelites}, Precisão: {precisao}")
    print(f"SSID: {ssid}, IP: {ip}, RSSI: {rssi}")
    print(f"ax: {ax}, ay: {ay}, az: {az}, gx: {gx}, gy: {gy}, gz: {gz}")
    
    if latitude != 0 and longitude != 0 and altitude != 0:
        acc_x.append(ax)
        acc_y.append(ay)
        acc_z.append(az)
        gyro_x.append(gx)
        gyro_y.append(gy)
        gyro_z.append(gz)
        temperatura.append(float(temperature))
        umidade.append(float(humidity))
        
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = "N/A"

        if location:
            address = location.address
            print("Endereço completo:", address)
        else:
            print("Endereço não encontrado.")
        
        socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude, 'velocidade': velocidade, 'satelites': satelites, 'precisao': precisao, 'address': address, 'ssid': ssid, 'ip': ip, 'rssi': rssi, 'ax': ax, 'ay': ay, 'az': az, 'gx': gx, 'gy': gy, 'gz': gz})
    else:
        acc_x.append(ax)
        acc_y.append(ay)
        acc_z.append(az)
        gyro_x.append(gx)
        gyro_y.append(gy)
        gyro_z.append(gz)
        temperatura.append(float(temperature))
        umidade.append(float(humidity))
        socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'latitude': 'N/A', 'longitude': 'N/A', 'altitude': 'N/A', 'velocidade': 'N/A', 'satelites': 'N/A', 'precisao': 'N/A', 'address': 'N/A', 'ssid': ssid, 'ip': ip, 'rssi': rssi, 'ax': ax, 'ay': ay, 'az': az, 'gx': gx, 'gy': gy, 'gz': gz})
        
        
    return 'Data received', 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index4.html')

def generate_chart():
    while True:
        with thread_lock:
            if temperatura and umidade:
                plt.figure(figsize=(12, 8))
                
                # Gráficos de temperatura e umidade
                plt.subplot(2, 2, 1)
                plt.plot(temperatura, label='Temperatura')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Temperatura (°C)')
                plt.ylim(0, 50)
                plt.legend()
                
                plt.subplot(2, 2, 2)
                plt.plot(umidade, label='Umidade')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Umidade (%)')
                plt.ylim(0, 100)
                plt.legend()

                # Gráficos do MPU6050
                plt.subplot(2, 2, 3)
                plt.plot(acc_x, label='Acelerômetro X')
                plt.plot(acc_y, label='Acelerômetro Y')
                plt.plot(acc_z, label='Acelerômetro Z')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Aceleração')
                plt.legend()
                
                plt.subplot(2, 2, 4)
                plt.plot(gyro_x, label='Giroscópio X')
                plt.plot(gyro_y, label='Giroscópio Y')
                plt.plot(gyro_z, label='Giroscópio Z')
                plt.xlabel('Tempo (s)')
                plt.ylabel('Giro')
                plt.legend()
                
                plt.tight_layout()
                
                # Salvar para BytesIO
                img = io.BytesIO()
                plt.savefig(img, format='png')
                img.seek(0)
                img_base64 = base64.b64encode(img.getvalue()).decode()
                plt.close()

                # Emitir gráfico para cliente
                socketio.emit('update_chart', {'chart': img_base64})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
