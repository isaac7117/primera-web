from conexiondb import ConexionMongo

class CRUDPublicaciones:
    def __init__(self):
        self.conexion = ConexionMongo()

    def crear_publicacion(self, titulo, contenido, imagen=None):
        publicacion = {'titulo': titulo, 'contenido': contenido, 'imagen': imagen}
        self.conexion.publicaciones.insert_one(publicacion)

    def obtener_publicaciones(self):
        return list(self.conexion.publicaciones.find())

    def eliminar_publicacion(self, id):
        self.conexion.publicaciones.delete_one({'_id': id})
