"""
Módulo: gestor_de_tareas
========================

Este módulo define la clase `GestorDeTareas`, que se encarga de gestionar las tareas
dentro de la aplicación. Permite crear, listar, modificar, filtrar, asignar, ordenar y
eliminar tareas. Se utiliza un decorador para el logueo de ciertas funciones.

Dependencias:
    - datetime para el manejo de fechas.
    - typing para especificar listas y tipos opcionales.
    - gestor_de_tareas.clases.tarea: Tarea, EstadoTarea.
    - gestor_de_tareas.utilidades.decoradores: log_funcion.
"""

from datetime import datetime
from typing import List, Optional
from gestor_de_tareas.clases.tarea import Tarea, EstadoTarea
from gestor_de_tareas.utilidades.decoradores import log_funcion  # Mantener import original


class GestorDeTareas:
    """
    Clase GestorDeTareas.

    Gestiona la creación, modificación, asignación, ordenación y eliminación de tareas.

    Attributes
    ----------
    tareas : List[Tarea]
        Lista de tareas gestionadas.
    contador_id : int
        Contador para asignar identificadores únicos a cada tarea.
    """

    def __init__(self) -> None:
        """
        Inicializa una nueva instancia de GestorDeTareas.

        Crea una lista vacía de tareas y establece el contador de IDs en 1.
        """
        self.tareas: List[Tarea] = []
        self.contador_id = 1

    @log_funcion  # Mantener decorador original
    def crear_tarea(self,
                    titulo: str,
                    descripcion: str = "",
                    fecha_limite_str: Optional[str] = None,
                    prioridad: int = 2,
                    etiquetas: Optional[List[str]] = None,
                    usuario_asignado: Optional[str] = None) -> Optional[Tarea]:
        """
        Crea una nueva tarea y la añade al gestor.

        Parameters
        ----------
        titulo : str
            Título de la tarea.
        descripcion : str, optional
            Descripción de la tarea. Por defecto es una cadena vacía.
        fecha_limite_str : str, optional
            Fecha límite en formato "YYYY-MM-DD". Si es None, la tarea no tendrá fecha límite.
        prioridad : int, optional
            Prioridad de la tarea (valor numérico, donde un valor menor indica mayor prioridad).
        etiquetas : Optional[List[str]], optional
            Lista de etiquetas asociadas a la tarea.
        usuario_asignado : Optional[str], optional
            Usuario asignado a la tarea.

        Returns
        -------
        Optional[Tarea]
            La tarea creada si la fecha se puede parsear correctamente; de lo contrario, None.
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

    def marcar_completada(self, id_tarea: int) -> bool:
        """
        Marca una tarea como completada.

        Parameters
        ----------
        id_tarea : int
            Identificador de la tarea a marcar como completada.

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
        Retorna la lista de todas las tareas gestionadas.

        Returns
        -------
        List[Tarea]
            Lista de tareas registradas en el gestor.
        """
        return self.tareas

    @log_funcion
    def obtener_por_id(self, id_tarea: int) -> Optional[Tarea]:
        """
        Obtiene una tarea a partir de su identificador.

        Parameters
        ----------
        id_tarea : int
            Identificador de la tarea a buscar.

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
        Filtra las tareas por un estado específico.

        Parameters
        ----------
        estado : EstadoTarea
            Estado de la tarea para el filtro.

        Returns
        -------
        List[Tarea]
            Lista de tareas que cumplen con el estado proporcionado.
        """
        return [t for t in self.tareas if t.estado == estado]

    @log_funcion
    def cambiar_estado_tarea(self, id_tarea: int, nuevo_estado: EstadoTarea) -> bool:
        """
        Cambia el estado de una tarea identificada por su ID.

        Parameters
        ----------
        id_tarea : int
            Identificador de la tarea.
        nuevo_estado : EstadoTarea
            Nuevo estado a asignar a la tarea.

        Returns
        -------
        bool
            True si la tarea fue encontrada y su estado fue actualizado, False en caso contrario.
        """
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.cambiar_estado(nuevo_estado)
            return True
        return False

    @log_funcion
    def modificar_tarea(self,
                        id_tarea: int,
                        titulo: Optional[str] = None,
                        descripcion: Optional[str] = None,
                        fecha_limite: Optional[datetime] = None,
                        prioridad: Optional[int] = None,
                        etiquetas: Optional[List[str]] = None) -> bool:
        """
        Modifica los atributos de una tarea existente.

        Solo se actualizan los campos cuyo valor no es None.

        Parameters
        ----------
        id_tarea : int
            Identificador de la tarea a modificar.
        titulo : str, optional
            Nuevo título para la tarea.
        descripcion : str, optional
            Nueva descripción para la tarea.
        fecha_limite : datetime, optional
            Nueva fecha límite para la tarea.
        prioridad : int, optional
            Nueva prioridad para la tarea.
        etiquetas : Optional[List[str]], optional
            Nueva lista de etiquetas para la tarea.

        Returns
        -------
        bool
            True si la tarea fue encontrada y modificada, False en caso contrario.
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
            Identificador de la tarea.
        usuario : str
            Usuario que se asignará a la tarea.

        Returns
        -------
        bool
            True si la tarea fue encontrada y se asignó el usuario, False en caso contrario.
        """
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.asignar_usuario(usuario)
            return True
        return False

    @log_funcion
    def ordenar_por_prioridad(self) -> List[Tarea]:
        """
        Devuelve una lista de tareas ordenadas según su prioridad.

        Las tareas se ordenan de forma ascendente, donde un número menor indica una mayor prioridad.

        Returns
        -------
        List[Tarea]
            Lista de tareas ordenadas por prioridad.
        """
        return sorted(self.tareas)

    @log_funcion
    def eliminar_tarea(self, id_tarea: int) -> bool:
        """
        Elimina la tarea con el ID especificado.

        Parameters
        ----------
        id_tarea : int
            Identificador de la tarea que se desea eliminar.

        Returns
        -------
        bool
            True si la tarea fue eliminada, False en caso contrario.
        """
        for i, t in enumerate(self.tareas):
            if t.id_tarea == id_tarea:
                del self.tareas[i]
                return True
        return False
