class Tarea:
    def __init__(self, titulo, descripcion, estado):

        self.titulo = titulo
        self.descripcion = descripcion
        self.estado = estado
        self.asignado = None

    def editar(self, nuevo_titulo=None, nueva_descripcion=None, nuevo_estado=None):
        if nuevo_titulo:
            self.titulo = nuevo_titulo
        if nueva_descripcion:
            self.descripcion = nueva_descripcion
        if nuevo_estado:
            self.estado = nuevo_estado

    def asignar_usuario(self, usuario):

        self.asignado = usuario
        print (f"La tarea {self.titulo}, ha sido asignada a {usuario}")

    def __str__(self):
        return f"Tarea: {self.titulo}\nDescripción: {self.descripcion}"


class GestorTareas:
    def __init__(self):
        self.tareas = []

    def crear_tarea(self, titulo, descripcion, estado):
        nueva_tarea = Tarea(titulo, descripcion, estado)
        self.tareas.append(nueva_tarea)

    def mostrar_tareas(self):
        if not self.tareas:
            print("No hay tareas.")
        else:
            for i, tarea in enumerate(self.tareas, 1):
                print(f"{i}. {tarea}")

    def editar_tarea(self, indice, nuevo_titulo = None, nueva_descripcion = None, nuevo_estado = None):
        if 0 <= indice < len(self.tareas):
            self.tareas[indice].editar(nuevo_titulo, nueva_descripcion, nuevo_estado)
        else:
            print("Índice no válido.")

    def eliminar_tarea(self, indice):
        if 0 <= indice < len(self.tareas):
            self.tareas.pop(indice)
        else:
            print("Índice no válido.")

    def asignar_tarea(self, titulo, usuario):

        for tarea in self.tareas:
            if tarea.titulo == titulo:
                tarea.asignar_usuario(usuario)
                return

        print(f"No se encontró ninguna tarea con el título {titulo}")

    #TODO Asignar prioridadesd, fecha límite, etc

