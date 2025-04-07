class Proyecto:
    def __init__(self, nombre):
        self.nombre = nombre
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def listar_tareas(self):
        for i, tarea in enumerate(self.tareas, 1):
            estado = "✔️" if tarea.completada else "❌"
            print(f"{i}. {tarea.nombre} [{estado}]")

    def progreso(self):
        if not self.tareas:
            return 0
        completadas = sum(t.completada for t in self.tareas)
        return (completadas / len(self.tareas)) * 100


class GestorProyectos:
    def __init__(self):
        self.proyectos = {}

    def crear_proyecto(self, nombre):
        if nombre not in self.proyectos:
            self.proyectos[nombre] = Proyecto(nombre)
            print(f"Proyecto '{nombre}' creado.")
        else:
            print(f"El proyecto '{nombre}' ya existe.")

    def borrar_proyecto(self, nombre):
        if nombre in self.proyectos:
            del self.proyectos[nombre]
            print(f"Proyecto '{nombre}' borrado.")
        else:
            print(f"El proyecto '{nombre}' no existe.")

    def agregar_tarea_a_proyecto(self, nombre_proyecto, tarea):
        if nombre_proyecto in self.proyectos:
            self.proyectos[nombre_proyecto].agregar_tarea(tarea)
            print(f"Tarea '{tarea.nombre}' añadida a '{nombre_proyecto}'.")
        else:
            print(f"Proyecto '{nombre_proyecto}' no encontrado.")

    def listar_tareas_de_proyecto(self, nombre_proyecto):
        if nombre_proyecto in self.proyectos:
            print(f"Tareas en proyecto '{nombre_proyecto}':")
            self.proyectos[nombre_proyecto].listar_tareas()
        else:
            print(f"Proyecto '{nombre_proyecto}' no encontrado.")

    def mostrar_progreso_proyecto(self, nombre_proyecto):
        if nombre_proyecto in self.proyectos:
            progreso = self.proyectos[nombre_proyecto].progreso()
            print(f"Progreso de '{nombre_proyecto}': {progreso:.2f}%")
        else:
            print(f"Proyecto '{nombre_proyecto}' no encontrado.")
