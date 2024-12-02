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
ssid = ""
ip = ""
rssi = ""
thread = None
thread_lock = Lock()

geolocator = Nominatim(user_agent="gps_app")

@app.route('/', methods=['POST'])
def receive_data():
    global latitude, longitude, altitude, velocidade, satelites, precisao, ssid, ip, rssi

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
    

    temperatura.append(float(temperature))
    umidade.append(float(humidity))

    location = geolocator.reverse(f"{latitude}, {longitude}")

    address = location.address
    print("Endereço completo:", address)

    
    socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude, 'velocidade': velocidade, 'satelites': satelites, 'precisao': precisao, 'address': address, 'ssid': ssid, 'ip': ip, 'rssi': rssi})
    #socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'location': address})
    #socketio.emit('update_map', {'map': generate_map(address)})  # Atualiza o mapa com a nova localização

    return 'Data received', 200

@app.route('/', methods=['GET'])
def index():
    # Renderiza o template HTML que contém o mapa e os gráficos
    return render_template('index.html')

'''def generate_map(address):
    # Função para gerar e retornar o mapa utilizando folium e os dados de GPS
    map = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Marker([latitude, longitude], popup='Localização Atual', tooltip=address).add_to(map)
    return map._repr_html_()'''

def generate_chart():
    # Função para gerar os gráficos de temperatura e umidade
    while True:
        with thread_lock:
            if temperatura and umidade:
                plt.figure(figsize=(10, 5))
                
                plt.subplot(1, 2, 1)
                plt.plot(temperatura, label='Temperatura')
                plt.xlabel('Tempo (s)')
                plt.xlim(0, 60)
                plt.ylabel('Temperatura (°C)')
                plt.ylim(0, 50)
                plt.legend()
                
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                temp_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                buf.close()

                plt.subplot(1, 2, 2)
                plt.plot(umidade, label='Umidade')
                plt.xlabel('Tempo (s)')
                plt.xlim(0, 60)
                plt.ylabel('Umidade (%)')
                plt.ylim(0, 100)
                plt.legend()

                # Convertendo o gráfico para uma imagem base64 para enviar para o cliente
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                hum_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                buf.close()
                
                socketio.emit('update_chart', {'temperature_chart': temp_chart_base64, 'humidity_chart': hum_chart_base64})
                #socketio.emit('update_chart', {'temperature_chart': image_base64, 'humidity_chart': image_base64})

        socketio.sleep(1)

@socketio.on('connect')
def handle_connect():
    # Quando um cliente se conecta, inicia a geração dos gráficos
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=generate_chart)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)