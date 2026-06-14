import pygame
from settings import GROUND_Y


class Player:
    def __init__(self):
        self.image = pygame.image.load("bilder/dino.png").convert_alpha()

        # Dino verkleinern
        self.image = pygame.transform.scale(self.image, (55, 80))

        self.rect = self.image.get_rect()

        self.rect.x = 100
        self.rect.y = GROUND_Y - self.rect.height  # automatisch auf Boden

        # Kleinere Kollisionsbox (innerhalb des Bildes, damit es fair wirkt)
        self.hitbox = pygame.Rect(
            self.rect.x + 8,
            self.rect.y + 8,
            self.rect.width - 16,
            self.rect.height - 10
        )

        self.velocity_y = 0
        self.gravity = 1
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.velocity_y = -18
            self.jumping = True

    def update(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        ground = GROUND_Y - self.rect.height
        if self.rect.y >= ground:
            self.rect.y = ground
            self.velocity_y = 0
            self.jumping = False

        # Hitbox mit Bild mitbewegen
        self.hitbox.x = self.rect.x + 8
        self.hitbox.y = self.rect.y + 8

    def draw(self, screen):
        screen.blit(self.image, self.rect)
