import numpy as np
import pygame
import sys

from nebelkammer import generate_rain, generate_muon_trace, generate_alpha_trace, generate_beta_trace, generate_scale



# Größe des Nebelkammer-Rasters
grid_size_x = 500  # Größe in x-Richtung [cm]
grid_size_y = 500  # Größe in y-Richtung [cm]
grid_size_z = 50  # Größe in z-Richtung (Dicke des sensitiven Bereichs)

# Pygame Framerate
framerate = 60  # 60 Frames pro Sekunde

# Fenstergröße für die Darstellung
window_size = (500, 500)

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ein einziges Surface erstellen
single_surf = pygame.Surface((window_size[0] // grid_size_x, window_size[1] // grid_size_y))


# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# Erzeugung der Nebelkammer-Daten
nebelkammer = np.zeros((grid_size_x, grid_size_y))

# Dict für die Spurkoordinaten
spurkoordinaten = {}

# Animationsschleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Generierung des Niederschlags
    #generate_rain(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten)

    # Generierung einer Myonenspur welche auf der Oberseite ankommt
    generate_muon_trace(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten)

    # Generierung einer Alpha-Teilchen-Spur
    generate_alpha_trace(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten)

    # Generierung einer Beta-Teilchen-Spur
    generate_beta_trace(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten)

    # Generierung eines Massstabes
    #generate_scale(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten)

    zu_loeschen = []  # Liste zum Speichern der zu löschenden Schlüssel

    for coords in spurkoordinaten:
        if nebelkammer[coords] >= 0 and spurkoordinaten[coords]>0:
            nebelkammer[coords] -= 1.5
            spurkoordinaten[coords] -= 0.2
        elif nebelkammer[coords] >= 0 and spurkoordinaten[coords]<=0:
            nebelkammer[coords] -= 4
        else:
            zu_loeschen.append(coords)  # Füge die Schlüssel der zu löschenden Elemente zur Liste hinzu anstatt sie sofort zu löschen

    # Lösche die Elemente nach der Iteration
    for coords in zu_loeschen:
        del spurkoordinaten[coords]
        nebelkammer[coords] = 0  # Setze den entsprechenden Wert in nebelkammer auf 0

    # Darstellung der Nebelkammer mit Myonenspur und Ereignissen
    screen.fill(BLACK)

    # Zeichnen der Spuren
    for y, x in spurkoordinaten:
        if nebelkammer[y, x] > 0:
            alpha = nebelkammer[y, x]
            color = (WHITE[0], WHITE[1], WHITE[2])  # Farbe ohne Transparenz
            single_surf.set_alpha(alpha)  # Einstellen der Transparenz des Surfaces
            single_surf.fill(color)  # Füllen des Surfaces mit der Farbe
            screen.blit(single_surf, (x * (window_size[0] // grid_size_x), y * (window_size[1] // grid_size_y)))  # Zeichnen des Surfaces auf den Bildschirm

    pygame.display.flip()
    clock.tick(60)
