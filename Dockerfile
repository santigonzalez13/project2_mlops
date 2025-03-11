# Usar la imagen oficial de Apache Airflow versión 2.6.0 como base
FROM apache/airflow:2.6.0

# Cambiar al usuario "airflow" para ejecutar las tareas con los permisos adecuados
USER airflow

# Copiar el archivo de requerimientos dentro del contenedor
COPY requirements.txt /requirements.txt

# Instalar las dependencias definidas en el archivo requirements.txt
# "--no-cache-dir" evita almacenar archivos temporales innecesarios
RUN pip install --no-cache-dir -r /requirements.txt