# API Concesionaria de Autos

API REST para gestionar una concesionaria de autos construida con FastAPI, SQLModel y PostgreSQL.

## Características

- ✅ CRUD completo para autos
- ✅ Gestión de ventas
- ✅ Filtros avanzados para búsqueda
- ✅ Estadísticas del inventario
- ✅ Validación de datos con Pydantic


## Instalación

1. Clonar el repositorio
2. Configurar base de datos
# PostgreSQL (recomendado)
DATABASE_URL=postgresql://usuario:password@localhost/concesionaria

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


## Api en funcionamiento ##
## ![Funcionando](image.png)
```
 Autos (/autos)
Método	Endpoint	Descripción
POST	/autos	Crear nuevo auto
GET	/autos	Listar autos (con filtros)
GET	/autos/{id}	Obtener auto por ID
PUT	/autos/{id}	Actualizar auto
DELETE	/autos/{id}	Eliminar auto
GET	/autos/chasis/{chasis}	Buscar por número de chasis
GET	/autos/{id}/with-ventas	Auto con historial de ventas
```
Health check
curl http://localhost:8000/health

# Verificar estructura de datos
curl http://localhost:8000/autos/

👥 Responsables del Proyecto

Estudiante: [Maria Florencia Godoy Del Castillo]
Materia: Programación IV
Carrera: Tecnicatura Universitaria en Programación
Universidad: Universidad Tecnológica Nacional
Año: 2025
📄 Licencia

Este proyecto fue desarrollado con fines educativos para la Universidad Tecnológica Nacional.
🚀 Próximos Pasos

Para comenzar a usar la API:

    Configurar la base de datos en database.py

    Ejecutar la aplicación con uvicorn main:app --reload

    Explorar la documentación en http://localhost:8000/docs

    Probar los endpoints con Postman o curl

¡La API está lista para producción! 🎉
