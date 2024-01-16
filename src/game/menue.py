

# %%
import pygame
import sys

import os
import json



# Initialisation de Pygame
pygame.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Police
pygame.font.init()
font = pygame.font.SysFont(None, 30)


# MENUE SELECTION PARAMETERS
menue_width = 100
choice_height = 50

# Solutions menue

sol_selected = 0  # Élément sélectionné par défaut
solution_x = 50


# Maps menue

map_selected = 0  # Élément sélectionné par défaut
map_x = 200

# RUN BUTTON PARAMETERS
run_x = 375
run_y = 50
run_width = 100
run_height = 200

# Définir les paramètres de la fenêtre
window_width = 500
window_height = 300




def menue(map_list):
    sol_selected = 0  
    map_selected = 0
    pygame.init()
    # Créer la fenêtre
    fenetre = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Mars Lander")

    def menue_display(solutions, maps):
        fenetre.fill(WHITE)

        # Afficher les éléments du menu
        for i, element in enumerate(solutions):
            texte = font.render(element, True, BLACK if i != sol_selected else RED)
            y = choice_height + i * choice_height
            fenetre.blit(texte, (solution_x, y))

        # Afficher les éléments du menu
        for i, element in enumerate(maps):
            texte = font.render(element, True, BLACK if i != map_selected else RED)
            y = choice_height + i * choice_height
            fenetre.blit(texte, (map_x, y))

        pygame.draw.rect(fenetre, GREEN, (run_x, run_y, run_width, run_height))
        texte_run = font.render("Run", True, WHITE)
        fenetre.blit(texte_run, (run_x+10, run_y + run_height//2))

        pygame.display.flip()

    solutions = ["Manual", "Genetic"]
    maps = list(map(lambda m: m['name'], map_list))
    # Boucle principale du programme
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche de la souris
                    if 350 <= event.pos[0] <= 450 :
                        print(f"Run MarsLander on map {maps[map_selected]} by {solutions[sol_selected]}")
                        pygame.quit()
                        return map_list[map_selected], solutions[sol_selected]
                    else:
                        # Vérifier quel élément a été sélectionné
                        x_mouse, y_mouse = event.pos
                        if 50<= x_mouse <= 150:
                            sol_selected = (y_mouse - 50) // 50
                        elif 200<= x_mouse <=300:
                            map_selected = (y_mouse - 50) // 50



        menue_display(solutions, maps)

if __name__ == "__main__":
    menue()

# %%
