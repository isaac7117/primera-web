from pymongo import MongoClient

class ConexionMongo:
    def __init__(self):
        self.cliente = MongoClient("mongodb://localhost:27017/")
        self.db = self.cliente['redsocial']
        self.publicaciones = self.db['publicaciones']
        
        # Verificar la conexión
        if self.cliente is not None:
            print("Conexión a MongoDB establecida correctamente.")
        else:
            print("Error al conectar a MongoDB.")
