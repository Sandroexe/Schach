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

## Entwickler

<table>
  <thead>
    <tr>
      <th align="center">Avatar</th>
      <th align="left">Name</th>
      <th align="left">GitHub</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">
        <a href="https://github.com/Sandroexe">
          <img src="https://github.com/Sandroexe.png" width="40" height="40" style="border-radius:50%;" alt="Sandro">
        </a>
      </td>
      <td>
        <a href="https://github.com/Sandroexe" style="color: inherit; text-decoration: none;">
          <strong>Sandro Exenberger</strong>
        </a>
      </td>
      <td><a href="https://github.com/Sandroexe">@Sandroexe</a></td>
    </tr>
    <tr>
      <td align="center">
        <a href="https://github.com/chrisfly97">
          <img src="https://github.com/chrisfly97.png" width="40" height="40" style="border-radius:50%;" alt="Christoph">
        </a>
      </td>
      <td>
        <a href="https://github.com/chrisfly97" style="color: inherit; text-decoration: none;">
          <strong>Christoph Widner</strong>
        </a>
      </td>
      <td><a href="https://github.com/chrisfly97">@chrisfly97</a></td>
    </tr>
  </tbody>
</table>
