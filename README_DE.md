Mazewalker
====

## Das Spiel

Das Spielprinzip ist relativ simpel gehalten. Man muss seine Figur zum Ziel (die kleine silber/goldene Falltür) steuern und muss dabei den in dem Labyrinth herumirrenden Skeletten ausweichen. Es ist möglich das Spiel jederzeit zu pausieren oder sich die bereits besuchten Felder anzeigen zu lassen. Der Spieler beginnt immer links oben (Quadrant II.) und das Ziel befindet sich in der rechten unteren Ecke (Quadrant IV.). Die Gegener beginnen auf zufälligen Feldern in allen Quadranten (I., III., IV.) außer dem linken oberen Quadranten (II.), in dem der Spieler beginnt.

## Steuerung

Die Bewegung der Spielfigur erfolgt mit den Tasten W, A, S, D.  
Das Spiel kann mit der Taste ESC verlassen und mit der Taste P pausiert werden.  
Das Anlegen der Markierungen kann mit der Taste T an- und ausgeschaltet werden, dass Anzeiger dieser mit der Taste M.     
Mit der Taste R lässt sich die Verschiebung auf den Spieler zentrieren und mit der Taste Z lässt sich die automatische Scroll-Funktion (de-)aktivieren.  
Durch das Drücken der linken Maustaste kann man den dargestellten Bereich der Karte verschieben, wenn das automatische Scrollen deaktivert wurde.

## Texturen

Die Texte im Menü und im Pausenbildschirm wurden mithilfe der Site [Textcraft.net](https://textcraft.net/) erstellt.  
Texturen für die Karte basieren auf angepassten Inhalten aus dem Spiel [Minecraft](https://www.minecraft.net).  
Die verwendeten Modelle für Spieler und Gegner wurden erstellt von Johannes Sjölund (Wulax) und auf der Seite [Open Game Art](https://opengameart.org/content/lpc-medieval-fantasy-character-sprites) veröffentlicht.

## Warum ein Labyrinth?

Ich habe mich entschieden ein dynamisch generiertes Labyrinth zu programmieren, da ich mich mit den dahinter stehenden Algorithmen auseinanderstzen wollte. Der hier verwendete [Wilson-Algorithmus](https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm) ist ein so genannter [Loop-Erased Random Walk](https://en.wikipedia.org/wiki/Loop-erased_random_walk). Das so erzeugte Labyrinth wird dann an die Bedürfnisse des Spiels angepasst und darin dann zufällig die Startpunkte für den Spieler und für die Gegner gewählt. Auch das Ziel ist ein zufällig gewähltes Feld.

## Verwendete Bilbiotheken

Die folgenden Bibliotheken wurden verwendet:

* pygame (Python-Programmbibliothek zur Spieleprogrammierung)
   * Genutzt als Basis für das gesamte Projekt
* math (Built-In Modul für mathematische Operationen)
   * Genutzt für das Runden von Zahlen
* random (Modul für die pseudo-zufällige Genration von Zahlen)
  * Generierung von Zahlen 
  * Durchmischen von Listen
* os (Modul für Operationen des Betriebssystem)
  * Anpassen von Pfaden zu den Bildern
* enum (Modul für Aufzählungen)
  * Aufzählungen für diverse Inhalte, z.B. Belegung des primären Arrays des Labyrinths

## Konfiguration

Die Konfiguration erfolgt über die [const.py](./const.py).  
Dort befinden sich am Anfang einer Datei Konstanten, die die folgenden Parameter einstellen können:

- TILE_SIZE: Größe eines Feldes in Pixeln
- ENEMY_SIZE = Größe eines Gegners in Pixeln (<= TILE_SIZE>)
- PLAYER_SIZE = Größe des Spielers in Pixeln (<= TILE_SIZE>)
- PLAYER_SPEED = Geschwindigkeit des Spielers in Feldern pro Sekunde
- ENEMY_SPEED = Basisgeschwindigkeit der Gegner in Feldern pro Sekunde
- ENEMY_RAND_SPEED = Zufällige Zusatzgeschwindigkeit der Gegner in Feldern pro Sekunde
- ENEMY_COUNT = Maximale Anzahl der Gegner
- WINDOW_SIZE = Größe des Fensters (Breite, Höhe)
- MAZE_SIZE = Größe des Labyrinths in Felder (Finale Größe ist 2*MAZE_SIZE+1 !!!)

## Interner Aufbau

Das Projekt ist objektorientiert aufgebaut.  
Die folgenden Klassen existieren:

* Main
   * Stellt das Hauptmenü dar
   * Startet ein einzelnes Spiel bei jedem Aufruf
* Game
   * Erstellt den Spieler
   * Lässt das Labyrinth von dem Generator erzeugen
   * Verwaltet den gesamten Spielablauf
   * Bewegt die Gegner
   * Reagiert auf Eingaben
* Player
   * Zeichnen des Spielers
* Models
   * Laden aller Sprite-Sheets für die Gegner
* Enemy
   * Zeichnen der Gegner
* Map
   * Erzeugen und Aufruf des Generators zur Labyrintherstellung
   * Zeichnen des Labyrinths
* Generator
   * Erzeugen des Labyrinths
   * Auswählen des Startpunktes des Spielers
   * Auswählen des Zielpunktes
   * Festlegend der Startpunkte der Gegner

Die folgenden Klassen die von enum.IntEnum erben existieren:

* game_state
   * Enthält die Werte, die die Schleifenvariablen in der Main und Game annehmen können
* direction
   * Die vier Richtungen (Oben, Links, Unten, Rechts) in der Reihenfolge wie sie in den Spritesheets vorhanden sind
* field_v
   * Werte die während der Generierung des Labyrinthes im Array abgelegt werden
* draw_v
   * Werte die am Ende der Generierung im Array liegen und das Aussehen der einzelnen Felder bestimmen
* base_id
   * Werte der 3 möglichen Feld-Typen (Weg, Wand, Ausgang)
* return_v
   * Werte die während der Generation des Labyrinths als Ergebnis einer Feldprüfung zurückgegeben werden