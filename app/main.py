from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import consultas

# ========================
# Inicialización de FastAPI
# ========================

app = FastAPI(
    title="ConsultasMedicas API Ing María Chaparro Caballero",
    version="1.0.0",
    description="API REST desacoplada para gestión de consultas médicas por María Chaparro Caballero - 2 DAW"
)

# ========================
# Configuración de CORS
# ========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos los orígenes (ajustar en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permitir todos los headers
)

# ========================
# Registro de Routers
# ========================

app.include_router(consultas.router)

# ========================
# Endpoint Raíz
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
