# Usar Python 3.12 como imagen base
FROM python:3.12-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Hacer ejecutable el script de entrada
RUN chmod +x docker-entrypoint.sh

# Crear directorio para la base de datos si no existe
RUN mkdir -p /app/data

# Exponer el puerto 8000
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["./docker-entrypoint.sh"]