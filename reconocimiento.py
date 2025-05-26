import cv2
import numpy as np
import insightface

class ReconocedorArcFace:
    def __init__(self):
         # Inicializa el modelo de reconocimiento facial de InsightFace
        self.model = insightface.app.FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        self.model.prepare(ctx_id=0, det_size=(640, 640))

    def extraer_embedding(self, ruta_imagen):
        # Extrae el embedding facial de la imagen dada
        img = cv2.imread(ruta_imagen)
        faces = self.model.get(img)
        if not faces:
            return None
        return faces[0].embedding  
    def comparar_embeddings(self, embedding1, embedding2, umbral=0.6):
        # Compara dos embeddings normalizados y retorna True si la distancia es menor al umbral
        self.emb1 = np.array([float(x) for x in embedding1.split(',')])
        self.emb2 = np.array([float(x) for x in embedding2.split(',')])
        self.emb1 = self.emb1 / np.linalg.norm(self.emb1)
        self.emb2 = self.emb2 / np.linalg.norm(self.emb2)
        distancia = np.linalg.norm(self.emb1 - self.emb2)
        print("Distancia entre embeddings:", distancia)
        return distancia < umbral

