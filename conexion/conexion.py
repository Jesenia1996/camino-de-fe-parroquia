# conexion/conexion.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()


def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            cursor_factory=RealDictCursor
        )

        return conexion

    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return None