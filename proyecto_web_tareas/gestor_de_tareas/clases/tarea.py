from enum import Enum
from datetime import date
from typing import Optional, List

class EstadoTarea(Enum):
    PENDIENTE = "Pendiente"
    EN_PROGRESO = "En progreso"
    COMPLETADA = "Completada"

class Tarea:
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

    def cambiar_estado(self, nuevo_estado: EstadoTarea):
        self.estado = nuevo_estado

    def completar(self):
        self.estado = EstadoTarea.COMPLETADA

    def __str__(self):
        return f"{self.titulo} [{self.estado.value}]"

    def asignar_usuario(self, usuario: str):
        self.usuario_asignado = usuario

    def modificar(self,
                  titulo=None,
                  descripcion=None,
                  fecha_limite=None,
                  prioridad=None,
                  etiquetas=None):
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

    def __lt__(self, otra_tarea: 'Tarea'):
        # Comparar por prioridad; prioridad menor significa más alta
        return self.prioridad < otra_tarea.prioridad

    def __str__(self):
        return f"[{self.estado.value.upper()}] {self.titulo} (Prioridad {self.prioridad})"

