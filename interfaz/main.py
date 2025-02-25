import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from conexion import *
from usuario import verificar_usuario
from menu import crear_menu_materias
import sys
import os

class IngresoUsuario:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Ingreso de Usuario")
        self.ventana.geometry("1280x72230")
        # Cargar la imagen de fondo
        self.cargar_imagen_fondo()

        # Si ocurrió un error y la ventana se destruyó, salimos inmediatamente
        if not self.ventana.winfo_exists():
            sys.exit()

        # Crear un canvas para la imagen de fondo
        self.canvas = tk.Canvas(self.ventana, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Añadir la imagen al canvas
        self.imagen_canvas = self.canvas.create_image(0, 0, image=self.imagen_fondo, anchor="nw")

        # Crear widgets de entrada y botón
        self.crear_widgets()

        # Vincular el evento de redimensionamiento para ajustar la imagen
        self.ventana.bind("<Configure>", self.ajustar_imagen)

        # Iniciar el loop principal
        self.ventana.mainloop()

    def cargar_imagen_fondo(self):
        try:
            # Calcula la ruta absoluta de la imagen: sube un nivel y entra en la carpeta 'imagenes'
            ruta_imagen = os.path.join(os.path.dirname(__file__), "..", "imagenes", "ingreso-alumnos.png")
            self.imagen_original = Image.open(ruta_imagen)
            self.imagen_fondo = ImageTk.PhotoImage(self.imagen_original)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
            self.ventana.destroy()
            import sys
            sys.exit()

    def crear_widgets(self):
        # Estilo personalizado para la entrada
        style = ttk.Style()
        style.theme_use('clam')
        style.element_create("Custom.Entry", "from", "clam")
        style.layout("Custom.TEntry", [('Entry.background', {'children': [('Entry.padding', {'children': [('Entry.textarea', {'sticky': 'nswe'})], 'sticky': 'nswe'})], 'sticky': 'nswe'})])
        style.configure("Custom.TEntry", background="#FFFFFF", borderwidth=0, relief="flat", padding=(11, 12))

        self.entrada = ttk.Entry(self.ventana, style="Custom.TEntry", width=30, font=('Comic Sans MS', 15))
        self.entrada.place(relx=0.265, rely=0.582, anchor="center")

        try:
            imagen_boton = Image.open(r"C:\Users\laufe\OneDrive\Escritorio\programacion\practica\imagenes\boton-ingresar.png")
            self.imagen_boton_original = imagen_boton.resize((180, 59))
            self.imagen_boton_tk = ImageTk.PhotoImage(self.imagen_boton_original)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del botón: {e}")
            self.ventana.destroy()
            sys.exit()

        # Crear un Label que actúe como botón
        self.boton_imagen = tk.Label(self.ventana, image=self.imagen_boton_tk, bg='#f6f6f6')
        self.boton_imagen.place(relx=0.265, rely=0.68, anchor="center")

        # Asignar el evento de clic
        self.boton_imagen.bind("<Button-1>", lambda e: self.manejar_ingreso())

    def ajustar_imagen(self, event):
        nuevo_ancho = self.ventana.winfo_width()
        nuevo_alto = self.ventana.winfo_height()

        if nuevo_ancho > 1 and nuevo_alto > 1:
            # Redimensionar la imagen de fondo
            imagen_redimensionada = self.imagen_original.resize((nuevo_ancho, nuevo_alto))
            self.imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)

            self.canvas.itemconfig(self.imagen_canvas, image=self.imagen_fondo)
            self.canvas.imagen_fondo = self.imagen_fondo  # Guardar referencia

    def manejar_ingreso(self):
        DNI = self.entrada.get().strip()
        if DNI:
            nombre = verificar_usuario(DNI)
            if nombre:
                messagebox.showinfo("Éxito", f"Bienvenido {nombre}.")
                for widget in self.ventana.winfo_children():
                    widget.destroy()  # Eliminar todos los widgets de la ventana principal
                crear_menu_materias(nombre, self.ventana)  # Cambiar el contenido a la vista del menú
            else:
                messagebox.showwarning("Advertencia", "DNI no válido.")
        else:
            messagebox.showwarning("Advertencia", "El campo DNI no puede estar vacío.")

if __name__ == "__main__":
    IngresoUsuario()
