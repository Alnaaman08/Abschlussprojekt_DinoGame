import pygame

from settings import *
from player import Player
from obstacle import Obstacle

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

player = Player()
obstacle = Obstacle()

score = 0

running = True
paused = False
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get(): #prüft Tastendrücke und Fenstereignisse
        if event.type == pygame.QUIT: #Fenster schließen
            running = False

        if event.type == pygame.KEYDOWN:

            # Pause
            if event.key == pygame.K_p: 
                paused = not paused

            # Neustart
            if event.key == pygame.K_r and game_over:
                player = Player()
                obstacle = Obstacle()

                score = 0
                game_over = False
                paused = False

            # Springen
            if (
                event.key == pygame.K_SPACE
                and not paused
                and not game_over
            ):
                player.jump()

    if not paused and not game_over: # nur aktualisieren, wenn nicht pausiert oder game over

        player.update()
        obstacle.update()

        if obstacle.rect.x < -30:
            obstacle.reset()
            score += 1

        if player.rect.colliderect(obstacle.rect): # Kollisionserkennung
            game_over = True

    screen.fill(WHITE)

    player.draw(screen)
    obstacle.draw(screen)

    score_text = font.render(
        f"Score: {score}",
        True,
        BLACK
    )

    screen.blit(score_text, (10, 10))

    if paused:
        pause_text = font.render(
            "PAUSIERT",
            True,
            BLACK
        )
        screen.blit(pause_text, (320, 150))

    if game_over:
        game_over_text = font.render(
            "GAME OVER - R zum Neustart",
            True,
            RED
        )
        screen.blit(game_over_text, (140, 150))

    pygame.display.update()

pygame.quit()