🛠️ Gestor de Tareas Colaborativo con Interfaz Web
Este proyecto es una aplicación interactiva desarrollada en Python con Flask, que permite a múltiples usuarios registrarse, iniciar sesión y gestionar tareas y proyectos de forma colaborativa a través de una interfaz web amigable.

🌐 Características
Registro de usuarios

Inicio de sesión seguro

Gestión de sesiones con Flask

Creación de tareas personales

Visualización de tareas por usuario

Creación y gestión de proyectos (versión consola o vía API)

Asignación de tareas a proyectos

Visualización de progreso por proyecto

Autenticación por tokens (para uso de API/CLI)

🧰 Tecnologías utilizadas
Python 3.x

Flask

Flask-Session

Flask-Bcrypt

HTML básico (para formularios web)

requests (para la parte cliente por consola)

API REST (para acceso desde otras herramientas)

🗂️ Estructura del Proyecto

/gestor-tareas/
│
├── main.py                 # Interfaz web Flask (inicio, registro, tareas)
├── api.py                  # API REST para uso desde consola o apps externas
├── proyectos.py            # Clase GestorProyectos y lógica de backend
├── templates/
│   ├── login.html
│   ├── register.html
│   └── tareas.html
├── static/                 # (opcional) CSS o imágenes
├── requirements.txt        # Librerías necesarias
└── README.md               # Este archivo

🚀 Instalación y ejecución
1. Clona el repositorio

git clone https://github.com/tu_usuario/gestor-tareas.git
cd gestor-tareas

2. Crea un entorno virtual (opcional pero recomendado)

python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate     # En Windows

3. Instala las dependencias

pip install -r requirements.txt

4. Ejecuta la app web

python main.py
La aplicación estará disponible en: http://127.0.0.1:5000

🧪 Uso desde consola (modo CLI)
También puedes interactuar con la API mediante el cliente por consola:

python consola.py
Desde allí puedes:

Registrar e iniciar sesión

Crear y ver tareas

Crear y gestionar proyectos

Ver progreso

🔐 Seguridad
Contraseñas cifradas con Bcrypt

Manejo de sesiones con cookies seguras

Tokens de acceso para la API

📌 Mejoras futuras
Panel de administración

Interfaz web para proyectos y asignación de tareas

Integración con bases de datos (SQLite, PostgreSQL)

Notificaciones o recordatorios por correo

Permisos de usuario por rol (admin, colaborador)

👨‍💻 Autor
Desarrollado por:

Jose David Samaniego Guerrero(Coordinador) 

José Javier Soler Martínez 

Mario Melero Morant 

Rodrigo Jover Bernabeu 

Darío Sainz Bear.









