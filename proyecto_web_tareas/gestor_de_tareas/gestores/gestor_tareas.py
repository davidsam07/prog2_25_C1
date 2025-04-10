from datetime import datetime
from typing import List, Optional
from gestor_de_tareas.clases.tarea import Tarea, EstadoTarea
from gestor_de_tareas.utilidades.decoradores import log_funcion  # Mantener import original


class GestorDeTareas:
    """
    Clase para gestionar tareas en la aplicación.

    Esta clase administra la creación, modificación, filtrado, asignación y eliminación de tareas,
    así como el ordenamiento de tareas por prioridad. Cada tarea se identifica de manera única mediante
    un contador que se incrementa con cada tarea creada.

    Attributes
    ----------
    tareas : List[Tarea]
        Lista que almacena las instancias de Tarea.
    contador_id : int
        Contador para asignar un ID único a cada tarea.
    """

    def __init__(self):
        """
        Inicializa una instancia de GestorDeTareas.

        Inicia la lista de tareas como vacía y establece el contador de ID en 1.
        """
        self.tareas: List[Tarea] = []
        self.contador_id = 1

    @log_funcion
    def crear_tarea(self,
                    titulo: str,
                    descripcion: str = "",
                    fecha_limite_str: str = None,
                    prioridad: int = 2,
                    etiquetas=None,
                    usuario_asignado=None) -> Optional[Tarea]:
        """
        Crea una nueva tarea y la añade a la lista.

        Parameters
        ----------
        titulo : str
            El título de la tarea.
        descripcion : str, optional
            La descripción de la tarea (por defecto es una cadena vacía).
        fecha_limite_str : str, optional
            La fecha límite de la tarea en formato 'YYYY-MM-DD'. Si no se especifica, se asigna None.
        prioridad : int, optional
            La prioridad de la tarea (1: alta, 2: media, 3: baja). Por defecto es 2 (media).
        etiquetas : list, optional
            Lista de etiquetas asociadas a la tarea.
        usuario_asignado : str, optional
            Nombre del usuario asignado a la tarea.

        Returns
        -------
        Optional[Tarea]
            La instancia de Tarea creada si se pudo crear correctamente, o None si ocurre un error (por ejemplo, en la conversión de la fecha).
        """
        try:
            fecha = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date() if fecha_limite_str else None
            tarea = Tarea(
                id_tarea=self.contador_id,
                titulo=titulo,
                descripcion=descripcion,
                fecha_limite=fecha,
                prioridad=prioridad,
                etiquetas=etiquetas,
                usuario_asignado=usuario_asignado
            )
            self.tareas.append(tarea)
            self.contador_id += 1
            return tarea
        except ValueError:
            print("[ERROR] Fecha mal formateada. Usa YYYY-MM-DD.")
            return None

    @log_funcion
    def marcar_completada(self, id_tarea: int) -> bool:
        """
        Marca una tarea como completada.

        Parameters
        ----------
        id_tarea : int
            El ID de la tarea a marcar como completada.

        Returns
        -------
        bool
            True si la tarea fue encontrada y marcada como completada, False en caso contrario.
        """
        tarea = next((t for t in self.tareas if t.id_tarea == id_tarea), None)
        if tarea:
            tarea.completar()
            return True
        return False

    @log_funcion
    def listar_tareas(self) -> List[Tarea]:
        """
        Retorna la lista completa de tareas.

        Returns
        -------
        List[Tarea]
            Una lista con todas las instancias de Tarea almacenadas.
        """
        return self.tareas

    @log_funcion
    def obtener_por_id(self, id_tarea: int) -> Optional[Tarea]:
        """
        Busca y retorna una tarea por su ID.

        Parameters
        ----------
        id_tarea : int
            El ID de la tarea a buscar.

        Returns
        -------
        Optional[Tarea]
            La tarea encontrada o None si no existe.
        """
        for t in self.tareas:
            if t.id_tarea == id_tarea:
                return t
        return None

    @log_funcion
    def filtrar_por_estado(self, estado: EstadoTarea) -> List[Tarea]:
        """
        Filtra y retorna las tareas cuyo estado coincide con el especificado.

        Parameters
        ----------
        estado : EstadoTarea
            El estado por el cual filtrar las tareas.

        Returns
        -------
        List[Tarea]
            Una lista de tareas que tienen el estado especificado.
        """
        return [t for t in self.tareas if t.estado == estado]

    @log_funcion
    def cambiar_estado_tarea(self, id_tarea: int, nuevo_estado: EstadoTarea) -> bool:
        """
        Cambia el estado de una tarea identificada por su ID.

        Parameters
        ----------
        id_tarea : int
            El ID de la tarea a actualizar.
        nuevo_estado : EstadoTarea
            El nuevo estado que se asignará a la tarea.

        Returns
        -------
        bool
            True si se encontró y actualizó la tarea, False en caso contrario.
        """
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.cambiar_estado(nuevo_estado)
            return True
        return False

    @log_funcion
    def modificar_tarea(self,
                        id_tarea: int,
                        titulo=None,
                        descripcion=None,
                        fecha_limite=None,
                        prioridad=None,
                        etiquetas=None) -> bool:
        """
        Modifica los datos de una tarea existente identificada por su ID.

        Parameters
        ----------
        id_tarea : int
            El ID de la tarea a modificar.
        titulo : str, optional
            Nuevo título para la tarea.
        descripcion : str, optional
            Nueva descripción.
        fecha_limite : date, optional
            Nueva fecha límite.
        prioridad : int, optional
            Nueva prioridad.
        etiquetas : list, optional
            Nuevas etiquetas.

        Returns
        -------
        bool
            True si la tarea fue modificada correctamente, False si no se encontró la tarea.
        """
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.modificar(titulo, descripcion, fecha_limite, prioridad, etiquetas)
            return True
        return False

    @log_funcion
    def asignar_usuario_tarea(self, id_tarea: int, usuario: str) -> bool:
        """
        Asigna un usuario a una tarea específica.

        Parameters
        ----------
        id_tarea : int
            El ID de la tarea.
        usuario : str
            El nombre del usuario que se asigna a la tarea.

        Returns
        -------
        bool
            True si se asignó el usuario correctamente, False si la tarea no fue encontrada.
        """
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.asignar_usuario(usuario)
            return True
        return False

    @log_funcion
    def ordenar_por_prioridad(self) -> List[Tarea]:
        """
        Retorna la lista de tareas ordenada por prioridad, utilizando la sobrecarga del operador __lt__.

        Returns
        -------
        List[Tarea]
            Una lista ordenada de tareas.
        """
        return sorted(self.tareas)

    @log_funcion
    def eliminar_tarea(self, id_tarea: int) -> bool:
        """
        Elimina la tarea con el ID especificado.

        Parameters
        ----------
        id_tarea : int
            El ID de la tarea a eliminar.

        Returns
        -------
        bool
            True si la tarea se eliminó correctamente; False en caso contrario.
        """
        for i, t in enumerate(self.tareas):
            if t.id_tarea == id_tarea:
                del self.tareas[i]
                return True
        return False
