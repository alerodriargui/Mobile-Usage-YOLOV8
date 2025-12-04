# Usamos Python 3.11 oficial
FROM python:3.11-slim

# Evitamos mensajes de buffer
ENV PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Copiamos requirements
COPY requirements.txt .

# Instalamos dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiamos el resto del proyecto
COPY . .

# Comando por defecto (puedes cambiarlo luego)
CMD ["python", "live_mobileuse.py"]
