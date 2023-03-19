import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# Conectar a la base de datos (se crea automáticamente si no existe)
conn = sqlite3.connect('mi_base_de_datos.sqlite')


# Crear una tabla en la base de datos
conn.execute('''CREATE TABLE usuarios
             (ID INT PRIMARY KEY     NOT NULL,
             NOMBRE           TEXT    NOT NULL,
             EDAD             INT     NOT NULL,
             CIUDAD           TEXT    NOT NULL);''')


engine = create_engine('sqlite:///mi_base_de_datos.sqlite', echo=False)

df = pd.read_sql_query("SELECT * FROM mi_tabla", conn)

df.to_sql('mi_tabla', engine, if_exists='replace', index=False)

# Cerrar la conexión a la base de datos
conn.close()