from sqlmodel import SQLModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class EstadoAuto(str, Enum):
    DISPONIBLE = "disponible"
    VENDIDO = "vendido"
    RESERVADO = "reservado"
    MANTENIMIENTO = "mantenimiento"

class TipoCombustible(str, Enum):
    GASOLINA = "gasolina"
    DIESEL = "diesel"
    ELECTRICO = "electrico"
    HIBRIDO = "hibrido"

class Auto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    marca: str = Field(index=True)
    modelo: str = Field(index=True)
    año: int = Field(gt=1900, lt=2030)
    precio: float = Field(gt=0)
    kilometraje: float = Field(ge=0)
    color: str
    tipo_combustible: TipoCombustible
    estado: EstadoAuto = Field(default=EstadoAuto.DISPONIBLE)
    fecha_ingreso: datetime = Field(default_factory=datetime.utcnow)
    descripcion: Optional[str] = Field(default=None)
    imagen_url: Optional[str] = Field(default=None)

class AutoCreate(BaseModel):
    marca: str
    modelo: str
    año: int
    precio: float
    kilometraje: float
    color: str
    tipo_combustible: TipoCombustible
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

class AutoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    año: Optional[int] = None
    precio: Optional[float] = None
    kilometraje: Optional[float] = None
    color: Optional[str] = None
    tipo_combustible: Optional[TipoCombustible] = None
    estado: Optional[EstadoAuto] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

class AutoResponse(BaseModel):
    id: int
    marca: str
    modelo: str
    año: int
    precio: float
    kilometraje: float
    color: str
    tipo_combustible: TipoCombustible
    estado: EstadoAuto
    fecha_ingreso: datetime
    descripcion: Optional[str]
    imagen_url: Optional[str]

class VentaCreate(BaseModel):
    auto_id: int
    cliente_nombre: str
    cliente_email: str
    cliente_telefono: str
    precio_venta: float
    fecha_venta: datetime = Field(default_factory=datetime.utcnow)

class VentaResponse(BaseModel):
    id: int
    auto_id: int
    cliente_nombre: str
    cliente_email: str
    cliente_telefono: str
    precio_venta: float
    fecha_venta: datetime

class EstadisticasResponse(BaseModel):
    total_autos: int
    autos_disponibles: int
    autos_vendidos: int
    valor_inventario: float
    ingresos_totales: float
    marca_mas_popular: str