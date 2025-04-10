from flask import Flask, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "bocatalomoya"  # Cambia esta clave por una más segura
jwt = JWTManager(app)

# Base de datos simulada para los usuarios y tareas
usuarios = {}
tareas = {}


# Ruta de prueba para verificar el funcionamiento de la API
@app.route('/')
def hello_world():
    return 'API de Gestión de Tareas Colaborativas'


# Registro de usuario
@app.route('/signup', methods=['POST'])
def signup():
    username = request.args.get('user', '')
    if username in usuarios:
        return f'Usuario {username} ya existe', 409
    else:
        contraseña = request.args.get('contraseña', '')
        hashed = hashlib.sha256(contraseña.encode()).hexdigest()
        usuarios[username] = hashed
        return f'Usuario {username} registrado con éxito', 200


# Inicio de sesión de usuario
@app.route('/signin', methods=['GET'])
def signin():
    username = request.args.get('user', '')
    contraseña = request.args.get('contraseña', '')
    hashed = hashlib.sha256(contraseña.encode()).hexdigest()

    if username in usuarios and usuarios[username] == hashed:
        # Crear el token de acceso
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200
    else:
        return 'Usuario o contraseña incorrectos', 401


# Obtener todas las tareas (requiere autenticación JWT)
@app.route('/tareas', methods=['GET'])
@jwt_required()
def get_tareas():
    usuario_actual = get_jwt_identity()  # Obtener el usuario actual
    usuario_tareas = {tarea_id: tarea for tarea_id, tarea in tareas.items() if tarea['user'] == usuario_actual}
    return usuario_tareas, 200


# Obtener una tarea específica (requiere autenticación JWT)
@app.route('/tareas/<tarea_id>', methods=['GET'])
@jwt_required()
def get_tarea(tarea_id):
    usuario_actual = get_jwt_identity()  # Obtener el usuario actual
    tarea = tareas.get(tarea_id)
    if tarea and tarea['user'] == usuario_actual:
        return tarea, 200
    else:
        return 'Tarea no encontrada o no tienes permiso', 404


# Crear una nueva tarea (requiere autenticación JWT)
@app.route('/tareas', methods=['POST'])
@jwt_required()
def create_tarea():
    usuario_actual = get_jwt_identity()  # Obtener el usuario actual
    tarea_name = request.args.get('name', '')
    tarea_description = request.args.get('description', '')

    if not tarea_name:
        return 'El nombre de la tarea es obligatorio', 400

    tarea_id = str(len(tareas) + 1)  # Generar un ID simple basado en la longitud de las tareas existentes
    tareas[tarea_id] = {
        'name': tarea_name,
        'description': tarea_description,
        'user': usuario_actual
    }
    return f'Tarea {tarea_id} creada con éxito', 201


# Actualizar una tarea existente (requiere autenticación JWT)
@app.route('/tareas/<tarea_id>', methods=['PUT'])
@jwt_required()
def update_tarea(tarea_id):
    usuario_actual = get_jwt_identity()  # Obtener el usuario actual
    tarea = tareas.get(tarea_id)

    if tarea and tarea['user'] == usuario_actual:
        tarea_name = request.args.get('name', tarea['name'])
        tarea_description = request.args.get('description', tarea['description'])

        tarea['name'] = tarea_name
        tarea['description'] = tarea_description
        return f'Tarea {tarea_id} actualizada', 200
    else:
        return 'Tarea no encontrada o no tienes permiso', 404


# Eliminar una tarea (requiere autenticación JWT)
@app.route('/tareas/<tarea_id>', methods=['DELETE'])
@jwt_required()
def delete_tarea(tarea_id):
    usuario_actual = get_jwt_identity()  # Obtener el usuario actual
    tarea = tareas.get(tarea_id)

    if tarea and tarea['user'] == usuario_actual:
        del tareas[tarea_id]
        return f'Tarea {tarea_id} eliminada', 200
    else:
        return 'Tarea no encontrada o no tienes permiso', 404


if __name__ == '__main__':
    app.run(debug=True)
