import pygame
from settings import GROUND_Y, BLACK


class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, GROUND_Y, 50, 50) # Spielerrechteck
        self.velocity_y = 0 # Vertikale Geschwindigkeit
        self.gravity = 1 
        self.jumping = False # speichert, ob der Spieler gerade springt

    def jump(self):
        if not self.jumping:
            self.velocity_y = -15 # Fenster (0,0) ist oben links
            self.jumping = True # Verhindert Doppel-Sprung

    def update(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= GROUND_Y:
            self.rect.y = GROUND_Y
            self.velocity_y = 0
            self.jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)