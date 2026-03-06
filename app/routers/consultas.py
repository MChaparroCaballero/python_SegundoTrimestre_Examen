from fastapi import APIRouter, HTTPException, Response
from typing import List
from decimal import Decimal
import mysql.connector
from app.schemas.consulta import Consulta, ConsultaCreate, ConsultaUpdate, ConsultaDB
from app.database import (
    fetch_all_consultas, fetch_consulta_by_id, 
    insert_consulta, update_consulta, delete_consulta
)

router = APIRouter(prefix="/consultas", tags=["Consultas"])

# ==========================================
# FUNCIÓN HELPER (Mapeo de BD a Pydantic)
# ==========================================
def map_rows_to_consultas(rows: List[dict]) -> List[ConsultaDB]:
    """Convierte resultados de MySQL a objetos ConsultaDB válidos."""
    consultas_db = []
    for row in rows:
        datos = dict(row)
        if isinstance(datos.get("costo"), Decimal):
            datos["costo"] = float(datos["costo"])
        consultas_db.append(ConsultaDB(**datos))
    return consultas_db

# ==========================================
# ENDPOINTS
# ==========================================

@router.get("/ping")
def ping():
    return {"message": "pong"}

@router.get("/", response_model=List[Consulta])
def listar_consultas():
    try:
        rows = fetch_all_consultas()
        return map_rows_to_consultas(rows)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener consultas: {str(e)}")

@router.get("/{consulta_id}", response_model=Consulta)
def obtener_consulta(consulta_id: int):
    row = fetch_consulta_by_id(consulta_id)
    if not row:
        raise HTTPException(status_code=404, detail=f"Consulta con ID {consulta_id} no encontrada")
    return map_rows_to_consultas([row])[0]

@router.post("/", response_model=Consulta, status_code=201)
def crear_consulta(consulta: ConsultaCreate):
    try:
        nuevo_id = insert_consulta(**consulta.model_dump())
        row = fetch_consulta_by_id(nuevo_id)
        if not row:
            raise HTTPException(status_code=500, detail="Error al recuperar la consulta creada")
        return map_rows_to_consultas([row])[0]
    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise HTTPException(status_code=409, detail="El DNI ya está registrado")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {err.msg}")

@router.put("/{consulta_id}", response_model=Consulta)
def actualizar_consulta_endpoint(consulta_id: int, consulta: ConsultaUpdate):
    existente = fetch_consulta_by_id(consulta_id)
    if not existente:
        raise HTTPException(status_code=404, detail=f"ID {consulta_id} no existe")
    try:
        update_consulta(consulta_id=consulta_id, **consulta.model_dump())
        row = fetch_consulta_by_id(consulta_id)
        return map_rows_to_consultas([row])[0]
    except mysql.connector.Error as err:
        if err.errno == 1062:
            raise HTTPException(status_code=409, detail="El DNI ya pertenece a otro paciente")
        raise HTTPException(status_code=500, detail=f"Error interno: {err.msg}")

@router.delete("/{consulta_id}", status_code=204)
def eliminar_consulta_endpoint(consulta_id: int):
    existente = fetch_consulta_by_id(consulta_id)
    if not existente:
        raise HTTPException(status_code=404, detail=f"ID {consulta_id} no existe")
    if not delete_consulta(consulta_id):
        raise HTTPException(status_code=500, detail="Error al eliminar")
    return Response(status_code=204)