# ♟️ Netzwerk-Schach

Dieses Projekt wurde im Rahmen der Abschlussarbeit an der **HTL Anichstraße** entwickelt. Es handelt sich um eine Multiplayer-Anwendung, die das klassische Schachspiel über eine direkte Netzwerkverbindung zwischen zwei Computern ermöglicht.

## 📖 Projektbeschreibung

Das Kernziel dieses Projekts ist die Verschmelzung von komplexer Spiellogik und moderner Netzwerkkommunikation. Anstatt lokal an einem einzigen PC zu spielen, erlaubt diese Applikation zwei Spielern, über eine Client-Server-Architektur gegeneinander anzutreten.

Dabei wurden zwei wesentliche Herausforderungen umgesetzt:
1.  **Spiellogik:** Die vollständige Implementierung des Schach-Regelwerks, inklusive der Validierung korrekter Spielzüge und der Erkennung von Spielzuständen wie Schach oder Schachmatt.
2.  **Synchronisation:** Der Aufbau einer stabilen Socket-Verbindung, um Züge in Echtzeit zwischen den beiden Instanzen zu übertragen, sodass beide Spieler stets denselben Spielstand sehen.

Das Resultat ist eine funktionale und performante Lösung für strategische Duelle im lokalen Netzwerk.

## ✨ Features

* **Echtzeit-Multiplayer:** Nahtlose Verbindung zwischen zwei PCs.
* **Automatisierte Zugprüfung:** Das System erkennt eigenständig, ob ein Zug nach den offiziellen Schachregeln erlaubt ist.
* **Effiziente Kommunikation:** Minimale Latenz bei der Übertragung der Spieldaten durch optimierte Netzwerkprotokolle.
* **Clean UI:** Eine übersichtliche Benutzeroberfläche, die den Fokus auf das Spielgeschehen legt.

## 🎮 Spielablauf

1.  **Host-Setup:** Ein PC startet das Programm als Server und wartet auf eine Verbindung.
2.  **Client-Verbindung:** Der zweite PC tritt dem Spiel durch Eingabe der IP-Adresse des Hosts bei.
3.  **Partie:** Nach erfolgreichem Handshake beginnt die Partie. Die Züge werden abwechselnd validiert und übertragen.

## 🛠️ Verwendete Technologien

* **Programmiersprache:** Python
* **Netzwerktechnik:** TCP / IP Sockets
* **GUI-Framework:** Pygame / Tkinter

## 👨‍💻 Entwickler

* **Sandro** – [GitHub Profil](https://github.com/DEIN-LINK)
* **Christoph** – [GitHub Profil](https://github.com/chrisfly97)

---
*Abschlussprojekt der HTL Anichstraße.*
