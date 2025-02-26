import os
import sys
import pygame
import csv
import random
import time
import tkinter as tk  # Para lanzar el menú de Tkinter al finalizar el juego

pygame.init()

# Rutas basadas en la ubicación de quiz.py
BASE_DIR = os.path.dirname(__file__)
BACKGROUND_IMG = os.path.join(BASE_DIR, 'assets', 'background.png')
CHARACTER_IMG = os.path.join(BASE_DIR, 'assets', 'character.png')
QUESTIONS_FILE = os.path.join(BASE_DIR, 'preguntas.csv')

# Cargar imágenes de fondo y personaje
try:
    background = pygame.image.load(BACKGROUND_IMG)
    character = pygame.image.load(CHARACTER_IMG)
except Exception as e:
    print("Error al cargar imágenes:", e)
    sys.exit(1)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Quiz de Historia Argentina")

# Colores y fuente
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)
questions = []

def load_questions():
    global questions
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rows = list(reader)
            # Si la primera fila es cabecera, se descarta
            if rows and rows[0] and rows[0][0].strip().lower().startswith("pregunta"):
                rows = rows[1:]
            questions = [row for row in rows if len(row) >= 5 and row[-1].strip().isdigit()]
    except Exception as e:
        print("Error al cargar preguntas, usando preguntas por defecto.", e)
        questions = [
            ["¿En qué año fue la Revolución de Mayo?", "1810", "1816", "1806", "0"],
            ["¿Quién fue el primer presidente argentino?", "Rivadavia", "San Martín", "Belgrano", "0"],
            ["¿Qué batalla marcó el fin del dominio español?", "Tucumán", "Ayacucho", "Salta", "1"],
        ]

def draw_text(text, font, color, x, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)

def draw_rounded_button(rect, color, border_color, text, font, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def redraw_screen():
    width, height = screen.get_size()
    bg_scaled = pygame.transform.scale(background, (width, height))
    screen.blit(bg_scaled, (0, 0))
    char_resized = pygame.transform.scale(character, (width // 3, height // 3))
    char_rect = char_resized.get_rect()
    char_rect.left = width // 4 - char_rect.width // 2
    char_rect.centery = height // 2
    screen.blit(char_resized, char_rect)

def show_final_screen(correct_answers, total_questions):
    width, height = screen.get_size()
    bg_scaled = pygame.transform.scale(background, (width, height))
    screen.blit(bg_scaled, (0, 0))
    draw_text("¡Fin del juego!", FONT, BLACK, width // 2, height // 6)
    draw_text(f"Respuestas correctas: {correct_answers}/{total_questions}", FONT, BLACK, width // 2, height // 3)
    
    button_width, button_height = 250, 80
    replay_button = pygame.Rect(width // 2 - 300, int(height * 0.65), button_width, button_height)
    menu_button = pygame.Rect(width // 2 + 50, int(height * 0.65), button_width, button_height)
    
    draw_rounded_button(replay_button, GREEN, BLACK, "Volver a jugar", FONT, WHITE)
    draw_rounded_button(menu_button, RED, BLACK, "Volver al menú", FONT, WHITE)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if replay_button.collidepoint(event.pos):
                    return "replay"
                elif menu_button.collidepoint(event.pos):
                    # Cerrar Pygame y abrir el menú usando crear_menu_juegosSS() importado desde juegosSS.py
                    pygame.quit()
                    # Agregar la carpeta "interfaz" a sys.path para poder importar juegosSS.py
                    interfaz_path = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "interfaz"))
                    if interfaz_path not in sys.path:
                        sys.path.insert(0, interfaz_path)
                    try:
                        from juegosSS import crear_menu_juegosSS
                        root = tk.Tk()
                        crear_menu_juegosSS("Nombre", root)
                        root.mainloop()
                    except Exception as e:
                        print("Error al abrir el menú:", e)
                    sys.exit()

def main():
    global screen
    load_questions()
    if len(questions) < 10:
        print("No hay suficientes preguntas válidas en preguntas.csv.")
        return

    while True:
        selected_questions = random.sample(questions, 10)
        current_question = 0
        correct_answers = 0
        running = True

        while running:
            width, height = screen.get_size()
            redraw_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if current_question < len(selected_questions):
                question, *options, correct_index = selected_questions[current_question]
                correct_index = int(correct_index)

                draw_text(question, FONT, BLACK, width // 2, height // 10)

                option_buttons = []
                button_width, button_height = max(width // 3, 350), max(height // 12, 60)
                start_y = height // 4
                for i, option in enumerate(options):
                    button_rect = pygame.Rect(width // 2 - button_width // 2 + 150,
                                                start_y + i * (button_height + 20),
                                                button_width,
                                                button_height)
                    option_buttons.append(button_rect)
                    draw_rounded_button(button_rect, WHITE, BLACK, option, FONT, BLACK)

                pygame.display.flip()

                answered = False
                while not answered:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            for i, button in enumerate(option_buttons):
                                if button.collidepoint(event.pos):
                                    answered = True
                                    if i == correct_index:
                                        draw_rounded_button(button, GREEN, BLACK, options[i], FONT, WHITE)
                                        correct_answers += 1
                                    else:
                                        draw_rounded_button(button, RED, BLACK, options[i], FONT, WHITE)
                                    pygame.display.flip()
                                    time.sleep(1)
                                    current_question += 1
                                    break
            else:
                action = show_final_screen(correct_answers, len(selected_questions))
                if action == "replay":
                    break

if __name__ == "__main__":
    main()
