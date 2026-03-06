
from enum import Enum

from pydantic import BaseModel, Field, field_validator
from typing import Annotated, List, Optional
from datetime import datetime
import re
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
    diagnostico: Optional[Annotated[str, Field(max_length=1000)]] = None
    estado: Annotated[str, Field(default="programada", max_length=100)]
    costo: float = Field(ge=0, lt=10000)

   # --- 1. VALIDACIÓN GENERAL: NULOS Y VACÍOS ---
    @field_validator(
        'paciente_nombre', 'paciente_dni', 'medico_nombre', 
        'fecha_consulta', 'motivo_consulta', 'estado', 
        'costo', mode='before'
    )
    @classmethod
    def validar_no_nulo_ni_vacio(cls, v, info):
        if v is None:
            raise ValueError(f'El campo {info.field_name} no puede ser nulo')
        
        if isinstance(v, str) and not v.strip():
            raise ValueError(f'El campo {info.field_name} no puede estar vacío')
        
        return v
    
    # --- 2. VALIDACIÓN DE NOMBRES: SIN NÚMEROS + REGEX + TITLE CASE ---
    @field_validator('paciente_nombre', 'medico_nombre')
    @classmethod
    def validar_nombres_estricto(cls, v: str) -> str:
        v = v.strip()
        # Bloquear números
        if any(char.isdigit() for char in v):
            raise ValueError('Este campo no puede contener números')
        
        # Validar Regex sugerida (letras y espacios)
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\.]+$", v):
            raise ValueError('Formato de nombre inválido. Solo letras y espacios')
        
        # Convertir a Title Case
        return v.title()
    
    # --- 3. VALIDACIÓN DE DNI: LIMPIEZA Y MAYÚSCULAS ---
    @field_validator('paciente_dni')
    @classmethod
    def limpiar_y_validar_dni(cls, v: str) -> str:
        v = v.strip().upper()
        if not re.match(r"^\d{8}[A-Z]$", v):
            raise ValueError('DNI inválido. Debe ser 8 números y 1 letra (ej: 12345678Z)')
        return v
    
    # --- 4. VALIDACIÓN DE FECHA: FORMATO + LÍMITE AÑO 2000 ---
    @field_validator('fecha_consulta', mode='before')
    @classmethod
    def validar_fecha_completa(cls, v):
        # Si es string, forzamos formato
        if isinstance(v, str):
            try:
                v = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError('Formato de fecha inválido. Debe ser YYYY-MM-DD HH:MM:SS')
        
        # Validar que no sea anterior al año 2000
        if v.year < 2000:
            raise ValueError('La fecha de consulta no puede ser anterior al año 2000')
        
        return v

    # --- 5. VALIDACIÓN DE MOTIVO: MÍNIMO 10 CARACTERES ---
    @field_validator('motivo_consulta')
    @classmethod
    def validar_motivo_largo(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError('El motivo debe tener al menos 10 caracteres')
        return v

    # --- 6. VALIDACIÓN DE ESTADO: VALORES PERMITIDOS ---
    @field_validator('estado')
    @classmethod
    def validar_estado_lista(cls, v: str) -> str:
        estados_validos = ['programada', 'confirmada', 'realizada', 'cancelada', 'no_asistio']
        v = v.strip().lower()
        if v not in estados_validos:
            raise ValueError(f'Estado inválido. Debe ser uno de: {", ".join(estados_validos)}')
        return v

    # --- 7. VALIDACIÓN DE COSTO: NÚMEROS, RANGO Y 2 DECIMALES ---
    @field_validator('costo', mode='before')
    @classmethod
    def validar_costo_final(cls, v):
        try:
            valor_float = float(v)
        except (ValueError, TypeError):
            raise ValueError('El costo debe ser un número válido')

        if valor_float <= 0 or valor_float >= 10000:
            raise ValueError('El costo debe ser mayor que 0 y menor que 10000')

        # Validar máximo 2 decimales
        if round(valor_float, 2) != valor_float:
            raise ValueError('El costo no puede tener más de 2 decimales')
            
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
    creado_en: datetime


class ConsultaCreate(ConsultaBase):
    """Modelo para crear nueva consulta (sin ID)."""
    pass


class ConsultaUpdate(ConsultaBase):
    """Modelo para actualizar consulta (sin ID)."""
    pass


class Consulta(ConsultaBase):
    """Modelo completo de Consulta (con ID y validaciones)."""
    id: int
    creado_en: datetime