import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import update_consulta

if __name__ == "__main__":
    try:
        resultado = update_consulta(
            consulta_id=1,
            paciente_nombre='Juan Pérez',
            paciente_dni='12345678Z',
            medico_nombre='Dr. García',
            fecha_consulta='2025-01-15 10:30:00',
            motivo_consulta='Revisión médica general',
            diagnostico='Paciente en buen estado general',
            estado='realizada',
            costo=150.00
        )

        if resultado:
            print('✅ Consulta actualizada correctamente')
        else:
            print('⚠️ Consulta no encontrada')
    except Exception as e:
        print('❌ Error al actualizar consulta →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_update_consulta.py
