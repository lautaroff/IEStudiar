import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class JuegosSS:
    def __init__(self, nombre, ventana):
        self.nombre = nombre
        self.ventana = ventana
        self.ventana.title("Menú de Materias")
        self.ventana.geometry("1280x720")

        # Lista para almacenar referencias a las imágenes de los botones
        self.imagenes_botones = []

        # Construir la ruta base: sube un nivel desde "interfaz" a la raíz y entra en "imagenes"
        ruta_imagenes = os.path.join(os.path.dirname(__file__), "..", "imagenes")

        # Cargar la imagen de fondo (menu-juegos-ciencias-sociales.png)
        fondo_path = os.path.join(ruta_imagenes, "menu-juegos-ciencias-sociales.png")
        try:
            self.imagen_original = Image.open(fondo_path)
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
        ruta_imagenes = os.path.join(os.path.dirname(__file__), "..", "imagenes")
        # Utilizamos la misma imagen para todos los botones (boton-jugar-ciencias-sociales.png)
        imagen_boton_path = os.path.join(ruta_imagenes, "boton-jugar-ciencias-sociales.png")
        self.boton(imagen_boton_path, 0.170, self.juego_adivinanzas)
        self.boton(imagen_boton_path, 0.387, self.juego_rompecabezas)
        self.boton(imagen_boton_path, 0.601, self.juego_sopa_de_letras)
        self.boton(imagen_boton_path, 0.83, self.juego_quiz)

    def boton(self, ref, pos, fun):
        try:
            imagen_boton = Image.open(ref)
            imagen_boton = imagen_boton.resize((100, 35))
            imagen_boton_tk = ImageTk.PhotoImage(imagen_boton)
            self.imagenes_botones.append(imagen_boton_tk)
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
            self.canvas.imagen_fondo = imagen_fondo

    def cerrar_menu(self):
        self.ventana.destroy()

    def juego_rompecabezas(self):
        print("Ingreso juego rompecabezas")

    def juego_sopa_de_letras(self):
        print("Ingreso juego sopa de letras")

    def juego_quiz(self):
        import subprocess, os
        self.cerrar_menu()  # Cierra la ventana del menú

        # Construir la ruta absoluta hacia quiz.py (que se encuentra en juegos/quiz/)
        quiz_path = os.path.join(os.path.dirname(__file__), "..", "juegos", "quiz", "quiz.py")
        quiz_path = os.path.abspath(quiz_path)
        subprocess.Popen(['python', quiz_path])

    def juego_adivinanzas(self):
        print("Ingreso juego adivinanzas")

def crear_menu_juegosSS(nombre, ventana):
    JuegosSS(nombre, ventana)
