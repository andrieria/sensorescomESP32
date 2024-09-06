from flask import Flask, render_template, jsonify
import serial
import math

app = Flask(__name__)

# Configuração da serial
ser = serial.Serial('COM13', 9600)  # ajuste para a porta correta

# Definição dos vértices do cubo
vertices = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1]
]

# Definição das arestas que conectam os vértices
edges = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Inicializar os ângulos de rotação
angle_x = 0
angle_y = 0
xp, yp = 0, 0

@app.route('/')
def index():
    return render_template('mpudados3.html')

@app.route('/data')
def data():
    global angle_x, angle_y, xp, yp

    # Ler dados do sensor
    data = ser.readline().decode('utf-8', errors='ignore').strip()
    datax = list(map(int, data.split()))
    xpos, ypos = datax[0], datax[1]

    # Atualizar ângulos de rotação
    if abs(xp - xpos) >= 5:
        angle_x += 0.05 if xpos - xp >= 0 else -0.05
        xp = xpos

    if abs(yp - ypos) >= 5:
        angle_y -= 0.05 if ypos - yp >= 0 else 0.05
        yp = ypos

    # Rotacionar vértices
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex

        # Rotacionar ao redor do eixo X
        new_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        new_z = y * math.sin(angle_x) + z * math.cos(angle_x)
        y, z = new_y, new_z

        # Rotacionar ao redor do eixo Y
        new_x = x * math.cos(angle_y) + z * math.sin(angle_y)
        rotated_vertices.append([new_x, y, z])

    # Converter vértices rotacionados para coordenadas 2D
    projected_vertices = [
        [int(v[0] * 100 + 200), int(v[1] * 100 + 200)] for v in rotated_vertices
    ]

    # Enviar dados como JSON
    return jsonify(vertices=projected_vertices, edges=edges)

if __name__ == '__main__':
    app.run(debug=True)
