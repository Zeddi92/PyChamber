import numpy as np

rain_flux = 200  # Isoprop Niderschlag

# Parameter für die Myonenspur
muon_flux = 1  # Myonenfluss in Myonen/qcm (Ist 1)
expected_angle = 180  # Erwarteter Eintrittswinkel in Grad (Ist 150)
std_dev_angle = 30  # Standardabweichung des Eintrittswinkels in Grad (Ist 20)
muon_lifetime = 2.2 # Lebensdauer eines Myons in Mikrosekunden

# Radon Aktivität
activity_concentration = 300  # Aktivitätskonzentration in Bq/m^3 (ist 300)
alpha_energy = 6.29  # Energie der Alpha-Teilchen in MeV

# Aktivitätskonzentration in Bq/m^3 für Beta-Teilchen
activity_concentration_beta = 150
max_steps_beta = 500  # Maximale Länge der Beta-Spur

step_length = 1

particle_size = 2


def generate_rain(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten):
    expected_rain = rain_flux * (grid_size_x * grid_size_y)  # Erwartete Anzahl an Myonen
    probability_per_frame = expected_rain / (framerate * 60)  # Wahrscheinlichkeit für ein Myon pro Frame
    if np.random.rand() < probability_per_frame:
        start_pos = (np.random.uniform(0, grid_size_x - 1), np.random.uniform(0, grid_size_y - 1), 10)

        num_steps = 1
        radius = 1
        x, y, z = start_pos
        for _ in range(num_steps):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))
            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx * dx + dy * dy <= radius * radius:
                            xj, yj = xi + dx, yi + dy
                            if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                                if nebelkammer[xj, yj] < 255:
                                    nebelkammer[xj, yj] += 40
                                    spurkoordinaten[(xj, yj)] = z

            z -= step_length


def generate_muon_trace(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten):
    expected_muons = muon_flux * (grid_size_x * grid_size_y * 9)  # Erwartete Anzahl an Myonen
    probability_per_frame = expected_muons / (framerate * 60)  # Wahrscheinlichkeit für ein Myon pro Frame
    if np.random.rand() < probability_per_frame:
        start_pos = (np.random.uniform(-grid_size_x + 1, grid_size_x * 2 - 1),
                     np.random.uniform(-grid_size_y + 1, grid_size_y * 2 - 1), grid_size_z - 1)

        polar_angle_degree = np.random.normal(expected_angle, std_dev_angle)
        azimuthal_angle_degree = np.random.uniform(0, 360)

        polar_angle = np.radians(polar_angle_degree)
        azimuthal_angle = np.radians(azimuthal_angle_degree)

        num_steps = abs(int(grid_size_z * np.tan(polar_angle)*5))
        radius = particle_size * 2
        x, y, z = start_pos
        for _ in range(num_steps):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))

            # Überprüfe, ob das Myon zerfällt
            if np.random.rand() < 1/(framerate * 60 * muon_lifetime * 1e6):
                # Generiere das Elektron
                generate_electron_trace(xi, yi, zi, grid_size_x, grid_size_y, grid_size_z, nebelkammer, spurkoordinaten)
                break

            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx * dx + dy * dy <= radius * radius:
                            xj, yj = xi + dx, yi + dy
                            if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                                if nebelkammer[xj, yj] < 255:
                                    nebelkammer[xj, yj] += 8
                                    spurkoordinaten[(xj, yj)] = z

            x += step_length * np.sin(polar_angle) * np.cos(azimuthal_angle)
            y += step_length * np.sin(polar_angle) * np.sin(azimuthal_angle)
            z -= step_length * abs(np.cos(polar_angle))

def generate_electron_trace(xi, yi, zi, grid_size_x, grid_size_y, grid_size_z, nebelkammer, spurkoordinaten):
    # Bestimmen Sie den Winkel des emittierten Elektrons
    polar_angle_degree = np.random.uniform(0, 180)
    azimuthal_angle_degree = np.random.uniform(0, 360)

    polar_angle = np.radians(polar_angle_degree)
    azimuthal_angle = np.radians(azimuthal_angle_degree)

    num_steps = abs(int(grid_size_z * np.tan(polar_angle)*5))
    # Bestimmen Sie die Anzahl der Schritte des Elektrons
    num_steps_electron = abs(int(grid_size_z * np.tan(polar_angle)*5))
    radius = particle_size * 2
    x, y, z = xi, yi, zi
    for _ in range(num_steps_electron):
        xk, yk, zk = int(round(x)), int(round(y)), int(round(z))
        if 0 <= xk < grid_size_x and 0 <= yk < grid_size_y and 0 <= zk < grid_size_z:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        xj, yj = xk + dx, yk + dy
                        if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                            if nebelkammer[xj, yj] < 255:
                                nebelkammer[xj, yj] += 8
                                spurkoordinaten[(xj, yj)] = z
        x += step_length * np.sin(polar_angle) * np.cos(azimuthal_angle)
        y += step_length * np.sin(polar_angle) * np.sin(azimuthal_angle)
        z -= step_length * np.cos(polar_angle)

def generate_alpha_trace(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten):
    probability_per_frame_alpha = activity_concentration / 1000000000000 * (grid_size_x * grid_size_y * grid_size_z)
    if np.random.rand() < probability_per_frame_alpha:
        start_pos_alpha = (np.random.uniform(0, grid_size_x - 1), np.random.uniform(0, grid_size_y - 1),
                           np.random.uniform(0, grid_size_z - 1))

        polar_angle_degree = np.random.uniform(0, 180)
        azimuthal_angle_degree = np.random.uniform(0, 360)

        polar_angle = np.radians(polar_angle_degree)
        azimuthal_angle = np.radians(azimuthal_angle_degree)

        num_steps_alpha = int(round(bethe_alpha(alpha_energy, np.random.uniform(4167, 5556))))
        x, y, z = start_pos_alpha
        radius = particle_size * 6
        for _ in range(num_steps_alpha):
            xi, yi, zi = int(round(x)), int(round(y)), int(round(z))
            if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        if dx * dx + dy * dy <= radius * radius:
                            xj, yj =xi + dx, yi + dy
                            if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                                if nebelkammer[xj, yj] < 255:
                                    nebelkammer[xj, yj] += 8
                                    spurkoordinaten[(xj, yj)] = z

            x += step_length * np.sin(polar_angle) * np.cos(azimuthal_angle)
            y += step_length * np.sin(polar_angle) * np.sin(azimuthal_angle)
            z -= step_length * abs(np.cos(polar_angle))

def bethe_alpha(energy,v_speed):
    return energy/(30.6437*1/v_speed/v_speed*np.log(1.1883969642*v_speed)*np.power(10,4)*0.19)

def generate_beta_trace(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten):
    probability_per_frame_beta = activity_concentration_beta/1000000000000 * (grid_size_x * grid_size_y * grid_size_z)  # Erwartete Anzahl an Beta-Teilchen

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

def generate_scale(grid_size_x, grid_size_y, grid_size_z, framerate, nebelkammer, spurkoordinaten):
    num_steps = 100
    x, y, z = (10, 10, 2)
    radius = particle_size
    for _ in range(num_steps):
        xi, yi, zi = int(round(x)), int(round(y)), int(round(z))
        if 0 <= xi < grid_size_x and 0 <= yi < grid_size_y and 0 <= zi < grid_size_z:
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if dx * dx + dy * dy <= radius * radius:
                        xj, yj =xi + dx, yi + dy
                        if 0 <= xj < grid_size_x and 0 <= yj < grid_size_y:
                            if nebelkammer[xj, yj] < 255:
                                nebelkammer[xj, yj] += 8
                                spurkoordinaten[(xj, yj)] = z

        x += step_length
