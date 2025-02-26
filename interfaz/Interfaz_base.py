import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox

# Agregamos la carpeta padre (practica/) al path para poder importar CRUD
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from CRUD import CRUD

class Interfaz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CRUD de Usuarios")
        self.root.geometry("600x500")

        self.crud = CRUD()  # Instancia de la clase CRUD

        # Crear interfaz gráfica
        self.crear_widgets()

        self.root.mainloop()

    def crear_widgets(self):
        # Frame para datos
        frame_datos = ttk.LabelFrame(self.root, text="Datos del Usuario")
        frame_datos.pack(fill="x", padx=10, pady=10)

        # Etiquetas y campos de entrada
        ttk.Label(frame_datos, text="DNI (8 dígitos):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_dni = ttk.Entry(frame_datos)
        self.entry_dni.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_datos, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nombre = ttk.Entry(frame_datos)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_datos, text="Grado:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_grado = ttk.Combobox(frame_datos, values=[str(i) for i in range(1, 8)])
        self.combo_grado.grid(row=2, column=1, padx=5, pady=5)

        # Botones para agregar, editar y eliminar
        ttk.Button(frame_datos, text="Agregar", command=self.agregar_usuario).grid(row=3, column=0, padx=5, pady=5)
        ttk.Button(frame_datos, text="Editar", command=self.editar_usuario).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(frame_datos, text="Eliminar", command=self.eliminar_usuario).grid(row=3, column=2, padx=5, pady=5)

        # Frame para filtros
        frame_filtros = ttk.LabelFrame(self.root, text="Filtros de Búsqueda")
        frame_filtros.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_filtros, text="Filtrar por Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_filtro_nombre = ttk.Entry(frame_filtros)
        self.entry_filtro_nombre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Filtrar por DNI:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_filtro_dni = ttk.Entry(frame_filtros)
        self.entry_filtro_dni.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_filtros, text="Filtrar por Grado:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_filtro_grado = ttk.Combobox(frame_filtros, values=[str(i) for i in range(1, 8)])
        self.combo_filtro_grado.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_filtros, text="Buscar", command=self.actualizar_lista).grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Tabla de datos (inicialmente oculta)
        self.cols = ("DNI", "Nombre", "Grado")
        self.tabla = ttk.Treeview(self.root, columns=self.cols, show="headings")
        for col in self.cols:
            self.tabla.heading(col, text=col)

        # Evento para seleccionar una fila en la tabla
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_fila)

        # Inicialmente oculta la tabla
        self.mostrar_ocultar_tabla(False)

    def agregar_usuario(self):
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        grado = self.combo_grado.get().strip()

        if not dni or not nombre or not grado:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not (dni.isdigit() and len(dni) == 8):
            messagebox.showerror("Error", "El DNI debe contener exactamente 8 dígitos numéricos.")
            return

        success, message = self.crud.agregar_usuario(dni, nombre, grado)
        messagebox.showinfo("Resultado", message)
        if success:
            self.actualizar_lista()

    def editar_usuario(self):
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        grado = self.combo_grado.get().strip()

        if not dni or not nombre or not grado:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not (dni.isdigit() and len(dni) == 8):
            messagebox.showerror("Error", "El DNI debe contener exactamente 8 dígitos numéricos.")
            return

        # Verificar si el usuario existe antes de editar
        registros = self.crud.buscar_usuarios("", dni, "")
        if not registros:
            messagebox.showwarning("Advertencia", "El usuario no existe.")
            return

        success, message = self.crud.editar_usuario(dni, nombre, grado)
        messagebox.showinfo("Resultado", message)
        if success:
            self.actualizar_lista()

    def eliminar_usuario(self):
        dni = self.entry_dni.get().strip()
        if not dni:
            messagebox.showerror("Error", "Debe ingresar el DNI para eliminar un usuario.")
            return

        if not (dni.isdigit() and len(dni) == 8):
            messagebox.showerror("Error", "El DNI debe contener exactamente 8 dígitos numéricos.")
            return

        # Verificar si el usuario existe antes de eliminar
        registros = self.crud.buscar_usuarios("", dni, "")
        if not registros:
            messagebox.showwarning("Advertencia", "El usuario no existe.")
            return

        success, message = self.crud.eliminar_usuario(dni)
        messagebox.showinfo("Resultado", message)
        if success:
            self.actualizar_lista()

    def actualizar_lista(self):
        filtro_nombre = self.entry_filtro_nombre.get().strip()
        filtro_dni = self.entry_filtro_dni.get().strip()
        filtro_grado = self.combo_filtro_grado.get().strip()

        # Si no se aplican filtros, mostrar todos los registros
        try:
            registros = self.crud.buscar_usuarios(filtro_nombre, filtro_dni, filtro_grado)
            if not registros:
                messagebox.showinfo("Información", "No se encontraron usuarios con esos criterios.")
            self.mostrar_datos(registros)
            self.mostrar_ocultar_tabla(len(registros) > 0)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def mostrar_datos(self, registros):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        for row in registros:
            self.tabla.insert('', 'end', values=row)

    def seleccionar_fila(self, event):
        try:
            item = self.tabla.selection()[0]  # Obtiene el primer elemento seleccionado
            datos = self.tabla.item(item, 'values')  # Obtiene los valores de la fila seleccionada
            
            # Rellena los campos de entrada con los datos seleccionados
            self.entry_dni.delete(0, tk.END)
            self.entry_dni.insert(0, datos[0])
            
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, datos[1])
    
            self.combo_grado.set(datos[2])
        except IndexError:
            pass  # No hay selección

    def mostrar_ocultar_tabla(self, mostrar):
        if mostrar:
            self.tabla.pack(fill="both", expand=True)
        else:
            self.tabla.pack_forget()


if __name__ == "__main__":
    Interfaz()
