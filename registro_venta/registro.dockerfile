FROM python:3.10.12-slim

USER root


# Establece el directorio de trabajo
WORKDIR /app

# Copia el contenido de la aplicación al contenedor
COPY . /app

# Actualiza paquetes e instala las dependencias

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Comando para ejecutar gunicorn con un timeout más alto (120 segundos)
CMD ["gunicorn", "--bind", "0.0.0.0:5056", "--timeout", "120", "app:app"]