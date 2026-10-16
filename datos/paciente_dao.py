from mysql.connector import Error
from datos.conexion import conectar


class PacienteDAO:

    # ---------- INSERTAR PACIENTE ----------
    def insertar(self, dni, nombre, apellido, telefono=""):
        """Inserta un paciente. Devuelve el id generado."""
        #Abre la conexión con MariaDB en Linux.
        conn = conectar()
        try:
            # Crea el objeto Cursor, lleva las consultas y trae las respuestas de la DB
            cur = conn.cursor()
            
            cur.execute( # Envia la consulta y la ejecuta
                "INSERT INTO pacientes (dni, nombre, apellido, telefono) "
                "VALUES (%s, %s, %s, %s)",
                (dni, nombre, apellido, telefono)
            )
            conn.commit() #Guarda los cambios de forma permanente en DB
            return cur.lastrowid #devuelve el ID del paciente 
        except Error as e:
            conn.rollback() # Revierte los cambios en caso de error
            raise Exception(f"Error al insertar paciente: {e}")
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------
    #  CONSULTAS
 # Busca un paciente por su dni
    def buscar_por_dni(self, dni):
        conn = conectar()
        try:
            cur = conn.cursor(dictionary=True) # Devuelve cada fila como un diccionario
            cur.execute("SELECT * FROM pacientes WHERE dni = %s", (dni,))
            return cur.fetchone() #Devuelve la primera fila que cumpla la condicion de la consulta
        finally:
            cur.close()
            conn.close()

# Busca un paciente por su id
    def buscar_por_id(self, id_paciente):
        conn = conectar()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM pacientes WHERE id = %s", (id_paciente,))
            return cur.fetchone() #Devuelve la primera fila que cumpla la condicion de la consulta
        finally:
            cur.close() # Cierra el cursor para liberar memoria en el servidor
            conn.close() #cierra la comunicacion
            

    def listar(self):
        conn = conectar()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM pacientes ORDER BY apellido, nombre")
            return cur.fetchall() #Trae todas las filas de la consulta hecha
        finally:
            cur.close()
            conn.close()


#----------------------------------------------------------------------------
#Actualiza los datos del paciente 
    def actualizar(self, dni, nombre, apellido, telefono=""):
        conn = conectar()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE pacientes "
                "SET nombre = %s, apellido = %s, telefono = %s "
                "WHERE dni = %s",
                (nombre, apellido, telefono, dni)
            )
            conn.commit()
            # cur.rowcount indica cuántas filas modificó el UPDATE
            return cur.rowcount > 0 
        except Error as e:
            conn.rollback() # Revierte los cambios en caso de error
            raise Exception(f"Error al actualizar paciente: {e}")
        finally:
            cur.close()
            conn.close()



    # ---------- ELIMINAR PACIENTE----------
    def eliminar(self, dni):
        conn = conectar()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM pacientes WHERE id = %s", (dni,))
            conn.commit()
            return cur.rowcount > 0
        except Error as e:
            conn.rollback()
            raise Exception(f"Error al eliminar paciente: {e}")
        finally:
            cur.close()
            conn.close()