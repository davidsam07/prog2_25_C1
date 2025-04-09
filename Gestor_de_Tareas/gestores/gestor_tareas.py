from datetime import datetime
from typing import List, Optional
from models.tarea import Tarea, EstadoTarea
from utils.decoradores import log_funcion

class TareaManager:
    """
    Gestor de tareas que permite crearlas, listarlas, ordenarlas y filtrarlas.
    """

    def __init__(self):
        self.tareas: List[Tarea] = []

    @log_funcion
    def crear_tarea(self, titulo: str, descripcion: str, fecha_limite_str: str, prioridad: int, etiquetas: Optional[List[str]] = None) -> Optional[Tarea]:
        """
        Crea una nueva tarea y la añade a la lista.

        Returns
        -------
        Tarea or None
            La tarea creada o None si hubo un error en los datos.
        """
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
        except ValueError:
            print("[ERROR] Fecha mal formateada. Usa YYYY-MM-DD.")
            return None
        tarea = Tarea(titulo, descripcion, fecha_limite, prioridad, etiquetas)
        self.tareas.append(tarea)
        return tarea

    @log_funcion
    def listar_tareas(self, estado: Optional[EstadoTarea] = None) -> List[Tarea]:
        """Devuelve todas las tareas o solo las de cierto estado."""
        return [t for t in self.tareas if t.estado == estado] if estado else self.tareas

    @log_funcion
    def ordenar_por_prioridad(self) -> List[Tarea]:
        """Devuelve tareas ordenadas por prioridad."""
        return sorted(self.tareas)

    @log_funcion
    def buscar_por_etiqueta(self, etiqueta: str) -> List[Tarea]:
        """Devuelve tareas que contienen una etiqueta específica."""
        return [t for t in self.tareas if etiqueta in t.etiquetas]


