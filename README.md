# ♟️ Multiplayer Schach - HTL Abschlussarbeit FSST

![GitHub License](https://img.shields.io/github/license/Sandroexe/schach?style=flat-square)
![GitHub Stars](https://img.shields.io/github/stars/Sandroexe/schach?style=flat-square)
![GitHub Issues](https://img.shields.io/github/issues/Sandroexe/schach?style=flat-square)

Eine moderne, performante Schach-Anwendung mit grafischer Benutzeroberfläche, integrierter Logikprüfung und Netzwerk-Multiplayer. Dieses Projekt wurde als Abschlussarbeit im Fach FSST entwickelt und fokussiert sich auf eine saubere Netzwerk-Architektur, effiziente Zugberechnungen und ein modulares Design.

---

## ✨ Features

* **Multiplayer über WLAN/LAN:** Unkomplizierte Verbindung zwischen Server und Client im selben lokalen Netzwerk (Socket-Verbindung).
* **Grafische Oberfläche:** Simpel, performant und vollkommen modular aufgebautes UI.
* **Move Validation:** Echtzeit-Erkennung aller regelkonformen Schachzüge (lässt nur valide Züge zu).
* **Modularer Aufbau:** Strikte Trennung von Netzwerk-Logik, UI (Frontend) und der zugrundeliegenden Schach-Regelprüfung (Backend).

---

## 🖥️ Unterstützte Systeme & Voraussetzungen

Das Projekt ist plattformunabhängig konzipiert und wurde erfolgreich auf folgenden Systemen getestet:
* **Linux:** CachyOS, Arch Linux, Debian, Ubuntu und Derivate.
* **Windows:** Windows 10 / 11.

---

## 🚀 Installation & Setup

Du kannst das Projekt entweder vollautomatisch über das Terminal (empfohlen für Linux) oder Schritt für Schritt manuell einrichten.

### Methode 1: Automatischer Einzeiler (Linux - CachyOS, Arch, Debian, Ubuntu)
Öffne dein Terminal und füge einfach den folgenden Befehl ein. Das Skript erkennt dein System, installiert alle benötigten Grafik- und Netzwerklibraries und lädt das Spiel in den aktuellen Ordner herunter:

```bash
curl -sSL [https://raw.githubusercontent.com/Sandroexe/schach/main/install.sh](https://raw.githubusercontent.com/Sandroexe/schach/main/install.sh) | bash
