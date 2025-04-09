from flask import Flask, render_template, request, redirect
from gestor_de_tareas.gestores.gestor_tareas import GestorDeTareas

app = Flask(__name__)
gestor = GestorDeTareas()

@app.route("/")
def index():
    tareas = gestor.listar_tareas()
    return render_template("index.html", tareas=tareas)

@app.route("/crear", methods=["POST"])
def crear():
    titulo = request.form["titulo"]
    if titulo:
        gestor.crear_tarea(titulo, "", "2025-05-30", 2)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
