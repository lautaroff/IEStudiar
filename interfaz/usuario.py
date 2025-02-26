from conexion import ConexionBD
from tkinter import messagebox
import sqlite3

def verificar_usuario(DNI):
    try:
        dni_int = int(DNI)
    except ValueError:
        messagebox.showerror("Error", "El DNI debe ser un número entero.")
        return None

    conn_bd = ConexionBD()
    conn = conn_bd.conn  # La conexión ya se crea en el constructor
    if conn is None:
        return  # No se pudo conectar

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE DNI = ?", (dni_int,))
        resultado = cursor.fetchone()
        if resultado:
            nombre = resultado[1]  # Suponiendo el orden: DNI, Nombre, Grado
            return nombre
        else:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return None
    except sqlite3.Error as err:
        messagebox.showerror("Error", f"Error ejecutando la consulta: {err}")
        return None
    finally:
        cursor.close()
        conn_bd.cerrar()
