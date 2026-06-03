# ♟️ Multiplayer Schach

> LAN-Multiplayer-Schach mit grafischer Oberfläche — HTL Abschlussarbeit FSST

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-GUI-green?logo=pygame)
![License](https://img.shields.io/github/license/Sandroexe/schach?style=flat)

---

## Features

- **LAN-Multiplayer** — Spiele gegen einen Freund über WLAN/LAN (Socket-Verbindung)
- **Grafische Oberfläche** — Übersichtliches Schachbrett mit Pygame
- **Zugvalidierung** — Nur regelkonforme Züge werden zugelassen
- **Server & Client** — Ein Spieler hostet, der andere verbindet sich

---

## Installation

### Automatisch (Linux / macOS)

```bash
curl -sSL https://raw.githubusercontent.com/Sandroexe/schach/main/install.sh | bash
```

### Manuell

```bash
git clone https://github.com/Sandroexe/schach.git
cd schach
pip install pygame
```

---

## Starten

```bash
python3 schach.py
```

Wähle im Menü zwischen **Server** (hostet das Spiel) und **Client** (verbindet sich).

---

## Projektstruktur

```
schach/
├── schach.py              # Einstiegspunkt
├── chess/                 # Schach-Logik & Board
├── connection/            # Netzwerk (Server/Client, Sockets)
├── gui/                   # Pygame-Oberfläche & Menü
│   └── images/            # Figuren & Brett-Texturen
└── install.sh             # Automatisches Setup-Script
```

---

## Entwickler

## Entwickler

| | Name | GitHub |
| :---: | :--- | :--- |
| <img src="https://github.com/Sandroexe.png" width="40" height="40" style="border-radius:50%;"> | **Sandro Exenberger** | [@Sandroexe](https://github.com/Sandroexe) |
| <img src="https://github.com/chrisfly97.png" width="40" height="40" style="border-radius:50%;"> | **Christoph Widner** | [@chrisfly97](https://github.com/chrisfly97) |
