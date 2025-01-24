import pygame
import csv
import random
import time

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Quiz de Historia Argentina")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fuentes
FONT = pygame.font.Font(None, 36)

# Cargar imágenes
BACKGROUND_IMG = pygame.image.load("assets/background.png")
CHARACTER_IMG = pygame.image.load("assets/character.png")

# Preguntas (CSV)
QUESTIONS_FILE = "preguntas.csv"
questions = []

# Cargar preguntas desde un archivo CSV con validación
def load_questions():
    global questions
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            questions = [
                row for row in reader
                if len(row) >= 5 and row[-1].isdigit()  # Validar formato: al menos 5 columnas y el último valor es un número
            ]
    except FileNotFoundError:
        print("Archivo de preguntas no encontrado.")
        questions = [
            ["¿En qué año fue la Revolución de Mayo?", "1810", "1816", "1806", "0"],
            ["¿Quién fue el primer presidente argentino?", "Rivadavia", "San Martín", "Belgrano", "0"],
            ["¿Qué batalla marcó el fin del dominio español?", "Tucumán", "Ayacucho", "Salta", "1"],
        ]

# Dibujar texto centrado
def draw_text(text, font, color, x, y):
    render = font.render(text, True, color)
    rect = render.get_rect(center=(x, y))
    screen.blit(render, rect)

# Dibujar botón con bordes redondeados
def draw_rounded_button(rect, color, border_color, text, font, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, border_color, rect, width=2, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Redibujar fondo y personaje en tiempo real
def redraw_screen():
    width, height = screen.get_size()
    screen.blit(pygame.transform.scale(BACKGROUND_IMG, (width, height)), (0, 0))
    character_resized = pygame.transform.scale(CHARACTER_IMG, (width // 6, height // 3))
    character_rect = character_resized.get_rect(center=(width // 4, height // 2))
    screen.blit(character_resized, character_rect)
    return character_rect

def show_final_screen(correct_answers, total_questions):
    width, height = screen.get_size()
    screen.blit(pygame.transform.scale(BACKGROUND_IMG, (width, height)), (0, 0))  # Mantener el fondo del juego
    draw_text("¡Fin del juego!", FONT, BLACK, width // 2, height // 4)
    draw_text(f"Respuestas correctas: {correct_answers}/{total_questions}", FONT, BLACK, width // 2, height // 2)
    
    # Botones de acción
    button_width, button_height = 250, 80
    replay_button = pygame.Rect((width // 2 - 300, height // 1.5), (button_width, button_height))
    menu_button = pygame.Rect((width // 2 + 50, height // 1.5), (button_width, button_height))
    
    draw_rounded_button(replay_button, GREEN, BLACK, "Volver a jugar", FONT, WHITE)
    draw_rounded_button(menu_button, RED, BLACK, "Volver al menú", FONT, WHITE)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if replay_button.collidepoint(event.pos):
                    return "replay"
                elif menu_button.collidepoint(event.pos):
                    return "menu"


# Main loop
def main():
    global screen
    load_questions()

    # Validar que haya suficientes preguntas
    if len(questions) < 10:
        print("No hay suficientes preguntas válidas.")
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
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            if current_question < len(selected_questions):
                question, *options, correct_index = selected_questions[current_question]
                correct_index = int(correct_index)

                # Dibujar pregunta
                draw_text(question, FONT, BLACK, width // 2, height // 10)

                # Dibujar opciones
                option_buttons = []
                button_width, button_height = max(width // 3, 350), max(height // 12, 60)
                for i, option in enumerate(options):
                    button_rect = pygame.Rect(width // 2 - button_width // 2 + 150, height // 4 + (i + 1) * (button_height + 20), button_width, button_height)
                    option_buttons.append(button_rect)
                    draw_rounded_button(button_rect, WHITE, BLACK, option[:60], FONT, BLACK)

                pygame.display.flip()

                # Esperar respuesta
                clicked = False
                while not clicked:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            for i, button in enumerate(option_buttons):
                                if button.collidepoint(event.pos):
                                    clicked = True
                                    if i == correct_index:
                                        draw_rounded_button(button, GREEN, BLACK, options[i], FONT, WHITE)
                                        correct_answers += 1
                                    else:
                                        draw_rounded_button(button, RED, BLACK, options[i], FONT, WHITE)
                                    pygame.display.flip()
                                    time.sleep(1)
                                    current_question += 1

            else:
                # Pantalla final
                action = show_final_screen(correct_answers, len(selected_questions))
                if action == "replay":
                    break
                elif action == "menu":
                    running = False
                    break

if __name__ == "__main__":
    main()
