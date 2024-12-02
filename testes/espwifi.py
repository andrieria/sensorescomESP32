from flask import Flask, request

app = Flask(__name__)

temperatura = []
umidade = []
frase = None


@app.route('/', methods=['POST'])
def receive_data():
    i = 0
    while i < 5:
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        temperatura.append(temperature)
        umidade.append(humidity)
        
        i+=1
    return 'Data received', 200

@app.route('/', methods=['GET'])
def show_data():
    frase = (f"Temperaturas: {temperatura}, Umidades: {umidade}")
    return frase

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Certifique-se de que a porta aqui corresponde ao ESP32
