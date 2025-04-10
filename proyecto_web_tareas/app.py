"""
Aplicación Web de Gestión de Tareas y Proyectos
===============================================

Este módulo implementa la aplicación web para gestionar tareas y proyectos utilizando Flask.
Se definen rutas para crear, listar, modificar, filtrar, asignar, cambiar el estado y eliminar tareas,
además de gestionar proyectos.

Dependencias:
    - Flask: para crear la aplicación web.
    - gestor_de_tareas.gestores.gestor_tareas: GestorDeTareas para gestionar las tareas.
    - gestor_de_tareas.clases.tarea: EstadoTarea para indicar el estado de cada tarea.
    - (Opcional) gestor_de_tareas.gestores.proyectos: GestorProyectos para la gestión de proyectos.

Ejemplo de ejecución:
    Ejecutar el módulo para iniciar el servidor en modo debug:
        $ python app.py
"""

from flask import Flask, render_template, request, redirect, url_for
from gestor_de_tareas.gestores.gestor_tareas import GestorDeTareas
from gestor_de_tareas.clases.tarea import EstadoTarea

# Se asume que existe un módulo para la gestión de proyectos.
# En un ejemplo completo, se debería importar así:
# from gestor_de_tareas.gestores.proyectos import GestorProyectos

app = Flask(__name__)
gestor = GestorDeTareas()
# Se crea un diccionario vacío para proyectos, pero se asume que en la versión completa se utiliza
# una instancia de GestorProyectos. Por ejemplo:
# gestor_proyectos = GestorProyectos()
# Para efectos de este ejemplo, se utiliza la variable 'gestor_proyectos' definida a continuación.
gestor_proyectos = type("GestorProyectosDummy", (), {"proyectos": {}})()  # Dummy para evitar errores


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Ruta principal para visualizar y crear tareas.

    Para solicitudes GET, se listan todas las tareas y se renderiza la plantilla "index.html".
    Para solicitudes POST, se extraen los datos del formulario para crear una nueva tarea y se redirige
    nuevamente a la página principal.

    Returns
    -------
    flask.Response
        Respuesta HTTP que renderiza la plantilla correspondiente o redirige a la misma ruta.
    """
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form.get("descripcion", "")
        fecha = request.form.get("fecha")  # Fecha recibida desde el formulario (en formato de cadena).
        prioridad = int(request.form.get("prioridad", 2))
        usuario = request.form.get("usuario", None)

        # Creación de la tarea utilizando parámetros nombrados.
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
    Ruta para filtrar tareas por estado.

    Obtiene el parámetro 'estado' desde la URL, lo mapea a un valor de EstadoTarea y
    renderiza la plantilla "filtrar.html" con las tareas que coinciden con dicho estado.

    Returns
    -------
    flask.Response
        Respuesta HTTP que renderiza la plantilla "filtrar.html" con la lista de tareas filtradas.
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
    Ruta para cambiar el estado de una tarea.

    Se esperan los parámetros 'id' y 'estado' en la URL. Si alguno no se proporciona,
    redirige a la página principal. Se mapea el estado recibido a un miembro de EstadoTarea
    y se actualiza la tarea correspondiente.

    Returns
    -------
    flask.Response
        Redirige a la ruta principal tras actualizar el estado de la tarea.
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
    Ruta para modificar una tarea existente.

    En una solicitud GET, se recupera la tarea mediante su ID y se muestra en la plantilla "modificar.html".
    En una solicitud POST, se actualizan los campos de la tarea utilizando los datos del formulario y se redirige
    a la página principal.

    Returns
    -------
    flask.Response
        Renderiza la plantilla "modificar.html" en GET o redirige a la página principal en POST.
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
    Ruta para asignar un usuario a una tarea.

    Se reciben los parámetros 'id' y 'usuario' desde la URL. Si alguno falta,
    redirige a la página principal. Se actualiza la asignación del usuario a la tarea.

    Returns
    -------
    flask.Response
        Redirige a la ruta principal tras asignar el usuario.
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
    Ruta para eliminar una tarea.

    Se obtiene el parámetro 'id' desde la URL. Si no se proporciona, redirige a la página principal.
    La tarea identificada se elimina y se redirige de nuevo a la ruta principal.

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
    Ruta para visualizar la lista de proyectos.

    Se recupera el diccionario de proyectos y se renderiza la plantilla "proyectos.html".

    Returns
    -------
    flask.Response
        Respuesta HTTP que renderiza la plantilla "proyectos.html" con los proyectos.
    """
    proyectos = gestor_proyectos.proyectos
    return render_template("proyectos.html", proyectos=proyectos)


@app.route("/proyectos/crear", methods=["POST"])
def crear_proyecto():
    """
    Ruta para crear un nuevo proyecto.

    Se obtiene el nombre del proyecto desde un formulario y, de existir, se invoca la creación
    del proyecto, redirigiendo posteriormente a la lista de proyectos.

    Returns
    -------
    flask.Response
        Redirige a la ruta "/proyectos" después de intentar crear el proyecto.
    """
    nombre = request.form.get("nombre")
    if nombre:
        gestor_proyectos.crear_proyecto(nombre)
    return redirect(url_for("ver_proyectos"))


@app.route("/proyectos/asignar", methods=["POST"])
def asignar_tarea_a_proyecto():
    """
    Ruta para asignar una tarea a un proyecto.

    Se obtiene el ID de la tarea y el nombre del proyecto desde el formulario.
    Si la tarea existe y el proyecto es válido, se asigna la tarea al proyecto.

    Returns
    -------
    flask.Response
        Redirige a la ruta "/proyectos" tras asignar la tarea.
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
    Ruta para listar las tareas asociadas a un proyecto específico.

    Parameters
    ----------
    nombre : str
        Nombre del proyecto.

    Returns
    -------
    flask.Response
        Si el proyecto existe, renderiza "tareas_proyecto.html" con sus tareas.
        Si no, redirige a la ruta de visualización de proyectos.
    """
    proyecto = gestor_proyectos.proyectos.get(nombre)
    if not proyecto:
        return redirect(url_for("ver_proyectos"))
    tareas = proyecto.tareas
    return render_template("tareas_proyecto.html", nombre=proyecto.nombre, tareas=tareas)


@app.route("/proyectos/<nombre>/progreso")
def progreso_de_proyecto(nombre: str):
    """
    Ruta para visualizar el progreso de un proyecto.

    Se obtiene el proyecto por nombre, se calcula el porcentaje de tareas completadas y se
    renderiza la plantilla "progreso.html" mostrando dicho progreso.

    Parameters
    ----------
    nombre : str
        Nombre del proyecto.

    Returns
    -------
    flask.Response
        Si el proyecto existe, renderiza "progreso.html" con el progreso.
        Si no, redirige a la ruta de visualización de proyectos.
    """
    proyecto = gestor_proyectos.proyectos.get(nombre)
    if not proyecto:
        return redirect(url_for("ver_proyectos"))
    progreso = proyecto.progreso()
    return render_template("progreso.html", nombre=nombre, progreso=progreso)


if __name__ == "__main__":
    app.run(debug=True)
