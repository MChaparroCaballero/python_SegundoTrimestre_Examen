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
- Los estados de la consulta sean consistentes (`pendiente`, `en proceso`, `finalizada`, `cancelada`).
- El coste de la consulta nunca sea negativo.
- La trazabilidad temporal (fechas de consulta y creación) sea automática.

---

## 📋 Especificación de la Base de Datos

### Script de Estructura (SQL)
La base de datos utiliza `utf8mb4` para soportar caracteres especiales y tildes en nombres y diagnósticos.

```sql
CREATE DATABASE IF NOT EXISTS ConsultasApp CHARACTER SET utf8mb4;
USE ConsultasApp;

CREATE TABLE `consultas` (
  `id` int(11) NOT NULL,
  `paciente_nombre` varchar(100) NOT NULL,
  `paciente_dni` varchar(9) NOT NULL,
  `medico_nombre` varchar(100) NOT NULL,
  `fecha_consulta` datetime NOT NULL,
  `motivo_consulta` varchar(255) NOT NULL,
  `diagnostico` varchar(255) DEFAULT NULL,
  `estado` enum('pendiente','en proceso','finalizada','cancelada') NOT NULL DEFAULT 'pendiente',
  `costo` decimal(10,2) NOT NULL,
  `creado_en` timestamp NOT NULL DEFAULT current_timestamp()
);

## 🏗️ Arquitectura y Conceptos

La API implementa una **Arquitectura en Capas** para separar las responsabilidades y facilitar el mantenimiento del código:



* **Capa de Presentación (FastAPI):** Gestiona los métodos HTTP y las rutas en `main.py`. Se encarga de recibir las peticiones del cliente y devolver las respuestas.
* **Capa de Validación (Pydantic):** Utiliza los modelos `ConsultaBase`, `ConsultaBD` , `ConsultaCreate` y `ConsultaUpdate` para asegurar que los datos cumplan las reglas de negocio antes de interactuar con la base de datos.
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
DB_USER=tu usuario
DB_PASSWORD=tu password
DB_NAME=ConsultasMedicasApp```

###3. Ejecutar la API
```Desde la terminal, utiliza el siguiente comando para iniciar el servidor en modo desarrollo:

Bash
uvicorn app.main:app --reload```

## 🔌 Detalle de Endpoints de la API

La API de **ConsultasMedicas** implementa los siguientes endpoints siguiendo los estándares RESTful:

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
  "fecha_consulta": "2024-03-01 10:30:00",
  "motivo_consulta": "Revisión anual",
  "diagnostico": "Paciente estable",
  "estado": "pendiente",
  "coste": 50.00
}
```
## ✅ Validaciones Pydantic

Se describen a continuación las validaciones actuales implementadas con **Pydantic V2** (modelo `ConsultaBase` en `app/main.py`):

- **Restricciones de campo (Field):**
  - `paciente_nombre`: `min_length=1`, `max_length=100`, patrón `^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s]+$`.
  - `paciente_dni`: `min_length=1`, `max_length=9`, patrón `^\d{8}[A-Za-z]$`.
  - `medico_nombre`: `min_length=1`, `max_length=100`, patrón `^[a-zA-ZÁÉÍÓÚáéíóúÑñ\s\.]+$`.
  - `motivo_consulta`: `min_length=1`, `max_length=255`.
  - `diagnostico`: opcional, `max_length=255`.
  - `estado`: `default="pendiente"`, `max_length=100`.
  - `costo`: `Field(ge=0)` (no negativo) y además validado estrictamente por validador.
  - `fecha_consulta`: `datetime` con descripción y validación de formato.

- **Validadores personalizados (`@field_validator`):**
  - `validar_no_nulo_ni_vacio` (mode='before'): bloquea `None` y cadenas vacías para campos críticos (`paciente_nombre`, `paciente_dni`, `medico_nombre`, `fecha_consulta`, `motivo_consulta`, `estado`, `costo`).
  - `limpiar_y_validar_sin_numeros`: hace `strip()` y rechaza cualquier valor que contenga dígitos en `paciente_nombre`, `medico_nombre` y `motivo_consulta`.
  - `validar_formato_fecha` (mode='before'): si se recibe una cadena la parsea obligatoriamente con el formato `YYYY-MM-DD HH:MM:SS`, devolviendo un `datetime` o lanzando error en caso contrario.
  - `limpiar_y_validar_dni`: `strip()` y `upper()`, y validad con regex `^[0-9]{8}[A-Z]$` (ej: `12345678Z`).
  - `validar_costo_estricto` (mode='before'): intenta convertir a número (float), rechaza valores no numéricos y prohíbe valores negativos.

Estas reglas están definidas en `ConsultaBase` y heredadas por `ConsultaCreate` y `ConsultaUpdate`, garantizando que tanto creación como actualización cumplan las mismas restricciones.