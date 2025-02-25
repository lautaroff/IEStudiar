import os
import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk
from juegosSS import *

class MenuMaterias:
    def __init__(self, nombre, ventana):
        self.nombre = nombre
        self.ventana = ventana
        self.ventana.title("Menú de Materias")
        self.ventana.geometry("1280x720")

        # Lista para almacenar referencias a las imágenes de los botones
        self.imagenes_botones = []

        # Construir la ruta absoluta para la imagen de fondo
        ruta_fondo = os.path.join(os.path.dirname(__file__), "..", "imagenes", "fondo-materias.png")
        try:
            self.imagen_original = Image.open(ruta_fondo)
            self.imagen_fondo = ImageTk.PhotoImage(self.imagen_original)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
            return

        # Crear un canvas para la imagen de fondo
        self.canvas = tk.Canvas(self.ventana, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Añadir la imagen al canvas
        self.imagen_canvas = self.canvas.create_image(0, 0, image=self.imagen_fondo, anchor="nw")
        self.canvas.imagen_fondo = self.imagen_fondo  # Guardar referencia

        # Crear los botones
        self.crear_botones()

        # Vincular el evento de redimensionamiento para ajustar la imagen
        self.ventana.bind("<Configure>", self.ajustar_imagen)

    def crear_botones(self):
        # Ruta base para las imágenes de los botones (están en la carpeta 'imagenes' del proyecto)
        ruta_base = os.path.join(os.path.dirname(__file__), "..", "imagenes")
        self.boton(os.path.join(ruta_base, 'boton-jugar-ciencias-naturales.png'), 0.612, self.juegos_naturales)
        self.boton(os.path.join(ruta_base, 'boton-jugar-lengua.png'), 0.390, self.juegos_lengua)
        self.boton(os.path.join(ruta_base, 'boton-jugar-matematicas.png'), 0.807, self.juegos_matematica)
        self.boton(os.path.join(ruta_base, 'boton-jugar-ciencias-sociales.png'), 0.195, self.juegos_sociales)

    def boton(self, ref, pos, fun):
        try:
            imagen_boton = Image.open(ref)
            imagen_boton = imagen_boton.resize((90, 25))
            imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)
            self.imagenes_botones.append(imagen_boton_tk)
            boton_imagen = tk.Label(self.ventana, image=imagen_boton_tk, bg='white')
            boton_imagen.place(relx=pos, rely=0.412, anchor="center")
            boton_imagen.bind("<Button-1>", lambda e: fun())
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen del botón: {e}")

    def ajustar_imagen(self, event):
        nuevo_ancho = self.ventana.winfo_width()
        nuevo_alto = self.ventana.winfo_height()
        if nuevo_ancho > 1 and nuevo_alto > 1:
            imagen_redimensionada = self.imagen_original.resize((nuevo_ancho, nuevo_alto))
            imagen_fondo = ImageTk.PhotoImage(imagen_redimensionada)
            self.canvas.itemconfig(self.imagen_canvas, image=imagen_fondo)
            self.canvas.imagen_fondo = imagen_fondo

    def cerrar_menu(self):
        self.ventana.destroy()  # Cierra la ventana del menú

    def juegos_naturales(self):
        print("Ingreso juego naturales")

    def juegos_matematica(self):
        print("Ingreso juego matematicas")

    def juegos_sociales(self):
        # Se eliminan los widgets y se llama a crear_menu_juegosSS para cargar el menú de juegos sociales
        for widget in self.ventana.winfo_children():
            widget.destroy()  
        crear_menu_juegosSS(self.nombre, self.ventana)

    def juegos_lengua(self):
        print("Ingreso juego lengua")

def crear_menu_materias(nombre, ventana):
    MenuMaterias(nombre, ventana)
