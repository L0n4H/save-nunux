import pygame
from settings import * # Nécessite TILE_SIZE, ENEMY_SPEED, ENEMY_GRAVITY

class Ennemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        super().__init__()
        

        # 1. Image et Rectangle de Collision
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill('darkgreen') # Remplissage pour visualisation
        self.rect = self.image.get_rect(topleft=(x, y))

        # 2. Santé
        self.max_health = health
        self.current_health = health
        self.alive = True

        # 3. Variables de Mouvement
        self.direction = pygame.math.Vector2(1, 0) # Commence par se déplacer à droite (x=1)
        self.speed = ENEMY_SPEED 
        self.gravity = ENEMY_GRAVITY # À définir dans settings.py

        # 4. État
        self.on_ground = False

    # --- Méthodes de Mouvement ---

    def apply_gravity(self, dt):
        """Applique l'accélération verticale (gravité) au sprite."""
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y

    def reverse_direction(self):
        """Inverse la direction horizontale pour simuler une patrouille."""
        self.direction.x *= -1
        # Optionnel: Inverser l'image si vous utilisez une texture

    # --- Gestion de Collision ---

    def horizontal_movement_collision(self, tiles,dt):
        """Met à jour la position X et gère les collisions horizontales."""
        
        # Déplacement horizontal
        self.rect.x += self.direction.x * self.speed * dt
        
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                # Inverse la direction si un mur ou un autre obstacle est détecté
                if self.direction.x < 0: # Collision Gauche
                    self.rect.left = tile.rect.right
                    self.reverse_direction()
                elif self.direction.x > 0: # Collision Droite
                    self.rect.right = tile.rect.left
                    self.reverse_direction()

    def vertical_movement_collision(self, tiles, dt):
        """Gère la gravité et les collisions verticales (sol/plafond)."""
        self.apply_gravity(dt)

        # Vérification des collisions après application de la gravité
        for tile in tiles:
            if tile.rect.colliderect(self.rect):
                if self.direction.y > 0: # Collision Bas (Atterrissage)
                    self.rect.bottom = tile.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                elif self.direction.y < 0: # Collision Haut (Plafond)
                    self.rect.top = tile.rect.bottom
                    self.direction.y = 0
        
        # Réinitialiser on_ground si aucune collision de sol n'est trouvée
        if self.direction.y != 0:
            self.on_ground = False


    # --- Méthode Principale d'Update ---
    
    def update(self, dt, solid_tiles):
        """
        Appelée à chaque frame (dans game.update).
        dt: Delta Time (secondes écoulées depuis la dernière frame)
        solid_tiles: Groupe de sprites de collision (TileMap).
        """
        if self.alive:
            self.horizontal_movement_collision(solid_tiles, dt)
            self.vertical_movement_collision(solid_tiles, dt)
        
        # Optionnel: Si la santé est <= 0, définir self.alive = False et déclencher l'animation de mort.