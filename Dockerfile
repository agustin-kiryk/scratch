
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos y la aplicación manejo ese copy para mantener aridad con los paquetes
COPY requirements.txt .
COPY src/ src/

# Instalar las dep
RUN pip install --no-cache-dir -r requirements.txt

# puerto
EXPOSE 5000

# comand start
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
