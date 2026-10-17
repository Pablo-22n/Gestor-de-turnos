# presentacion/web/app.py
# presentacion/web/app.py
"""
Aplicación Flask del sistema de turnos con Login.
"""
from datetime import date, time
from functools import wraps  # Para el decorador de protección

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)

from logica.gestor_turnos import GestorTurnos
from logica.gestor_usuarios import GestorUsuarios  # <-- NUEVO
from exceptions import TurnoError


def create_app():
    """Crea la aplicación Flask y registra todas las rutas."""

    app = Flask(__name__)
    # Clave para firmar las cookies de los mensajes flash y de la sesión.
    app.secret_key = "clave-secreta-cambiar-en-produccion"

    # Instancias únicas de los gestores
    gestor = GestorTurnos()
    gestor_usr = GestorUsuarios()  # <-- NUEVO

    # =========================================================
    # DECORADOR DE PROTECCIÓN
    # =========================================================
    def requiere_login(f):
        """Obliga a que el usuario esté logueado para acceder a la ruta."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "usuario" not in session:
                flash("Tenés que iniciar sesión primero", "error")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function

    # =========================================================
    # LOGIN Y LOGOUT
    # =========================================================
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            try:
                user = gestor_usr.login(
                    request.form["usuario"].strip(),
                    request.form["password"]
                )
                session["usuario"] = user["usuario"]
                session["rol"] = user["rol"]
                flash(f"Bienvenido, {user['usuario']}", "success")
                return redirect(url_for("index"))
            except TurnoError as e:
                flash(str(e), "error")
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Sesión cerrada correctamente", "success")
        return redirect(url_for("login"))

    # =========================================================
    # INICIO (Protegido)
    # =========================================================
    @app.route("/")
    @requiere_login
    def index():
        return render_template("index.html")

    # =========================================================
    # PACIENTES (Protegidos)
    # =========================================================
    @app.route("/pacientes")
    @requiere_login
    def pacientes():
        lista = gestor.listar_pacientes()
        return render_template("pacientes.html", pacientes=lista)

    @app.route("/pacientes/nuevo", methods=["POST"])
    @requiere_login
    def alta_paciente():
        try:
            gestor.alta_paciente(
                dni=request.form["dni"].strip(),
                nombre=request.form["nombre"].strip(),
                apellido=request.form["apellido"].strip(),
                telefono=request.form.get("telefono", "").strip(),
            )
            flash("Paciente registrado correctamente", "success")
        except TurnoError as e:
            flash(str(e), "error")
        return redirect(url_for("pacientes"))

    @app.route("/pacientes/<dni>/eliminar", methods=["POST"])
    @requiere_login
    def baja_paciente(dni):
        try:
            gestor.baja_paciente(dni)
            flash("Paciente eliminado", "success")
        except TurnoError as e:
            flash(str(e), "error")
        return redirect(url_for("pacientes"))

    # =========================================================
    # PROFESIONALES (Protegidos)
    # =========================================================
    @app.route("/profesionales")
    @requiere_login
    def profesionales():
        lista = gestor.listar_profesionales()
        return render_template("profesionales.html", profesionales=lista)

    @app.route("/profesionales/nuevo", methods=["POST"])
    @requiere_login
    def alta_profesional():
        try:
            gestor.alta_profesional(
                dni=request.form["dni"].strip(),
                nombre=request.form["nombre"].strip(),
                apellido=request.form["apellido"].strip(),
                especialidad=request.form.get("especialidad", "").strip(),
            )
            flash("Profesional registrado correctamente", "success")
        except TurnoError as e:
            flash(str(e), "error")
        return redirect(url_for("profesionales"))

    @app.route("/profesionales/<dni>/eliminar", methods=["POST"])
    @requiere_login
    def baja_profesional(dni):
        try:
            gestor.baja_profesional(dni)
            flash("Profesional eliminado", "success")
        except TurnoError as e:
            flash(str(e), "error")
        return redirect(url_for("profesionales"))

    # =========================================================
    # TURNOS (Protegidos)
    # =========================================================
    @app.route("/turnos")
    @requiere_login
    def turnos():
        fecha_str = request.args.get("fecha", date.today().isoformat())
        try:
            fecha = date.fromisoformat(fecha_str)
        except ValueError:
            fecha = date.today()

        lista = gestor.turnos_por_fecha(fecha)
        return render_template("turnos.html", turnos=lista, fecha=fecha)

    @app.route("/turnos/nuevo", methods=["POST"])
    @requiere_login
    def alta_turno():
        try:
            fecha = date.fromisoformat(request.form["fecha"])
            hora = time.fromisoformat(request.form["hora"])

            gestor.alta_turno(
                dni_paciente=request.form["dni_paciente"].strip(),
                dni_profesional=request.form["dni_profesional"].strip(),
                fecha=fecha,
                hora=hora,
            )
            flash("Turno creado correctamente", "success")
            return redirect(url_for("turnos", fecha=fecha.isoformat()))
        except (TurnoError, ValueError) as e:
            flash(str(e), "error")
            return redirect(url_for("turnos"))

    @app.route("/turnos/<int:id_turno>/confirmar", methods=["POST"])
    @requiere_login
    def confirmar_turno(id_turno):
        try:
            gestor.confirmar_turno(id_turno)
            flash("Turno confirmado", "success")
        except TurnoError as e:
            flash(str(e), "error")
        return redirect(request.referrer or url_for("turnos"))

    @app.route("/turnos/<int:id_turno>/cancelar", methods=["POST"])
    @requiere_login
    def cancelar_turno(id_turno):
        try:
            gestor.cancelar_turno(id_turno)
            flash("Turno cancelado", "success")
        except TurnoError as e:
            flash(str(e), "error")
        return redirect(request.referrer or url_for("turnos"))

    return app