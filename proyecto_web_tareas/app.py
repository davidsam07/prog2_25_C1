from flask import Flask, render_template, request, redirect, url_for

from gestor_de_tareas.gestores.gestor_tareas import GestorDeTareas
from gestor_de_tareas.clases.tarea import EstadoTarea


app = Flask(__name__)
gestor = GestorDeTareas()
proyectos = {}  

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form.get("descripcion", "")
        fecha = request.form.get("fecha")  # <- viene del formulario
        prioridad = int(request.form.get("prioridad", 2))
        usuario = request.form.get("usuario", None)

        # ✅ llamada correcta con nombre de parámetro correcto
        gestor.crear_tarea(
            titulo=titulo,
            descripcion=descripcion,
            fecha_limite_str=fecha,
            prioridad=prioridad,
            usuario_asignado=usuario
        )
        return redirect(url_for("index"))

    tareas = gestor.listar_tareas()
    return render_template("index.html", tareas=tareas)


@app.route("/filtrar")
def filtrar():
    estado_str = request.args.get("estado", "pendiente").lower()
    mapa_estados = {
        "pendiente": EstadoTarea.PENDIENTE,
        "en_progreso": EstadoTarea.EN_PROGRESO,
        "completada": EstadoTarea.COMPLETADA
    }
    estado = mapa_estados.get(estado_str, EstadoTarea.PENDIENTE)
    tareas_filtradas = gestor.filtrar_por_estado(estado)
    return render_template("filtrar.html", tareas=tareas_filtradas)


@app.route("/cambiar_estado")
def cambiar_estado():
    id_str = request.args.get("id")
    estado_str = request.args.get("estado")

    if not id_str or not estado_str:
        return redirect(url_for("index"))

    id_tarea = int(id_str)
    mapa_estados = {
        "pendiente": EstadoTarea.PENDIENTE,
        "en_progreso": EstadoTarea.EN_PROGRESO,
        "completada": EstadoTarea.COMPLETADA
    }
    nuevo_estado = mapa_estados.get(estado_str, EstadoTarea.PENDIENTE)
    gestor.cambiar_estado_tarea(id_tarea, nuevo_estado)
    return redirect(url_for("index"))


@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    id_str = request.args.get("id")
    if not id_str:
        return redirect(url_for("index"))

    id_tarea = int(id_str)

    if request.method == "GET":
        tarea = gestor.obtener_por_id(id_tarea)
        if not tarea:
            return redirect(url_for("index"))
        return render_template("modificar.html", tarea=tarea)
    else:
        titulo = request.form.get("titulo", "")
        descripcion = request.form.get("descripcion", "")
        fecha = request.form.get("fecha", None)
        prioridad = request.form.get("prioridad", None)
        prioridad = int(prioridad) if prioridad else None
        gestor.modificar_tarea(id_tarea, titulo, descripcion, fecha, prioridad)
        return redirect(url_for("index"))


@app.route("/asignar")
def asignar():
    id_str = request.args.get("id")
    usuario = request.args.get("usuario")

    if not id_str or not usuario:
        return redirect(url_for("index"))

    id_tarea = int(id_str)
    gestor.asignar_usuario_tarea(id_tarea, usuario)
    return redirect(url_for("index"))


@app.route("/eliminar")
def eliminar():
    id_str = request.args.get("id")
    if not id_str:
        return redirect(url_for("index"))

    id_tarea = int(id_str)
    gestor.eliminar_tarea(id_tarea)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)


@app.route('/proyectos', methods=['POST'])
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
def listar_proyectos():
    usuario = get_jwt_identity()
    return proyectos.get(usuario, {}), 200



@app.route('/proyectos/<nombre>/tareas', methods=['POST'])
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
def tareas_de_proyecto(nombre):
    usuario = get_jwt_identity()

    if usuario not in proyectos or nombre not in proyectos[usuario]:
        return 'Proyecto no encontrado', 404

    ids = proyectos[usuario][nombre]["tareas"]
    tareas_proyecto = {i: tareas[i] for i in ids if i in tareas}
    return tareas_proyecto, 200



@app.route('/proyectos/<nombre>/progreso', methods=['GET'])
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
