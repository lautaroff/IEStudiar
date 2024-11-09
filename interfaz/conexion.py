import mysql.connector
from tkinter import messagebox

class ConexionBD:
    def __init__(self):
        self.conn = None

    def conectar(self):
        if self.conn is None:
            try:
                self.conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="1597845",
                    database="iestudiar"
                )
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se puede conectar a la base de datos: {err}")
        return self.conn

    def cerrar(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None