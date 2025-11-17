#Este archivo permite importar el paquete con `import machine_learning`.


# try y except para ver que se importe bien en controller
try:
    from .data_set import predecir, obtener_equipos  # noqa: F401
except Exception:
    # Si hay errores al importar (p. ej. dependencias faltantes), no fallamos en la carga del paquete.
    pass
