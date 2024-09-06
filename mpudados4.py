from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

angle_x = 0
angle_y = 0
xp, yp = 0, 0

@app.route('/')
def index():
    return render_template('mpudados4.html')

@app.route('/data', methods=['POST'])  # Certifique-se de que está aceitando o método POST
def data():
    global angle_x, angle_y, xp, yp

    # Obtenha os valores xpos e ypos da requisição POST
    xpos = int(request.form['xpos'])
    ypos = int(request.form['ypos'])

    # Atualizar ângulos de rotação
    if abs(xp - xpos) >= 5:
        angle_x += 0.05 if xpos - xp >= 0 else -0.05
        xp = xpos

    if abs(yp - ypos) >= 5:
        angle_y -= 0.05 if ypos - yp >= 0 else 0.05
        yp = ypos

    # Enviar os ângulos como JSON
    return jsonify(angle_x=angle_x, angle_y=angle_y)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



'''from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

angle_x = 0
angle_y = 0
xp, yp = 0, 0

@app.route('/')
def index():
    return render_template('mpudados4.html')

@app.route('/data', methods=['POST'])
def data():
    global angle_x, angle_y, xp, yp

    xpos = int(request.form['xpos'])
    ypos = int(request.form['ypos'])

    # Atualizar ângulos de rotação
    if abs(xp - xpos) >= 5:
        angle_x += 0.05 if xpos - xp >= 0 else -0.05
        xp = xpos

    if abs(yp - ypos) >= 5:
        angle_y -= 0.05 if ypos - yp >= 0 else 0.05
        yp = ypos

    # Enviar os ângulos como JSON
    return jsonify(angle_x=angle_x, angle_y=angle_y)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
'''