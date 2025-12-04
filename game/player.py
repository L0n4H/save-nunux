# player.py
import pygame
import os
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # --- chargement du spritesheet ---
        sheet_path = os.path.join("assets", "player", "player.png")
        self.spritesheet = pygame.image.load(sheet_path).convert_alpha()

        # paramètres du sheet
        self.rows = 4           # 4 lignes
        self.cols = 8           # <-- à ajuster selon ton image
        sheet_w, sheet_h = self.spritesheet.get_size()
        frame_w = sheet_w // self.cols
        frame_h = sheet_h // self.rows

        # --- récupération des frames de course (dernière ligne) ---
        run_row = self.rows - 1   # 0,1,2,3 -> 3 = 4e ligne
        self.run_frames = []
        for c in range(self.cols):
            rect = pygame.Rect(c * frame_w, run_row * frame_h, frame_w, frame_h)
            frame = self.spritesheet.subsurface(rect)

            # optionnel : redimensionner à ta grille
            scale_h = int(TILE_SIZE * (frame_h / frame_w))
            frame = pygame.transform.scale(frame, (TILE_SIZE, scale_h))

            self.run_frames.append(frame)

        # état initial
        self.frame_index = 0
        self.animation_speed = 12   # images de course par seconde
        self.anim_timer = 0
        self.facing_right = True

        self.image = self.run_frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        # physique
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_force = -15
        self.gravity = 0.8
        self.on_ground = False


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

    def animate(self, dt):
        # si on bouge horizontalement -> animer la course
        if self.vel.x != 0:
            self.anim_timer += dt
            if self.anim_timer >= 1 / self.animation_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % len(self.run_frames)

            img = self.run_frames[self.frame_index]

            # orientation
            if self.vel.x < 0:
                img = pygame.transform.flip(img, True, False)
                self.facing_right = False
            else:
                self.facing_right = True

            self.image = img
        else:
            # idle = première frame, orientée dans la dernière direction
            base = self.run_frames[0]
            if self.facing_right:
                self.image = base
            else:
                self.image = pygame.transform.flip(base, True, False)

    def update(self, dt, tiles):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(tiles)
        self.animate(dt)