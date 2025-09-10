 DocsFlow API

Sistema de gestión de documentos operativos con FastAPI + MySQL.

 Instalación

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements.txt

# correr el proyecto
uvicorn app.main:app --reload

# Registro de usuarios 
el primer usuario se creara admi por defecto 
expira en 30 minutos 

