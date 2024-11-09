import mysql.connector 
from conexion import ConexionBD  

class CRUD:
    def __init__(self):
        self.conexion_bd = ConexionBD()

    def agregar_usuario(self, dni, nombre, grado):
        if dni and nombre and grado:
            conn = self.conexion_bd.conectar()
            cursor = conn.cursor()
            try:
                sql_query_insert = "INSERT INTO usuarios (DNI, Nombre, Grado) VALUES (%s, %s, %s)"
                values = (dni, nombre, grado)
                cursor.execute(sql_query_insert,values)
                conn.commit()
                cursor.close()
                return True, "Usuario agregado correctamente"
            except mysql.connector.Error as err:
                return False, f"No se pudo agregar el usuario: {err}"
            finally:
                cursor.close()
        else:
            return False, "Por favor, complete todos los campos"

    def editar_usuario(self, dni, nombre, grado):
        if dni and nombre and grado:
            conn = self.conexion_bd.conectar()
            cursor = conn.cursor()
            try:
                sql_query_update = "UPDATE usuarios SET Nombre = %s, Grado = %s WHERE DNI = %s"
                values =(nombre, grado, dni)
                cursor.execute(sql_query_update,values)
                conn.commit()
                cursor.close()
                return True, "Usuario editado correctamente"
            except mysql.connector.Error as err:
                return False, f"No se pudo editar el usuario: {err}"
            finally:
                cursor.close()
        else:
            return False, "Por favor, complete todos los campos"

    def eliminar_usuario(self, dni):
        if dni:
            conn = self.conexion_bd.conectar()
            cursor = conn.cursor()
            try:
                sql_query_delete ="DELETE FROM usuarios WHERE DNI = %s"
                values = (dni,)
                cursor.execute(sql_query_delete,values)
                conn.commit()
                cursor.close()
                return True, "Usuario eliminado correctamente"
            except mysql.connector.Error as err:
                return False, f"No se pudo eliminar el usuario: {err}"
            finally:
                cursor.close()
        else:
            return False, "Debe seleccionar un usuario para eliminar"

    def buscar_usuarios(self, filtro_nombre, filtro_dni, filtro_grado):
        conn = self.conexion_bd.conectar()
        cursor = conn.cursor()
        query = "SELECT * FROM usuarios WHERE 1=1"
        params = []

        if filtro_nombre:
            query += " AND Nombre LIKE %s"
            params.append(f"%{filtro_nombre}%")
        
        if filtro_dni:
            query += " AND DNI = %s"
            params.append(filtro_dni)
        
        if filtro_grado:
            query += " AND Grado = %s"
            params.append(filtro_grado)

        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            raise Exception(f"No se pudieron obtener los datos: {err}")
        finally:
            cursor.close()


