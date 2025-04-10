"""
Task Management Web Application
================================

Este módulo implementa una aplicación web utilizando Flask para la gestión de tareas y proyectos.
Se definen rutas para crear, listar, modificar, filtrar, eliminar tareas, así como para gestionar proyectos.

Dependencias:
    - Flask
    - gestor_de_tareas.gestores.gestor_tareas (GestorDeTareas)
    - gestor_de_tareas.clases.tarea (EstadoTarea)
    - gestor_de_tareas.gestores.proyectos (GestorProyectos)

Ejemplo de uso:
    Ejecutar el módulo para iniciar el servidor de desarrollo:
        $ python app.py
"""

from flask import Flask, render_template, request, redirect, url_for
from gestor_de_tareas.gestores.gestor_tareas import GestorDeTareas
from gestor_de_tareas.clases.tarea import EstadoTarea
from gestor_de_tareas.gestores.proyectos import GestorProyectos

app = Flask(__name__)
gestor = GestorDeTareas()  # Instancia para gestionar tareas
proyectos = {}  
gestor_proyectos = GestorProyectos()  # Instancia para gestionar proyectos

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Muestra la lista de tareas y permite la creación de una nueva tarea.

    Para solicitudes GET, se renderiza la plantilla principal con la lista de tareas.
    Para solicitudes POST, se obtiene la información del formulario y se crea una nueva tarea.

    Returns
    -------
    flask.Response
        Si el método es GET, retorna la plantilla 'index.html' con la lista de tareas.
        Si el método es POST, redirige a la ruta principal tras crear la tarea.
    """
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form.get("descripcion", "")
        fecha = request.form.get("fecha")  # Fecha proveniente del formulario
        prioridad = int(request.form.get("prioridad", 2))
        usuario = request.form.get("usuario", None)

        # Creación de la tarea con los parámetros indicados.
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
    """
    Filtra y muestra las tareas según su estado.

    Obtiene el parámetro 'estado' desde la URL y lo mapea a un objeto EstadoTarea.
    Si no se especifica, se usa el estado 'pendiente' por defecto.

    Returns
    -------
    flask.Response
        Renderiza la plantilla 'filtrar.html' con la lista de tareas filtradas.
    """
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
    """
    Cambia el estado de una tarea.

    Se espera que se pasen los parámetros 'id' y 'estado' en la URL.
    Si alguno de ellos falta, redirige a la página principal.
    Mapea el parámetro 'estado' a un objeto de EstadoTarea y actualiza la tarea.

    Returns
    -------
    flask.Response
        Redirige a la ruta principal.
    """
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
    """
    Permite modificar los datos de una tarea existente.

    Para solicitudes GET, se recupera la tarea a modificar y se muestra en la plantilla 'modificar.html'.
    Para solicitudes POST, se actualizan los campos de la tarea con los datos enviados por el formulario.

    Returns
    -------
    flask.Response
        En GET: Renderiza 'modificar.html' con la tarea.
        En POST: Redirige a la página principal tras actualizar la tarea.
    """
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
    """
    Asigna un usuario a una tarea.

    Se reciben los parámetros 'id' y 'usuario' por la URL, y se asigna el usuario correspondiente a la tarea.
    Si los parámetros faltan, redirige a la página principal.

    Returns
    -------
    flask.Response
        Redirige a la ruta principal.
    """
    id_str = request.args.get("id")
    usuario = request.args.get("usuario")

    if not id_str or not usuario:
        return redirect(url_for("index"))

    id_tarea = int(id_str)
    gestor.asignar_usuario_tarea(id_tarea, usuario)
    return redirect(url_for("index"))

@app.route("/eliminar")
def eliminar():
    """
    Elimina una tarea.

    Se obtiene el identificador de la tarea desde la URL y se elimina la tarea.
    Si no se indica el ID, se redirige a la página principal.

    Returns
    -------
    flask.Response
        Redirige a la ruta principal.
    """
    id_str = request.args.get("id")
    if not id_str:
        return redirect(url_for("index"))

    id_tarea = int(id_str)
    gestor.eliminar_tarea(id_tarea)
    return redirect(url_for("index"))

@app.route("/proyectos")
def ver_proyectos():
    """
    Muestra la lista de proyectos.

    Recupera el diccionario de proyectos desde el gestor de proyectos y renderiza la plantilla
    'proyectos.html' con dichos proyectos.

    Returns
    -------
    flask.Response
        Renderiza la plantilla 'proyectos.html' con la lista de proyectos.
    """
    proyectos = gestor_proyectos.proyectos
    return render_template("proyectos.html", proyectos=proyectos)

@app.route("/proyectos/crear", methods=["POST"])
def crear_proyecto():
    """
    Crea un nuevo proyecto.

    Recibe desde un formulario el nombre del proyecto y lo crea si se proporciona.
    Redirige a la lista de proyectos después de la creación.

    Returns
    -------
    flask.Response
        Redirige a la ruta '/proyectos'.
    """
    nombre = request.form.get("nombre")
    if nombre:
        gestor_proyectos.crear_proyecto(nombre)
    return redirect(url_for("ver_proyectos"))

@app.route("/proyectos/asignar", methods=["POST"])
def asignar_tarea_a_proyecto():
    """
    Asigna una tarea a un proyecto específico.

    Recibe el ID de la tarea y el nombre del proyecto desde el formulario.
    Si la tarea existe y el proyecto es válido, agrega la tarea al proyecto.
    Redirige a la lista de proyectos.

    Returns
    -------
    flask.Response
        Redirige a la ruta '/proyectos'.
    """
    id_tarea = int(request.form.get("id_tarea"))
    nombre_proyecto = request.form.get("nombre_proyecto")

    tarea = gestor.obtener_por_id(id_tarea)
    if tarea and nombre_proyecto in gestor_proyectos.proyectos:
        gestor_proyectos.agregar_tarea_a_proyecto(nombre_proyecto, tarea)

    return redirect(url_for("ver_proyectos"))

@app.route("/proyectos/<nombre>/tareas")
def tareas_de_proyecto(nombre: str):
    """
    Muestra las tareas asociadas a un proyecto específico.

    Parámetros
    ----------
    nombre : str
        Nombre del proyecto.

    Returns
    -------
    flask.Response
        Si el proyecto existe, renderiza 'tareas_proyecto.html' con las tareas.
        Si no existe, redirige a la lista de proyectos.
    """
    proyecto = gestor_proyectos.proyectos.get(nombre)
    if not proyecto:
        return redirect(url_for("ver_proyectos"))
    tareas = proyecto.tareas
    return render_template("tareas_proyecto.html", nombre=proyecto.nombre, tareas=tareas)

@app.route("/proyectos/<nombre>/progreso")
def progreso_de_proyecto(nombre: str):
    """
    Muestra el progreso de un proyecto.

    Obtiene el proyecto por nombre, calcula su progreso mediante el método
    correspondiente y renderiza la plantilla 'progreso.html' con los datos.

    Parámetros
    ----------
    nombre : str
        Nombre del proyecto.

    Returns
    -------
    flask.Response
        Si el proyecto existe, renderiza 'progreso.html' con el progreso del proyecto.
        Si no existe, redirige a la lista de proyectos.
    """
    proyecto = gestor_proyectos.proyectos.get(nombre)
    if not proyecto:
        return redirect(url_for("ver_proyectos"))
    progreso = proyecto.progreso()
    return render_template("progreso.html", nombre=nombre, progreso=progreso)

if __name__ == "__main__":
    app.run(debug=True)
