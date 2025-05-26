from flask import render_template, request, session
from conectar import Conectar, insertar_usuarios

class Login:
    def login(self):
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

class Registrar:
    def registrar(self):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            return render_template('register.html', error="Faltan datos")
        guardar = insertar_usuarios()
        guardar.registrar(username, email, password)
        session['username'] = username
        return render_template('tomarcaras.html')