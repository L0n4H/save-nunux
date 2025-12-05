# boss.py

import pygame
from settings import *          # TILE_SIZE, ENEMY_SPEED, ENEMY_GRAVITY
from ennemy import Ennemy       # collisions / gravité déjà faites


class Boss(Ennemy):
    def __init__(self, x, y, health):
        super().__init__(x, y, health)

        # Cube rouge un peu plus gros qu'un ennemi
        width = int(TILE_SIZE * 1.5)
        height = int(TILE_SIZE * 1.5)
        self.image = pygame.Surface((width, height))
        self.image.fill((200, 0, 0))

        # Même logique de position que Ennemy -> topleft
        self.rect = self.image.get_rect(topleft=(x, y))

        # Un peu plus lent/rapide si tu veux, sinon garde ENEMY_SPEED
        self.speed = ENEMY_SPEED

    def update(self, dt, solid_tiles, player):
        if not self.alive:
            return

        # Suivre le joueur horizontalement
        if player.rect.centerx < self.rect.centerx:
            self.direction.x = -1
        elif player.rect.centerx > self.rect.centerx:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Utiliser EXACTEMENT la même physique que Ennemy
        super().update(dt, solid_tiles)

    def draw_health_bar(self, surface):
        bar_width = self.rect.width
        bar_height = 6
        bar_x = self.rect.left
        bar_y = self.rect.top - 10

        ratio = self.current_health / self.max_health

        pygame.draw.rect(surface, (60, 60, 60),
                         (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (200, 0, 0),
                         (bar_x, bar_y, bar_width * ratio, bar_height))
        pygame.draw.rect(surface, (255, 255, 255),
                         (bar_x, bar_y, bar_width, bar_height), 1)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)
