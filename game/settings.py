# settings.py
WIDTH, HEIGHT = 1280, 720
TITLE = "Save Nunux"
BG_COLOR = (20, 20, 40)   # Fond sombre


# Taux de rafraîchissement (Frames Per Second)
FPS = 60

# Constantes de Physique
TILE_SIZE = 32 # Taille de chaque tuile du niveau / equivalent render distance un peu 

# Paramètres du Joueur
PLAYER_SPEED = 400
PLAYER_GRAVITY = 800
PLAYER_JUMP_VELOCITY = -450

# Paramètres de l'Ennemi
ENEMY_SPEED = 100 # Vitesse de patrouille
ENEMY_GRAVITY = 800 # (Idéalement la même que PLAYER_GRAVITY)