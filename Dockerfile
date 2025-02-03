# Usa la imagen oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación FastAPI al contenedor
COPY . .

# Expone el puerto 8000 (puedes cambiarlo si es necesario)
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
