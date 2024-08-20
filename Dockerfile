# Utiliza una imagen base de Python
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /

# Copia el script de Python en el directorio de trabajo dentro del contenedor
COPY data/ data/
COPY main.py .

# Define el comando para ejecutar el script
CMD ["python", "main.py"]
