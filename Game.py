import pygame
import random

from settings import *
from player import Player
from obstacle import Obstacle
from db import get_connection

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

background = pygame.image.load("bilder/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

player = Player()
obstacles = [Obstacle(850)]

score = 0

running = True
paused = False
game_over = False
enter_name = False
show_highscores = False

name = ""

# ---------------- SQL HIGH SCORE ----------------

def save_score(name, score):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO highscores (name, score) VALUES (%s, %s)"
    cursor.execute(sql, (name, score))

    conn.commit()
    conn.close()


def load_scores():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, score FROM highscores ORDER BY score DESC LIMIT 5"
    )
    results = cursor.fetchall()

    conn.close()
    return results


def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, BLACK, rect, 2)

    txt = font.render(text, True, BLACK)
    screen.blit(txt, (x + 10, y + 10))

    return rect


# ---------------- GAME LOOP ----------------

while running:
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # ---------------- KEY INPUT ----------------
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_SPACE and not paused and not game_over:
                player.jump()

            # NAME INPUT
            if enter_name:
                if event.key == pygame.K_RETURN:
                    save_score(name, score)
                    show_highscores = True
                    enter_name = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 10:
                        name += event.unicode

            # RESTART (TASTATUR)
            if event.key == pygame.K_r and game_over and not enter_name:
                player = Player()
                obstacles = [Obstacle(850)]
                score = 0
                game_over = False
                paused = False
                show_highscores = False
                name = ""

        # ---------------- MOUSE INPUT ----------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            # GAME OVER MENU
            if game_over and not enter_name and not show_highscores:

                restart_btn = pygame.Rect(250, 180, 300, 50)
                highscore_btn = pygame.Rect(250, 250, 300, 50)

                if restart_btn.collidepoint(mx, my):
                    player = Player()
                    obstacles = [Obstacle(850)]
                    score = 0
                    game_over = False
                    paused = False
                    name = ""

                if highscore_btn.collidepoint(mx, my):
                    enter_name = True

            # HIGH SCORE SCREEN
            if show_highscores:
                restart_btn = pygame.Rect(250, 300, 300, 50)

                if restart_btn.collidepoint(mx, my):
                    player = Player()
                    obstacles = [Obstacle(850)]
                    score = 0
                    game_over = False
                    paused = False
                    show_highscores = False
                    name = ""

    # ---------------- GAME LOGIC ----------------

    if not paused and not game_over:

        player.update()

        for obstacle in obstacles:
            obstacle.move()

        for obstacle in obstacles:
            if player.rect.colliderect(obstacle.hitbox):
                game_over = True

        for obstacle in obstacles[:]:
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                score += 1

                if random.randint(1, 2) == 1:
                    obstacles.append(Obstacle(850))
                else:
                    obstacles.append(Obstacle(850))
                    obstacles.append(Obstacle(1050))

    # ---------------- DRAW ----------------

    screen.blit(background, (0, 0))

    player.draw(screen)

    for obstacle in obstacles:
        obstacle.draw(screen)

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # PAUSE
    if paused:
        pause_text = font.render("PAUSIERT", True, BLACK)
        screen.blit(pause_text, (320, 150))

    # ---------------- GAME OVER SCREEN ----------------
    if game_over and not enter_name and not show_highscores:

        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (320, 80))

        draw_button("Nochmal spielen", 250, 180, 300, 50)
        draw_button("Highscore eintragen", 250, 250, 300, 50)

    # ---------------- NAME INPUT ----------------
    if enter_name:
        txt = font.render("Name: " + name, True, BLACK)
        screen.blit(txt, (250, 150))

    # ---------------- HIGH SCORES ----------------
    if show_highscores:

        title = font.render("TOP 5", True, BLACK)
        screen.blit(title, (350, 80))

        scores = load_scores()

        y = 130
        for i, (n, s) in enumerate(scores):
            line = font.render(f"{i+1}. {n} - {s}", True, BLACK)
            screen.blit(line, (320, y))
            y += 30

        draw_button("Press R to restart", 250, 300, 300, 50)

    pygame.display.update()

pygame.quit()