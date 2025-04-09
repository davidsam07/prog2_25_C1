def log_funcion(funcion):
    """
    Decorador para imprimir un log antes y después de llamar a la función.
    """
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando: {funcion.__name__}")
        resultado = funcion(*args, **kwargs)
        print(f"[LOG] Finalizado: {funcion.__name__}")
        return resultado
    return envoltura
