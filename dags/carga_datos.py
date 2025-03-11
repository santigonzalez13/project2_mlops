import pandas as pd
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from sqlalchemy import create_engine

# Configuración de argumentos predeterminados para el DAG
default_args = {
    'owner': 'airflow',                      # Propietario del DAG
    'depends_on_past': False,               # Indica si las ejecuciones dependen de ejecuciones pasadas
    'start_date': datetime(2025, 3, 10)     # Fecha de inicio definida del DAG
}

def load_dataset():
    """
    Función para cargar un conjunto de datos desde un archivo CSV y guardarlo en una base de datos MySQL.
    """
    # Ruta del archivo CSV con el conjunto de datos
    parent_directory = "/opt/airflow/datos/penguins_lter.csv"
    
    # Carga el archivo CSV en un DataFrame de pandas
    penguins = pd.read_csv(parent_directory)
    
    # Establece la conexión a la base de datos MySQL usando SQLAlchemy
    engine = create_engine('mysql://root:airflow@mysql:3306/penguin_data')
    
    # Guarda el DataFrame en la tabla 'penguins' dentro de la base de datos
    # Reemplaza la tabla si ya existe y no incluye el índice
    penguins.to_sql('penguins', con=engine, if_exists='replace', index=False)
    
    # Mensaje de confirmación
    print("Datos cargados en MySQL")

# Definición del DAG (Directed Acyclic Graph) en Airflow
with DAG(dag_id='data_loading',            # Identificador único del DAG
         default_args=default_args,           # Argumentos predeterminados
         schedule_interval=None) as dag:      # Sin programación automática de ejecución

    # Definición de la tarea para ejecutar la función de carga de datos
    load_data_task = PythonOperator(task_id='load_dataset',      # Identificador único de la tarea
                                    python_callable=load_dataset) # Función a ejecutar