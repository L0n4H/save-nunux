# boss.py

import pygame
from settings import *          # pour TILE_SIZE, ENEMY_SPEED, ENEMY_GRAVITY
from ennemy import Ennemy       # on réutilise toute la logique d'Ennemy


class Boss(Ennemy):
    def __init__(self, x, y, health):
        super().__init__(x, y, health)

        # Sprite plus grand : gros carré rouge (3x3 tiles)
        self.image = pygame.Surface((TILE_SIZE * 3, TILE_SIZE * 3))
        self.image.fill((200, 0, 0))

        # Recalcule le rect par rapport à la nouvelle image
        # x, y sera la position du "pied" du boss (milieu bas)
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Optionnel : un peu plus lent qu'un ennemi normal
        self.speed = ENEMY_SPEED * 0.6

    def update(self, dt, solid_tiles, player):
        """Met à jour le boss en le faisant suivre le joueur."""
        if not self.alive:
            return

        # IA simple : suit le joueur horizontalement
        if player.rect.centerx < self.rect.centerx:
            self.direction.x = -1
        elif player.rect.centerx > self.rect.centerx:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Réutilise les collisions déjà codées dans Ennemy
        self.horizontal_movement_collision(solid_tiles, dt)
        self.vertical_movement_collision(solid_tiles, dt)

    def draw_health_bar(self, surface):
        """Dessine la barre de vie au-dessus du boss."""
        bar_width = self.rect.width
        bar_height = 8
        bar_x = self.rect.left
        bar_y = self.rect.top - 12

        ratio = self.current_health / self.max_health

        # fond (barre vide)
        pygame.draw.rect(surface, (60, 60, 60),
                         (bar_x, bar_y, bar_width, bar_height))
        # vie actuelle
        pygame.draw.rect(surface, (200, 0, 0),
                         (bar_x, bar_y, bar_width * ratio, bar_height))
        # contour
        pygame.draw.rect(surface, (255, 255, 255),
                         (bar_x, bar_y, bar_width, bar_height), 2)

    def draw(self, surface):
        """Dessine le boss + sa barre de vie."""
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)
