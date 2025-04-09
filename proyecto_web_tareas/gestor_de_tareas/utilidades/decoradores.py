def log_funcion(funcion):
    def envoltura(*args, **kwargs):
        print(f"[LOG] Ejecutando: {funcion.__name__}")
        resultado = funcion(*args, **kwargs)
        print(f"[LOG] Finalizado: {funcion.__name__}")
        return resultado
    return envoltura
