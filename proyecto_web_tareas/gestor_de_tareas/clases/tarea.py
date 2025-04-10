"""
Módulo de gestión de tareas.

Este módulo define la clase Tarea junto con el enum EstadoTarea para representar
los estados de una tarea y gestionar sus atributos (título, descripción, fecha límite,
prioridad, etiquetas y usuario asignado).

Se implementan métodos para modificar, cambiar de estado, asignar un usuario y
comparar tareas por prioridad. Los docstrings siguen un estilo similar al de NumPy.
"""

from enum import Enum
from datetime import date
from typing import Optional, List

class EstadoTarea(Enum):
    """
    Enumeración que define los posibles estados de una tarea.

    Attributes
    ----------
    PENDIENTE : str
        Estado inicial; indica que la tarea está pendiente.
    EN_PROGRESO : str
        Indica que la tarea está en curso.
    COMPLETADA : str
        Indica que la tarea ha sido finalizada.
    """
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En progreso"
    COMPLETADA = "Completada"

class Tarea:
    """
    Representa una tarea con seguimiento de estado, prioridad y usuario asignado.

    Parameters
    ----------
    id_tarea : int
        Identificador único de la tarea.
    titulo : str
        Título o nombre de la tarea.
    descripcion : str
        Descripción detallada de la tarea.
    fecha_limite : date
        Fecha límite para completar la tarea.
    prioridad : int
        Nivel de prioridad (1 = Alta, 2 = Media, 3 = Baja).
    etiquetas : list of str, optional
        Lista de etiquetas que categorizan la tarea.
    usuario_asignado : str, optional
        Nombre del usuario asignado a la tarea.

    Attributes
    ----------
    estado : EstadoTarea
        Estado actual de la tarea, inicialmente `EstadoTarea.PENDIENTE`.
    """
    def __init__(self,
                 id_tarea: int,
                 titulo: str,
                 descripcion: str,
                 fecha_limite: date,
                 prioridad: int,
                 etiquetas: Optional[List[str]] = None,
                 usuario_asignado: Optional[str] = None):
        self.id_tarea = id_tarea
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.estado = EstadoTarea.PENDIENTE
        self.prioridad = prioridad
        self.etiquetas = etiquetas if etiquetas else []
        self.usuario_asignado = usuario_asignado

    def cambiar_estado(self, nuevo_estado: EstadoTarea) -> None:
        """
        Cambia el estado actual de la tarea.

        Parameters
        ----------
        nuevo_estado : EstadoTarea
            El nuevo estado a asignar a la tarea.
        """
        self.estado = nuevo_estado

    def completar(self) -> None:
        """
        Marca la tarea como completada.
        """
        self.estado = EstadoTarea.COMPLETADA

    def asignar_usuario(self, usuario: str) -> None:
        """
        Asigna un usuario a la tarea.

        Parameters
        ----------
        usuario : str
            Nombre del usuario a asignar.
        """
        self.usuario_asignado = usuario

    def modificar(self,
                  titulo: Optional[str] = None,
                  descripcion: Optional[str] = None,
                  fecha_limite: Optional[date] = None,
                  prioridad: Optional[int] = None,
                  etiquetas: Optional[List[str]] = None) -> None:
        """
        Modifica los atributos de la tarea.

        Parameters
        ----------
        titulo : str, optional
            Nuevo título de la tarea.
        descripcion : str, optional
            Nueva descripción.
        fecha_limite : date, optional
            Nueva fecha límite.
        prioridad : int, optional
            Nueva prioridad (1, 2 o 3).
        etiquetas : list of str, optional
            Nuevas etiquetas.
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
        Compara dos tareas basándose en su prioridad.

        Parameters
        ----------
        otra_tarea : Tarea
            Otra tarea para comparar.

        Returns
        -------
        bool
            True si la prioridad de esta tarea es menor (más alta) que la de otra tarea.
        """
        return self.prioridad < otra_tarea.prioridad

    def __str__(self) -> str:
        """
        Retorna una representación legible de la tarea.

        Returns
        -------
        str
            Cadena que muestra el estado en mayúsculas, el título y la prioridad.
        """
        return f"[{self.estado.value.upper()}] {self.titulo} (Prioridad {self.prioridad})"

