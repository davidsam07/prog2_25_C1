import requests
from proyectos import GestorProyectos  # Asegúrate de que el archivo esté nombrado correctamente



# URL base de la API
BASE_URL = "http://127.0.0.1:5000"  # Asegúrate de que tu servidor Flask esté en funcionamiento


# Función para registrar un usuario
def signup():
    usuario = input("Introduce el nombre de usuario: ")
    contraseña = input("Introduce la contraseña: ")

    respuesta = requests.post(f"{BASE_URL}/signup", params={'user': usuario, 'contraseña': contraseña})
    print(respuesta.text)


# Función para iniciar sesión (y obtener el token)
def signin():
    usuario = input("Introduce el nombre de usuario: ")
    contraseña = input("Introduce la contraseña: ")

    respuesta = requests.get(f"{BASE_URL}/signin", params={'usuario': usuario, 'contraseña': contraseña})
    if respuesta.status_code == 200:
        data = respuesta.json()
        print(f"Token de acceso: {data['access_token']}")
        return data['access_token']
    else:
        print(respuesta.text)
        return None


# Función para obtener todas las tareas (requiere token)
def get_tasks(token):
    headers = {'Authorization': f'Bearer {token}'}
    respuesta = requests.get(f"{BASE_URL}/tareas", headers=headers)

    if respuesta.status_code == 200:
        tareas = respuesta.json()
        if tareas:
            print("Tareas:")
            for tarea_id, tarea in tasks.items():
                print(f"ID: {tarea_id}, Nombre: {tarea['nombre']}, Descripción: {tarea['description']}")
        else:
            print("No tienes tareas.")
    else:
        print(respuesta.text)


# Función para crear una nueva tarea (requiere token)
def create_task(token):
    headers = {'Authorization': f'Bearer {token}'}
    nombre = input("Introduce el nombre de la tarea: ")
    descripcion = input("Introduce la descripción de la tarea: ")

    respuesta = requests.post(f"{BASE_URL}/tareas", params={'nombre': nombre, 'descripcion': descripcion}, headers=headers)
    print(respuesta.text)


# Función para actualizar una tarea (requiere token)
def update_task(token):
    headers = {'Authorization': f'Bearer {token}'}
    tarea_id = input("Introduce el ID de la tarea a actualizar: ")
    
    # Primero obtener la tarea actual
    respuesta = requests.get(f"{BASE_URL}/tareas/{tarea_id}", headers=headers)
    if respuesta.status_code != 200:
        print("Error al obtener la tarea:", respuesta.text)
        return
    
    tarea_actual = respuesta.json()
    
    # Solicitar nuevos valores
    nombre = input(f"Nuevo nombre [{tarea_actual['name']}]: ") or tarea_actual['name']
    descripcion = input(f"Nueva descripción [{tarea_actual.get('description', '')}]: ") or tarea_actual.get('description', '')
    estado = input(f"Nuevo estado (Pendiente/Completada) [{tarea_actual.get('estado', 'Pendiente')}]: ") or tarea_actual.get('estado', 'Pendiente')
    
    # Actualizar la tarea
    respuesta = requests.put(f"{BASE_URL}/tareas/{tarea_id}",
                          params={'name': nombre, 'description': descripcion, 'estado': estado},
                          headers=headers)
    print(respuesta.text)

    def completar_tarea(token):
    headers = {'Authorization': f'Bearer {token}'}
    tarea_id = input("Introduce el ID de la tarea a completar: ")
    respuesta = requests.put(f"{BASE_URL}/tareas/{tarea_id}",
                          params={'estado': 'Completada'},
                          headers=headers)
    print(respuesta.text)

# Función para eliminar una tarea (requiere token)
def delete_task(token):
    headers = {'Authorization': f'Bearer {token}'}
    tarea_id = input("Introduce el ID de la tarea a eliminar: ")

    respuesta = requests.delete(f"{BASE_URL}/tareas/{tarea_id}", headers=headers)
    print(respuesta.text)

# Función para crear un proyecto (requiere token)
def crear_proyecto(token):
    headers = {'Authorization': f'Bearer {token}'}
    nombre = input("Introduce el nombre del proyecto: ")
    respuesta = requests.post(f"{BASE_URL}/proyectos", params={'nombre': nombre}, headers=headers)
    print(respuesta.text)

# Función para ver un proyecto (requiere token)
def ver_proyectos(token):
    headers = {'Authorization': f'Bearer {token}'}
    respuesta = requests.get(f"{BASE_URL}/proyectos", headers=headers)
    if respuesta.status_code == 200:
        proyectos = respuesta.json()
        if proyectos:
            print("\nProyectos:")
            print("-" * 40)
            for nombre, detalles in proyectos.items():
                print(f"Nombre: {nombre}")
                print(f"Tareas asignadas: {len(detalles['tareas'])}")
                print("-" * 40)
        else:
            print("No tienes proyectos.")
    else:
        print(respuesta.text)

# Función para asignar una tarea a un proyecto (requiere token)
def asignar_tarea_a_proyecto(token):
    headers = {'Authorization': f'Bearer {token}'}
    nombre_proyecto = input("Introduce el nombre del proyecto: ")
    tarea_id = input("Introduce el ID de la tarea a asignar: ")
    respuesta = requests.post(f"{BASE_URL}/proyectos/{nombre_proyecto}/tareas", params={'id': tarea_id}, headers=headers)
    print(respuesta.text)

# Función para ver las tareas de un proyecto (requiere token)
def ver_tareas_de_proyecto(token):
    headers = {'Authorization': f'Bearer {token}'}
    nombre_proyecto = input("Introduce el nombre del proyecto: ")
    respuesta = requests.get(f"{BASE_URL}/proyectos/{nombre_proyecto}/tareas", headers=headers)
    if respuesta.status_code == 200:
        tareas_proyecto = respuesta.json()
        if tareas_proyecto:
            print(f"\nTareas del proyecto '{nombre_proyecto}':")
            print("-" * 60)
            for tarea_id, tarea in tareas_proyecto.items():
                print(f"ID: {tarea_id}")
                print(f"Nombre: {tarea['name']}")
                print(f"Descripción: {tarea.get('description', 'Sin descripción')}")
                print(f"Estado: {tarea.get('estado', 'Pendiente')}")
                print("-" * 60)
        else:
            print("El proyecto no tiene tareas asignadas.")
    else:
        print(respuesta.text)

# Función para ver el progreso de un proyecto (requiere token)
def ver_progreso(token):
    headers = {'Authorization': f'Bearer {token}'}
    nombre_proyecto = input("Introduce el nombre del proyecto: ")
    respuesta = requests.get(f"{BASE_URL}/proyectos/{nombre_proyecto}/progreso", headers=headers)
    if respuesta.status_code == 200:
        progreso = respuesta.json()
        print(f"\nProgreso del proyecto '{nombre_proyecto}':")
        print(f"Tareas completadas: {progreso.get('completadas', 0)}")
        print(f"Total de tareas: {progreso.get('total', 0)}")
        print(f"Progreso: {progreso.get('progreso', 0):.2f}%")
    else:
        print(respuesta.text)



def main():
    print("Bienvenido al sistema de gestión de tareas colaborativas.")

    gestor_proyectos = GestorProyectos()

    # Menú de opciones
    while True:
        print("\nOpciones:")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver tareas")
        print("4. Crear tarea")
        print("5. Actualizar tarea")
        print("6. Eliminar tarea")
        print("7. Salir")
        print("8. Crear proyecto")
        print("9. Ver proyectos")
        print("10. Asignar tarea a proyecto")
        print("11. Ver tareas de un proyecto")
        print("12. Ver progreso de un proyecto")


        op = input("Seleccione una opción (1-7): ")

        if op == '1':
            signup()
        elif op == '2':
            token = signin()
        elif op == '3' and 'token' in locals():
            get_tasks(token)
        elif op == '4' and 'token' in locals():
            create_task(token)
        elif op == '5' and 'token' in locals():
            update_task(token)
        elif op == '6' and 'token' in locals():
            delete_task(token)
        elif op == '7':
            print("Saliendo del programa...")
            break
        elif op == '8' and 'token' in locals():
            crear_proyecto(token)
        elif op == '9' and 'token' in locals():
            ver_proyectos(token)
        elif op == '10' and 'token' in locals():
            asignar_tarea_a_proyecto(token)
        elif op == '11' and 'token' in locals():
            ver_tareas_de_proyecto(token)
        elif op == '12' and 'token' in locals():
            ver_progreso(token)

        else:
            print("Por favor, inicie sesión primero.")


if __name__ == "__main__":
    main()
