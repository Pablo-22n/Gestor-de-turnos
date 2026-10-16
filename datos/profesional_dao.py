from mysql.connector import Error
from datos.conexion import conectar


class ProfesionalDAO:

#Agrega un nuevo profesional, los datos son pasado como argumento
    def insertar(self, dni, nombre, apellido, especialidad=""):
        
        conn = conectar() # Se establece la conexión con la DB.
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO profesionales (dni, nombre, apellido, especialidad) "
                # Los '%s' actúan como  parámetros
                "VALUES (%s, %s, %s, %s)", 
                # Reemplaza los casilleros %s en orden con las variables que tienen los datos reales.
                (dni, nombre, apellido, especialidad)
            )
            conn.commit() #Guarda los cambios de forma permanente en DB
            return cur.lastrowid
        except Error as e:
             # Deshace los cambios realizados en caso de error
            conn.rollback()
            raise Exception(f"Error al insertar profesional: {e}")
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------   
# Busca un profesional en la base de datos utilizando su DNI.
    def buscar_por_dni(self, dni):
        
        conn = conectar() # Se establece la conexión con la DB.

        try:
            # Crea un cursor que devuelve los registros como diccionarios
            cur = conn.cursor(dictionary=True) 
             # Se ejecuta la consulta utilizando 'dni' como parámetro
            cur.execute(
                "SELECT * FROM profesionales WHERE dni = %s",
                (dni,)
            )
            #devuelve el primer registro que cumpla la condicion de la consulta
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------
# Busca un profesional en la base de datos utilizando su ID
    def buscar_por_id(self, id_profesional):

        conn = conectar() # Establece la conexión con la base de datos.
        try:
            cur = conn.cursor(dictionary=True)
    #Ejecuta la consulta para buscar segun el ID que se pase por parametro
            cur.execute(
                "SELECT * FROM profesionales WHERE id = %s",
                (id_profesional,)
            )
    # Devuelve el primer registro encontrado
            return cur.fetchone() 
        finally:
            cur.close()
            conn.close() #cierra la comunicacion

#----------------------------------------------------------------------------
# Devuelve una lista con todos los profesionales
    def listar(self):
        
        conn = conectar() # Se establece la conexión con la DB.
        try:
            cur = conn.cursor(dictionary=True)
    # Ejecuta la consulta para obtener todos los profesionales, ordenados por apellido y nombre.
            cur.execute(
                "SELECT * FROM profesionales ORDER BY apellido, nombre"
            )
             # Devuelve todos los registros encontrados
            return cur.fetchall()
        finally:
            cur.close()
            conn.close() #cierra la comunicacion

#----------------------------------------------------------------------------
# Actualiza los datos del profesional, segun el ID del mismo
    def actualizar(self, dni, nombre, apellido, especialidad=""):
        conn = conectar()
        try:
            cur = conn.cursor() #Establece la conexión con la DB.
            cur.execute(
                "UPDATE profesionales "
                "SET nombre = %s, apellido = %s, especialidad = %s "
                "WHERE dni = %s",
                # Pasa como parametro los valores que se van a actualizar
                (nombre, apellido, especialidad, dni)
            )
            conn.commit()
            return cur.rowcount > 0
        except Error as e:
            conn.rollback() # Deshace los cambios realizados en caso de error
            raise Exception(f"Error al actualizar profesional: {e}")
        finally:
            cur.close()
            conn.close() #cierra la comunicacion


#----------------------------------------------------------------------------
  #Elimina un profesional por DNI
    def eliminar(self, dni):
   
        conn = conectar() #Establece la conexion con la DB
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM profesionales WHERE id = %s",
                (dni,)
            )
            conn.commit() #Guarda los cambios en la DB
            return cur.rowcount > 0
        
        except Error as e:
    # Deshace los cambios realizados en caso de error
            conn.rollback() 
            raise Exception(f"Error al eliminar profesional: {e}")
        finally:
            cur.close()
            conn.close()