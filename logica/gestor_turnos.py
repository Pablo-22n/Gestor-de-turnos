# negocio/gestor_turnos.py
"""
Capa de LÓGICA (NEGOCIO).
Reglas del sistema: validaciones, decisiones, excepciones.
"""
from datetime import date, time, datetime

#Importacion de clases
from datos.paciente_dao import PacienteDAO
from datos.profesional_dao import ProfesionalDAO 
from datos.turno_dao import TurnoDAO 

from exceptions import (
    DatosInvalidosError, TurnoNoEncontradoError, ConflictoHorarioError
)

class GestorTurnos:
    """Lógica del sistema de turnos."""

    def __init__(self):
        # Instancio las clases.
        self.paciente_dao = PacienteDAO()
        self.profesional_dao = ProfesionalDAO()
        self.turno_dao = TurnoDAO()


    def _validar_fecha_futura(self, fecha, hora):

        #valida que no sea una fechas pasada
        if fecha < date.today():
            raise DatosInvalidosError("No se permiten fechas pasadas")
        #Combina fecha+hora y verfica si es menor al horario actual
        if datetime.combine(fecha, hora) <= datetime.now():
            raise DatosInvalidosError("El horario debe ser futuro")
        

 # =========================================================================
                            # PACIENTES
  # =========================================================================                           

    def alta_paciente(self, dni, nombre, apellido, telefono=""):

        # Si el DNI está vacío, muestra el siguiente mensaje.
        if not dni:
            raise DatosInvalidosError("El DNI es obligatorio")
        
        #Invoca la funcion de la clase paciente, valida si ya existe un paciente con ese dni
        elif self.paciente_dao.buscar_por_dni(dni):
            raise DatosInvalidosError(f"Ya existe un paciente con DNI {dni}")
        
        # 3. Si no entró a ninguna de las dos fallas anteriores, ejecuta la funcion de la clase paciente e inserta un nuevo paciente
        else:
            return self.paciente_dao.insertar(dni, nombre, apellido, telefono)
        
#----------------------------------------------------------------------------
    def modificar_paciente(self, dni, nombre, apellido, telefono=""):

        #Invoca la función de la clase paciente. Si no encuentra nada, lanza el error.
        if not self.paciente_dao.buscar_por_dni(dni):
            raise TurnoNoEncontradoError(                
                f"El Paciente con id {dni} no existe")
        else:
            self.paciente_dao.actualizar(dni, nombre, apellido, telefono)

#----------------------------------------------------------------------------
    def baja_paciente(self, dni):
        
        #Invoca la función de paciente para verificar por ID. 
        # Si el paciente no existe, frena el flujo.
        if not self.paciente_dao.buscar_por_dni(dni):
            raise TurnoNoEncontradoError(f"Paciente con id {dni} no existe")
        
        # 2. Si el paciente existe, lo elimina
        else:
            self.paciente_dao.eliminar(dni)

    def listar_pacientes(self):
        return self.paciente_dao.listar()

    def buscar_paciente(self, dni):
        return self.paciente_dao.buscar_por_dni(dni)
    

# ===========================================================================
                    # PROFESIONALES
 # =========================================================================

#Registra un nuevo profesional en la base de datos
    def alta_profesional(self, dni, nombre, apellido, especialidad=""):

    #Valida que el dni no este vacio
        if not dni:
            raise DatosInvalidosError("El DNI es obligatorio")
        
  #Invoca la funcion de la clase profesional para verificar si el DNI ya está registrado
        if self.profesional_dao.buscar_por_dni(dni):
            raise DatosInvalidosError(f"Ya existe un profesional con DNI {dni}")

    #Registra el nuevo profesional en la base de datos 
        return self.profesional_dao.insertar(
            dni, nombre, apellido, especialidad)
    
#----------------------------------------------------------------------------
# Actualiza los datos de un profesional
    def modificar_profesional(self, dni, nombre, apellido, especialidad=""):

  #Invoca la funcion para buscar por dni al profesional a actualizar     
        if not self.profesional_dao.buscar_por_dni(dni):
            raise TurnoNoEncontradoError(f"El profesional con dni {dni} no existe")
    
        else:
            #Si el profesional existe, lo actualiza   
           self.profesional_dao.actualizar(dni, nombre, apellido, especialidad)

#----------------------------------------------------------------------------
#Elimina un profesional
    def baja_profesional(self, dni):

    #valida que el profesional exista
        if not self.profesional_dao.buscar_por_dni(dni):
            raise TurnoNoEncontradoError(f"Profesional con dni {dni} no existe")
        
        try:
    #Invoca al metodo de la clase profesional para eliminar al profesional por dni
            self.profesional_dao.eliminar(dni)
        except Exception:
            raise DatosInvalidosError(
                "No se puede eliminar el profesional: tiene turnos asociados")

#----------------------------------------------------------------------------
    def listar_profesionales(self):
        return self.profesional_dao.listar()

    def buscar_profesional(self, dni):
        return self.profesional_dao.buscar_por_dni(dni)


# ===========================================================================
                                # TURNOS
# =========================================================================

    def alta_turno(self, dni_paciente, dni_profesional, fecha, hora):
      
#invoca a la funcion interna para verificar que la fecha del turno sea valida
        self._validar_fecha_futura(fecha, hora)

    #valida que exista el paciente al que se le asignara el turno
    #Invoca la funcion de la clase paciente
        paciente = self.paciente_dao.buscar_por_dni(dni_paciente)
        if not paciente:
            raise TurnoNoEncontradoError(
                f"Paciente con DNI {dni_paciente} no existe")

        #valida que exista el paciente al que se le asignara el turno
        profesional = self.profesional_dao.buscar_por_dni(dni_profesional)
        if not profesional:
            raise TurnoNoEncontradoError(
                f"Profesional con DNI {dni_profesional} no existe")

        conflictos = self.turno_dao.buscar_conflictos(
            profesional["id"], fecha, hora)
        if conflictos:
            raise ConflictoHorarioError(
                "El profesional ya tiene un turno en ese horario")

        # Persistir
        return self.turno_dao.insertar(
            paciente["id"], profesional["id"], fecha, hora)

#----------------------------------------------------------------------------
# Confirma un turno existente cambiando su estado a 'confirmado
    def confirmar_turno(self, id_turno):

        turno = self.turno_dao.buscar_por_id(id_turno)
    #Si el turno no existe muestra el mensaje de error y corta el flujo
        if not turno:
            raise TurnoNoEncontradoError(f"Turno {id_turno} no existe")
        
      #valida si el turno se encuentra pendiente  
        if turno["estado"] != "pendiente":
            raise DatosInvalidosError("Solo se confirman turnos pendientes")
    #Si el turno es válido y está pendiente, lo actualiza
        self.turno_dao.actualizar_estado(id_turno, "confirmado")

#----------------------------------------------------------------------------
    def cancelar_turno(self, id_turno):

# Invoca la función de la clase turno para buscar el turno original por su ID
        turno = self.turno_dao.buscar_por_id(id_turno)
 
        if not turno:
            # Lanza error si el ID ingresado no coincide con ningún turno
            raise TurnoNoEncontradoError(f"Turno {id_turno} no existe")
        
        if turno["estado"] in ("atendido", "cancelado"):
     #Si el turno ya figura como atendido o cancelado, lanza el mensaje y corta el flujo
            raise DatosInvalidosError(f"No se puede cancelar un turno {turno['estado']}")
        
     # Si pasa las validaciones, actualiza el estado del turno a cancelado   
        self.turno_dao.actualizar_estado(id_turno, "cancelado")

#----------------------------------------------------------------------------
    def marcar_atendido(self, id_turno):
        turno = self.turno_dao.buscar_por_id(id_turno)
        if not turno:
            raise TurnoNoEncontradoError(f"Turno {id_turno} no existe")
        self.turno_dao.actualizar_estado(id_turno, "atendido")

#----------------------------------------------------------------------------
 #  Cambia la fecha y hora de un turno existente   
    def reprogramar_turno(self, id_turno, nueva_fecha, nueva_hora):
        
# Invoca la función interna para validar que la nueva fecha elegida sea futura
        self._validar_fecha_futura(nueva_fecha, nueva_hora)

 #Invoca la funcion de la clase turno      
        turno = self.turno_dao.buscar_por_id(id_turno)
 #Lanza error si el ID ingresado con coincide con ningun turno
        if not turno:
            raise TurnoNoEncontradoError(f"Turno {id_turno} no existe")
        
        if turno["estado"] in ("atendido", "cancelado"):
            raise DatosInvalidosError("No se puede reprogramar este turno")

        # Si la nueva fecha/hora es la misma que la actual, no hay nada que hacer
        if turno["fecha"] == nueva_fecha and turno["hora"] == nueva_hora:
            return #corta el flujo

 #Almacena en la variable conflictos el turno del profesional especifico que coinicidan con
# la fecha y hora que se quiere reprogramar. Si no hay devuelve la lista vacia   
        conflictos = self.turno_dao.buscar_conflictos(turno["profesional_id"], nueva_fecha, nueva_hora)

        #Si hay un turno para el horario especificado lanza el mensaje de error y corta el flujo
        if conflictos:
            raise ConflictoHorarioError("El nuevo horario está ocupado")

    # Si no hay turnos en el nuevo horario, se actualiza el turno
    # con la nueva fecha y hora.
        self.turno_dao.reprogramar(id_turno, nueva_fecha, nueva_hora)

#----------------------------------------------------------------------------
    def turnos_por_fecha(self, fecha):
        return self.turno_dao.listar_por_fecha(fecha)

# Devuelve la lista de turnos asociados a un paciente específico
    def turnos_de_paciente(self, dni_paciente):
        #Almacena el paciente como diccionario
        paciente = self.paciente_dao.buscar_por_dni(dni_paciente)

        if not paciente:
            # Lanza error si el DNI ingresado no coincide con ningún paciente
            raise TurnoNoEncontradoError(f"Paciente con DNI {dni_paciente} no existe")
       # Si el paciente existe, extrae el id del diccionario, lo pasa como argumento 
       # y devuelve una lista de turnos pertenecientes al paciente especificado
        return self.turno_dao.listar_por_paciente(paciente["id"])