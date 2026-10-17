# datos/usuario_dao.py
from mysql.connector import Error
from datos.conexion import conectar

class UsuarioDAO:

#D evuelve los datos del usuario o None si no existe
    def buscar_por_usuario(self, usuario):
        conn = conectar()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()