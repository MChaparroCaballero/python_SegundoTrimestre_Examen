import sys
from pathlib import Path

# Agregar la raíz del proyecto al path para los imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.database import fetch_consulta_by_id

if __name__ == "__main__":
    try:
        # Validar que se haya pasado el ID como parámetro
        if len(sys.argv) < 2:
            print('❌ Error: Debes proporcionar el ID de la consulta como argumento')
            print('Uso: python tests/test_fetch_consulta_by_id.py <ID>')
            sys.exit(1)
        
        # Obtener el ID de la consulta desde los argumentos
        consulta_id = int(sys.argv[1])
        consulta = fetch_consulta_by_id(consulta_id)

        if consulta:
            print('✅ Consulta encontrada:')
            print(consulta)
        else:
            print('⚠️ Consulta no encontrada para el ID:', consulta_id)
    except ValueError:
        print('❌ Error: El ID debe ser un número entero')
        sys.exit(1)
    except Exception as e:
        print('❌ Error al buscar consulta →', e)

# ===== EJECUCIÓN DESDE CMD =====
# python tests/test_fetch_consulta_by_id.py 1
