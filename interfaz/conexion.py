import os
import sqlite3
from tkinter import messagebox

class ConexionBD:
    def __init__(self):
        self.conn = None
        self.conectar()
        self.crear_tabla()

    def conectar(self):
        try:
            # Ubicación: sube un nivel para ir a la raíz (practica/) y allí crea/usa iestudiar.db
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(BASE_DIR, "..", "iestudiar.db")
            self.conn = sqlite3.connect(db_path)
        except sqlite3.Error as err:
            messagebox.showerror("Error", f"No se puede conectar a la base de datos: {err}")

    def crear_tabla(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                          DNI INTEGER PRIMARY KEY,
                          Nombre TEXT NOT NULL,
                          Grado INTEGER NOT NULL)''')
        self.conn.commit()

    def cerrar(self):
        if self.conn:
            self.conn.close()
            self.conn = None
