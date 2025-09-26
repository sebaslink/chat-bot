# Dockerfile para Chat Masivo WhatsApp

FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p data/database static/uploads uploads logs

# Exponer puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_APP=SISTEMA_UNIFICADO_FINAL.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando por defecto
CMD ["python", "SISTEMA_UNIFICADO_FINAL.py"]
