# logica/gestor_usuarios.py
import hashlib
from datos.usuario_dao import UsuarioDAO
from exceptions import DatosInvalidosError

class GestorUsuarios:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

#Convierte la contraseña a un hash SHA-256.
    def _encriptar(self, password):
  
        return hashlib.sha256(password.encode()).hexdigest()


    # Valida las credenciales
    #Devuelve un diccionario con los datos del usuario si es correcto.
    def login(self, usuario, password):

    # Verifica si alguno de los campos de inicio de sesión quedó en blanco   
        if not usuario or not password:
            raise DatosInvalidosError("Usuario y contraseña son obligatorios")

        # Buscamos en la db
        user_db = self.usuario_dao.buscar_por_usuario(usuario)

        if not user_db:
            # Si el usuario no existe en la base de datos, lanza el mensaje
            raise DatosInvalidosError("Usuario o contraseña incorrectos")

        
    # Encripta la contraseña escrita por el usuario para poder compararla con la que está guardada
        hash_ingresado = self._encriptar(password)
        if hash_ingresado != user_db["password_hash"]:
            raise DatosInvalidosError("Usuario o contraseña incorrectos")

        # Si llegó acá, el login es correcto, devuelve los datos de sesión
        return {"id": user_db["id"], "usuario": user_db["usuario"], "rol": user_db["rol"]}