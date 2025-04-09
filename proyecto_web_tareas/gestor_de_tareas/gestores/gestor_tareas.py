from datetime import datetime
from typing import List, Optional
from gestor_de_tareas.clases.tarea import Tarea, EstadoTarea
from gestor_de_tareas.utilidades.decoradores import log_funcion

class GestorDeTareas:
    def __init__(self):
        self.tareas: List[Tarea] = []
        self.contador_id = 1  # Para asignar IDs únicos a cada tarea

    @log_funcion
    def crear_tarea(self,
                    titulo: str,
                    descripcion: str,
                    fecha_limite_str: str,
                    prioridad: int,
                    etiquetas=None,
                    usuario_asignado=None) -> Optional[Tarea]:
        """
        Crea una nueva tarea y la añade a la lista.
        """
        try:
            fecha = datetime.strptime(fecha_limite_str, "%Y-%m-%d").date()
        except ValueError:
            print("[ERROR] Fecha mal formateada. Usa YYYY-MM-DD.")
            return None
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

    @log_funcion
    def listar_tareas(self) -> List[Tarea]:
        return self.tareas

    @log_funcion
    def obtener_por_id(self, id_tarea: int) -> Optional[Tarea]:
        for t in self.tareas:
            if t.id_tarea == id_tarea:
                return t
        return None

    @log_funcion
    def filtrar_por_estado(self, estado: EstadoTarea) -> List[Tarea]:
        return [t for t in self.tareas if t.estado == estado]

    @log_funcion
    def cambiar_estado_tarea(self, id_tarea: int, nuevo_estado: EstadoTarea) -> bool:
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.cambiar_estado(nuevo_estado)
            return True
        return False

    @log_funcion
    def modificar_tarea(self,
                        id_tarea: int,
                        titulo=None,
                        descripcion=None,
                        fecha_limite=None,
                        prioridad=None,
                        etiquetas=None) -> bool:
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.modificar(titulo, descripcion, fecha_limite, prioridad, etiquetas)
            return True
        return False

    @log_funcion
    def asignar_usuario_tarea(self, id_tarea: int, usuario: str) -> bool:
        tarea = self.obtener_por_id(id_tarea)
        if tarea:
            tarea.asignar_usuario(usuario)
            return True
        return False

    @log_funcion
    def ordenar_por_prioridad(self) -> List[Tarea]:
        """
        Devuelve una lista ordenada por prioridad (se usa __lt__ en Tarea).
        """
        return sorted(self.tareas)
