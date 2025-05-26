from flask import Flask, render_template, request, jsonify, session
from conectar import Conectar, insertar_usuarios
from procesar_imagenes import ProcesarImagen, VerificarImagen
from login_register import Login, Registrar

class App:
    def __init__(self):
        # Inicializa la aplicación Flask y configura la clave secreta para sesiones
        self.app = Flask(__name__, static_folder="static", template_folder='templates')
        self.app.secret_key = 'no_me_vas_a_hakear'
        self.setup_routes() # Define las rutas de la aplicación

    def setup_routes(self):
        # Ruta principal: muestra la página de inicio
        @self.app.route('/')
        def index():
            return render_template('index.html')

        # Ruta para login: deja la lógica a la clase Login
        @self.app.route('/login', methods=['POST'])
        def login():
            return Login().login()

        # Ruta para registro: deja la lógica a la clase Registrar
        @self.app.route('/registrar', methods=['POST'])
        def registrar():
            return Registrar().registrar()

        # Ruta para procesar imagen (registro facial): delega a ProcesarImagen
        @self.app.route('/procesar-imagen', methods=['POST'])
        def procesar_imagen():
            return ProcesarImagen().procesar()

    # Ruta para verificar imagen (login facial): delega a VerificarImagen
        @self.app.route('/verificar-imagen', methods=['POST'])
        def verificar_imagen():
            return VerificarImagen().verificar()

    def run(self):
        # Inicia la aplicación Flask
        self.app.run(debug=True)

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()