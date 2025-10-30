from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.routers import eventos_router, catalogos_router
from app.config.database import create_db_and_tables
from fastapi_mcp import FastApiMCP  # Comentado para Docker

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown
    pass

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API para registro de eventos y asignación de folios IPH",
    version=settings.version,
    debug=settings.debug,
    # lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # Incluir los routers
app.include_router(eventos_router)
app.include_router(catalogos_router)


@app.get("/")
async def root():
    """
    Endpoint raíz de la API
    """
    return {
        "message": "Bienvenido al Sistema IPH",
        "version": settings.version,
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", operation_id="health_check")
async def health_check():
    """
    Endpoint para verificar el estado de la API
    """
    return {"status": "healthy", "version": settings.version}


if __name__ == "__main__":
    mcp = FastApiMCP(app)  # Comentado para Docker
    mcp.mount_http()  # 👈 habilita POST en /mcp
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)