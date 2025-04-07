from enum import Enum
from datetime import date
from typing import List, Optional

class EstadoTarea(Enum):
    PENDIENTE = "pendiente"
    EN_PROGRESO = "en progreso"
    COMPLETADA = "completada"

class Tarea:
    def __init__(self, titulo: str, descripcion: str, fecha_limite: date, prioridad: int, etiquetas: Optional[List[str]] = None):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_limite = fecha_limite
        self.estado = EstadoTarea.PENDIENTE
        self.prioridad = prioridad
        self.etiquetas = etiquetas if etiquetas else []
        self.asignado = None  # Usuario asignado
        self.proyecto = None  # Proyecto relacionado (opcional)

    def cambiar_estado(self, nuevo_estado: EstadoTarea):
        self.estado = nuevo_estado

    def modificar(self, titulo=None, descripcion=None, fecha_limite=None, prioridad=None, etiquetas=None):
        if titulo: self.titulo = titulo
        if descripcion: self.descripcion = descripcion
        if fecha_limite: self.fecha_limite = fecha_limite
        if prioridad: self.prioridad = prioridad
        if etiquetas is not None: self.etiquetas = etiquetas

    def asignar_a_usuario(self, usuario):
        self.asignado = usuario

    def asignar_a_proyecto(self, proyecto):
        self.proyecto = proyecto

    def __lt__(self, otra_tarea):
        return self.prioridad < otra_tarea.prioridad

    def __str__(self):
        return f"[{self.estado.value.upper()}] {self.titulo} (Prioridad {self.prioridad})"