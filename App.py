from flask import Flask, render_template, request, flash, redirect, jsonify, session
from conectar import Conectar, insertar_usuarios
from datetime import datetime
from reconocimiento import ReconocedorArcFace
import os
import base64
import numpy as np

reconocedor = ReconocedorArcFace()


app = Flask(__name__, static_folder="static", template_folder='templates')
app.secret_key = 'clave_secreta_segura'  

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camara')
def camara():
    return render_template('tomarcaras.html')
@app.route('/verificar')
def verificar():
    return render_template('comprobar_cara.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        return render_template('index.html', error="Faltan datos")

    
    conexion = Conectar()
    cursor = conexion.cursor
    sql = "SELECT contraseña FROM usuarios WHERE nombre = %s"
    cursor.execute(sql, (username,))
    resultado = cursor.fetchone()
    if not resultado or resultado[0] != password:
        return render_template('index.html', error="Usuario o contraseña incorrectos")

    
    session['username'] = username
    return render_template('comprobar_cara.html')
    
@app.route('/registrar', methods=['POST'])
def registrar():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not username or not email or not password:
        return "Faltan datos", 400

    guardar = insertar_usuarios()
    guardar.registrar(username, email, password)

 
    session['username'] = username

    return render_template('tomarcaras.html')

@app.route('/procesar-imagen', methods=['POST'])
def procesar_imagen():
    data = request.get_json()
    image_base64 = data.get('image')
    username = session.get('username')  

    if not username:
        return jsonify({'message': 'No hay usuario en sesión'}), 400

 
    image_data = image_base64.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + '.png'
    user_folder = os.path.join('static', 'uploads', username)
    os.makedirs(user_folder, exist_ok=True)
    filepath = os.path.join(user_folder, filename)
    with open(filepath, 'wb') as f:
        f.write(image_bytes)    

    
    embedding = reconocedor.extraer_embedding(filepath)
    if embedding is None:
        return jsonify({'message': 'No se detectó rostro'}), 400

    
    embedding_str = ','.join(map(str, embedding.tolist()))

    guardar = insertar_usuarios()
    guardar.guardar_embedding(username, embedding_str)

    return jsonify({'message': 'Imagen recibida y embedding guardado correctamente'})

@app.route('/verificar-imagen', methods=['POST'])
def verificar_imagen():
    data = request.get_json()
    image_base64 = data.get('image')
    username = session.get('username')  

    if not username or not image_base64:
        return jsonify({'success': False, 'message': 'No hay usuario en sesión o imagen no enviada'}), 400

    
    conexion = Conectar()
    cursor = conexion.cursor
    sql = "SELECT embedding FROM usuarios WHERE nombre = %s"
    cursor.execute(sql, (username,))
    resultado = cursor.fetchone()
    if not resultado or not resultado[0]:
        return jsonify({'success': False, 'message': 'Usuario no encontrado o sin embedding'}), 400
    embedding_guardado = resultado[0]


    image_data = image_base64.split(',')[1]
    image_bytes = base64.b64decode(image_data)
    filename = 'temp_verificar.png'
    filepath = os.path.join('static', 'uploads', filename)
    with open(filepath, 'wb') as f:
        f.write(image_bytes)

    embedding_login = reconocedor.extraer_embedding(filepath)
    if embedding_login is None:
        return jsonify({'success': False, 'message': 'No se detectó rostro'}), 400
    embedding_login_str = ','.join(map(str, embedding_login.tolist()))

    print("Tamaño embedding guardado:", len(embedding_guardado.split(',')))
    print("Tamaño embedding login:", len(embedding_login_str.split(',')))
    print("Embedding guardado:", embedding_guardado[:100], "...")  
    print("Embedding login:", embedding_login_str[:100], "...")
    print("Primeros 10 valores embedding guardado:", embedding_guardado.split(',')[:10])
    print("Primeros 10 valores embedding login:", embedding_login_str.split(',')[:10])
    

    if reconocedor.comparar_embeddings(embedding_guardado, embedding_login_str):
        return jsonify({'success': True, 'message': 'Acceso concedido'})
    else:
        return jsonify({'success': False, 'message': 'Rostro no coincide'})
    
if __name__ == '__main__':
    app.run(debug=True)
