# player.py

import pygame
import os
from pathlib import Path
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # facteur de zoom du perso
        self.SCALE_FACTOR = 1.5  # essaie 1.5, 2, 3...

        # --- chargement du spritesheet ---
        BASE_DIR = Path(__file__).parent 
        sheet_path = BASE_DIR / 'assets' / 'player'/'player.png' 
        self.spritesheet = pygame.image.load(str(sheet_path)).convert()

        # paramètres du sheet
        self.rows = 4          # 4 lignes
        self.cols = 8          # à ajuster si besoin

        sheet_w, sheet_h = self.spritesheet.get_size()
        frame_w = sheet_w // self.cols
        frame_h = sheet_h // self.rows

        # largeur/hauteur après zoom
        scale_w = int(TILE_SIZE * self.SCALE_FACTOR)
        scale_h = int(scale_w * (frame_h / frame_w))

        # --- frame d'idle : 1ère ligne, 1ère colonne ---
        idle_rect = pygame.Rect(0, 0, frame_w, frame_h)
        idle = self.spritesheet.subsurface(idle_rect)
        self.idle_frame = pygame.transform.scale(idle, (scale_w, scale_h))

        # --- récupération des frames de course (dernière ligne) ---
        run_row = self.rows - 1  # 0,1,2,3 -> 3 = 4e ligne
        self.run_frames = []

        for c in range(self.cols):
            rect = pygame.Rect(c * frame_w, run_row * frame_h, frame_w, frame_h)
            frame = self.spritesheet.subsurface(rect)
            frame = pygame.transform.scale(frame, (scale_w, scale_h))
            self.run_frames.append(frame)

        # état initial
        self.frame_index = 0
        self.animation_speed = 12   # images de course par seconde
        self.anim_timer = 0
        self.facing_right = True

        # image et rect de départ = idle
        self.image = self.idle_frame
        self.rect = self.image.get_rect(topleft=(x, y))

        # physique
        self.vel = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.jump_force = -15
        self.gravity = 0.8
        self.on_ground = False
        self.max_health = 100
        self.health = 100

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
                if self.vel.x > 0:      # va à droite
                    self.rect.right = tile.rect.left
                elif self.vel.x < 0:    # va à gauche
                    self.rect.left = tile.rect.right

        # déplacement vertical
        self.rect.y += self.vel.y
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:      # tombe
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:    # monte
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
            # idle = frame (1,1), orientée dans la dernière direction
            img = self.idle_frame
            if not self.facing_right:
                img = pygame.transform.flip(img, True, False)

            self.image = img
            # on reset l'anim de course
            self.frame_index = 0
            self.anim_timer = 0

    def update(self, dt, tiles):
        self.handle_input()
        self.apply_gravity()
        self.move_and_collide(tiles)
        self.animate(dt)
