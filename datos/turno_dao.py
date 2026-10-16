# datos/turno_dao.py
from mysql.connector import Error
from datos.conexion import conectar


class TurnoDAO:

#Agrega un turno
    def insertar(self, paciente_id, profesional_id, fecha, hora):
       
        conn = conectar() #Establece la conexion con la DB
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO turnos "
                "(paciente_id, profesional_id, fecha, hora) "
                "VALUES (%s, %s, %s, %s)",
                (paciente_id, profesional_id, fecha, hora)
            )
            conn.commit()
            return cur.lastrowid
        
        #En caso de oucrrir un error revierte los cambios realizados
        except Error as e:
            conn.rollback() 
            raise Exception(f"Error al insertar turno: {e}")
        finally:
            cur.close()
            conn.close()

 #----------------------------------------------------------------------------
    def buscar_por_id(self, id_turno):
   
        conn = conectar() #Establece la conexion con la DB
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT * FROM turnos WHERE id = %s",
                (id_turno,)
            )
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------
# Devuelve una lista con los turnos que ocupan el mismo profesional, fecha y hora
    def buscar_conflictos(self, profesional_id, fecha, hora):
 
     conn = conectar() #Establece la conexion con la DB
     try:
         cur = conn.cursor(dictionary=True)
         cur.execute("""
             SELECT id FROM turnos
             WHERE profesional_id = %s
               AND fecha = %s
               AND hora = %s
               AND estado NOT IN ('cancelado', 'ausente')
         """, (profesional_id, fecha, hora))
         return cur.fetchall()
     finally:
         cur.close()
         conn.close()

#----------------------------------------------------------------------------
  #cambia solo el estado del turno (ej: 'confirmado', 'cancelado'
    def actualizar_estado(self, id_turno, nuevo_estado):
      
        conn = conectar() #Establece la conexion con la DB
        try:
            cur = conn.cursor() # Crea el objeto cursor para enviar la consulta SQL.
            cur.execute(
                "UPDATE turnos SET estado = %s WHERE id = %s",
        #pasa como argumento el estado que se quiere y el id del turno
                (nuevo_estado, id_turno)
            )
            conn.commit() #Guarda los cambios de forma permanente en DB
            return cur.rowcount > 0
        except Error as e:
            conn.rollback() #En caso de oucrrir un error revierte los cambios realizados
            raise Exception(f"Error al actualizar estado del turno: {e}")
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------
# Cambia la fecha y hora de un turno existente
    def reprogramar(self, id_turno, nueva_fecha, nueva_hora):
     
        conn = conectar() # Se establece la conexión con la DB.
        try:
            cur = conn.cursor() # Crea el objeto cursor para enviar la consulta SQL.
            cur.execute(
                "UPDATE turnos "
                "SET fecha = %s, hora = %s, estado = 'pendiente' "
                "WHERE id = %s",
     # Pasa como parámetro (%s) los nuevos datos de tiempo junto al ID del turno a modificar
                (nueva_fecha, nueva_hora, id_turno)
            )
            conn.commit() #guarda los cambios en la DB
            return cur.rowcount > 0
        
        except Error as e:
        # Deshace los cambios realizados en caso de error
            conn.rollback() 
            raise Exception(f"Error al reprogramar turno: {e}")
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------
#Devuelve la lista de turnos para la fecha pasada como parametro
    def listar_por_fecha(self, fecha):

        conn = conectar()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT t.id, t.fecha, t.hora, t.estado,
                       CONCAT(p.apellido, ', ', p.nombre) AS paciente,
                       CONCAT(pr.apellido, ', ', pr.nombre) AS profesional
                FROM turnos t
                JOIN pacientes p ON p.id = t.paciente_id
                JOIN profesionales pr ON pr.id = t.profesional_id
                WHERE t.fecha = %s AND t.estado <> 'cancelado'
                ORDER BY t.hora
            """, (fecha,))
        # Devuelve la lista completa con todos los turnos del día.
            return cur.fetchall() 
        finally:
            cur.close()
            conn.close()

#----------------------------------------------------------------------------
#Devuelve todos los turnos pertenecientes a un paciente especifico
    def listar_por_paciente(self, paciente_id):

        conn = conectar()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("""
                SELECT t.id, t.fecha, t.hora, t.estado,
                       CONCAT(pr.apellido, ', ', pr.nombre) AS profesional
                FROM turnos t
                JOIN profesionales pr ON pr.id = t.profesional_id
                WHERE t.paciente_id = %s
                ORDER BY t.fecha DESC, t.hora DESC
            """, (paciente_id,))
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
