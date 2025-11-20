from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import Session
from typing import List, Optional
import models
import crud
from database import get_session, create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas al iniciar la aplicación
    create_db_and_tables()
    yield

app = FastAPI(
    title="API Concesionaria de Autos",
    description="API para gestionar la venta de autos en una concesionaria",
    version="1.0.0",
    lifespan=lifespan
)

# Endpoints para Autos
@app.post("/autos/", response_model=models.AutoResponse, tags=["Autos"])
def crear_auto(
    auto: models.AutoCreate, 
    session: Session = Depends(get_session)
):
    """Crear un nuevo auto en el inventario"""
    return crud.create_auto(session, auto)

@app.get("/autos/", response_model=List[models.AutoResponse], tags=["Autos"])
def listar_autos(
    skip: int = 0,
    limit: int = 100,
    marca: Optional[str] = Query(None, description="Filtrar por marca"),
    estado: Optional[models.EstadoAuto] = Query(None, description="Filtrar por estado"),
    tipo_combustible: Optional[models.TipoCombustible] = Query(None, description="Filtrar por tipo de combustible"),
    precio_min: Optional[float] = Query(None, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, description="Precio máximo"),
    session: Session = Depends(get_session)
):
    """Listar todos los autos con filtros opcionales"""
    return crud.get_autos(
        session, 
        skip=skip, 
        limit=limit,
        marca=marca,
        estado=estado,
        tipo_combustible=tipo_combustible,
        precio_min=precio_min,
        precio_max=precio_max
    )

@app.get("/autos/{auto_id}", response_model=models.AutoResponse, tags=["Autos"])
def obtener_auto(auto_id: int, session: Session = Depends(get_session)):
    """Obtener un auto específico por ID"""
    auto = crud.get_auto(session, auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@app.put("/autos/{auto_id}", response_model=models.AutoResponse, tags=["Autos"])
def actualizar_auto(
    auto_id: int, 
    auto_update: models.AutoUpdate, 
    session: Session = Depends(get_session)
):
    """Actualizar información de un auto"""
    auto = crud.update_auto(session, auto_id, auto_update)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@app.delete("/autos/{auto_id}", tags=["Autos"])
def eliminar_auto(auto_id: int, session: Session = Depends(get_session)):
    """Eliminar un auto del inventario"""
    success = crud.delete_auto(session, auto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return {"message": "Auto eliminado correctamente"}

# Endpoints para Ventas
@app.post("/autos/{auto_id}/vender", response_model=models.AutoResponse, tags=["Ventas"])
def vender_auto(
    auto_id: int,
    venta: models.VentaCreate,
    session: Session = Depends(get_session)
):
    """Marcar un auto como vendido"""
    venta.auto_id = auto_id
    auto = crud.vender_auto(session, venta)
    if not auto:
        raise HTTPException(
            status_code=400, 
            detail="Auto no encontrado o no disponible para venta"
        )
    return auto

# Endpoints para Estadísticas
@app.get("/estadisticas/", response_model=models.EstadisticasResponse, tags=["Estadísticas"])
def obtener_estadisticas(session: Session = Depends(get_session)):
    """Obtener estadísticas generales de la concesionaria"""
    return crud.get_estadisticas(session)

# Health Check
@app.get("/health", tags=["Sistema"])
def health_check():
    """Verificar el estado de la API"""
    return {"status": "healthy", "message": "API de Concesionaria funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)