from gestor_de_tareas.clases.tarea import Tarea, EstadoTarea

class Proyecto:
    """
    Representa un proyecto que contiene múltiples tareas.

    Attributes
    ----------
    nombre : str
        Nombre del proyecto.
    tareas : List[Tarea]
        Lista de tareas asociadas al proyecto.
    """
    def __init__(self, nombre: str) -> None:
        """
        Inicializa una nueva instancia de Proyecto.

        Parameters
        ----------
        nombre : str
            Nombre del proyecto.
        """
        self.nombre = nombre
        self.tareas = []

    def agregar_tarea(self, tarea: Tarea) -> None:
        """
        Agrega una nueva tarea al proyecto.

        Parameters
        ----------
        tarea : Tarea
            La tarea a agregar.
        """
        self.tareas.append(tarea)

    def listar_tareas(self) -> None:
        """
        Imprime en consola la lista de tareas asociadas al proyecto.

        Cada tarea se muestra numerada junto con su título y un indicador visual
        del estado: "✔️" para tareas completadas y "❌" para tareas no completadas.
        """
        for i, tarea in enumerate(self.tareas, 1):
            estado = "✔️" if tarea.estado == EstadoTarea.COMPLETADA else "❌"
            print(f"{i}. {tarea.titulo} [{estado}]")

    def progreso(self) -> float:
        """
        Calcula el porcentaje de tareas completadas en el proyecto.

        Returns
        -------
        float
            Porcentaje de tareas completadas. Si no hay tareas, retorna 0.
        """
        if not self.tareas:
            return 0
        completadas = sum(1 for t in self.tareas if t.estado == EstadoTarea.COMPLETADA)
        return (completadas / len(self.tareas)) * 100

class GestorProyectos:
    """
    Gestiona múltiples proyectos.

    Attributes
    ----------
    proyectos : dict[str, Proyecto]
        Diccionario que mapea el nombre del proyecto a su objeto Proyecto.
    """
    def __init__(self) -> None:
        """
        Inicializa el gestor de proyectos.
        """
        self.proyectos = {}

    def crear_proyecto(self, nombre: str) -> None:
        """
        Crea un nuevo proyecto.

        Si el proyecto ya existe, se imprime un mensaje indicando que ya existe.

        Parameters
        ----------
        nombre : str
            Nombre del proyecto a crear.
        """
        if nombre not in self.proyectos:
            self.proyectos[nombre] = Proyecto(nombre)
            print(f"Proyecto '{nombre}' creado.")
        else:
            print(f"El proyecto '{nombre}' ya existe.")

    def borrar_proyecto(self, nombre: str) -> None:
        """
        Borra un proyecto existente.

        Parameters
        ----------
        nombre : str
            Nombre del proyecto a borrar.
        """
        if nombre in self.proyectos:
            del self.proyectos[nombre]
            print(f"Proyecto '{nombre}' borrado.")
        else:
            print(f"El proyecto '{nombre}' no existe.")

    def agregar_tarea_a_proyecto(self, nombre_proyecto: str, tarea: Tarea) -> None:
        """
        Agrega una tarea a un proyecto específico.

        Parameters
        ----------
        nombre_proyecto : str
            Nombre del proyecto al que se desea agregar la tarea.
        tarea : Tarea
            La tarea a agregar.
        """
        if nombre_proyecto in self.proyectos:
            self.proyectos[nombre_proyecto].agregar_tarea(tarea)
            print(f"Tarea '{tarea}' añadida a '{nombre_proyecto}'.")
        else:
            print(f"Proyecto '{nombre_proyecto}' no encontrado.")

    def listar_tareas_de_proyecto(self, nombre_proyecto: str) -> None:
        """
        Lista las tareas de un proyecto.

        Parameters
        ----------
        nombre_proyecto : str
            Nombre del proyecto del que se desean listar las tareas.
        """
        if nombre_proyecto in self.proyectos:
            print(f"Tareas en proyecto '{nombre_proyecto}':")
            self.proyectos[nombre_proyecto].listar_tareas()
        else:
            print(f"Proyecto '{nombre_proyecto}' no encontrado.")

    def mostrar_progreso_proyecto(self, nombre_proyecto: str) -> None:
        """
        Muestra el progreso (porcentaje de tareas completadas) de un proyecto.

        Parameters
        ----------
        nombre_proyecto : str
            Nombre del proyecto para el cual se desea conocer el progreso.
        """
        if nombre_proyecto in self.proyectos:
            progreso = self.proyectos[nombre_proyecto].progreso()
            print(f"Progreso de '{nombre_proyecto}': {progreso:.2f}%")
        else:
            print(f"Proyecto '{nombre_proyecto}' no encontrado.")
