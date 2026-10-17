# Guía de Despliegue - Sistema de Gestión de Turnos

## FASE 1: Configuración de la Máquina Virtual (Linux)

### 1. Prender la VM y verificar la IP
Abrir la terminal en la VM y ejecutar:
```bash
hostname -I
```
Anotar la IP (ej: `192.168.1.84`). Si no es fija, configurarla como IP estática.

### 2. Instalar Apache, MariaDB y PHP (para phpMyAdmin)
```bash
sudo apt update
sudo apt install apache2 mariadb-server php php-mysql libapache2-mod-php -y
```

### 3. Instalar phpMyAdmin (opcional pero recomendado)
```bash
sudo apt install phpmyadmin -y
```
*(Durante la instalación, elegir `apache2` con la barra espaciadora y aceptar).*

### 4. Instalar Python y herramientas
```bash
sudo apt install python3 python3-pip -y
```

### 5. Permitir conexiones externas en MariaDB
Editar el archivo de configuración:
```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
Buscar `bind-address = 127.0.0.1` y cambiarlo a:
```text
bind-address = 0.0.0.0
```
Guardar (`Ctrl+O`, `Enter`, `Ctrl+X`) y reiniciar:
```bash
sudo systemctl restart mariadb
```

---

## FASE 2: Crear la Base de Datos

### 1. Entrar a la consola de MariaDB en la VM
```bash
sudo mariadb
```

### 2. Ejecutar los siguientes comandos SQL
*(Crear base, usuario y tablas):*
```sql
CREATE DATABASE IF NOT EXISTS turnos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'turnos_admin'@'%' IDENTIFIED BY 'Turnos2026!';
GRANT ALL PRIVILEGES ON turnos.* TO 'turnos_admin'@'%';
FLUSH PRIVILEGES;

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

-- Usuario admin por defecto (Usuario: admin / Contraseña: admin123)
INSERT INTO usuarios (usuario, password_hash, rol) 
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin');

EXIT;
```

---

## FASE 3: Configurar el Proyecto en Windows

### 1. Instalar Git y Python
Descargar e instalar desde [git-scm.com](https://git-scm.com) y [python.org](https://python.org).

### 2. Clonar el repositorio
Abrir CMD o PowerShell en Windows, ir a la carpeta donde quieran el proyecto y ejecutar:
```bash
git clone https://github.com
cd Gestor-de-turnos
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la conexión a la base de datos
Abrir el archivo `config.py` y modificar la IP de la VM y la contraseña:
```python
DB_CONFIG = {
    "host": "192.168.1.84",  # <-- CAMBIAR POR LA IP DE LA VM
    "port": 3306,
    "user": "turnos_admin",
    "password": "Turnos2026!", # <-- CAMBIAR POR LA CONTRASEÑA ELEGIDA
    "database": "turnos",
    "charset": "utf8mb4",
}
```

---

## FASE 4: Probar en Windows (Opcional)

Para probar que todo funciona antes de subirlo al servidor web:
```bash
python main.py
```
Abrir el navegador en `http://127.0.0.1:5000` y loguearse con `admin` / `admin123`.

---

## FASE 5: Desplegar en el Servidor Web (Apache) en la VM

### 1. Instalar el módulo de Python para Apache
En la VM:
```bash
sudo apt install libapache2-mod-wsgi-py3 -y
sudo a2enmod wsgi
sudo systemctl restart apache2
```

### 2. Crear la carpeta del proyecto en la VM
```bash
sudo mkdir -p /var/www/turnos
sudo chown -R $USER:$USER /var/www/turnos
```

### 3. Copiar el proyecto desde Windows a la VM
Desde la terminal de Windows (estando en la carpeta del proyecto clonado):
```bash
scp -r * usuario_vm@192.168.1.84:/var/www/turnos/
```
*(Reemplazar `usuario_vm` por el nombre de usuario de la máquina virtual).*

### 4. Instalar las librerías de Python en la VM (Global)
```bash
sudo pip3 install flask mysql-connector-python --break-system-packages
```

### 5. Ajustar la conexión en la VM
Como el servidor web y la base de datos están en la misma máquina, cambiar el host:
```bash
nano /var/www/turnos/config.py
```
Cambiar `"host": "192.168.1.31"` por `"host": "localhost"`.

### 6. Crear el archivo de conexión WSGI
```bash
nano /var/www/turnos/turnos.wsgi
```
Pegar esto:
```python
import sys
import os
sys.path.insert(0, "/var/www/turnos")
os.chdir("/var/www/turnos")
from presentacion.web.app import create_app
application = create_app()
```

### 7. Configurar Apache
```bash
sudo nano /etc/apache2/sites-available/turnos.conf
```
Pegar esto:
```apache
<VirtualHost *:80>
    ServerName 192.168.1.31
    WSGIScriptAlias /turnos /var/www/turnos/turnos.wsgi
    <Directory /var/www/turnos>
        Require all granted
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/turnos-error.log
    CustomLog ${APACHE_LOG_DIR}/turnos-access.log combined
</VirtualHost>
```

### 8. Habilitar el sitio y reiniciar
```bash
sudo a2ensite turnos.conf
sudo systemctl restart apache2
```

### 9. Permisos finales (por si Apache no puede leer los archivos)
```bash
sudo chown -R www-data:www-data /var/www/turnos
```

---

## Listo para usar!

Abrir el navegador en Windows y entrar a:
👉 `192.168.1.84/turnos`

* **Usuario:** admin
* **Contraseña:** admin123


# 🛠️ Solución de Problemas Frecuentes

* **Error 500 en Apache:** Revisar el log con `sudo tail -20 /var/log/apache2/turnos-error.log`.
* **Error "Can't connect to MySQL":** Verificar que MariaDB esté corriendo en la VM y que la IP en `config.py` sea la correcta.
* **Cambios no se reflejan:** Reiniciar Apache con `sudo systemctl restart apache2`.