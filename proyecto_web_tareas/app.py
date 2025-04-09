from flask import Flask, render_template, request, redirect, url_for
from gestor_de_tareas.gestores.gestor_tareas import GestorDeTareas, EstadoTarea

app = Flask(__name__)
gestor = GestorDeTareas()

@app.route("/")
def index():
    # Mostramos todas las tareas en la página principal
    tareas = gestor.listar_tareas()
    return render_template("index.html", tareas=tareas)

@app.route("/crear", methods=["POST"])
def crear():
    titulo = request.form["titulo"]
    descripcion = request.form.get("descripcion", "")
    fecha = request.form.get("fecha", "2025-05-30")
    prioridad = int(request.form.get("prioridad", 2))
    usuario = request.form.get("usuario", None)

    gestor.crear_tarea(titulo, descripcion, fecha, prioridad, usuario_asignado=usuario)
    return redirect(url_for("index"))

@app.route("/filtrar")
def filtrar():
    estado_str = request.args.get("estado", "pendiente").lower()
    # Convertimos a enum
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
    id_str = request.args.get("id", None)
    estado_str = request.args.get("estado", None)

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
    id_str = request.args.get("id", None)
    if not id_str:
        return redirect(url_for("index"))
    id_tarea = int(id_str)

    if request.method == "GET":
        # Renderizamos formulario
        tarea = gestor.obtener_por_id(id_tarea)
        if not tarea:
            return redirect(url_for("index"))
        return render_template("modificar.html", tarea=tarea)
    else:
        # Procesamos formulario
        titulo = request.form.get("titulo", "")
        descripcion = request.form.get("descripcion", "")
        fecha = request.form.get("fecha", None)
        prioridad = request.form.get("prioridad", None)
        prioridad = int(prioridad) if prioridad else None

        gestor.modificar_tarea(id_tarea, titulo, descripcion, fecha, prioridad)
        return redirect(url_for("index"))

@app.route("/asignar")
def asignar():
    id_str = request.args.get("id", None)
    usuario = request.args.get("usuario", None)

    if not id_str or not usuario:
        return redirect(url_for("index"))

    id_tarea = int(id_str)
    gestor.asignar_usuario_tarea(id_tarea, usuario)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def index():
    tareas = gestor.listar_tareas()
    return render_template("indice.html", tareas=tareas)
#Esto sirve para llamar al documento que le da forma y diseño a la página