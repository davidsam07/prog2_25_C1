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

@app.route('/proyectos', methods=['POST'])
@jwt_required()
def crear_proyecto():
    usuario = get_jwt_identity()
    nombre = request.args.get('nombre')

    if not nombre:
        return 'Nombre del proyecto requerido', 400

    if usuario not in proyectos:
        proyectos[usuario] = {}

    if nombre in proyectos[usuario]:
        return 'El proyecto ya existe', 409

    proyectos[usuario][nombre] = {"tareas": []}
    return f"Proyecto '{nombre}' creado para {usuario}", 201


@app.route('/proyectos', methods=['GET'])
@jwt_required()
def listar_proyectos():
    usuario = get_jwt_identity()
    return proyectos.get(usuario, {}), 200


@app.route('/proyectos/<nombre>/tareas', methods=['POST'])
@jwt_required()
def asignar_tarea_a_proyecto(nombre):
    usuario = get_jwt_identity()
    tarea_id = request.args.get('id')

    if not tarea_id or tarea_id not in tareas:
        return 'Tarea inválida o no encontrada', 404

    if tareas[tarea_id]['user'] != usuario:
        return 'No tienes permiso para esa tarea', 403

    if usuario not in proyectos or nombre not in proyectos[usuario]:
        return 'Proyecto no encontrado', 404

    if tarea_id not in proyectos[usuario][nombre]["tareas"]:
        proyectos[usuario][nombre]["tareas"].append(tarea_id)

    return f"Tarea {tarea_id} asignada al proyecto '{nombre}'", 200


@app.route('/proyectos/<nombre>/tareas', methods=['GET'])
@jwt_required()
def tareas_de_proyecto(nombre):
    usuario = get_jwt_identity()

    if usuario not in proyectos or nombre not in proyectos[usuario]:
        return 'Proyecto no encontrado', 404

    ids = proyectos[usuario][nombre]["tareas"]
    tareas_proyecto = {i: tareas[i] for i in ids if i in tareas}
    return tareas_proyecto, 200


@app.route('/proyectos/<nombre>/progreso', methods=['GET'])
@jwt_required()
def progreso_proyecto(nombre):
    usuario = get_jwt_identity()

    if usuario not in proyectos or nombre not in proyectos[usuario]:
        return 'Proyecto no encontrado', 404

    ids = proyectos[usuario][nombre]["tareas"]
    total = len(ids)
    if total == 0:
        return {"progreso": 0}, 200

    completadas = sum(1 for i in ids if i in tareas and tareas[i].get('estado') == 'Completada')
    progreso = (completadas / total) * 100
    return {"progreso": progreso}, 200
