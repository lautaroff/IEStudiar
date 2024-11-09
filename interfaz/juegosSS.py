import tkinter as tk
from tkinter import  messagebox
from PIL import Image, ImageTk

class JuegosSS:
    def __init__(self, nombre, ventana):
        self.nombre = nombre
        self.ventana = ventana
        self.ventana.title("Menú de Materias")
        self.ventana.geometry("1280x720")

        # Lista para almacenar referencias a las imágenes de los botones
        self.imagenes_botones = []  # Aquí almacenamos las imágenes de los botones

        # Cargar la imagen de fondo
        try:
            self.imagen_original = Image.open('imagenes/menu-juegos-ciencias-sociales.png')
            self.imagen_fondo = ImageTk.PhotoImage(self.imagen_original)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")
            return

        # Crear un canvas para la imagen de fondo
        self.canvas = tk.Canvas(self.ventana, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)

        # Añadir la imagen al canvas
        self.imagen_canvas = self.canvas.create_image(0, 0, image=self.imagen_fondo, anchor="nw")
        self.canvas.imagen_fondo = self.imagen_fondo  # Guardar referencia de la imagen de fondo

        # Crear los botones
        self.crear_botones()

        # Vincular el evento de redimensionamiento para ajustar la imagen
        self.ventana.bind("<Configure>", self.ajustar_imagen)

    def crear_botones(self):
        self.boton('imagenes/boton-jugar-ciencias-sociales.png', 0.170, self.juego_adivinanzas)
        self.boton('imagenes/boton-jugar-ciencias-sociales.png', 0.387, self.juego_rompecabezas)
        self.boton('imagenes/boton-jugar-ciencias-sociales.png', 0.601, self.juego_sopa_de_letras)
        self.boton('imagenes/boton-jugar-ciencias-sociales.png', 0.83, self.juego_quiz)

    def boton(self, ref, pos, fun):
        try:
            imagen_boton = Image.open(ref)
            imagen_boton = imagen_boton.resize((100, 35))  # Ajustar el tamaño del botón si es necesario
            imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)

            # Guardar referencia a la imagen para evitar que el Garbage Collector la elimine
            self.imagenes_botones.append(imagen_boton_tk)

            # Crear un Label que actúe como botón
            boton_imagen = tk.Label(self.ventana, image=imagen_boton_tk, bg='white')
            boton_imagen.place(relx=pos, rely=0.628, anchor="center")
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
            self.canvas.imagen_fondo = imagen_fondo  # Guardar referencia para evitar que desaparezca

    def cerrar_menu(self):
        self.ventana.destroy()  # Solo cerramos la ventana del menú

    def juego_rompecabezas(self):
        print("Ingreso juego rompecabezas")

    def juego_sopa_de_letras(self):
        print("Ingreso juego sopa de letras")

    def juego_quiz(self):
        print("Ingreso juego quiz")

    def juego_adivinanzas(self):
        print("Ingreso juego adivinanzas")

# Función para llamar desde main.py
def crear_menu_juegosSS(nombre, ventana):
    JuegosSS(nombre, ventana)

