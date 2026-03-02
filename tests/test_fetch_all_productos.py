import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import fetch_all_consultas

if __name__ == "__main__":
    try:
        consultas = fetch_all_consultas()
        print(f'✅ Consultas encontradas: {len(consultas)}')
        for c in consultas:
            print(c)
    except Exception as e:
        print('❌ Error al obtener consultas →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_fetch_all_consultas.py
