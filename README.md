# 🏥 ConsultasApp API REST - Guía Educativa
## API de Gestión de Consultas Médicas
## Por María Chaparro Caballero
[Enlace de perfil de github:](https://github.com/MChaparroCaballero)

---

## 📖 Índice
1. [Caso de Uso: Centro Médico Sanitas](#-caso-de-uso-centro-médico-sanitas)
2. [El Problema a Resolver](#-el-problema-a-resolver)
3. [Especificación de la Base de Datos](#-especificación-de-la-base-de-datos)
4. [Arquitectura y Conceptos](#-arquitectura-y-conceptos)
5. [Librerías Python](#-librerías-python)
6. [Instalación y Ejecución](#-instalación-y-ejecución)
7. [Endpoints de la API](#-endpoints-de-la-api)
8. [Validaciones Pydantic](#-validaciones-pydantic)

---

## 🏢 Caso de Uso: Centro Médico Sanitas

### El Contexto
El Centro Médico Sanitas ha crecido rápidamente, atendiendo a cientos de pacientes semanalmente. Hasta hoy, la gestión de citas y diagnósticos se realizaba en hojas de cálculo compartidas, lo que generaba duplicidad de datos, pérdida de historiales clínicos y errores en el cobro de consultas.

### La Solución
Se ha desarrollado **ConsultasApp**, una API REST que centraliza la gestión de las consultas médicas, permitiendo que tanto el personal administrativo como los médicos puedan registrar, actualizar y consultar el estado de cada paciente de forma segura y eficiente.

---

## 🎯 El Problema a Resolver

Digitalizar el flujo de trabajo médico bajo un estándar **CRUD**, asegurando que:
- Los datos del paciente sean únicos (DNI).
- Los estados de la consulta sean consistentes (`pendiente`, `en_curso`, `finalizada`, `cancelada`).
- El coste de la consulta nunca sea negativo.
- La trazabilidad temporal (fechas de consulta y creación) sea automática.

---

## 📋 Especificación de la Base de Datos

### Script de Estructura (SQL)
La base de datos utiliza `utf8mb4` para soportar caracteres especiales y tildes en nombres y diagnósticos.

```sql
CREATE DATABASE IF NOT EXISTS ConsultasApp CHARACTER SET utf8mb4;
USE ConsultasApp;

CREATE TABLE consulta_medica (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  paciente_nombre VARCHAR(100) NOT NULL,
  paciente_dni VARCHAR(20) NOT NULL UNIQUE,
  medico_nombre VARCHAR(100) NOT NULL,
  fecha_consulta DATETIME NOT NULL,
  motivo_consulta VARCHAR(255) NULL,
  diagnostico VARCHAR(255) NOT NULL,
  estado ENUM('pendiente', 'en_curso', 'finalizada', 'cancelada') NOT NULL DEFAULT 'pendiente',
  coste DECIMAL(8,2) NOT NULL,
  fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
## 🏗️ Arquitectura y Conceptos

La API implementa una **Arquitectura en Capas** para separar las responsabilidades y facilitar el mantenimiento del código:



* **Capa de Presentación (FastAPI):** Gestiona los métodos HTTP y las rutas en `main.py`. Se encarga de recibir las peticiones del cliente y devolver las respuestas.
* **Capa de Validación (Pydantic):** Utiliza los modelos `ConsultaBase`, `ConsultaCreate` y `ConsultaUpdate` para asegurar que los datos cumplan las reglas de negocio antes de interactuar con la base de datos.
* **Capa de Datos (Repository Pattern):** Encapsula las funciones en `database.py` que ejecutan el SQL utilizando `mysql-connector-python`, abstrayendo la complejidad de las consultas al resto de la aplicación.

---

## 📦 Librerías Python

Para el desarrollo de esta API se han seleccionado las siguientes herramientas:

* **FastAPI:** Framework moderno y de alto rendimiento para la creación de los endpoints.
* **Pydantic:** Motor de validación de datos basado en *Type Hinting* de Python.
* **Uvicorn:** Servidor ASGI de baja latencia para ejecutar la aplicación.
* **MySQL Connector:** Driver oficial para la comunicación fluida con MariaDB/MySQL.
* **python-dotenv:** Librería para gestionar credenciales y configuraciones sensibles de forma segura mediante archivos `.env`.

---

## 🚀 Instalación y Ejecución

Sigue estos pasos para configurar el entorno de desarrollo:

### 1. Clonar y preparar entorno
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt```

### 2. Configurar Variables de Env (.env)
```Crea un archivo llamado .env en la raíz del proyecto con el siguiente contenido:

DB_HOST=localhost
DB_USER=consultasappMaria
DB_PASSWORD=consultasapp123
DB_NAME=ConsultasApp```

###3. Ejecutar la API
```Desde la terminal, utiliza el siguiente comando para iniciar el servidor en modo desarrollo:

Bash
uvicorn app.main:app --reload```

## 🔌 Detalle de Endpoints de la API

La API de **ConsultasApp** implementa los siguientes endpoints siguiendo los estándares RESTful:

### 🏠 General
* **`GET /`**: Ruta raíz que devuelve un mensaje de bienvenida, la versión actual de la API y enlaces directos a la documentación interactiva (`/docs` y `/redoc`).
* **`GET /ping`**: Endpoint de salud (*Health Check*) para verificar que el servidor y la conexión están activos. Devuelve `{"message": "pong"}`.

### 🏥 Gestión de Consultas
| Método | Endpoint | Descripción | Status Code |
| :--- | :--- | :--- | :--- |
| **GET** | `/consultas` | Recupera el listado completo de consultas. Realiza un mapeo interno desde los tipos raw de MySQL a modelos Pydantic. | `200 OK` |
| **GET** | `/consulta/{id}` | Busca una consulta específica por su ID. Devuelve error `404` si el ID no existe en la base de datos. | `200 OK` |
| **POST** | `/consultas` | Crea un nuevo registro médico. Valida los datos con `ConsultaCreate` e inserta en MySQL, devolviendo el objeto creado con su ID generado. | `201 Created` |
| **PUT** | `/consultas/{id}` | Actualiza una consulta existente. Primero verifica su existencia y luego aplica los cambios validados con `ConsultaUpdate`. | `200 OK` |
| **DELETE** | `/consultas/{id}` | Elimina de forma permanente un registro tras verificar que existe. | `200 OK` |

---

## 🛠️ Lógica Interna y Flujo de Datos

Cada endpoint de **ConsultasApp** sigue un flujo riguroso para garantizar la integridad de la información médica:

1. **Recepción y Validación:** FastAPI recibe el *request* y Pydantic valida los tipos de datos (por ejemplo, que el coste sea un número positivo).
2. **Interacción con MySQL:** Se utilizan funciones de repositorio como `fetch_all_consultas()` o `insert_consulta()` para comunicarse con MariaDB.
3. **Mapeo de Datos:** Los datos crudos (*rows*) devueltos por MySQL se procesan mediante `map_rows_to_consultas` para asegurar que formatos como fechas o decimales sean compatibles con JSON.
4. **Manejo de Errores:** Se implementan excepciones `HTTPException` (404 para no encontrados, 500 para errores de inserción) para dar feedback claro al cliente.



---

## 📝 Ejemplo de Uso (Payload)

Para registrar una consulta (**POST**), el cuerpo del mensaje debe seguir esta estructura:

```json
{
  "paciente_nombre": "Juan Pérez",
  "paciente_dni": "12345678A",
  "medico_nombre": "Dr. García",
  "fecha_consulta": "2024-03-01T10:30:00",
  "motivo_consulta": "Revisión anual",
  "diagnostico": "Paciente estable",
  "estado": "pendiente",
  "coste": 50.00
}
```
## ✅ Validaciones Pydantic

Se han implementado reglas estrictas mediante **Pydantic V2** para garantizar la integridad de la historia clínica y evitar datos inconsistentes en la base de datos:



* **Validación de Texto:** * Uso de `@field_validator` para aplicar `.strip()` automáticamente a nombres y diagnósticos, eliminando espacios accidentales al inicio o final.
    * Restricción de `min_length=1` para asegurar que ningún campo obligatorio sea enviado como una cadena vacía.

* **Validación de Coste:** * Restricción matemática mediante `Field(ge=0)`, lo que garantiza que el coste de la consulta sea siempre **mayor o igual a cero**, evitando errores de facturación negativos.

* **Validación de Fechas:** * Procesamiento mediante objetos `datetime` nativos. Esto asegura la compatibilidad total con el formato **ISO 8601** y evita errores de formato al insertar datos en las columnas `DATETIME` y `TIMESTAMP` de MySQL.

* **Validación de Estados:** * Control de flujo mediante tipos enumerados que solo permiten los estados definidos en la base de datos: `pendiente`, `en_curso`, `finalizada` o `cancelada`.