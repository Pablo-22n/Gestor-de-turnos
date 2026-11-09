import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "TU_CONTRASEÑA_AQUI"), # <-- La que pusiste en el Paso 2
    "database": os.getenv("DB_NAME", "turnos"),
    "charset": "utf8mb4",
}