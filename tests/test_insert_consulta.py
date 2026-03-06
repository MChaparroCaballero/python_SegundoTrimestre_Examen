import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import insert_consulta

if __name__ == "__main__":
    try:
        nuevo_id = insert_consulta(
            paciente_nombre='Juan Pérez',
            paciente_dni='12345678Z',
            medico_nombre='Dr. García',
            fecha_consulta='2025-01-15 10:30:00',
            motivo_consulta='Revisión médica general',
            diagnostico='Paciente en buen estado general',
            estado='realizada',
            costo=50.00
        )

        print('🆔 ID consulta insertada →', nuevo_id)
    except Exception as e:
        print('❌ Error al insertar consulta →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_insert_consulta.py
