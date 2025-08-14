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

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado en tu sistema:

- **Python 3.10 o superior** (recomendado Python 3.12+)
- **Git** para clonar el repositorio
- **pip** (gestor de paquetes de Python)

## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd sistema-gestion-academica
```

### 2. Crear Entorno Virtual

Es **altamente recomendado** crear un entorno virtual para evitar conflictos con otros proyectos:

```bash
# En Windows
python -m venv env
env\Scripts\activate

# En macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar Migraciones

```bash
python manage.py migrate
```

### 5. Crear Superusuario

```bash
python manage.py createsuperuser
```

### 6. Ejecutar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El proyecto estará disponible en: http://127.0.0.1:8000/

## 🛠️ Comandos Útiles

### Desarrollo
```bash
# Ejecutar servidor de desarrollo
python manage.py runserver
```

### Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations
```

### Shell de Django
```bash
# Abrir shell interactivo
python manage.py shell
```

## 📁 Estructura del Proyecto

```
sistema-gestion-academica/
├── core/                   # Configuración principal de Django
│   ├── __init__.py
│   ├── asgi.py           # Configuración ASGI
│   ├── settings.py       # Configuraciones del proyecto
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── env/                   # Entorno virtual (no incluido en git)
├── manage.py             # Script de administración de Django
├── requirements.txt       # Dependencias del proyecto
└── README.md             # Este archivo
```

## 🌐 Acceso a la Aplicación

- **URL principal**: http://127.0.0.1:8000/
- **Admin de Django**: http://127.0.0.1:8000/admin/ (requiere superusuario)

## 📝 Notas de Desarrollo

- El proyecto está configurado con `DEBUG=True` por defecto
- La clave secreta está hardcodeada en `settings.py` (cambiar en producción)
- Se recomienda usar variables de entorno para configuraciones sensibles

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'django'"
```bash
# Activa el entorno virtual
env\Scripts\activate  # Windows
source env/bin/activate  # macOS/Linux

# Reinstala las dependencias
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Usa otro puerto
python manage.py runserver 8080
```

### Error: "Database is locked"
```bash
# Detén el servidor y vuelve a ejecutar
# O elimina db.sqlite3 y ejecuta migrate
```

## 🤝 Contribución

1. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
2. Realiza tus cambios
3. Haz commit (`git commit -am 'Agregar nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request
