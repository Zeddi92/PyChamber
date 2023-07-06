import numpy as np
import pygame
import sys

grid_size = 500

# Größe des Nebelkammer-Rasters
grid_size_x = 500  # Größe in x-Richtung [cm]
grid_size_y = 500  # Größe in y-Richtung [cm]
grid_size_z = 50  # Größe in z-Richtung (Dicke des sensitiven Bereichs)

rain_flux = 200  # Isoprop Niderschlag

# Parameter für die Myonenspur
muon_flux = 1  # Myonenfluss in Myonen/qcm (Ist 1)
expected_angle = 180  # Erwarteter Eintrittswinkel in Grad (Ist 150)
std_dev_angle = 30  # Standardabweichung des Eintrittswinkels in Grad (Ist 20)

# Radon Aktivität
activity_concentration = 300  # Aktivitätskonzentration in Bq/m^3 (ist 300)
alpha_energy = 6.29  # Energie der Alpha-Teilchen in MeV
max_steps_alpha = 200  # Maximale Länge der Alpha-Spur

activity_concentration_beta = 300  # Aktivitätskonzentration in Bq/m^3 für Beta-Teilchen
max_steps_beta = 900  # Maximale Länge der Beta-Spur

# Pygame Framerate
framerate = 60  # 60 Frames pro Sekunde

step_length = 1


# Fenstergröße für die Darstellung
window_size = (500, 500)

#Dicke der Teilchen
particle_size = 2

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ein einziges Surface erstellen
single_surf = pygame.Surface((window_size[0] // grid_size, window_size[1] // grid_size))


# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# Erzeugung der Nebelkammer-Daten
nebelkammer = np.zeros((grid_size, grid_size))

# Set für die Spurkoordinaten
#spurkoordinaten = set()
spurkoordinaten = {}


# Animationsschleife
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Generierung des Niederschlags
    expected_rain = rain_flux * (grid_size_x * grid_size_y)  # Erwartete Anzahl an Myonen
    probability_per_frame = expected_rain / (framerate * 60)  # Wahrscheinlichkeit für ein Myon pro Frame
    if np.random.rand() < probability_per_frame:
        # Generierung einer Myonenspur
        start_pos = (np.random.uniform(0, grid_size_x-1), np.random.uniform(0, grid_size_y-1), 10)

        num_steps = 1
        radius = 1
        x, y, z = start_pos
        for _ in range(num_steps):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Quadrat um den Punkt herum, um eine breitere Spur zu erzeugen
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx*dx + dy*dy <= radius*radius:  # Überprüfen, ob der Punkt innerhalb des Kreises liegt
                            xj, yj = xi + dx, yi + dy
                            if 0 <= xj < grid_size and 0 <= yj < grid_size:
                                if nebelkammer[yj, xj] < 255:
                                    nebelkammer[yj, xj] += 40  # Größere Erhöhung der Transparenz für sichtbarere Spuren
                                    spurkoordinaten[(yj, xj)] = z

            # Aktualisieren der Koordinaten
            z -= step_length

    # Generierung einer Myonenspur welche auf der Oberseite ankommt
    expected_muons = muon_flux * (grid_size_x * grid_size_y * 9)  # Erwartete Anzahl an Myonen
    probability_per_frame = expected_muons / (framerate * 60)  # Wahrscheinlichkeit für ein Myon pro Frame
    if np.random.rand() < probability_per_frame:
        # Generierung einer Myonenspur
        start_pos = (np.random.uniform(-grid_size_x+1, grid_size_x*2-1), np.random.uniform(-grid_size_y+1, grid_size_y*2-1), grid_size_z-1)

        polar_angle_degree = np.random.normal(expected_angle, std_dev_angle)  # Winkel in Grad
        azimuthal_angle_degree = np.random.uniform(0, 360)  # Azimutalwinkel in Grad

        polar_angle = np.radians(polar_angle_degree)  # Polarer Winkel in Radiant
        azimuthal_angle = np.radians(azimuthal_angle_degree)  # Azimutalwinkel in Radiant

        num_steps = abs(int(grid_size_z * np.tan(polar_angle)))  # Länge der Spur abhängig vom Winkel
        radius = particle_size*2
        x, y, z = start_pos
        for _ in range(num_steps):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Quadrat um den Punkt herum, um eine breitere Spur zu erzeugen
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx*dx + dy*dy <= radius*radius:  # Überprüfen, ob der Punkt innerhalb des Kreises liegt
                            xj, yj = xi + dx, yi + dy
                            if 0 <= xj < grid_size and 0 <= yj < grid_size:
                                if nebelkammer[yj, xj] < 255:
                                    nebelkammer[yj, xj] += 8  # Größere Erhöhung der Transparenz für sichtbarere Spuren
                                    spurkoordinaten[(yj, xj)] = z

            # Aktualisieren der Koordinaten
            x += step_length * np.sin(polar_angle) * np.cos(azimuthal_angle)
            y += step_length * np.sin(polar_angle) * np.sin(azimuthal_angle)
            z -= step_length * abs(np.cos(polar_angle))



    # Generierung einer Alpha-Teilchen-Spur
    expected_alphas = activity_concentration/1000000000 * (grid_size_x * grid_size_y * grid_size_z)  # Erwartete Anzahl an Alpha-Teilchen
    probability_per_frame_alpha = expected_alphas / (framerate * 60)  # Wahrscheinlichkeit für ein Alpha-Teilchen pro Frame
    if np.random.rand() < probability_per_frame_alpha:
        # Generierung einer Alpha-Spur
        start_pos_alpha = (np.random.uniform(0, grid_size_x-1), np.random.uniform(0, grid_size_y-1), np.random.uniform(0, grid_size_z-1))

        polar_angle_degree = np.random.uniform(0, 180)  # Polarer Winkel in Grad
        azimuthal_angle_degree = np.random.uniform(0, 360)  # Azimutalwinkel in Grad

        polar_angle = np.radians(polar_angle_degree)  # Polarer Winkel in Radiant
        azimuthal_angle = np.radians(azimuthal_angle_degree)  # Azimutalwinkel in Radiant

        num_steps_alpha = max_steps_alpha  # Länge der Alpha-Spur ist immer maximal
        x, y, z = start_pos_alpha
        radius = particle_size*6
        for _ in range(num_steps_alpha):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Kreis um den Punkt herum, um eine rundliche Spur zu erzeugen
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx*dx + dy*dy <= radius*radius:  # Überprüfen, ob der Punkt innerhalb des Kreises liegt
                            xj, yj = xi + dx, yi + dy
                            if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                                if nebelkammer[yj, xj] < 255:
                                    nebelkammer[yj, xj] += 4  # Größere Erhöhung der Transparenz für sichtbarere Spuren
                                    spurkoordinaten[(yj, xj)] = z

            # Aktualisieren der Koordinaten
            x += step_length * np.sin(polar_angle) * np.cos(azimuthal_angle)
            y += step_length * np.sin(polar_angle) * np.sin(azimuthal_angle)
            z += step_length * np.cos(polar_angle)



    # Generierung einer Beta-Teilchen-Spur
    activity_concentration_beta = 400  # Aktivitätskonzentration in Bq/m^3 für Beta-Teilchen
    max_steps_beta = 200  # Maximale Länge der Beta-Spur

    expected_betas = activity_concentration_beta/100000000 * (grid_size_x * grid_size_y * grid_size_z)  # Erwartete Anzahl an Beta-Teilchen
    probability_per_frame_beta = expected_betas / (framerate * 60)  # Wahrscheinlichkeit für ein Beta-Teilchen pro Frame

    if np.random.rand() < probability_per_frame_beta:
        # Generierung einer Beta-Spur
        start_pos_beta = (np.random.uniform(0, grid_size_x-1), np.random.uniform(0, grid_size_y-1), np.random.uniform(0, grid_size_z-1))


        polar_angle_degree = np.random.uniform(0, 180)  # Polarer Winkel in Grad
        azimuthal_angle_degree = np.random.uniform(0, 360)  # Azimutalwinkel in Grad

        polar_angle = np.radians(polar_angle_degree)  # Polarer Winkel in Radiant
        azimuthal_angle = np.radians(azimuthal_angle_degree)  # Azimutalwinkel in Radiant

        num_steps_beta = max_steps_beta  # Länge der Alpha-Spur ist immer maximal
        x, y, z = start_pos_beta
        radius = particle_size*1
        for _ in range(num_steps_beta):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))  # Ganzzahlige Positionen für das Raster
            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:  # Überprüfen, ob die Position im Raster liegt
                # Erhöhung der Transparenz in einem Kreis um den Punkt herum, um eine rundliche Spur zu erzeugen
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx*dx + dy*dy <= radius*radius:  # Überprüfen, ob der Punkt innerhalb des Kreises liegt
                            xj, yj = xi + dx, yi + dy
                            if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                                if nebelkammer[yj, xj] < 255:
                                    nebelkammer[yj, xj] += 4  # Größere Erhöhung der Transparenz für sichtbarere Spuren
                                    spurkoordinaten[(yj, xj)] = z

            # Zufällige Richtungsänderung bei jedem Schritt
            direction = np.random.randint(0, 6)
            if direction == 0:
                x -= step_length
            elif direction == 1:
                x += step_length
            elif direction == 2:
                y -= step_length
            elif direction == 3:
                y += step_length
            elif direction == 4 and z > 0:
                z -= step_length
            elif direction == 5:
                z += step_length
            else:
                x += step_length


    zu_loeschen = []  # Liste zum Speichern der zu löschenden Schlüssel

    for coords in spurkoordinaten:
        if nebelkammer[coords] > 0 and spurkoordinaten[coords]>0:
            nebelkammer[coords] -= 1
            spurkoordinaten[coords] -= 0.1
        else:
            zu_loeschen.append(coords)  # Füge die Schlüssel der zu löschenden Elemente zur Liste hinzu anstatt sie sofort zu löschen

    # Lösche die Elemente nach der Iteration
    for coords in zu_loeschen:
        del spurkoordinaten[coords]




    # Darstellung der Nebelkammer mit Myonenspur und Ereignissen
    screen.fill(BLACK)

    # Zeichnen der Spuren
    for y, x in spurkoordinaten:
        if nebelkammer[y, x] > 0:
            alpha = nebelkammer[y, x]
            color = (WHITE[0], WHITE[1], WHITE[2])  # Farbe ohne Transparenz
            single_surf.set_alpha(alpha)  # Einstellen der Transparenz des Surfaces
            single_surf.fill(color)  # Füllen des Surfaces mit der Farbe
            screen.blit(single_surf, (x * (window_size[0] // grid_size), y * (window_size[1] // grid_size)))  # Zeichnen des Surfaces auf den Bildschirm



    pygame.display.flip()
    clock.tick(60)
