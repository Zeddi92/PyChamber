import numpy as np
import pygame
import sys

# Größe des Nebelkammer-Rasters
grid_size = 200

step_length = 1


# Fenstergröße für die Darstellung
window_size = (500, 500)

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# Erzeugung der Nebelkammer-Daten
nebelkammer = np.zeros((grid_size, grid_size))

# Liste für die Ereignisse
events = []

# Animationsschleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Generierung einer Myonenspur
    if np.random.randint(1000) < 5:  # Myonenspuren werden seltener generiert
        # Generierung einer Myonenspur
        start_pos = (np.random.uniform(0, grid_size-1), np.random.uniform(0, grid_size-1))
        num_steps = np.random.randint(50, 600)  # Variable Länge der Myonenspur

        angle = np.random.uniform(0, 2*np.pi)  # Winkel in Radiant

        x, y = start_pos
        for _ in range(num_steps):
            xi, yi = int(round(x)), int(round(y))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size and 0 <= yi < grid_size:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Quadrat um den Punkt herum, um eine breitere Spur zu erzeugen
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        xj, yj = xi + dx, yi + dy
                        if 0 <= xj < grid_size and 0 <= yj < grid_size:
                            if nebelkammer[yj, xj] < 255:
                                nebelkammer[yj, xj] += 40  # Größere Erhöhung der Transparenz für sichtbarere Spuren

            x += step_length * np.cos(angle)
            y += step_length * np.sin(angle)


    # Generierung einer Alpha-Teilchen-Spur
    if np.random.randint(2000) < 5:  # Alpha-Teilchen-Spuren werden seltener generiert
        start_pos = (np.random.uniform(0, grid_size-1), np.random.uniform(0, grid_size-1))
        num_steps = np.random.randint(10, 200)  # Variable Länge der Alpha-Teilchen-Spur (kürzer als Myonenspur)

        angle = np.random.uniform(0, 2*np.pi)  # Winkel in Radiant

        x, y = start_pos
        for _ in range(num_steps):
            xi, yi = int(round(x)), int(round(y))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size and 0 <= yi < grid_size:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Quadrat um den Punkt herum, um eine breitere Spur zu erzeugen
                for dx in range(-np.random.randint(3, 4), np.random.randint(4, 5)):
                    for dy in range(-np.random.randint(3, 4), np.random.randint(4, 5)):
                        xj, yj = xi + dx, yi + dy
                        if 0 <= xj < grid_size and 0 <= yj < grid_size:
                            if nebelkammer[yj, xj] < 255:
                                nebelkammer[yj, xj] += 25  # Größere Erhöhung der Transparenz für Alpha-Teilchen

            x += step_length * np.cos(angle)
            y += step_length * np.sin(angle)



    # Generierung einer Beta-Teilchen-Spur
    if np.random.randint(1000) < 10:  # Beta-Teilchen-Spuren werden seltener generiert
        start_pos = (np.random.randint(grid_size), np.random.randint(grid_size))
        num_steps = np.random.randint(10, 100)

        x, y = start_pos
        direction = np.random.randint(0, 4)
        for _ in range(num_steps):

            xi, yi = int(round(x)), int(round(y))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size and 0 <= yi < grid_size:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Quadrat um den Punkt herum, um eine breitere Spur zu erzeugen
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        xj, yj = xi + dx, yi + dy
                        if 0 <= xj < grid_size and 0 <= yj < grid_size:
                            if nebelkammer[yj, xj] < 255:
                                nebelkammer[yj, xj] += np.random.randint(5, 20)  # Größere Erhöhung der Transparenz für Alpha-Teilchen

            if nebelkammer[y, x] < 255:
                nebelkammer[y, x] += 5
            # Die Richtung ändert sich bei jedem Schritt, aber mit einer geringeren Wahrscheinlichkeit
            if np.random.randint(100) < 30:  # 30% Wahrscheinlichkeit für Richtungsänderung
                direction = np.random.randint(0, 4)
            if direction == 0 and y > 0:
                y -= step_length
            elif direction == 1 and y < grid_size - 1:
                y += step_length
            elif direction == 2 and x > 0:
                x -= step_length
            elif direction == 3 and x < grid_size - 1:
                x += step_length


    # Aktualisieren der Ereignisse
    for event in events:
        if event.fade():
            events.remove(event)  # Ereignis entfernen, wenn es vollständig verblasst ist

    # Reduzieren der Transparenz der Myonenspur
    for y in range(grid_size):
        for x in range(grid_size):
            if nebelkammer[y, x] > 0:
                nebelkammer[y, x] = max(0, nebelkammer[y, x] - 1)  # Alpha-Wert kann nicht unter 0 fallen


    # Darstellung der Nebelkammer mit Myonenspur und Ereignissen
    screen.fill(BLACK)

    # Zeichnen der Myonenspur
    for y in range(grid_size):
        for x in range(grid_size):
            if nebelkammer[y, x] > 0:
                alpha = nebelkammer[y, x]
                color = (WHITE[0], WHITE[1], WHITE[2])  # Farbe ohne Transparenz
                surf = pygame.Surface((window_size[0] // grid_size, window_size[1] // grid_size))  # Erstellen des Surfaces
                surf.set_alpha(alpha)  # Einstellen der Transparenz des Surfaces
                surf.fill(color)  # Füllen des Surfaces mit der Farbe
                screen.blit(surf, (x * (window_size[0] // grid_size), y * (window_size[1] // grid_size)))  # Zeichnen des Surfaces auf den Bildschirm

    # Zeichnen der Ereignisse
    for event in events:
        alpha = event.alpha
        color = (WHITE[0], WHITE[1], WHITE[2], alpha)  # Farbe mit Transparenz
        rect = pygame.Rect(event.x * (window_size[0] // grid_size), event.y * (window_size[1] // grid_size),
                           window_size[0] // grid_size, window_size[1] // grid_size)
        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()
    clock.tick(60)
