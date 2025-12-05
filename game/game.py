# game.py
import pygame
from settings import *
from level import Level, LEVEL_1_LAYOUT
import os
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        bg_path = os.path.join("assets", "Basecolor.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        self.level = Level(LEVEL_1_LAYOUT)

        
        self.player = Player(100, 100)
        self.solid_tiles = self.level.tiles.sprites()



    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update(self, dt):
        self.player.update(dt, self.solid_tiles)



    def draw_health_bar(self):

        bar_x = 20
        bar_y = 20
        bar_width = 200
        bar_height = 20


        ratio = self.player.health / self.player.max_health
        current_width = int(bar_width * ratio)

        # fond (barre vide)
        pygame.draw.rect(self.screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))

        pygame.draw.rect(self.screen, (200, 50, 50), (bar_x, bar_y, current_width, bar_height))
        # contour
        pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

    def draw(self):

        self.screen.blit(self.background, (0, 0))
        self.level.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_health_bar()


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # secondes
            self.handle_events()
            self.update(dt)
            self.draw()
            pygame.display.flip()
