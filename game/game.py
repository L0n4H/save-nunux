# game.py
import pygame
from settings import *
from level import Level, LEVEL_1_LAYOUT

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        self.level = Level(LEVEL_1_LAYOUT)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        # pour l’instant, pas de logique
        pass

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.level.draw(self.screen)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # secondes
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
