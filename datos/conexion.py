# datos/conexion.py
"""
Función para conectarse a MariaDB.
Todos los DAOs la usan para obtener una conexión.

Esta es la ÚNICA función del sistema que sabe cómo conectarse.
Si mañana cambia el servidor, se toca solo acá.
"""
import mysql.connector
from config import DB_CONFIG


def conectar():
    """
    Devuelve una conexión nueva a MariaDB.
    El que llama es responsable de cerrarla con conn.close().
    """
    return mysql.connector.connect(**DB_CONFIG)