from datetime import datetime
from typing import List, Optional
from models.tarea import Tarea, EstadoTarea
from utils.decoradores import log_funcion

class TareaManager:
    def __init__(self):
        self.tareas: List[Tarea] = []

    @log_funcion
    def crear_tarea(self, titulo, descripcion, fecha_limite_str, prioridad, etiquetas=None):
        fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
        tarea = Tarea(titulo, descripcion, fecha_limite, prioridad, etiquetas)
        self.tareas.append(tarea)
        return tarea

    @log_funcion
    def listar_tareas(self, estado: Optional[EstadoTarea] = None):
        if estado:
            return [t for t in self.tareas if t.estado == estado]
        return self.tareas

    @log_funcion
    def ordenar_por_prioridad(self):
        return sorted(self.tareas)

    @log_funcion
    def buscar_por_etiqueta(self, etiqueta):
        return [t for t in self.tareas if etiqueta in t.etiquetas]
