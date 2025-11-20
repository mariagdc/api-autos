# API Concesionaria de Autos

API REST para gestionar una concesionaria de autos construida con FastAPI, SQLModel y PostgreSQL.

## Características

- ✅ CRUD completo para autos
- ✅ Gestión de ventas
- ✅ Filtros avanzados para búsqueda
- ✅ Estadísticas del inventario
- ✅ Validación de datos con Pydantic
- ✅ Documentación automática con Swagger UI

## Instalación

1. Clonar el repositorio
3. Instalar dependencias:
```bash
pip install -r requirements.txt
```
## Ejecutar la Aplicación

Asegúrate de tener el entorno virtual activado

# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate

Iniciar el servidor de desarrollo

uvicorn main:app --reload

O alternativamente:

python -m uvicorn main:app --reload

    La aplicación estará disponible en:
        API: http://localhost:8000
      
## Detener la Aplicación y Desactivar el Entorno

Para detener el servidor: Presiona Ctrl + C en la terminal

Para desactivar el entorno virtual:

deactivate



![Funcionando](image.png)
