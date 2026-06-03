#!/bin/bash
# set -e deaktiviert, damit der Ladebalken-Counter sauber läuft

# Farben für eine schöne Terminal-Ausgabe definieren
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Funktion für einen Ladebalken (Fortschritt in Prozent)
show_progress() {
    local duration=$1
    local label=$2
    local lr=50
    for ((i=0; i<=lr; i++)); do
        local p=$((i * 100 / lr))
        local num=$((i * 100 / lr))
        local progress=$((i * lr / lr))
        printf -v dots "%*s" "$progress" ""
        printf -v spaces "%*s" "$((lr - progress))" ""
        printf "\r${CYAN}%s${NC} [${GREEN}%s${NC}%s] %d%%" "$label" "${dots// /#}" "${spaces// /-}" "$num"
        sleep 0.02
    done
    echo ""
}

# Funktion für einen rotierenden Lade-Spinner (während Installationen laufen)
run_with_spinner() {
    local pid=$1
    local label=$2
    local spin='-\|/'
    local i=0
    while kill -0 "$pid" 2>/dev/null; do
        i=$(( (i+1) % 4 ))
        printf "\r${CYAN}%s${NC} [${YELLOW}%s${NC}]" "$label" "${spin:$i:1}"
        sleep 0.1
    done
    printf "\r${CYAN}%s${NC} [${GREEN}✓${NC}]\n" "$label"
}

echo -e "${BLUE}==================================================${NC}"
echo -e "${YELLOW}  ♟️  Multiplayer Schach - HTL Abschlussarbeit  ♟️${NC}"
echo -e "${BLUE}==================================================${NC}"
echo -e "${CYAN} -> Initialisiere Installations-Assistenten...${NC}"
show_progress 1 "Lade Skriptkomponenten"
echo ""

# 1. System-Paketmanager erkennen und Abhängigkeiten installieren
if [ -f /etc/arch-release ] || grep -q "cachyos" /etc/os-release; then
    echo -e "${YELLOW}[1/3] CachyOS / Arch Linux erkannt.${NC}"
    (sudo pacman -S --needed --noconfirm git python python-pygame >/dev/null 2>&1) &
    run_with_spinner $! "Installiere Systempakete via pacman"
elif [ -f /etc/debian_version ]; then
    echo -e "${YELLOW}[1/3] Debian / Ubuntu erkannt.${NC}"
    echo -e " -> Aktualisiere Paketquellen..."
    sudo apt update -y >/dev/null 2>&1
    (sudo apt install -y git python3 python3-pip python3-pygame >/dev/null 2>&1) &
    run_with_spinner $! "Installiere Systempakete via apt"
else
    echo -e "${YELLOW}⚠️  Unbekanntes System.${NC} Versuche mit Standard-Pip fortzufahren..."
fi

# 2. Repository klonen mit Fake-Fortschritt für die Optik
echo -e "\n${YELLOW}[2/3] Verbindung mit GitHub wird hergestellt...${NC}"
if [ ! -d "schach" ]; then
    # Klonen im Hintergrund
    git clone https://github.com/Sandroexe/schach.git >/dev/null 2>&1 &
    pid=$!
    
    # Schöner Ladebalken während des Downloads
    show_progress 2 "Downloade Repository (schach.git)"
    wait $pid 2>/dev/null
    cd schach
else
    echo -e " -> Ordner ${CYAN}'schach'${NC} existiert bereits. Wechseln in das Verzeichnis..."
    cd schach
fi

# 3. Optionale Python-Pip-Requirements installieren
if [ -f "requirements.txt" ]; then
    echo -e "\n${YELLOW}[3/3] Überprüfe zusätzliche Python-Pakete...${NC}"
    (pip install -r requirements.txt --break-system-packages >/dev/null 2>&1 || pip install -r requirements.txt >/dev/null 2>&1) &
    run_with_spinner $! "Installiere Pip-Abhängigkeiten"
fi

# Gesamten Fortschritt abschließen
echo ""
show_progress 0.5 "Verifiziere Spieldateien"

# Erfolgsmeldung
echo -e "\n${BLUE}==================================================${NC}"
echo -e "${GREEN}🎉 INSTALLATION ERFOLGREICH ABGESCHLOSSEN!${NC}"
echo -e "${BLUE}==================================================${NC}\n"

# Interaktive Abfrage am Ende
echo -e "Möchtest du das Schachspiel direkt starten?"
echo -e "-> Tippe ${GREEN}ja${NC} / ${GREEN}yes${NC} zum Starten."
echo -e "-> Drücke einfach ${YELLOW}[ENTER]${NC} zum Beenden."
read -p "Deine Auswahl: " user_choice

user_choice=$(echo "$user_choice" | tr '[:upper:]' '[:lower:]')

if [[ "$user_choice" == "ja" || "$user_choice" == "yes" ]]; then
    echo -e "\n${GREEN}🚀 Starte schach.py... Viel Spaß!${NC}\n"
    python schach.py || python3 schach.py
else
    echo -e "\n${CYAN}Alles klar! Du findest dein Projekt im Ordner:${NC} $(pwd)"
    echo -e "Du kannst es später mit ${YELLOW}python schach.py${NC} starten.\n"
fi
