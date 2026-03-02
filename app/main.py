import re
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
    paciente_nombre: Annotated[str, Field(min_length=1, max_length=100,pattern=r"^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$")]
    paciente_dni: Annotated[str, Field(min_length=1, max_length=9, pattern=r"^\d{8}[A-Za-z]$")]
    medico_nombre: Annotated[str, Field(min_length=1, max_length=100,pattern=r"^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s\.]+$")]
    fecha_consulta: datetime = Field(description="Fecha de la cita")
    motivo_consulta: Annotated[str, Field(min_length=1, max_length=255)]
    diagnostico: Optional[Annotated[str, Field(max_length=255)]]=None
    estado: Annotated[str, Field(default="pendiente", max_length=100)]
    costo: float = Field(ge=0)
    creado_en: Optional[datetime] = Field(default_factory=datetime.now)

    # --- VALIDADOR PARA EVITAR NULOS Y VACÍOS EN TODOS LOS CAMPOS ---
    @field_validator(
        'paciente_nombre', 'paciente_dni', 'medico_nombre', 
        'fecha_consulta', 'motivo_consulta', 'estado', 
        'costo', mode='before'
    )
    @classmethod
    def validar_no_nulo_ni_vacio(cls, v, info):
        # 1. Comprobar si es estrictamente nulo (None)
        if v is None:
            raise ValueError(f'El campo {info.field_name} no puede ser nulo')
        
        # 2. Si es una cadena de texto, comprobar si está vacía
        if isinstance(v, str):
            if not v.strip():
                raise ValueError(f'El campo {info.field_name} no puede estar vacío')
        
        return v

   # --- VALIDADOR PARA LIMPIAR Y BLOQUEAR NÚMEROS ---
    @field_validator('paciente_nombre', 'medico_nombre', 'motivo_consulta')
    @classmethod
    def limpiar_y_validar_sin_numeros(cls, v: str) -> str:
        # 1. Quitar espacios
        v = v.strip()
        
        # 3. BLOQUEAR NÚMEROS: Si encuentra cualquier dígito (0-9), lanza error
        if any(char.isdigit() for char in v):
            raise ValueError('Este campo no puede contener números')
            
        return v

    # --- VALIDADOR DE FORMATO DE FECHA ---
    @field_validator('fecha_consulta', mode='before')
    @classmethod
    def validar_formato_fecha(cls, v):
        """Fuerza el formato YYYY-MM-DD HH:MM:SS antes de convertir a objeto datetime."""
        if isinstance(v, str):
            try:
                # Intentamos parsear el string con el formato exacto
                return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError('Formato de fecha inválido. Debe ser YYYY-MM-DD HH:MM:SS')
        return v

    # --- VALIDADOR DE DNI (LIMPIEZA, MAYÚSCULAS Y REGEX) ---
    @field_validator('paciente_dni')
    @classmethod
    def limpiar_y_validar_dni(cls, v: str) -> str:
        # 1. Limpieza básica
        v = v.strip().upper()
        
        # 2. Comprobar formato con Regex (8 números + 1 letra)
        # ^[0-9]{8}[A-Z]$ significa: empezar con 8 dígitos y terminar con una letra de la A a la Z
        if not re.match(r"^[0-9]{8}[A-Z]$", v):
            raise ValueError('Formato de DNI inválido. Debe ser 8 números seguidos de una letra (ej: 12345678Z)')
        
        return v
    
    # --- VALIDADOR DE COSTO (LIMPIEZA Y VALIDACIÓN ESTRICTA DE NUMEROS POSITIVOS) ---
    @field_validator('costo', mode='before')
    @classmethod
    def validar_costo_estricto(cls, v):
        """Valida que el costo sea un número, no tenga letras y sea positivo."""

        # Intentamos convertir a float para ver si tiene letras
        try:
            valor_float = float(v)
        except (ValueError, TypeError):
            raise ValueError('El costo debe ser un número válido (no se permiten letras)')

        # Validamos que no sea negativo
        if valor_float < 0:
            raise ValueError('El costo no puede ser un valor negativo')
            
        return valor_float

class ConsultaDB(BaseModel):
    """Modelo para lectura desde BD (sin validaciones estrictas para datos históricos)."""
    id: int
    paciente_nombre: str
    paciente_dni: str
    medico_nombre: str
    fecha_consulta: datetime
    motivo_consulta: str
    diagnostico: str | None
    estado: str
    costo: float
    creado_en: datetime | None


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
        if isinstance(consulta_data.get("costo"), Decimal):
            consulta_data["costo"] = float(consulta_data["costo"])
        
              
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
        "message": "Bienvenido a ConsultasMedicas API by María Chaparro Caballero - 2 DAW",
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
        costo=consulta.costo,
        creado_en=consulta.creado_en
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
        costo=consulta.costo,
        creado_en=consulta.creado_en
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