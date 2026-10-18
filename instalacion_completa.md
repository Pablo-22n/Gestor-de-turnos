# ⚡ Guía Rápida: Probar el sistema en tu PC (Windows desde Cero)

Esta guía está pensada para cualquier persona que quiera probar el sistema en su computadora con Windows, **sin necesidad de tener conocimientos previos de programación ni herramientas instaladas**. 

Al finalizar, vas a tener el sistema de turnos corriendo en tu navegador y vas a poder ver la base de datos en phpMyAdmin.

---

## 📋 Lo que vamos a instalar
1. **Python** (Para ejecutar el código).
2. **Visual Studio Code** (Para abrir y correr el proyecto).
3. **AppServ** (Para tener la base de datos y phpMyAdmin).
4. **El proyecto descargado** (El código de la aplicación).

---

## Paso 1: Instalar Python
1. Andá a la página oficial: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Hacé clic en el botón amarillo grande que dice **"Download Python 3.x.x"**.
3. Ejecutá el instalador que se descargó.
4. ⚠️ **MUY IMPORTANTE:** En la primera pantalla del instalador, **tildá la casilla de abajo que dice "Add python.exe to PATH"** (Agregar Python al PATH). Si no hacés esto, después va a dar error.
5. Hacé clic en **"Install Now"** y esperá a que termine. Cerrá la ventana.

---

## Paso 2: Instalar Visual Studio Code
1. Andá a: [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Hacé clic en el botón azul de **"Download for Windows"**.
3. Ejecutá el instalador. Aceptá los términos y dale "Siguiente" a todo (podés tildar la opción "Agregar al menú contextual" si querés).
4. Abrí Visual Studio Code cuando termine.

---

## Paso 3: Descargar el proyecto
Vamos a descargarlo como ZIP:
1. Andá a la página de GitHub del proyecto: [https://github.com/Pablo-22n/Gestor-de-turnos](https://github.com/Pablo-22n/Gestor-de-turnos)
2. Hacé clic en el botón verde que dice **"<> Code"** y elegí **"Download ZIP"**.
3. Se va a descargar un archivo `.zip` (por ejemplo, `Gestor-de-turnos-main.zip`).
4. Hacé clic derecho sobre el ZIP y elegí **"Extraer todo..."**. 
5. Guardá la carpeta extraída en un lugar fácil de encontrar, como el **Escritorio**.

---

## Paso 4: Instalar AppServ (Base de Datos + phpMyAdmin)
1. Descargá el instalador de **AppServ** desde su página oficial o un repositorio confiable (buscá "AppServ 8.6.0").
2. Ejecutá el instalador `.exe` con permisos de administrador.
3. Seguí los pasos:
   * **Ruta:** Dejá la que viene por defecto (`C:\AppServ`).
   * **Componentes:** Dejá tildados **Apache**, **MySQL**, **PHP** y **phpMyAdmin**.
   * **Configuración de Apache:** Dejá el puerto `80`. (Si te dice que está ocupado, poné `8080` y anotalo).
   * **Configuración de MySQL:** Te va a pedir una contraseña para el usuario `root`. **Anotá esa contraseña en un papel o en el bloc de notas**. Dejá el charset en `utf8mb4`.
4. Terminá la instalación.

---

## Paso 5: Crear la base de datos desde phpMyAdmin
1. Abrí tu navegador (Chrome, Edge, etc.) y entrá a: 👉 **`http://localhost/phpmyadmin`** (si en el paso anterior usaste el puerto 8080, entrá a `http://localhost:8080/phpmyadmin`).
2. Logueate con:
   * **Usuario:** `root`
   * **Contraseña:** la que pusiste en el Paso 4.
3. Hacé clic en la pestaña **"SQL"** arriba.
4. Copiá y pegá **TODO** este bloque y dale a **"Continuar"**:

```sql
CREATE DATABASE IF NOT EXISTS turnos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE turnos;

CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(30)
);

CREATE TABLE IF NOT EXISTS profesionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    profesional_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('pendiente','confirmado','atendido','cancelado','ausente') NOT NULL DEFAULT 'pendiente',
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id),
    FOREIGN KEY (profesional_id) REFERENCES profesionales(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    rol VARCHAR(20) NOT NULL DEFAULT 'recepcionista'
);

INSERT INTO usuarios (usuario, password_hash, rol) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');
```

---

## Paso 6: Abrir el proyecto y configurar la conexión
1. Abrí **Visual Studio Code**.
2. Andá a **Archivo > Abrir Carpeta** y seleccioná la carpeta del proyecto que extrajiste en el Escritorio (la que se llama `Gestor-de-turnos-main`).
3. En el panel de la izquierda, buscá y abrí el archivo llamado `config.py`.
4. Vas a ver un código. Tenés que cambiar la parte de la contraseña para que coincida con la que pusiste en el Paso 4. Debería quedar así:

```python
import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "TU_CONTRASEÑA_DE_APPSERV"), # <-- Cambiá esto por tu contraseña
    "database": os.getenv("DB_NAME", "turnos"),
    "charset": "utf8mb4",
}
```
5. Guardá el archivo presionando las teclas **Ctrl + S**.

---

## Paso 7: Instalar las dependencias y ejecutar
1. En Visual Studio Code, abrí la terminal integrada yendo al menú superior: **Terminal > Nueva Terminal**.
2. Se va a abrir una consola abajo. Escribí el siguiente comando y presioná **Enter**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Esperá a que descargue e instale unas cosas. Puede tardar un minuto).*
3. Una vez que termine, escribí este otro comando y presioná **Enter**:
   ```bash
   python main.py
   ```
4. Si todo salió bien, vas a ver un mensaje al final de la consola que dice algo como: `* Running on http://127.0.0.1:5000`.

---

## Paso 8: ¡Entrar al sistema!
1. Abrí tu navegador de siempre (Chrome, Edge, Firefox).
2. En la barra de direcciones, escribí: 👉 **`http://127.0.0.1:5000`**
3. ¡Listo! Vas a ver la pantalla de Login. Entrá usando estas credenciales:
   * **Usuario:** `admin`
   * **Contraseña:** `admin123`
