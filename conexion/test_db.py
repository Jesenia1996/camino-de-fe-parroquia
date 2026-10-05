# test_db.py
import mysql.connector
from mysql.connector import Error

try:
    print("Intentando conectar...")
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # Si tu XAMPP tiene contraseña, ponla aquí. Si no, déjalo así.
        database='caminos_de_fe'
    )
    if conexion.is_connected():
        print("✅ ¡Conexión exitosa a la base de datos 'caminos_de_fe'!")
        conexion.close()
except Error as e:
    print(f"❌ Error de MySQL: {e}")
except Exception as e:
    print(f"❌ Error inesperado: {e}")