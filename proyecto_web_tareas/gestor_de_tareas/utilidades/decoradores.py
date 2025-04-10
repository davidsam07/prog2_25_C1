from typing import Callable, Any

def log_funcion(funcion: Callable) -> Callable:
    """
    Decorador para imprimir un log antes y después de llamar a la función.

    Este decorador envuelve la función original para mostrar mensajes de log que indican
    cuándo se inicia y cuándo se finaliza la ejecución de la función.

    Parameters
    ----------
    funcion : Callable
        La función a la que se le aplicará el decorador.

    Returns
    -------
    Callable
        Una función envuelta que imprime mensajes de log antes y después de ejecutar la
        función original, devolviendo posteriormente el resultado de dicha función.
    """
    def envoltura(*args: Any, **kwargs: Any) -> Any:
        print(f"[LOG] Ejecutando: {funcion.__name__}")
        resultado = funcion(*args, **kwargs)
        print(f"[LOG] Finalizado: {funcion.__name__}")
        return resultado
    return envoltura

