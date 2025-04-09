from gestor_de_tareas.clases.tarea import Tarea
from datetime import datetime
from typing import List, Optional

class GestorDeTareas:
    def __init__(self):
        self.tareas: List[Tarea] = []

    def crear_tarea(self, titulo: str, descripcion: str, fecha_limite_str: str, prioridad: int) -> Optional[Tarea]:
        try:
            fecha_limite = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
        except ValueError:
            print("[ERROR] Fecha incorrecta. Usa el formato YYYY-MM-DD.")
            return None
        tarea = Tarea(titulo, descripcion, fecha_limite, prioridad)
        self.tareas.append(tarea)
        return tarea

    def listar_tareas(self) -> List[Tarea]:
        return self.tareas
