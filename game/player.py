# player.py

import pygame
import os

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # facteur de zoom du perso
        self.SCALE_FACTOR = 1.5  # essaie 1.5, 2, 3...

        # --- chargement du spritesheet ---
        sheet_path = os.path.join("assets", "player", "player.png")
        self.spritesheet = pygame.image.load(sheet_path).convert_alpha()

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
        # dash mecha
        self.is_dashing = False
        self.dash_speed = 10
        self.dash_duration = 0.10 # Durée du dash en secondes
        self.dash_timer = 0


    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Si le dash est en cours, l'entrée du joueur est ignorée pour le mouvement
        if self.is_dashing:
            return 
        
        self.dash_input_x = 0
        self.dash_input_y = 0
        
        self.vel.x = 0

        if keys[pygame.K_q]:
            self.vel.x = -self.speed
            self.dash_input_x = -1
        if keys[pygame.K_d]:
            self.vel.x = self.speed
            self.dash_input_x = 1
            
        if keys[pygame.K_z]: # Exemple : touche Z pour monter
             self.dash_input_y = -1
        if keys[pygame.K_s]: # Exemple : touche S pour descendre
             self.dash_input_y = 1

    def apply_gravity(self):
        # La gravité est appliquée uniquement si le joueur n'est PAS en train de dasher
        if self.is_dashing:
            self.vel.y = 0 # Annuler l'effet de la gravité pendant le dash
            return
        self.vel.y += self.gravity
        if self.vel.y > 20:
            self.vel.y = 20

    def jump(self):
        if self.on_ground and self.can_dash:
            self.vel.y = self.jump_force
            self.on_ground = False

    def dash(self):
        if self.can_dash: 
            # 1. Crée un vecteur direction basé sur les entrées enregistrées
            dash_vector = pygame.math.Vector2(self.dash_input_x, self.dash_input_y)
            
            # 2. Si aucune direction n'est spécifiée, le dash se fait dans la direction où le joueur fait face
            if dash_vector.length_squared() == 0:
                dash_vector.x = 1 if self.facing_right else -1
            
            # 3. Normalise le vecteur pour que la vitesse soit constante, même en diagonale
            # La division par zéro est gérée par la condition précédente.
            dash_vector = dash_vector.normalize()
            
            # 4. Applique la vélocité et met à jour l'état
            self.is_dashing = True
            self.can_dash = False 
            self.dash_timer = self.dash_duration
            
            self.vel.x = dash_vector.x * self.dash_speed
            self.vel.y = dash_vector.y * self.dash_speed
                

    def move_and_collide(self, tiles):
        
        # Déplacement horizontal
        self.rect.x += int(self.vel.x)
        
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:       # Va à droite
                    self.rect.right = tile.rect.left
                    if self.is_dashing:
                        self.is_dashing = False
                        self.vel.x = 0
                        self.vel.y = 0  # ⬅️ NOUVEAU : Arrêt total du mouvement X/Y
                elif self.vel.x < 0:     # Va à gauche
                    self.rect.left = tile.rect.right
                    if self.is_dashing:
                        self.is_dashing = False
                        self.vel.x = 0
                        self.vel.y = 0  # ⬅️ NOUVEAU : Arrêt total du mouvement X/Y

        # Déplacement vertical
        self.rect.y += int(self.vel.y)
        self.on_ground = False
        
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.y > 0:       # Tombe
                    self.rect.bottom = tile.rect.top
                    self.vel.y = 0
                    self.on_ground = True
                    self.can_dash = True 
                    
                    if self.is_dashing:  # Arrêt du dash si collision verticale (vers le bas)
                        self.is_dashing = False
                        self.vel.x = 0  # ⬅️ NOUVEAU : Arrêt total du mouvement X/Y
                        self.vel.y = 0
                        
                elif self.vel.y < 0:     # Monte (Plafond)
                    self.rect.top = tile.rect.bottom
                    self.vel.y = 0
                    
                    if self.is_dashing:  # Arrêt du dash si collision verticale (vers le haut)
                        self.is_dashing = False
                        self.vel.x = 0  # ⬅️ NOUVEAU : Arrêt total du mouvement X/Y
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
