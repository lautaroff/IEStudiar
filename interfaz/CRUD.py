import sqlite3
from conexion import ConexionBD  

class CRUD:
    def __init__(self):
        self.conexion_bd = ConexionBD()

    def agregar_usuario(self, dni, nombre, grado):
        if dni and nombre and grado:
            try:
                dni_int = int(dni)
            except ValueError:
                return False, "El DNI debe ser un número entero de 8 dígitos."
            conn = self.conexion_bd.conn
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (DNI, Nombre, Grado) VALUES (?, ?, ?)", (dni_int, nombre, grado))
                conn.commit()
                return True, "Usuario agregado correctamente"
            except sqlite3.Error as err:
                return False, f"No se pudo agregar el usuario: {err}"
        else:
            return False, "Por favor, complete todos los campos"

    def editar_usuario(self, dni, nombre, grado):
        if dni and nombre and grado:
            try:
                dni_int = int(dni)
            except ValueError:
                return False, "El DNI debe ser un número entero de 8 dígitos."
            conn = self.conexion_bd.conn
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE usuarios SET Nombre = ?, Grado = ? WHERE DNI = ?", (nombre, grado, dni_int))
                conn.commit()
                return True, "Usuario editado correctamente"
            except sqlite3.Error as err:
                return False, f"No se pudo editar el usuario: {err}"
        else:
            return False, "Por favor, complete todos los campos"

    def eliminar_usuario(self, dni):
        if dni:
            try:
                dni_int = int(dni)
            except ValueError:
                return False, "El DNI debe ser un número entero de 8 dígitos."
            conn = self.conexion_bd.conn
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM usuarios WHERE DNI = ?", (dni_int,))
                conn.commit()
                return True, "Usuario eliminado correctamente"
            except sqlite3.Error as err:
                return False, f"No se pudo eliminar el usuario: {err}"
        else:
            return False, "Debe ingresar un DNI para eliminar"

    def buscar_usuarios(self, filtro_nombre, filtro_dni, filtro_grado):
        conn = self.conexion_bd.conn
        cursor = conn.cursor()
        query = "SELECT * FROM usuarios WHERE 1=1"
        params = []

        if filtro_nombre:
            query += " AND Nombre LIKE ?"
            params.append(f"%{filtro_nombre}%")
        
        if filtro_dni:
            try:
                filtro_dni_int = int(filtro_dni)
            except ValueError:
                raise Exception("El DNI debe ser un número entero.")
            query += " AND DNI = ?"
            params.append(filtro_dni_int)
        
        if filtro_grado:
            try:
                filtro_grado_int = int(filtro_grado)
            except ValueError:
                raise Exception("El Grado debe ser un número entero.")
            query += " AND Grado = ?"
            params.append(filtro_grado_int)

        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except sqlite3.Error as err:
            raise Exception(f"No se pudieron obtener los datos: {err}")
