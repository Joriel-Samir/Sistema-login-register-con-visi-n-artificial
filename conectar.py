import mysql.connector
class Conectar():
    def __init__(self):
        # Inicializa la conexión a la base de datos MySQL
        self.conectar = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "joriel",
        database = "usuarios"
    )   
        self.cursor = self.conectar.cursor()
    def retornar(self):
        # Retorna la conexión (por si se necesita en otro lugar)
        return self.conectar

class insertar_usuarios(Conectar): 
    def __init__(self,):
        super().__init__()

    def registrar(self, username, email, password, embedding=None):
        # Inserta un nuevo usuario en la base de datos
        if embedding is not None:
            sql = "INSERT INTO usuarios (nombre, correo, contraseña, embedding) VALUES (%s, %s, %s, %s)"
            valores = (username, email, password, embedding)
        else:
            sql = "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s, %s)"
            valores = (username, email, password)
        self.cursor.execute(sql, valores)
        self.conectar.commit()
    def guardar_embedding(self, username, embedding):
        # Actualiza el embedding de un usuario existente
        sql = "UPDATE usuarios SET embedding = %s WHERE nombre = %s"
        valores = (embedding, username)
        self.cursor.execute(sql, valores)
        self.conectar.commit()
        
# Instancias 
conexion = Conectar()
guardar = insertar_usuarios()

