# game.py
import pygame
import os
from pathlib import Path  # Utilisation de pathlib pour la portabilité des chemins
from settings import *
from level import Level, LEVEL_1_LAYOUT
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # --- GESTION ROBUSTE DES ASSETS (compatible Windows/Linux) ---
        # 1. Définir le répertoire de base : Path(__file__).parent pointe vers le dossier 'game'
        BASE_DIR = Path(__file__).parent 
        
        # 2. Construction du chemin corrigé : 
        #    [Dossier 'game'] / 'assets' / 'Social' / 'Basecolor.png'
        #    Note : On retire le .parent car 'assets' est dans le même dossier que 'game.py'
        bg_path = BASE_DIR / 'assets' / 'Basecolor.png' 
        
        # 3. Charger l'image
        try:
            # str(bg_path) est essentiel pour Pygame.image.load()
            self.background = pygame.image.load(str(bg_path)).convert()
        except pygame.error as e:
            print(f"Erreur de chargement d'image: {e}")
            print(f"Chemin de l'asset non trouvé (Chemin Absolu Tenté): {bg_path.resolve()}")
            raise e
        
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # --- Initialisation des Composants de Jeu ---
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

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.level.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            pygame.display.flip()