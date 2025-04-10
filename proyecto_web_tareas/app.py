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


@app.route("/proyectos")
def ver_proyectos():
    proyectos = gestor_proyectos.proyectos
    return render_template("proyectos.html", proyectos=proyectos)


@app.route("/proyectos/crear", methods=["POST"])
def crear_proyecto():
    nombre = request.form.get("nombre")
    if nombre:
        gestor_proyectos.crear_proyecto(nombre)
    return redirect(url_for("ver_proyectos"))


@app.route("/proyectos/asignar", methods=["POST"])
def asignar_tarea_a_proyecto():
    id_tarea = int(request.form.get("id_tarea"))
    nombre_proyecto = request.form.get("nombre_proyecto")

    tarea = gestor.obtener_por_id(id_tarea)
    if tarea and nombre_proyecto in gestor_proyectos.proyectos:
        gestor_proyectos.agregar_tarea_a_proyecto(nombre_proyecto, tarea)

    return redirect(url_for("ver_proyectos"))



@app.route("/proyectos/<nombre>/tareas")
def tareas_de_proyecto(nombre):
    proyecto = gestor_proyectos.proyectos.get(nombre)
    if not proyecto:
        return redirect(url_for("ver_proyectos"))
    tareas = proyecto.tareas
    return render_template("tareas_proyecto.html", nombre=proyecto.nombre, tareas=tareas)



@app.route("/proyectos/<nombre>/progreso")
def progreso_de_proyecto(nombre):
    proyecto = gestor_proyectos.proyectos.get(nombre)
    if not proyecto:
        return redirect(url_for("ver_proyectos"))
    progreso = proyecto.progreso()
    return render_template("progreso.html", nombre=nombre, progreso=progreso)



if __name__ == "__main__":
    app.run(debug=True)