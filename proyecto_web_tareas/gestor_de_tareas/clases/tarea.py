from enum import Enum
from datetime import date
from typing import Optional, List

class EstadoTarea(Enum):
    """
    Enumeración que define los posibles estados de una tarea.

    Attributes
    ----------
    PENDIENTE : str
        Indica que la tarea está pendiente.
    EN_PROGRESO : str
        Indica que la tarea está en progreso.
    COMPLETADA : str
        Indica que la tarea ha sido completada.
    """
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En progreso"
    COMPLETADA = "Completada"

class Tarea:
    """
    Clase que representa una tarea.

    La clase Tarea encapsula información sobre una tarea, incluyendo su identificador,
    título, descripción, fecha límite, estado, prioridad, etiquetas y el usuario asignado.
    Se inicializa el estado de la tarea a PENDIENTE por defecto.

    Parameters
    ----------
    id_tarea : int
        Identificador único de la tarea.
    titulo : str
        Título de la tarea.
    descripcion : str
        Descripción detallada de la tarea.
    fecha_limite : date
        Fecha límite para completar la tarea.
    prioridad : int
        Valor numérico que representa la prioridad; un valor menor indica mayor prioridad.
    etiquetas : Optional[List[str]], optional
        Lista de etiquetas asociadas a la tarea. Por defecto es None, lo que se traduce en una lista vacía.
    usuario_asignado : Optional[str], optional
        Nombre o identificador del usuario asignado a la tarea. Por defecto es None.
    """
    def __init__(self,
                 id_tarea: int,
                 titulo: str,
                 descripcion: str,
                 fecha_limite: date,
                 prioridad: int,
                 etiquetas: Optional[List[str]] = None,
                 usuario_asignado: Optional[str] = None):
        """
        Inicializa una nueva instancia de Tarea.

        Parameters
        ----------
        id_tarea : int
            Identificador único de la tarea.
        titulo : str
            Título de la tarea.
        descripcion : str
            Descripción de la tarea.
        fecha_limite : date
            Fecha límite para la tarea.
        prioridad : int
            Prioridad de la tarea.
        etiquetas : Optional[List[str]], optional
            Lista de etiquetas (default es None, lo que se interpreta como lista vacía).
        usuario_asignado : Optional[str], optional
            Usuario asignado a la tarea (default es None).
        """
        self.id_tarea = id_tarea
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.estado = EstadoTarea.PENDIENTE
        self.prioridad = prioridad
        self.etiquetas = etiquetas if etiquetas else []
        self.usuario_asignado = usuario_asignado

    def cambiar_estado(self, nuevo_estado: EstadoTarea):
        """
        Cambia el estado de la tarea.

        Parameters
        ----------
        nuevo_estado : EstadoTarea
            Nuevo estado a asignar a la tarea.
        """
        self.estado = nuevo_estado

    def completar(self):
        """
        Marca la tarea como completada.

        Este método cambia el estado de la tarea a COMPLETADA.
        """
        self.estado = EstadoTarea.COMPLETADA

    def asignar_usuario(self, usuario: str):
        """
        Asigna un usuario a la tarea.

        Parameters
        ----------
        usuario : str
            Nombre o identificador del usuario a asignar.
        """
        self.usuario_asignado = usuario

    def modificar(self,
                  titulo: Optional[str] = None,
                  descripcion: Optional[str] = None,
                  fecha_limite: Optional[date] = None,
                  prioridad: Optional[int] = None,
                  etiquetas: Optional[List[str]] = None):
        """
        Modifica los atributos de la tarea.

        Se actualizan los campos que se proporcionan (no nulos). Si no se especifica un parámetro,
        ese campo no se modifica.

        Parameters
        ----------
        titulo : Optional[str], optional
            Nuevo título de la tarea.
        descripcion : Optional[str], optional
            Nueva descripción de la tarea.
        fecha_limite : Optional[date], optional
            Nueva fecha límite para la tarea.
        prioridad : Optional[int], optional
            Nueva prioridad.
        etiquetas : Optional[List[str]], optional
            Nueva lista de etiquetas. Si se pasa explícitamente None, no se realiza cambio.
        """
        if titulo:
            self.titulo = titulo
        if descripcion:
            self.descripcion = descripcion
        if fecha_limite:
            self.fecha_limite = fecha_limite
        if prioridad:
            self.prioridad = prioridad
        if etiquetas is not None:
            self.etiquetas = etiquetas

    def __lt__(self, otra_tarea: 'Tarea') -> bool:
        """
        Compara dos tareas en base a su prioridad.

        Parameters
        ----------
        otra_tarea : Tarea
            Otra instancia de Tarea para comparar.

        Returns
        -------
        bool
            True si la prioridad de la tarea actual es menor (mayor prioridad) que la de otra_tarea.
        """
        return self.prioridad < otra_tarea.prioridad

    def __str__(self) -> str:
        """
        Retorna una representación en cadena de la tarea.

        Returns
        -------
        str
            Cadena de texto que muestra el estado (en mayúsculas), el título y la prioridad.
        """
        return f"[{self.estado.value.upper()}] {self.titulo} (Prioridad {self.prioridad})"

