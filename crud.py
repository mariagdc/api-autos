from sqlmodel import Session, select, func
from typing import List, Optional
from models import Auto, AutoCreate, AutoUpdate, EstadoAuto, VentaCreate, VentaResponse
from datetime import datetime

# CRUD para Autos
def create_auto(session: Session, auto: AutoCreate) -> Auto:
    db_auto = Auto(**auto.dict())
    session.add(db_auto)
    session.commit()
    session.refresh(db_auto)
    return db_auto

def get_auto(session: Session, auto_id: int) -> Optional[Auto]:
    return session.get(Auto, auto_id)

def get_autos(
    session: Session, 
    skip: int = 0, 
    limit: int = 100,
    marca: Optional[str] = None,
    estado: Optional[EstadoAuto] = None,
    tipo_combustible: Optional[str] = None,
    precio_min: Optional[float] = None,
    precio_max: Optional[float] = None
) -> List[Auto]:
    
    statement = select(Auto)
    
    if marca:
        statement = statement.where(Auto.marca.ilike(f"%{marca}%"))
    if estado:
        statement = statement.where(Auto.estado == estado)
    if tipo_combustible:
        statement = statement.where(Auto.tipo_combustible == tipo_combustible)
    if precio_min is not None:
        statement = statement.where(Auto.precio >= precio_min)
    if precio_max is not None:
        statement = statement.where(Auto.precio <= precio_max)
    
    statement = statement.offset(skip).limit(limit)
    results = session.exec(statement)
    return results.all()

def update_auto(session: Session, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
    db_auto = session.get(Auto, auto_id)
    if db_auto:
        update_data = auto_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_auto, field, value)
        session.add(db_auto)
        session.commit()
        session.refresh(db_auto)
    return db_auto

def delete_auto(session: Session, auto_id: int) -> bool:
    auto = session.get(Auto, auto_id)
    if auto:
        session.delete(auto)
        session.commit()
        return True
    return False

# Funciones para ventas
def vender_auto(session: Session, venta: VentaCreate) -> Optional[Auto]:
    auto = session.get(Auto, venta.auto_id)
    if auto and auto.estado == EstadoAuto.DISPONIBLE:
        auto.estado = EstadoAuto.VENDIDO
        session.add(auto)
        session.commit()
        session.refresh(auto)
        return auto
    return None

# Funciones para estadísticas
def get_estadisticas(session: Session) -> dict:
    # Total de autos
    total_autos = session.exec(select(func.count(Auto.id))).first()
    
    # Autos por estado
    autos_disponibles = session.exec(
        select(func.count(Auto.id)).where(Auto.estado == EstadoAuto.DISPONIBLE)
    ).first()
    
    autos_vendidos = session.exec(
        select(func.count(Auto.id)).where(Auto.estado == EstadoAuto.VENDIDO)
    ).first()
    
    # Valor del inventario (solo autos disponibles)
    valor_inventario = session.exec(
        select(func.sum(Auto.precio)).where(Auto.estado == EstadoAuto.DISPONIBLE)
    ).first() or 0
    
    # Marca más popular (más autos en inventario)
    marca_popular = session.exec(
        select(Auto.marca, func.count(Auto.id))
        .group_by(Auto.marca)
        .order_by(func.count(Auto.id).desc())
        .limit(1)
    ).first()
    
    return {
        "total_autos": total_autos,
        "autos_disponibles": autos_disponibles,
        "autos_vendidos": autos_vendidos,
        "valor_inventario": valor_inventario,
        "marca_mas_popular": marca_popular[0] if marca_popular else "N/A"
    }