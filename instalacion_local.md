# ⚡ Guía Rápida: Probar el sistema en tu PC (Windows)

Esta guía te explica paso a paso cómo descargar el proyecto, configurar la base de datos local con **XAMPP** (la herramienta más usada para desarrollo local), y ejecutar la aplicación web desde Visual Studio Code.

> **¿Por qué usamos XAMPP y no solo `pip install`?**
> `pip install` solo instala librerías de Python. Para tener una base de datos y ver las tablas en una interfaz web como `localhost/phpmyadmin`, necesitás un **servidor web** (Apache) y un **motor de base de datos** (MySQL/MariaDB) corriendo en tu PC. **XAMPP** es el estándar de la industria para principiantes porque instala todo esto (Apache, PHP, MySQL y phpMyAdmin) en un solo instalador, sin necesidad de configurar nada a mano.

---

## 📋 Requisitos previos
1. **Python 3.8+** (Descargalo de [python.org](https://www.python.org/) y **tildá la casilla "Add Python to PATH"** durante la instalación).
2. **Visual Studio Code** (o tu editor de código preferido).
3. **Git** (opcional, para clonar el repo).

---

## Paso 1: Descargar el proyecto
Abrí una terminal (CMD o PowerShell), andá a la carpeta donde quieras guardar el proyecto y ejecutá:
```bash
git clone https://github.com/Pablo-22n/Gestor-de-turnos.git
cd Gestor-de-turnos
```
*(Si no tenés Git, descargá el ZIP desde GitHub, descomprimilo y abrí esa carpeta en VS Code).*

---

## Paso 2: Instalar XAMPP (Base de datos + phpMyAdmin)
1. Descargá XAMPP desde su página oficial: https://www.apachefriends.org/es/index.html.
2. Ejecutá el instalador y seguí los pasos por defecto (dejá tildados Apache, MySQL, PHP y phpMyAdmin).
3. Abrí el Panel de Control de XAMPP desde el menú de inicio de Windows.
4. Hacé clic en "Start" en los módulos Apache y MySQL (los indicadores deben ponerse en verde).

> **Nota:** Si Apache no inicia, es probable que otro programa esté usando el puerto 80 (como Skype). Solución: cerrá ese programa o cambiá el puerto de Apache en XAMPP a 8080.

Abrí tu navegador y entrá a: 👉 http://localhost/phpmyadmin

* **Usuario:** root
* **Contraseña:** (dejar vacío)

---

## Paso 3: Crear la base de datos desde phpMyAdmin
En la página de phpMyAdmin, hacé clic en la pestaña "SQL" en la parte superior.

Copiá y pegá todo el siguiente bloque de comandos y hacé clic en el botón "Continuar" (o "Go") en la parte inferior derecha:

```sql
CREATE DATABASE IF NOT EXISTS turnos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE turnos;

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(30)
);

CREATE TABLE profesionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100)
);

CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    profesional_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('pendiente','confirmado','atendido','cancelado','ausente') NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id),
    INDEX ix_turnos_prof_fecha (profesional_id, fecha)
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'recepcionista'
);

-- Crea el usuario admin por defecto (Usuario: admin / Contraseña: admin123)
INSERT INTO usuarios (usuario, password_hash, rol) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');
```

---

## Paso 4: Abrir el proyecto en Visual Studio Code
1. Abrí VS Code.
2. Andá a Archivo > Abrir Carpeta y seleccioná la carpeta del proyecto (Gestor-de-turnos).
3. Abrí la terminal integrada de VS Code (Terminal > Nueva Terminal).

---

## Paso 5: Instalar las dependencias de Python
En la terminal de VS Code, ejecutá el siguiente comando para instalar Flask y el conector de MySQL:
```bash
pip install -r requirements.txt
```

---

## Paso 6: Configurar la conexión en config.py
En VS Code, abrí el archivo `config.py` y verificá que los datos de conexión coincidan con XAMPP:
```python
DB_CONFIG = {
    "host": "localhost",      # XAMPP corre en tu propia PC
    "port": 3306,             # Puerto por defecto de MySQL
    "user": "root",           # Usuario por defecto de XAMPP
    "password": "",           # XAMPP no tiene contraseña por defecto
    "database": "turnos",     # La base que creamos en el Paso 3
    "charset": "utf8mb4",
}
```

---

## Paso 7: ¡Ejecutar el sistema!
En la terminal de VS Code, ejecutá:
```bash
python main.py
```

Abrí tu navegador en:
👉 `http://127.0.0.1:5000`

* **Usuario:** admin
* **Contraseña:** admin123

⚠️ **Importante:** Para detener el servidor de la web cuando termines de probar, volvé a la terminal de VS Code y presioná `Ctrl + C`.


## 🛠️ Solución de problemas frecuentes

* **"python no se reconoce como un comando...":** No instalaste Python o no tildaste la casilla "Add Python to PATH". Reinstalalo marcando esa casilla.

* **Apache no inicia en XAMPP:** Otro programa está usando el puerto 80 (Skype, IIS). Cerrá ese programa o cambiá el puerto de Apache a 8080 en la configuración de XAMPP.

* **"Access denied for user 'root'@'localhost'":** Asegurate de que en config.py la contraseña esté vacía ("") y que XAMPP esté corriendo.

* **"Can't connect to MySQL server":** El servicio de MySQL en XAMPP no está iniciado. Hacé clic en "Start" en el panel de control.

* **La web da error 500:** Revisá que hayas pegado el script SQL completo en phpMyAdmin sin errores.
