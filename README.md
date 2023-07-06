# PyChamber

PyChamber ist ein Python-Skript, das eine Nebelkammer-Simulation implementiert. Eine Nebelkammer wird verwendet, um die Spuren von geladenen Teilchen zu visualisieren. Das Skript nutzt die Pygame-Bibliothek, um die Simulation darzustellen.


## main.py

Das `main.py`-Skript enthält den Hauptcode für die Nebelkammer-Simulation.

### Verwendete Bibliotheken

- `numpy`: Wird verwendet, um mit Arrays und mathematischen Operationen zu arbeiten.
- `pygame`: Eine Bibliothek zum Erstellen von Spielen und grafischen Anwendungen.

### Parameter

- `grid_size_x`: Die Größe des Nebelkammer-Rasters in x-Richtung [cm].
- `grid_size_y`: Die Größe des Nebelkammer-Rasters in y-Richtung [cm].
- `grid_size_z`: Die Dicke des sensitiven Bereichs in z-Richtung.
- `framerate`: Die Bildrate der Animation.
- `window_size`: Die Größe des Darstellungsfensters.

### Farben

- `BLACK`: Eine Farbe, die den Hintergrund darstellt.
- `WHITE`: Eine Farbe, die für die Teilchenspuren verwendet wird.

### Hauptfunktionen

1. `generate_rain`: Generiert Niederschlag in der Nebelkammer.
2. `generate_muon_trace`: Generiert eine Myonenspur, die auf der Oberseite der Nebelkammer ankommt.
3. `generate_alpha_trace`: Generiert eine Alpha-Teilchen-Spur in der Nebelkammer.
4. `generate_beta_trace`: Generiert eine Beta-Teilchen-Spur in der Nebelkammer.
5. `generate_scale`: Generiert einen Massstab in der Nebelkammer.

### Hauptschleife

Die Hauptschleife der Simulation enthält die folgenden Schritte:

1. Überprüfung von Benutzereingaben oder Schließen des Fensters.
2. Generierung von Myonenspuren.
3. Generierung von Alpha-Teilchen-Spuren.
4. Generierung von Beta-Teilchen-Spuren.
5. Aktualisierung und Löschung von Spuren in der Nebelkammer.
6. Darstellung der Nebelkammer und der Spuren auf dem Bildschirm.

Bitte beachten Sie, dass dies nur eine grobe Übersicht des Skripts ist. Weitere Details und Funktionalitäten können dem Code direkt entnommen werden.

## nebelkammer.py

Die `nebelkammer.py`-Datei enthält Funktionen für die Generierung von verschiedenen Spuren in der Nebelkammer.

### Parameter

- `rain_flux`: Der Niederschlagsfluss in der Nebelkammer.
- `muon_flux`: Der Myonenfluss in Myonen pro Quadratzentimeter.
- `expected_angle`: Der erwartete Eintrittswinkel der Myonen in Grad.
- `std_dev_angle`: Die Standardabweichung des Eintrittswinkels der Myonen in Grad.
- `muon_lifetime`: Die Lebensdauer eines Myons in Mikrosekunden.
- `activity_concentration`: Die Aktivitätskonzentration von Radon in Bq/m^3.
- `alpha_energy`: Die Energie der Alpha-Teilchen in MeV.
- `activity_concentration_beta`: Die Aktivitätskonzentration von Beta-Teilchen in Bq/m^3.
- `max_steps_beta`: Die maximale Länge der Beta-Teilchen-Spur.
- `step_length`: Die Schrittlänge für die Spurgenerierung.
- `particle_size`: Die Größe der Teilchen.

### Funktionen

1. `generate_rain`: Generiert Niederschlag in der Nebelkammer.
2. `generate_muon_trace`: Generiert eine Myonenspur in der Nebelkammer.
3. `generate_electron_trace`: Generiert eine Elektronenspur basierend auf einem Myonenzefalls.
4. `generate_alpha_trace`: Generiert eine Alpha-Teilchen-Spur in der Nebelkammer.
5. `bethe_alpha`: Berechnet die Länge der Alpha-Teilchen-Spur basierend auf der Energie und der Geschwindigkeit.
6. Weitere interne Hilfsfunktionen.

Bitte beachten Sie, dass diese Übersicht die wichtigsten Funktionen und Parameter in der `nebelkammer.py`-Datei enthält. Für weitere Details und Implementierungsdetails können Sie den Code direkt überprüfen.
