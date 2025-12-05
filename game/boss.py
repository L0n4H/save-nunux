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

        # Vitesse identique à un ennemi classique
        self.speed = ENEMY_SPEED

        # Paramètres de saut (à ajuster si besoin)
        self.jump_force = -450      # vers le haut
        self.can_jump = True        # évite le spam

    def _should_jump(self, solid_tiles):
        """Retourne True si un obstacle est juste devant le boss."""
        # Il doit être au sol et se déplacer
        if not self.on_ground or self.direction.x == 0:
            return False

        # Zone de détection devant, à hauteur des jambes
        offset_x = 8 if self.direction.x > 0 else -8

        # Petit rectangle devant, sur le tiers inférieur du boss
        check_height = self.rect.height // 2
        check_y = self.rect.bottom - check_height
        check_rect = pygame.Rect(
            self.rect.x + offset_x,
            check_y,
            self.rect.width,
            check_height
        )

        for tile in solid_tiles:
            if tile.rect.colliderect(check_rect):
                # On ignore les tiles complètement sous les pieds
                if tile.rect.top < self.rect.bottom - 2:
                    return True

        return False

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

        # Si obstacle juste devant et qu'on peut sauter -> impulsion vers le haut
        if self._should_jump(solid_tiles) and self.can_jump:
            self.direction.y = self.jump_force
            self.on_ground = False
            self.can_jump = False

        # Utiliser EXACTEMENT la même physique que Ennemy
        super().update(dt, solid_tiles)

        # Quand il retouche le sol, on réautorise un saut
        if self.on_ground:
            self.can_jump = True

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
