import pygame
from settings import GROUND_Y


class Obstacle:
    def __init__(self, start_x):
        self.image = pygame.image.load("bilder/cactus.png").convert_alpha()

        # Kaktus verkleinern
        self.image = pygame.transform.scale(self.image, (45, 65))

        self.rect = self.image.get_rect()

        self.rect.x = start_x
        self.rect.y = GROUND_Y - self.rect.height

        # Kleinere Kollisionsbox
        self.hitbox = pygame.Rect(
            self.rect.x + 6,
            self.rect.y + 5,
            self.rect.width - 12,
            self.rect.height - 5
        )

        self.speed = 5

    def move(self):
        self.rect.x -= self.speed
        self.hitbox.x = self.rect.x + 6

    def draw(self, screen):
        screen.blit(self.image, self.rect)