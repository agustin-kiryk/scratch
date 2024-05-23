# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos y la aplicación
COPY requirements.txt .
COPY src/ src/

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará la aplicación Flask
EXPOSE 5000

# Comando para correr la aplicación
CMD ["python", "src/app.py"]
