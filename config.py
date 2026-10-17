# config.py
"""
Configuración de conexión a la base de datos.
Todos los datos están centralizados acá: si cambia el servidor,
el usuario o la contraseña, se modifica SOLO este archivo.
"""
import os


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.1.31"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "turnos_admin"),
    "password": os.getenv("DB_PASSWORD", "admin.123"),  # ← CAMBIAR
    "database": os.getenv("DB_NAME", "turnos"),
    "charset": "utf8mb4",
}