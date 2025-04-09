from enum import Enum
from datetime import date
from typing import List, Optional

class EstadoTarea(Enum):
    """Enum para representar el estado de una tarea."""
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en progreso"
    COMPLETADA = "completada"

class Tarea:
    """
    Representa una tarea con prioridad, etiquetas, usuario y proyecto asignado.

    Parameters
    ----------
    titulo : str
        Título de la tarea.
    descripcion : str
        Descripción de la tarea.
    fecha_limite : date
        Fecha límite para completar la tarea.
    prioridad : int
        Nivel de prioridad de la tarea (1 = alta, 2 = media, 3 = baja).
    etiquetas : list of str, optional
        Lista de etiquetas asociadas a la tarea.
    """

    def __init__(self, titulo: str, descripcion: str, fecha_limite: date, prioridad: int, etiquetas: Optional[List[str]] = None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.estado = EstadoTarea.PENDIENTE
        self.prioridad = prioridad
        self.etiquetas = etiquetas if etiquetas else []
        self.asignado = None
        self.proyecto = None

    def cambiar_estado(self, nuevo_estado: EstadoTarea) -> None:
        """Cambia el estado de la tarea."""
        self.estado = nuevo_estado

    def modificar(self, titulo=None, descripcion=None, fecha_limite=None, prioridad=None, etiquetas=None) -> None:
        """Modifica los atributos de la tarea."""
        if titulo: self.titulo = titulo
        if descripcion: self.descripcion = descripcion
        if fecha_limite: self.fecha_limite = fecha_limite
        if prioridad: self.prioridad = prioridad
        if etiquetas is not None: self.etiquetas = etiquetas

    def asignar_a_usuario(self, usuario: object) -> None:
        """Asigna la tarea a un usuario."""
        self.asignado = usuario

    def asignar_a_proyecto(self, proyecto: object) -> None:
        """Asigna la tarea a un proyecto."""
        self.proyecto = proyecto

    def __lt__(self, otra_tarea) -> bool:
        """Permite comparar tareas por prioridad."""
        return self.prioridad < otra_tarea.prioridad

    def __str__(self) -> str:
        """Representación legible de la tarea."""
        return f"[{self.estado.value.upper()}] {self.titulo} (Prioridad {self.prioridad})"

class TareaImportante(Tarea):
    """
    Subclase que representa una tarea especialmente urgente.
    """

    def mostrar_alerta(self) -> str:
        """Devuelve un mensaje de alerta visual."""
        return f" ¡Tarea urgente!: {self.titulo.upper()}"
