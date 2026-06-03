#!/bin/bash
set -e

# Farben für eine schöne Terminal-Ausgabe definieren
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color (Reset)

echo -e "${BLUE}==================================================${NC}"
echo -e "${YELLOW}  ♟️  Multiplayer Schach - HTL Abschlussarbeit  ♟️${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "${CYAN} -> Starte automatische Systemkonfiguration...${NC}\n"

# 1. System-Paketmanager erkennen und Abhängigkeiten installieren
if [ -f /etc/arch-release ] || grep -q "cachyos" /etc/os-release; then
    echo -e "${YELLOW}[1/3] CachyOS / Arch Linux erkannt.${NC}"
    echo -e " -> Installiere Systempakete via pacman..."
    sudo pacman -S --needed --noconfirm git python python-pygame 2>/dev/null || \
    sudo pacman -S --needed --noconfirm git cmake sdl2 sdl2_image
elif [ -f /etc/debian_version ]; then
    echo -e "${YELLOW}[1/3] Debian / Ubuntu erkannt.${NC}"
    echo -e " -> Aktualisiere Paketquellen und installiere via apt..."
    sudo apt update
    sudo apt install -y git python3 python3-pip python3-pygame 2>/dev/null || \
    sudo apt install -y git cmake libsdl2-dev libsdl2-image-dev
else
    echo -e "${YELLOW}⚠️  Unbekanntes System.${NC} Bitte installiere Git und die benötigten Libraries manuell."
fi

echo -e "\n${GREEN}✓ Systemabhängigkeiten sind bereit!${NC}\n"

# 2. Repository in den aktuellen Ordner klonen
echo -e "${YELLOW}[2/3] Repository-Setup...${NC}"
if [ ! -d "schach" ]; then
    echo " -> Klone das Schach-Repository von GitHub..."
    git clone https://github.com/Sandroexe/schach.git
    cd schach
else
    echo -e " -> Ordner ${CYAN}'schach'${NC} existiert bereits. Wechseln in das Verzeichnis..."
    cd schach
fi

# 3. Optionale Python-Pip-Requirements installieren
if [ -f "requirements.txt" ]; then
    echo -e "\n${YELLOW}[3/3] Zusätzliche Python-Pakete...${NC}"
    echo " -> Installiere Pip-Abhängigkeiten..."
    pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt
fi

# Erfolgsmeldung
echo -e "\n${BLUE}==================================================${NC}"
echo -e "${GREEN}🎉 INSTALLATION ERFOLGREICH ABGESCHLOSSEN!${NC}"
echo -e "${BLUE}==================================================${NC}\n"

# Interaktive Abfrage am Ende
echo -e "Möchtest du das Schachspiel direkt starten?"
echo -e "-> Tippe ${GREEN}ja${NC} / ${GREEN}yes${NC} zum Starten."
echo -e "-> Drücke einfach ${YELLOW}[ENTER]${NC} zum Beenden."
read -p "Deine Auswahl: " user_choice

# Eingabe in Kleinbuchstaben umwandeln, um Fehler zu vermeiden
user_choice=$(echo "$user_choice" | tr '[:upper:]' '[:lower:]')

if [[ "$user_choice" == "ja" || "$user_choice" == "yes" ]]; then
    echo -e "\n${GREEN}🚀 Starte Schach... Viel Spaß!${NC}\n"
    # Falls dein Hauptskript schach.py heißt:
    python schach.py || python3 schach.py
else
    echo -e "\n${CYAN}Alles klar! Du findest dein Projekt im Ordner:${NC} $(pwd)"
    echo -e "Du kannst es später mit ${YELLOW}python schach.py${NC} starten.\n"
fi
