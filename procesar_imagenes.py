from flask import request, jsonify, session
from reconocimiento import ReconocedorArcFace
from conectar import insertar_usuarios, Conectar
import os, base64
from datetime import datetime


class Imagen:
    def guardar_imagen(self, image_base64, username, filename=None):
        #Decodifica la imagen base64, la guarda en disco y retorna la ruta del archivo.

        try:
            image_data = image_base64.split(',')[1]
            image_bytes = base64.b64decode(image_data)
            if not filename:
                filename = datetime.now().strftime("%Y%m%d%H%M%S") + '.png'
            user_folder = os.path.join('static', 'uploads', username)
            os.makedirs(user_folder, exist_ok=True)
            filepath = os.path.join(user_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            return filepath
        except Exception as e:
            print(f"Error guardando imagen: {e}")
            return None


class ProcesarImagen:
    #Procesa la imagen enviada por el usuario para registro facial:
    #Guarda la imagen
    #Extrae el embedding facial
    #Guarda el embedding en la base de datos
    
    def __init__(self):
        self.imagen_service = Imagen()
        self.reconocedor = ReconocedorArcFace()
        self.db = insertar_usuarios()

    def procesar(self):
        try:
            data = request.get_json()
            image_base64 = data.get('image')
            username = session.get('username')

            if not username:
                return jsonify({'message': 'No hay usuario en sesión'}), 400
            if not image_base64:
                return jsonify({'message': 'Imagen no enviada'}), 400

            filepath = self.imagen_service.guardar_imagen(image_base64, username)
            if not filepath:
                return jsonify({'message': 'Error al guardar imagen'}), 500

            embedding = self.reconocedor.extraer_embedding(filepath)
            if embedding is None:
                return jsonify({'message': 'No se detectó rostro'}), 400

            embedding_str = ','.join(map(str, embedding.tolist()))
            self.db.guardar_embedding(username, embedding_str)

            return jsonify({'message': 'Imagen recibida y embedding guardado correctamente'})
        except Exception as e:
            return jsonify({'message': 'Error procesando imagen', 'error': str(e)}), 500


class VerificarImagen:
    def __init__(self):
        self.imagen_service = Imagen()
        self.reconocedor = ReconocedorArcFace()
        self.conexion = Conectar()

    def verificar(self):
        #Verifica la imagen enviada por el usuario para login facial
        #Busca el embedding guardado
        #Extrae el embedding de la imagen enviada
        #Compara ambos embeddings
        
        try:
            data = request.get_json()
            image_base64 = data.get('image')
            username = session.get('username')

            if not username or not image_base64:
                return jsonify({'success': False, 'message': 'No hay usuario en sesión o imagen no enviada'}), 400

            cursor = self.conexion.cursor
            sql = "SELECT embedding FROM usuarios WHERE nombre = %s"
            cursor.execute(sql, (username,))
            resultado = cursor.fetchone()

            if not resultado or not resultado[0]:
                return jsonify({'success': False, 'message': 'Usuario no encontrado o sin embedding'}), 400

            embedding_guardado = resultado[0]

            filepath = self.imagen_service.guardar_imagen(image_base64, username='temp', filename='temp_verificar.png')
            if not filepath:
                return jsonify({'success': False, 'message': 'Error al guardar imagen'}), 500

            embedding_login = self.reconocedor.extraer_embedding(filepath)
            if embedding_login is None:
                return jsonify({'success': False, 'message': 'No se detectó rostro'}), 400

            embedding_login_str = ','.join(map(str, embedding_login.tolist()))

            if self.reconocedor.comparar_embeddings(embedding_guardado, embedding_login_str):
                return jsonify({'success': True, 'message': 'Acceso concedido'})
            else:
                return jsonify({'success': False, 'message': 'Rostro no coincide'})
        except Exception as e:
            return jsonify({'success': False, 'message': 'Error verificando imagen', 'error': str(e)}), 500
