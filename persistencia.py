
"""
Módulo de Persistencia de Datos

Este módulo se encarga de guardar y cargar la información de usuarios, tareas y proyectos
en un archivo binario usando pickle.

La idea es persistir el estado actual de la aplicación y recuperarlo en arranques posteriores.
Además, se registra la función de guardado automático al salir de la aplicación mediante atexit.

"""

import pickle
import atexit
from typing import Any, List, Dict, Tuple

def guardar_datos(usuarios: List[Any],
                  tareas: List[Any],
                  proyectos: Dict[str, Any],
                  filename: str = "datos.pkl") -> None:
    """
    Guarda los datos de usuarios, tareas y proyectos en un archivo binario.

    Parameters
    ----------
    usuarios : list
        Lista de usuarios.
    tareas : list
        Lista de tareas.
    proyectos : dict
        Diccionario de proyectos (por ejemplo, la variable 'proyectos' de una instancia de GestorProyectos).
    filename : str, optional
        Nombre del archivo donde se guardarán los datos (por defecto "datos.pkl").

    Returns
    -------
    None
    """
    try:
        datos = {"usuarios": usuarios, "tareas": tareas, "proyectos": proyectos}
        with open(filename, "wb") as archivo:
            pickle.dump(datos, archivo)
        print(f"[Persistencia] Datos guardados en '{filename}'.")
    except Exception as error:
        print("Error al guardar datos:", error)

def cargar_datos(filename: str = "datos.pkl") -> Tuple[List[Any], List[Any], Dict[str, Any]]:
    """
    Carga los datos de usuarios, tareas y proyectos desde un archivo binario.

    Parameters
    ----------
    filename : str, optional
        Nombre del archivo de donde se cargarán los datos (por defecto "datos.pkl").

    Returns
    -------
    tuple
        Una tupla con tres elementos: (usuarios, tareas, proyectos). Si el archivo no existe,
        se retornan listas/diccionarios vacíos.
    """
    try:
        with open(filename, "rb") as archivo:
            datos = pickle.load(archivo)
        print(f"[Persistencia] Datos cargados desde '{filename}'.")
        return datos.get("usuarios", []), datos.get("tareas", []), datos.get("proyectos", {})
    except FileNotFoundError:
        print(f"Archivo '{filename}' no encontrado. Se retornan estructuras vacías.")
        return ([], [], {})
    except Exception as error:
        print("Error al cargar datos:", error)
        return ([], [], {})

def registrar_guardado_automatico(usuarios: List[Any],
                                  tareas: List[Any],
                                  proyectos: Dict[str, Any],
                                  filename: str = "datos.pkl") -> None:
    """
    Registra la función de guardado automático usando atexit para que, al cerrar la aplicación,
    se guarden los datos.

    Parameters
    ----------
    usuarios : list
        Lista de usuarios.
    tareas : list
        Lista de tareas.
    proyectos : dict
        Diccionario de proyectos.
    filename : str, optional
        Nombre del archivo de guardado (por defecto "datos.pkl").

    Returns
    -------
    None
    """
    atexit.register(guardar_datos, usuarios, tareas, proyectos, filename)
    print("[Persistencia] Registro de guardado automático realizado.")
