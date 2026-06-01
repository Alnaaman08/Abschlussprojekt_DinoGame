import pygame
from settings import RED


class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(800, 320, 30, 30)
        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

    def reset(self):
        self.rect.x = 800

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)