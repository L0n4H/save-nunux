import pygame
from settings import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()
    running = True

    while running:
        # 1) Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2) Mise à jour du jeu (logique) -> pour l'instant vide

        # 3) Affichage
        screen.fill(BG_COLOR)  # efface l'écran
        pygame.display.flip()  # met à jour l'écran

        clock.tick(FPS)  # limite à FPS images/s

    pygame.quit()

if __name__ == "__main__":
    main()
