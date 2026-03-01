from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Annotated
from decimal import Decimal
from datetime import datetime

from app.database import delete_consulta, fetch_all_consultas, fetch_consulta_by_id, insert_consulta, update_consulta


app = FastAPI(
    title="ConsultasMedicas API Ing María Chaparro Caballero",
    version="1.0.0",
    description="API REST desacoplada para gestión de consultas médicas por María Chaparro Caballero - 2 DAW"
)


# ========================
# Modelos Pydantic
# ========================

class ConsultaBase(BaseModel):
    """Modelo base con validaciones compartidas para Consulta."""
    paciente_nombre: Annotated[str, Field(min_length=1, max_length=100)]
    paciente_dni: Annotated[str, Field(min_length=1, max_length=20)]
    medico_nombre: Annotated[str, Field(min_length=1, max_length=100)]
    fecha_consulta: datetime = Field(description="Fecha de la cita")
    motivo_consulta: Optional[Annotated[str, Field(max_length=255)]]
    diagnostico: Optional[Annotated[str, Field(max_length=255)]]
    estado: Annotated[str, Field(min_length=1, max_length=100)]
    coste: float = Field(ge=0)
    fecha_creacion: datetime = Field(default_factory=datetime.now)

    @field_validator('paciente_nombre', 'medico_nombre','paciente_dni', 'motivo_consulta', 'diagnostico', 'estado')
    @classmethod
    def validar_nombre_medico(cls, v: str) -> str:
        """Valida nombre y categoría."""
        if not v or not v.strip():
            raise ValueError('El campo no puede estar vacío')
        return v.strip()

# Validador para Datetime
    @field_validator('fecha_consulta', 'fecha_creacion')
    @classmethod
    def validar_fechas(cls, v: datetime) -> datetime:
        if v is None:
            raise ValueError('La fecha no puede estar vacía')
        # Aquí v ya es un objeto datetime, no un string
        return v
    
    @field_validator('coste')
    @classmethod
    def validar_coste(cls, v: float) -> float:
        """Valida que el coste sea un número válido y no negativo."""
        if v is None:
            raise ValueError('El coste no puede estar vacío')
        
        # Aunque Field(ge=0) ya lo hace, el validador refuerza la lógica
        if v < 0:
            raise ValueError('El coste no puede ser un valor negativo')
            
        return v

class ConsultaDB(BaseModel):
    """Modelo para lectura desde BD (sin validaciones estrictas para datos históricos)."""
    id: int
    paciente_nombre: str
    paciente_dni: str
    medico_nombre: str
    fecha_consulta: datetime
    motivo_consulta: str
    diagnostico: str
    estado: str
    coste: float
    fecha_creacion: datetime


class ConsultaCreate(ConsultaBase):
    """Modelo para crear nueva consulta (sin ID)."""
    pass


class ConsultaUpdate(ConsultaBase):
    """Modelo para actualizar consulta (sin ID)."""
    pass


class Consulta(ConsultaBase):
    """Modelo completo de Consulta (con ID y validaciones)."""
    id: int


# ========================
# Funciones Helper
# ========================

def map_rows_to_consultas(rows: List[dict]) -> List[ConsultaDB]:
    """
    Convierte las filas del SELECT * FROM consulta (dict) 
    en objetos ConsultaDB. Maneja conversión de tipos incompatibles
    como Decimal → float.
    """
    consultas_db = []
    for row in rows:
        # Preparar datos para ConsultaDB
        consulta_data = dict(row)
        
        # Convertir Decimal a float si es necesario
        if isinstance(consulta_data.get("coste"), Decimal):
            consulta_data["coste"] = float(consulta_data["coste"])
        
              
        # Crear objeto ConsultaDB desempacando el diccionario
        consulta = ConsultaDB(**consulta_data)
        consultas_db.append(consulta)

    return consultas_db

# ========================
# Endpoints
# ========================
@app.get("/")
def root():
    """Ruta raíz - Bienvenida a la API."""
    return {
        "message": "Bienvenido a ConsultasApp API by María Chaparro Caballero - 2 DAW",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/ping")
def ping():
    """Endpoint de prueba."""
    return {"message": "pong"}

@app.get("/consultas", response_model=List[Consulta])
def listar_consultas():
    """
    Devuelve la lista de todos los productos desde la base de datos.
    
    - Obtiene datos raw de MySQL
    - Mapea a ConsultaDB (convierte tipos incompatibles)
    - Valida estructura con Pydantic
    - Retorna lista de Consultas
    """
    # 1. Obtener datos desde MySQL
    rows = fetch_all_consultas()

    # 2. Mapear a ConsultaDB (conversión de tipos)
    consultas_db = map_rows_to_consultas(rows)

    # 3. Retornar como Consulta (con validación de Pydantic)
    return consultas_db

@app.get("/consulta/{consulta_id}", response_model=Consulta)
def obtener_consulta(consulta_id: int):
    """
    Devuelve una consulta específica por su ID.
    
    - Obtiene datos raw de MySQL
    - Mapea a ConsultaDB (convierte tipos incompatibles)
    - Valida estructura con Pydantic
    - Retorna la Consulta o lanza HTTPException 404 si no existe
    """
    # 1. Obtener datos desde MySQL
    row = fetch_consulta_by_id(consulta_id)
    
    # 2. Validar que el producto existe
    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"Consulta con ID {consulta_id} no encontrada"
        )
    
    # 3. Mapear a ConsultaDB (conversión de tipos)
    consultas_db = map_rows_to_consultas([row])
    
    # 4. Retornar el primer (y único) elemento
    return consultas_db[0]


@app.post("/consultas", response_model=Consulta, status_code=201)
def crear_consulta(consulta: ConsultaCreate):
    """
    Crea una nueva consulta en la base de datos.
    
    - Valida datos con Pydantic (ConsultaCreate)
    - Inserta en MySQL
    - Retorna la consulta creada con ID asignado
    """
    # 1. Insertar la consulta en MySQL (retorna ID)
    nuevo_id = insert_consulta(
        paciente_nombre=consulta.paciente_nombre,
        paciente_dni=consulta.paciente_dni,
        medico_nombre=consulta.medico_nombre,
        fecha_consulta=consulta.fecha_consulta,
        motivo_consulta=consulta.motivo_consulta,
        diagnostico=consulta.diagnostico,
        estado=consulta.estado,
        coste=consulta.coste,
        fecha_creacion=consulta.fecha_creacion
    )
    
    # 2. Validar que la inserción fue exitosa
    if not nuevo_id or nuevo_id == 0:
        raise HTTPException(
            status_code=500,
            detail="Error al insertar la consulta en la base de datos"
        )
    
    # 3. Recuperar la consulta creada desde la BD
    row = fetch_consulta_by_id(nuevo_id)
    
    if not row:
        raise HTTPException(
            status_code=500,
            detail="Error al recuperar la consulta recién creada"
        )
    
    # 4. Mapear y retornar
    consultas_db = map_rows_to_consultas([row])
    return consultas_db[0]
    


@app.put("/consultas/{consulta_id}", response_model=Consulta)
def actualizar_consulta(consulta_id: int, consulta: ConsultaUpdate):
    """
    Actualiza una consulta existente en la base de datos.
    
    - Valida que la consulta existe (404 si no)
    - Valida datos con Pydantic (ConsultaUpdate)
    - Actualiza en MySQL
    - Retorna la consulta actualizada
    """
    # 1. Validar que la consulta existe
    row_existente = fetch_consulta_by_id(consulta_id)
    
    if not row_existente:
        raise HTTPException(
            status_code=404,
            detail=f"Consulta con ID {consulta_id} no encontrada"
        )
    
    # 2. Actualizar la consulta en MySQL
    actualizado = update_consulta(
        consulta_id=consulta_id,
        paciente_nombre=consulta.paciente_nombre,
        paciente_dni=consulta.paciente_dni,
        medico_nombre=consulta.medico_nombre,
        fecha_consulta=consulta.fecha_consulta,
        motivo_consulta=consulta.motivo_consulta,
        diagnostico=consulta.diagnostico,
        estado=consulta.estado,
        coste=consulta.coste,
        fecha_creacion=consulta.fecha_creacion
    )
    
    # 3. Validar que la actualización fue exitosa
    if not actualizado:
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar la consulta en la base de datos"
        )
    
    # 4. Recuperar la consulta actualizada desde la BD
    row_actualizado = fetch_consulta_by_id(consulta_id)
    
    if not row_actualizado:
        raise HTTPException(
            status_code=500,
            detail="Error al recuperar la consulta actualizada"
        )
    
    # 5. Mapear y retornar
    consultas_db = map_rows_to_consultas([row_actualizado])
    return consultas_db[0]


@app.delete("/consultas/{consulta_id}", status_code=200)
def eliminar_consulta(consulta_id: int):
    """
    Elimina una consulta existente de la base de datos.
    
    - Valida que la consulta existe (404 si no)
    - Elimina de MySQL
    - Retorna mensaje de éxito
    """
    # 1. Validar que la consulta existe
    row_existente = fetch_consulta_by_id(consulta_id)
    
    if not row_existente:
        raise HTTPException(
            status_code=404,
            detail=f"Consulta con ID {consulta_id} no encontrada"
        )
    
    # 2. Eliminar la consulta de MySQL
    eliminado = delete_consulta(consulta_id)
    
    # 3. Validar que la eliminación fue exitosa
    if not eliminado:
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar la consulta de la base de datos"
        )
    
    # 4. Retornar mensaje de éxito
    return {
        "mensaje": "Consulta eliminada exitosamente",
        "id_consulta": consulta_id
    }