# conexion/conexion.py

import pymysql


def obtener_conexion():
    """
    Establece y retorna una conexión con la base de datos MySQL.
    """

    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="caminos_de_fe",
            cursorclass=pymysql.cursors.DictCursor
        )

        return conexion

    except Exception as e:

        print(f"Error al conectar con MySQL: {e}")

        return None