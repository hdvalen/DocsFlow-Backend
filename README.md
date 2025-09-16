# DocsFlow Backend - Sistema de Gestión de Documentos Operativos

## 📋 Descripción
Backend del sistema DocsFlow desarrollado con Python FastAPI para la gestión de documentos operativos empresariales. Permite subir, procesar y almacenar archivos PDF con extracción automática de datos estructurados.

## 🛠️ Tecnologías
- **Python 3.8+**
- **FastAPI** - Framework web para APIs
- **MySQL** - Base de datos (consultas manuales, sin ORM)
- **JWT** - Autenticación y autorización
- **pdfplumber** - Extracción de datos de PDFs
- **FastMail** - Envío de correos electrónicos
- **Uvicorn** - Servidor ASGI

## 🚀 Instalación y Configuración


### 1. Clonar el repositorio
```bash
git clone https://github.com/hdvalen/DocsFlow-Backend.git
cd DocsFlow-Backend
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=DocsFlow

# JWT
SECRET_KEY=tu_clave_secreta_muy_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_contraseña_de_app
```

### 5. Configurar base de datos
```bash
# Ejecutar script de creación de tablas
python scripts/create_database.py
```

### 6. Ejecutar el servidor
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔐 Autenticación y Seguridad

### Roles de Usuario
- **Admin**: Acceso completo a todos los documentos y gestión de usuarios
- **Operator**: Solo puede ver y subir documentos de su departamento

### Seguridad Implementada
- JWT con expiración de 30 minutos
- Bloqueo por 5 intentos fallidos (solo operadores)
- Tokens únicos para recuperación de contraseña

## 📡 Endpoints de la API

### 🔓 Endpoints Públicos
```
POST /auth/login
POST /auth/forgot-password
POST /auth/reset-password
```

### 🔐 Endpoints Privados (requieren token)
```
GET /users/me
GET /users/ (solo admin)
POST /documents/upload
GET /documents/
GET /documents/{id}
GET /tables/{document_id}
GET /tables/search?q={query}
DELETE /documents/{id}
```

## 📝 Variables de Entorno Requeridas
| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| DB_HOST | Host de MySQL | localhost |
| DB_PORT | Puerto de MySQL | 3306 |
| DB_USER | Usuario de BD | root |
| DB_PASSWORD | Contraseña de BD | password |
| DB_NAME | Nombre de BD | docsflow |
| SECRET_KEY | Clave para JWT | mi_clave_super_secreta |
| EMAIL_USER | Email para notificaciones | admin@empresa.com |
| EMAIL_PASSWORD | Contraseña del email | password123 |
