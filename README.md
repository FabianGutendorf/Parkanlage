# Parkanlage

Projekt für ein Client Server Beispiel.

Der Server übernimmt die Berechnung, während der Client den Aufruf der einzelnen Funktionen wahrnimmt.
Für das Frontend nutzen wir HTML. Für das Backend wird Python verwendet.

Hier nutzen wir den Service Flask, ein Webframework für Python, um die Verknüpfung von front- und backend zu ermöglichen.

# Installation
Damit das Projekt läuft, muss Flask installiert werden. Hier nutzen wir den Paket Manager von Python3 (pip3)

# Flask installation:
sudo pip3 install Flask

# Flask starten
FLASK_APP=WebServer.py flask run

# Debuggen
um das Projekt mit Debugger zu starten (auf Port achten)
python3 Webserver.py 