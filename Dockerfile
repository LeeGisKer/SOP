# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos y luego instala las dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia el contenido de la aplicación en el contenedor
COPY . .

# Expone el puerto en el que correrá la aplicación
EXPOSE 8000

# Define el comando de inicio
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
