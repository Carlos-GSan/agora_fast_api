from sqlmodel import create_engine, SQLModel, Session
from .settings import settings

# Determinar los argumentos de conexión basados en el tipo de base de datos
def get_engine_args():
    """Obtener argumentos de motor según el tipo de base de datos"""
    if settings.database_url.startswith("sqlite"):
        return {
            "connect_args": {"check_same_thread": False},  # Necesario para SQLite con FastAPI
            "echo": settings.debug  # Ver consultas SQL en desarrollo
        }
    else:  # PostgreSQL o otras bases de datos
        return {
            "echo": settings.debug,  # Ver consultas SQL en desarrollo
            "pool_pre_ping": True,  # Verificar conexiones antes de usarlas
            "pool_recycle": 300,  # Reciclar conexiones cada 5 minutos
        }

# Crear el motor de SQLAlchemy con configuración dinámica
engine = create_engine(
    settings.database_url,
    **get_engine_args()
)

def create_db_and_tables():
    """Crear todas las tablas en la base de datos"""
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener la sesión de base de datos
def get_session():
    with Session(engine) as session:
        yield session