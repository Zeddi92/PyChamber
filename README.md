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
