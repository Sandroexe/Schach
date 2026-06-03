#!/bin/bash
set -e

echo "♟️ Starte automatische Installation für das Schach-Projekt..."

# 1. System-Paketmanager erkennen und Abhängigkeiten installieren
if [ -f /etc/arch-release ] || grep -q "cachyos" /etc/os-release; then
    echo "-> Arch Linux / CachyOS erkannt. Installiere Abhängigkeiten via pacman..."
    sudo pacman -S --needed --noconfirm git python python-pip python-pygame 2>/dev/null || \
    sudo pacman -S --needed --noconfirm git cmake sdl2 sdl2_image
elif [ -f /etc/debian_version ]; then
    echo "-> Debian/Ubuntu erkannt. Installiere Abhängigkeiten via apt..."
    sudo apt update
    sudo apt install -y git python3 python3-pip python3-pygame 2>/dev/null || \
    sudo apt install -y git cmake libsdl2-dev libsdl2-image-dev
else
    echo "⚠️ Unbekanntes System. Bitte installiere Git und die benötigten Libraries manuell."
fi

# 2. Repository in den aktuellen Ordner klonen (falls noch nicht geschehen)
if [ ! -d "schach" ]; then
    echo "-> Klone das Repository..."
    git clone https://github.com/Sandroexe/schach.git
    cd schach
else
    echo "-> Ordner 'schach' existiert bereits."
    cd schach
fi

# 3. Optionale Python-Pip-Requirements installieren, falls vorhanden
if [ -f "requirements.txt" ]; then
    echo "-> Installiere Python-Pip-Pakete..."
    pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt
fi

echo "✅ Installation abgeschlossen! Du kannst das Projekt jetzt starten."
