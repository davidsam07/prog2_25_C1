import requests

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
    nombre = input("Introduce el nuevo nombre de la tarea: ")
    description = input("Introduce la nueva descripción de la tarea: ")

    respuesta = requests.put(f"{BASE_URL}/tareas/{tarea_id}", params={'nombre': nombre, 'description': description},
                            headers=headers)
    print(respuesta.text)


# Función para eliminar una tarea (requiere token)
def delete_task(token):
    headers = {'Authorization': f'Bearer {token}'}
    tarea_id = input("Introduce el ID de la tarea a eliminar: ")

    respuesta = requests.delete(f"{BASE_URL}/tareas/{tarea_id}", headers=headers)
    print(respuesta.text)


def main():
    print("Bienvenido al sistema de gestión de tareas colaborativas.")

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
        else:
            print("Por favor, inicie sesión primero.")


if __name__ == "__main__":
    main()
