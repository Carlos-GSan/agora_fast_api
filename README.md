# Sistema IPH - Registro de Eventos

## Descripción
API REST desarrollada con FastAPI para el registro de eventos policiales y asignación de folios IPH (Informe Policial Homologado).

## Características
- Registro completo de eventos policiales
- Asignación automática de folios IPH
- Gestión de catálogos (oficiales, detenidos, drogas, armas, etc.)
- API RESTful con documentación automática
- Base de datos SQLite (fácil configuración para desarrollo)
- Validación de datos con Pydantic

## Instalación

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd agora_fast_api
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno (opcional):
```bash
cp .env.example .env
# La configuración por defecto usa SQLite y funciona sin modificaciones
```

5. Ejecutar la aplicación:
```bash
python main.py
```

6. (Opcional) Inicializar con datos de ejemplo:
```bash
python init_db.py
```

La aplicación estará disponible en: http://localhost:8000

## Documentación de la API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Principales

### Eventos
- `POST /eventos/` - Crear nuevo evento
- `GET /eventos/` - Listar eventos
- `GET /eventos/{iph_id}` - Obtener evento específico
- `PUT /eventos/{iph_id}` - Actualizar evento
- `DELETE /eventos/{iph_id}` - Eliminar evento
- `GET /eventos/folio/{folio_cecom}` - Buscar por folio CECOM
- `GET /eventos/region/{id_region}` - Filtrar por región

### Catálogos
- `/catalogos/tipos-evento/` - Tipos de evento
- `/catalogos/intervenciones/` - Tipos de intervención
- `/catalogos/regiones/` - Regiones
- `/catalogos/unidades/` - Unidades vehiculares
- `/catalogos/oficiales/` - Oficiales
- `/catalogos/detenidos/` - Detenidos
- `/catalogos/motivos/` - Motivos y tipos de motivo
- `/catalogos/drogas/` - Catálogo de drogas
- `/catalogos/armas/` - Catálogo de armas

## Estructura del Proyecto

```
agora_fast_api/
├── app/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py      # Configuración de base de datos
│   │   └── settings.py      # Variables de entorno
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py        # Modelos SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base_schemas.py  # Esquemas base
│   │   └── evento_schemas.py # Esquemas de eventos
│   └── routers/
│       ├── __init__.py
│       ├── eventos.py       # Endpoints de eventos
│       └── catalogos.py     # Endpoints de catálogos
├── main.py                  # Archivo principal
├── requirements.txt         # Dependencias
├── .env.example            # Ejemplo de variables de entorno
└── README.md               # Este archivo
```

## Modelo de Datos

El sistema maneja los siguientes tipos de datos:

- **Eventos**: Registro principal con folio IPH
- **Oficiales**: Personal policial involucrado
- **Detenidos**: Personas detenidas en el evento
- **Motivos**: Razones del evento (delitos, faltas cívicas)
- **Drogas y Armas**: Evidencias decomisadas
- **Ubicación**: Región, colonia, calle, georreferencia

## Uso de la API

### Crear un evento
```python
import requests

evento_data = {
    "id_tpo_evento": 1,
    "id_intervencion": 1,
    "id_region": 1,
    "turno": "MATUTINO",
    "folio_cecom": "CECOM-2024-001",
    "colonia": "Centro",
    "calle": "Av. Principal",
    "narrativa": "Descripción del evento...",
    "oficiales": [{"id_oficial": 1}],
    "detenidos": [{"id_detenido": 1, "rnd_detenido": "RND123"}],
    "motivos": [{"id_mot": 1}]
}

response = requests.post("http://localhost:8000/eventos/", json=evento_data)
print(response.json())
```

## Licencia

Este proyecto está bajo la Licencia MIT.