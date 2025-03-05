# Usa una imagen base oficial de Python con SQLite
FROM python:3.9-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos y el código de la aplicación al contenedor
COPY requirements.txt requirements.txt
COPY app app
COPY app/db/init.sql app/db/init.sql

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Instala SQLite
RUN apt-get update && apt-get install -y sqlite3

# Inicializa la base de datos
RUN sqlite3 burger_shop.db < app/db/init.sql
RUN sqlite3 burger_shop.db < app/db/insert.sql

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]