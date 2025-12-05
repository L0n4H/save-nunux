import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, int(TILE_SIZE * 1.5)))
        self.image.fill((0, 200, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_force = -15
        self.gravity = 0.8
        self.on_ground = False
        self.healt = 100

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_q]:
            self.vel.x = -self.speed
        if keys[pygame.K_d]:
            self.vel.x = self.speed

    def apply_gravity(self):
        self.vel.y += self.gravity
        if self.vel.y > 20:
            self.vel.y = 20

    def jump(self):
        if self.on_ground:
            self.vel.y = self.jump_force
            self.on_ground = False

    def move_and_collide(self, tiles):
        # déplacement horizontal
        self.rect.x += self.vel.x
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:   # va à droite
                    self.rect.right = tile.rect.left
                elif self.vel.x < 0: # va à gauche
                    self.rect.left = tile.rect.right

        # déplacement vertical
        self.rect.y += self.vel.y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:   # tombe
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0: # monte
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0

    def update(self, dt, tiles):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(tiles)
