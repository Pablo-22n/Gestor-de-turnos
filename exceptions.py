# Se usa para distinguir errores de negocio (esperados, como "el DNIya existe") de los errores técnicos


class TurnoError(Exception):
    """Base de todas las excepciones del dominio."""
    pass


class TurnoNoEncontradoError(TurnoError):
    # Se usa cuando paciente, profesional o turno no existe
    pass


class ConflictoHorarioError(TurnoError):
    # Se usa cuando el profesional ya tiene un turno en ese horario
    pass


class DatosInvalidosError(TurnoError):
    # Se usa cuando dos datos no cumplen las reglas de negocio
    pass