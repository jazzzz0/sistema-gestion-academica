# Sistema de Gestión Académica
Trabajo final de la materia Desarrollo de Sistemas Web. 
Un sistema web desarrollado en Django para la gestión académica de instituciones educativas.

### Integrantes:
- Galeano, Jorgelina
- Godina, Lucas
- Luján, Rocío
- Maez, Jazmín
- Morais, Yamila
- Sarmiento, Camila

## 🔐 Usuarios y Permisos

El sistema cuenta con diferentes roles de usuario:

- **Superusuario:** Acceso completo al sistema y panel de administración
- **Administrador:** Gestión de estudiantes, profesores, carreras y materias
- **Profesor:** Visualización de estudiantes y materias asignadas
- **Estudiante:** Visualización e inscripción a materias que corresponden a su carrera


## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- **Python 3.10 o superior** (recomendado Python 3.12)
  - Puedes verificar tu versión ejecutando: `python --version`
  - Descargar desde: https://www.python.org/downloads/
- **Git** para clonar el repositorio
  - Descargar desde: https://git-scm.com/downloads
- **pip** (gestor de paquetes de Python, viene incluido con Python)

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

Abre tu terminal (PowerShell, CMD o Git Bash) y ejecuta:

```bash
git clone https://github.com/jazzzz0/sistema-gestion-academica.git
cd sistema-gestion-academica
```

Si ya tienes el proyecto descargado, simplemente navega a la carpeta:

```bash
cd C:\Repos\sistema-gestion-academica
```

### 2. Crear y Activar un Entorno Virtual

Es **altamente recomendado** crear un entorno virtual para aislar las dependencias del proyecto:

#### En Windows (PowerShell/CMD):
```powershell
python -m venv env
env\Scripts\activate
```

#### En macOS/Linux:
```bash
python3 -m venv env
source env/bin/activate
```

> **Nota:** Una vez activado, deberías ver `(env)` al inicio de tu línea de comandos.

### 3. Instalar Dependencias

Con el entorno virtual activado, instala todas las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

Este comando instalará:
- Django 5.2.5
- django-extensions
- django-schema-graph
- Y otras dependencias necesarias

### 4. Configurar la Base de Datos

Ejecuta las migraciones para crear la estructura de la base de datos SQLite:

```bash
python manage.py migrate
```

Este comando creará el archivo `db.sqlite3` con todas las tablas necesarias.

### 5. Crear un Superusuario (Administrador)

Para acceder al panel de administración de Django, necesitas crear un superusuario:

```bash
python manage.py createsuperuser
```

Se te pedirá que ingreses:
- **Email**
- **Password** (contraseña, no se mostrará mientras escribes)
- **Password confirmation** (confirmar contraseña)

> **Ejemplo:**
> ```
> Email: admin@example.com
> Password: ********
> Password (again): ********
> ```

### 6. Ejecutar el Servidor de Desarrollo

Inicia el servidor local de Django:

```bash
python manage.py runserver
```

Deberías ver un mensaje similar a:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### 7. Acceder a la Aplicación

Abre tu navegador web y visita:

- **Página principal:** http://127.0.0.1:8000/
- **Panel de administración:** http://127.0.0.1:8000/admin/

Para acceder al panel de administración, usa las credenciales del superusuario que creaste en el paso 5.

## 🛠️ Comandos Útiles

### Gestión del Servidor

```bash
# Iniciar el servidor de desarrollo
python manage.py runserver

# Iniciar en un puerto diferente
python manage.py runserver 8080

# Detener el servidor
# Presiona Ctrl+C en la terminal
```

### Gestión de la Base de Datos

```bash
# Crear nuevas migraciones después de cambios en los modelos
python manage.py makemigrations

# Aplicar migraciones pendientes
python manage.py migrate

# Ver el estado de las migraciones
python manage.py showmigrations

# Resetear la base de datos (¡CUIDADO! Elimina todos los datos)
# En Windows PowerShell:
Remove-Item db.sqlite3
python manage.py migrate
```

### Shell Interactivo de Django

```bash
# Abrir shell interactivo de Python con Django cargado
python manage.py shell

# Ejemplo de uso en el shell:
>>> from users.models import User
>>> User.objects.all()
>>> exit()
```

### Otros Comandos Útiles

```bash
# Ver todas las opciones de manage.py
python manage.py help

# Ejecutar tests
python manage.py test

# Recolectar archivos estáticos (para producción)
python manage.py collectstatic
```

## 🔧 Solución de Problemas Comunes

### Error: "python no se reconoce como un comando"

**Solución:** Asegúrate de que Python esté instalado y agregado al PATH del sistema.
- En Windows, reinstala Python marcando la opción "Add Python to PATH"
- O agrega manualmente Python al PATH del sistema

### Error: "No module named 'django'"

**Solución:** Asegúrate de tener el entorno virtual activado y las dependencias instaladas:
```bash
env\Scripts\activate  # En Windows
pip install -r requirements.txt
```

### Error: "Access is denied" al activar el entorno virtual en Windows

**Solución:** Si estás usando PowerShell, puede que necesites cambiar la política de ejecución:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Luego intenta activar el entorno virtual nuevamente.

### El servidor no inicia o muestra errores

**Solución:** Verifica que:
1. El entorno virtual esté activado
2. Las dependencias estén instaladas
3. Las migraciones estén aplicadas
4. El puerto 8000 no esté siendo usado por otro programa

### Error: "That port is already in use"

**Solución:** Cambia el puerto del servidor:
```bash
python manage.py runserver 8080
```