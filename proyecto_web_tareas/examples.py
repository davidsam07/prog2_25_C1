import requests
from time import sleep

BASE_URL = "http://127.0.0.1:5000"

def crear_tarea(titulo, descripcion, fecha, prioridad, usuario):
    data = {
        "titulo": titulo,
        "descripcion": descripcion,
        "fecha": fecha,
        "prioridad": prioridad,
        "usuario": usuario
    }
    res = requests.post(f"{BASE_URL}/", data=data)
    print(f"[+] Tarea creada: {titulo} | Status: {res.status_code}")

def listar_tareas():
    print("\n📋 Listando tareas actuales:")
    res = requests.get(f"{BASE_URL}/")
    if res.status_code == 200:
        print("Página principal cargada correctamente.\n")
    else:
        print("Error al cargar las tareas.")

def cambiar_estado(id_tarea, estado):
    res = requests.get(f"{BASE_URL}/cambiar_estado?id={id_tarea}&estado={estado}")
    print(f"[→] Tarea {id_tarea} cambiada a estado '{estado}' | Status: {res.status_code}")

def asignar_usuario(id_tarea, usuario):
    res = requests.get(f"{BASE_URL}/asignar?id={id_tarea}&usuario={usuario}")
    print(f"[→] Tarea {id_tarea} asignada a {usuario} | Status: {res.status_code}")

def modificar_tarea(id_tarea, nuevo_titulo, nueva_desc, nueva_fecha, nueva_prioridad):
    data = {
        "titulo": nuevo_titulo,
        "descripcion": nueva_desc,
        "fecha": nueva_fecha,
        "prioridad": nueva_prioridad
    }
    res = requests.post(f"{BASE_URL}/modificar?id={id_tarea}", data=data)
    print(f"[✏️] Tarea {id_tarea} modificada | Status: {res.status_code}")

def eliminar_tarea(id_tarea):
    res = requests.get(f"{BASE_URL}/eliminar?id={id_tarea}")
    print(f"[🗑️] Tarea {id_tarea} eliminada | Status: {res.status_code}")

def pausa():
    sleep(1.5)

# --------------------------
if __name__ == "__main__":
    print("=== GESTOR DE TAREAS - API DE PRUEBAS ===")

    # Crear tareas
    crear_tarea("Estudiar Flask", "Repasar rutas y Jinja", "2025-04-25", 1, "Darío")
    pausa()
    crear_tarea("Actualizar CV", "Añadir proyectos recientes", "2025-05-01", 2, "Laura")
    pausa()
    crear_tarea("Entrenamiento", "Gimnasio al menos 3 veces", "2025-04-30", 3, "")
    pausa()

    listar_tareas()
    pausa()

    modificar_tarea(1, "Estudiar Flask avanzado", "Jinja + sesiones", "2025-05-01", 1)
    pausa()

    cambiar_estado(1, "completada")
    pausa()
    cambiar_estado(2, "en_progreso")
    pausa()

    asignar_usuario(3, "Carlos")
    pausa()

    eliminar_tarea(2)
    pausa()

    listar_tareas()
    print("\n✅ Pruebas finalizadas.")
