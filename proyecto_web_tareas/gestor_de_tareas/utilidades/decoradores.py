def log_funcion(funcion):
    """
    Decorador para imprimir un log antes y después de la ejecución de una función.

    Este decorador se utiliza para depurar el flujo de ejecución, mostrando en la consola
    un mensaje cuando la función se inicia y cuando se termina de ejecutar.

    Parameters
    ----------
    funcion : callable
        La función que se desea decorar.

    Returns
    -------
    callable
        Una nueva función que envuelve la función original e imprime mensajes de log
        antes y después de su ejecución.
    """
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando: {funcion.__name__}")
        resultado = funcion(*args, **kwargs)
        print(f"[LOG] Finalizado: {funcion.__name__}")
        return resultado
    return envoltura
