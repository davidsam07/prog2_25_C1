from enum import Enum
from datetime import date
from typing import Optional, List

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

    def __str__(self) -> str:
        return f"{self.titulo} ({self.estado.name}) - Prioridad {self.prioridad}"

class TareaImportante(Tarea):
    def mostrar_alerta(self) -> str:
        return f" ¡Tarea urgente!: {self.titulo.upper()}"
