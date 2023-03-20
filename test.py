import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# Conectar a la base de datos (se crea automáticamente si no existe)
conn = sqlite3.connect('base_datos_tubetag.sqlite')

# Crear una tabla en la base de datos
conn.execute('''CREATE TABLE usuarios
             (ID_USUARIO INT PRIMARY KEY     NOT NULL,
             NOMBRE_USUARIO           TEXT    NOT NULL);''')

conn.execute('''CREATE TABLE subscripciones
             (ID_SUBSCRIPCION TEXT PRIMARY KEY     NOT NULL,
             NOMBRE           TEXT    NOT NULL,
             ID_CATEGORIA             TEXT     NOT NULL,
             ID_USUARIOS INT NOT NULL);''')

conn.execute('''CREATE TABLE categorias
             (ID_CATEGORIA INT PRIMARY KEY NOT NULL,
             CATEGORIA TEXT NOT NULL,
             ID_USUARIOS TEXT NOT NULL);''')

#id primary key, nombre canal, categorizacion

# Cerrar la conexión a la base de datos

conn.close()