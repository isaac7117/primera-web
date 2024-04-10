from flask import Flask, request, redirect, url_for, jsonify, render_template, url_for, send_from_directory,session
from crud import CRUDPublicaciones
from werkzeug.utils import secure_filename
import os
from pymongo import MongoClient
from flask import flash

app = Flask(__name__)
app.secret_key = '12345'
crud = CRUDPublicaciones()
app.static_folder = 'uploads'


# Configuración para el cargado de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    publicaciones = crud.obtener_publicaciones()
    return render_template('index.html', publicaciones=publicaciones)


@app.route('/publicaciones', methods=['POST'])
def crear_publicacion():
    datos = request.form
    titulo = datos['titulo']
    contenido = datos['contenido']
    
    # Manejo de la imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '' and allowed_file(imagen.filename):
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
    else:
        filename = None
    
    crud.crear_publicacion(titulo, contenido, filename)
    
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/publicaciones/<id>', methods=['DELETE'])
def eliminar_publicacion(id):
    crud.eliminar_publicacion(id)
    return jsonify({'mensaje': 'Publicación eliminada satisfactoriamente'})


#-----------Login-------------#

# Conectar a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['registro_usuarios']
usuarios_collection = db['usuarios']

@app.route('/registro', methods=['POST'])
def registro():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Insertar el usuario en la colección
    usuarios_collection.insert_one({'username': username, 'email': email, 'password': password})
    return redirect(url_for('index'))


# Definir ruta para el inicio de sesión
@app.route('/inicio_sesion', methods=['POST'])
def inicio_sesion():
    email = request.form['email']
    password = request.form['password']

    # Buscar el usuario en la base de datos por email
    usuario = usuarios_collection.find_one({'email': email})

    # Verificar la contraseña
    if usuario and usuario['password'] == password:
        # Inicio de sesión exitoso, establecer sesión
        session['email'] = email
        return redirect(url_for('index'))
    else:
        # Usuario o contraseña incorrectos, redirigir de nuevo al formulario de inicio de sesión
        return render_template('inicio.html', error='Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'email' in session:
        email = session['email']
        usuario = usuarios_collection.find_one({'email': email})
        
        if request.method == 'POST':
            # Manejar la inserción de la foto de perfil
            foto_perfil = request.files['foto_perfil']
            if foto_perfil:
                nombre_foto_perfil = secure_filename(foto_perfil.filename)
                foto_perfil.save(os.path.join(app.config['UPLOAD_FOLDER'], nombre_foto_perfil))
                usuarios_collection.update_one({'_id': usuario['_id']}, {'$set': {'foto_perfil': nombre_foto_perfil}})
                flash('Foto de perfil actualizada correctamente', 'success')
                return redirect(url_for('perfil'))
        
        # Obtener las publicaciones del usuario
        publicaciones = crud.obtener_publicaciones_usuario(email)
        
        return render_template('perfil.html', email=email, usuario=usuario, publicaciones=publicaciones)
    else:
        return 'Debes iniciar sesión para acceder al perfil'


@app.route('/mostrar_perfil/<nombre_foto>')
def mostrar_perfil(nombre_foto):
    return send_from_directory(app.config['UPLOAD_FOLDER'], nombre_foto)

@app.route('/retornar_a_perfil')
def retornar_a_perfil():
    return redirect(url_for('perfil'))

@app.route("/inicio")
def inicia():
    return render_template("inicio.html")


@app.route("/login")
def logi():
    return render_template("Registro.html")

@app.route("/perf")
def perfi():
    return render_template("perfil.html")

#--------Perfil--------#

@app.route('/mostrar_usuario')
def mostrar_usuario():
    # Obtener el nombre de usuario desde la base de datos (aquí asumiendo que se obtiene el primer usuario)
    usuario = usuarios_collection.find_one()

    # Obtener el nombre de usuario si se encuentra en la base de datos
    nombre_de_usuario = usuario['username'] if usuario else "Usuario desconocido"

    # Pasar el nombre de usuario a la plantilla mostrar_usuario.html
    return render_template('mostrar_usuario.html', nombre_de_usuario=nombre_de_usuario)

# Consultar todos los documentos en la colección usuarios
datos = usuarios_collection.find()

# Iterar sobre los documentos y mostrarlos en la terminal
for dato in datos:
    print(dato)

if __name__ == '__main__':
    app.run(debug=True, ssl_context=("cert.pem", "key.pem"))