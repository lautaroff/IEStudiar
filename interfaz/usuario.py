from conexion import ConexionBD
from tkinter import messagebox
import mysql.connector
def verificar_usuario(DNI):
    conn_bd = ConexionBD()
    conn = conn_bd.conectar()
    
    if conn is None:
        return  # Si no hay conexión, no continuar

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE DNI = %s", (DNI,))
        resultado = cursor.fetchone()

        if resultado:
            nombre = resultado[1]  # Obtener el nombre
            return nombre
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error ejecutando la consulta: {err}")
    finally:
        cursor.close()
        conn_bd.cerrar()
