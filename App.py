from flask import Flask, render_template, request, jsonify, session
from conectar import Conectar, insertar_usuarios
from procesar_imagenes import ProcesarImagen, VerificarImagen
from login_register import Login, Registrar

class App:
    def __init__(self):
        self.app = Flask(__name__, static_folder="static", template_folder='templates')
        self.app.secret_key = 'clave_secreta_segura'
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/login', methods=['POST'])
        def login():
            return Login().login()

        @self.app.route('/registrar', methods=['POST'])
        def registrar():
            return Registrar().registrar()

        @self.app.route('/procesar-imagen', methods=['POST'])
        def procesar_imagen():
            return ProcesarImagen().procesar()

        @self.app.route('/verificar-imagen', methods=['POST'])
        def verificar_imagen():
            return VerificarImagen().verificar()

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app_instance = App()
    app_instance.run()