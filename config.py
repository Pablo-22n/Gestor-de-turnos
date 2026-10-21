# config.py
"""
Configuración de conexión a la base de datos.
Todos los datos están centralizados acá: si cambia el servidor,
el usuario o la contraseña, se modifica SOLO este archivo.
"""
import os


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"), # <-- Poné localhost o ip de tu VM
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),  # ← CAMBIAR
    "password": os.getenv("DB_PASSWORD", ""),  # ← CAMBIAR
    "database": os.getenv("DB_NAME", "turnos"),
    "charset": "utf8mb4",
}