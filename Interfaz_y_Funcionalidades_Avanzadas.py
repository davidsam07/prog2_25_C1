class Tarea:
    """
    Representa una tarea individual con un nombre y un estado.

    Parameters
    ----------
    nombre : str
        Nombre de la tarea.
    estado : str, optional
        Estado inicial de la tarea, por defecto "Pendiente".
    """

    def __init__(self, nombre, estado="Pendiente"):
        self.nombre = nombre
        self.estado = estado

    def completar(self):
        """
        Marca la tarea como completada.

        Modifica el atributo `estado` a "Completada".
        """
        self.estado = "Completada"


class GestorDeTareas:
    """
    Gestiona una lista de tareas, permitiendo agregarlas y mostrarlas.
    """

    def __init__(self):
        """
        Inicializa el gestor con una lista vacía de tareas.
        """
        self.tareas = []

    def agregar_tarea(self, nombre):
        """
        Agrega una nueva tarea con el nombre dado.

        Parameters
        ----------
        nombre : str
            Nombre de la nueva tarea a agregar.
        """
        nueva = Tarea(nombre)
        self.tareas.append(nueva)
        print(f"Tarea '{nombre}' agregada.")

    def mostrar_tareas(self):
        """
        Muestra todas las tareas en una tabla con Rich.

        Utiliza `rich.table.Table` y `rich.console.Console` para imprimir
        una tabla con el nombre y estado de cada tarea.
        """
        from rich.table import Table
        from rich.console import Console

        table = Table(title="Tareas")
        table.add_column("Nombre")
        table.add_column("Estado")

        for tarea in self.tareas:
            table.add_row(tarea.nombre, tarea.estado)

        console = Console()
        console.print(table)


class Interfaz:
    """
    Controla la interacción con el usuario para gestionar tareas.
    """

    def __init__(self):
        """
        Inicializa la interfaz con un gestor de tareas.
        """
        self.gestor = GestorDeTareas()

    def iniciar(self):
        """
        Inicia el menú de la aplicación para interactuar con el usuario.

        Opciones disponibles:
        1. Agregar tarea
        2. Ver tareas
        3. Salir

        Captura errores genéricos para evitar caídas inesperadas.
        """
        while True:
            try:
                print("\n1. Agregar tarea\n2. Ver tareas\n3. Salir")
                opcion = input("Elige una opción: ")

                if opcion == "1":
                    nombre = input("Nombre de la tarea: ")
                    self.gestor.agregar_tarea(nombre)
                elif opcion == "2":
                    self.gestor.mostrar_tareas()
                elif opcion == "3":
                    break
                else:
                    print("Opción no válida.")
            except Exception as e:
                print(f"⚠️ Error: {e}")