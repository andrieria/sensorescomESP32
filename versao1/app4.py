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

def plot_graph(temperatura, umidade):
    plt.figure(figsize=(10, 5))
    
    # Usa o índice dos elementos para o eixo x
    plt.plot(range(len(temperatura)), temperatura, label='Temperatura', color='red')
    plt.plot(range(len(umidade)), umidade, label='Umidade', color='blue')
    
    plt.xlabel('Número de Amostras')
    plt.ylabel('Valores')
    plt.title('Gráfico de Temperatura e Umidade')
    plt.legend()
    
    # O limite do eixo x é automaticamente ajustado com base na quantidade de dados
    plt.xlim(0, max(60, len(temperatura)))  # Define o limite inicial como 60 e expande conforme necessário
    
    # Salva a figura em memória
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    
    # Codifica a imagem para exibição em HTML
    image_base64 = base64.b64encode(image_png).decode('utf-8')
    
    return image_base64




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
    
    print(f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}")
    print(f"Temperatura: {temperature}, Umidade: {humidity}")
    print(f"Velocidade: {velocidade}, Satélites: {satelites}, Precisão: {precisao}")
    print(f"SSID: {ssid}, IP: {ip}, RSSI: {rssi}")
    
    if latitude != 0 and longitude != 0 and altitude != 0:
         
        temperatura.append(float(temperature))
        umidade.append(float(humidity))
        image_base64 = plot_graph(temperatura, umidade)

        '''location = geolocator.reverse(f"{latitude}, {longitude}")

        address = location.address
        print("Endereço completo:", address)'''
        location = geolocator.reverse(f"{latitude}, {longitude}")
        address = "N/A"  # Valor padrão caso o endereço não seja encontrado

        if location:
            address = location.address
            print("Endereço completo:", address)
        else:
            print("Endereço não encontrado.")


        
        socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'latitude': latitude, 'longitude': longitude, 'altitude': altitude, 'velocidade': velocidade, 'satelites': satelites, 'precisao': precisao, 'address': address, 'ssid': ssid, 'ip': ip, 'rssi': rssi, 'graph_image': image_base64})
    #socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'location': address})
    #socketio.emit('update_map', {'map': generate_map(address)})  # Atualiza o mapa com a nova localização

    else:
        temperatura.append(float(temperature))
        umidade.append(float(humidity))
        
        image_base64 = plot_graph(temperatura, umidade)
        
        socketio.emit('update_data', {'temperature': temperature, 'humidity': humidity, 'latitude': 'N/A', 'longitude': 'N/A', 'altitude': 'N/A', 'velocidade': 'N/A', 'satelites': 'N/A', 'precisao': 'N/A', 'address': 'N/A', 'ssid': ssid, 'ip': ip, 'rssi': rssi, 'graph_image': image_base64})
        
    return 'Data received', 200

@app.route('/', methods=['GET'])
def index():
    # Renderiza o template HTML que contém o mapa e os gráficos
    return render_template('index2.html')

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
                
                # Gráfico de temperatura
                plt.subplot(1, 2, 1)
                plt.plot(temperatura, label='Temperatura')
                plt.xlabel('Tempo (s)')
                plt.xlim(0, 60)
                plt.ylabel('Temperatura (°C)')
                plt.ylim(0, 50)
                plt.legend()
                
                # Gráfico de umidade
                plt.subplot(1, 2, 2)
                plt.plot(umidade, label='Umidade')
                plt.xlabel('Tempo (s)')
                plt.xlim(0, 60)
                plt.ylabel('Umidade (%)')
                plt.ylim(0, 100)
                plt.legend()

                # Salvar os dois gráficos em um único buffer
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
                #chart_base64 = "data:image/png;base64," + base64_encoded_chart
                buf.close()
                
                # Enviar a imagem base64 para o cliente
                #chart_base64 = "data:image/png;base64," + base64_encoded_chart

                socketio.emit('update_chart', {'chart': chart_base64})

        socketio.sleep(1)

@socketio.on('connect')
def handle_connect():
    # Quando um cliente se conecta, inicia a geração dos gráficos
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=generate_chart)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)