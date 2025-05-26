from flask import render_template, request, session
from conectar import Conectar, insertar_usuarios

class Login:
    def login(self):
        # Obtiene usuario y contraseña del formulario
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            # Si faltan datos, muestra error
            return render_template('index.html', error="Faltan datos")
        # Conecta a la base de datos y verifica credenciales
        conexion = Conectar()
        cursor = conexion.cursor
        sql = "SELECT contraseña FROM usuarios WHERE nombre = %s"
        cursor.execute(sql, (username,))
        resultado = cursor.fetchone()
        if not resultado or resultado[0] != password:
            # Si no coincide, muestra error
            return render_template('index.html', error="Usuario o contraseña incorrectos")
        # Si es correcto, guarda usuario en sesión y pasa a verificación facial
        session['username'] = username
        return render_template('comprobar_cara.html')

class Registrar:
    def registrar(self):
        # Obtiene datos del formulario de registro
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            # Si faltan datos, muestra error
            return render_template('register.html', error="Faltan datos")
        # Registra el usuario en la base de datos
        guardar = insertar_usuarios()
        guardar.registrar(username, email, password)
        # Guarda usuario en sesión y pasa a captura de rostro
        session['username'] = username
        return render_template('tomarcaras.html')