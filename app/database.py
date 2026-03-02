from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict  # opción C si la prefieres

# Carga .env desde la raíz
load_dotenv(find_dotenv())

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),        # <— corregidos nombres
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "ConsultasMedicasApp"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

def fetch_all_consultas() -> List[Dict[str, Any]]:
    """
    Ejecuta SELECT * FROM consultas y devuelve una lista de dicts.
    """
    conn = None
    try:
        conn = get_connection()

        # Opción C (anotación explícita del cursor)
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]

        try:
            cur.execute(
                """
                SELECT
                    id,
                    paciente_nombre,
                    paciente_dni,
                    medico_nombre,
                    fecha_consulta,
                    motivo_consulta,
                    diagnostico,
                    estado,
                    costo,
                    creado_en
                FROM consultas;
                """
            )

            # Opción A: cast para contentar al type checker
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows

            # Opción B alternativa (sin cast):
            # return [dict(row) for row in cur.fetchall()]

        finally:
            cur.close()

    finally:
        if conn:
            conn.close()


def insert_consulta(
    paciente_nombre: str,
    paciente_dni: str,
    medico_nombre: str,
    fecha_consulta: str,
    motivo_consulta: str,
    diagnostico: str,
    estado: str,
    costo: float,
    creado_en: str
) -> int:
    """
    Inserta una nueva consulta médica en la base de datos.
    Retorna el ID de la consulta insertada.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO consultas
                    (paciente_nombre, paciente_dni, medico_nombre, fecha_consulta, motivo_consulta, diagnostico, estado, costo, creado_en)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    paciente_nombre,
                    paciente_dni,
                    medico_nombre,
                    fecha_consulta,
                    motivo_consulta,
                    diagnostico,
                    estado,
                    costo,
                    creado_en
                )
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()



def delete_consulta(consulta_id: int) -> bool:
    """
    Elimina una consulta médica de la base de datos por su ID.
    Retorna True si se eliminó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM consultas WHERE id = %s",
                (consulta_id,)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def fetch_consulta_by_id(consulta_id: int) -> Dict[str, Any] | None:
    """
    Obtiene una consulta médica por su ID.
    Retorna un dict con los datos de la consulta o None si no existe.
    """
    conn = None
    try:
        conn = get_connection()

        # Cursor tipado explícitamente (mismo patrón)
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]

        try:
            cur.execute(
                """
                SELECT
                   id,
                    paciente_nombre,
                    paciente_dni,
                    medico_nombre,
                    fecha_consulta,
                    motivo_consulta,
                    diagnostico,
                    estado,
                    costo,
                    creado_en
                FROM consultas
                WHERE id = %s
                """,
                (consulta_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


def update_consulta(
    consulta_id: int,
    paciente_nombre: str,
    paciente_dni: str,
    medico_nombre: str,
    fecha_consulta: str,
    motivo_consulta: str,
    diagnostico: str,
    estado: str,
    costo: float,
    creado_en: str
) -> bool:
    """
    Actualiza los datos de una consulta médica existente.
    Retorna True si se actualizó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE consultas
                SET
                   id= %s,
                    paciente_nombre = %s,
                    paciente_dni = %s,
                    medico_nombre = %s,
                    fecha_consulta = %s,
                    motivo_consulta = %s,
                    diagnostico = %s,
                    estado = %s,
                    costo = %s,
                    creado_en = %s
                WHERE id = %s
                """,
                (
                    consulta_id,
                    paciente_nombre,
                    paciente_dni,
                    medico_nombre,
                    fecha_consulta,
                    motivo_consulta,
                    diagnostico,
                    estado,
                    costo,
                    creado_en,
                    consulta_id
                )
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()