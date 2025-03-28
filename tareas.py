class Tarea:
    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion

    def editar(self, nuevo_titulo=None, nueva_descripcion=None):
        if nuevo_titulo:
            self.titulo = nuevo_titulo
        if nueva_descripcion:
            self.descripcion = nueva_descripcion

    def __str__(self):
        return f"Tarea: {self.titulo}\nDescripción: {self.descripcion}"


class GestorTareas:
    def __init__(self):
        self.tareas = []

    def crear_tarea(self, titulo, descripcion):
        nueva_tarea = Tarea(titulo, descripcion)
        self.tareas.append(nueva_tarea)

    def mostrar_tareas(self):
        if not self.tareas:
            print("No hay tareas.")
        else:
            for i, tarea in enumerate(self.tareas, 1):
                print(f"{i}. {tarea}")

    def editar_tarea(self, indice, nuevo_titulo=None, nueva_descripcion=None):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].editar(nuevo_titulo, nueva_descripcion)
        else:
            print("Índice no válido.")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas.pop(indice)
        else:
            print("Índice no válido.")

