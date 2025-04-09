def log_funcion(func):
    """
    Decorador para registrar llamadas a funciones.
    """
    def wrapper(*args, **kwargs):
        print(f"[LOG] Ejecutando: {func.__name__}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] Finalizado: {func.__name__}")
        return resultado
    return wrapper
