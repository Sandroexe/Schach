#!/bin/bash
set -e

# ============================================================
#  Multiplayer Schach – Installer
#  Kompatibel mit: Linux (Arch, Debian/Ubuntu, Fedora, openSUSE)
#                  macOS (Homebrew), Windows (Git Bash / WSL)
# ============================================================

# ── Farben & Styles ─────────────────────────────────────────
BOLD='\033[1m'
DIM='\033[2m'
ITALIC='\033[3m'
UNDERLINE='\033[4m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
BG_BLUE='\033[44m'
BG_GREEN='\033[42m'
BG_MAGENTA='\033[45m'
NC='\033[0m'

# ── Hilfsfunktionen ─────────────────────────────────────────

# Gesamtfortschritt: 5 Schritte
TOTAL_STEPS=5
CURRENT_STEP=0

# Fortschrittsbalken (gesamt) zeichnen
draw_overall_progress() {
    local step=$1
    local total=$2
    local label="$3"
    local width=40
    local filled=$(( step * width / total ))
    local empty=$(( width - filled ))
    local percent=$(( step * 100 / total ))

    local bar=""
    for (( i=0; i<filled; i++ )); do bar+="█"; done
    for (( i=0; i<empty; i++ )); do bar+="░"; done

    printf "\r  ${MAGENTA}${BOLD}Gesamt${NC} ${DIM}[${NC}${GREEN}${bar}${NC}${DIM}]${NC} ${WHITE}${percent}%%${NC}  ${DIM}${label}${NC}    "
}

# Simulations-Ladebalken (für kurze Aktionen)
progress_bar() {
    local label="$1"
    local duration=${2:-1}    # Sekunden
    local width=30
    local steps=20

    printf "\n"
    for (( i=1; i<=steps; i++ )); do
        local filled=$(( i * width / steps ))
        local empty=$(( width - filled ))
        local percent=$(( i * 100 / steps ))

        local bar=""
        for (( j=0; j<filled; j++ )); do bar+="█"; done
        for (( j=0; j<empty; j++ )); do bar+="░"; done

        printf "\r    ${CYAN}${label}${NC} ${DIM}[${NC}${BLUE}${bar}${NC}${DIM}]${NC} ${WHITE}${percent}%%${NC}"
        sleep "$(echo "scale=3; $duration / $steps" | bc 2>/dev/null || echo "0.05")"
    done
    printf "\r    ${GREEN}✓${NC} ${label} $(printf '%*s' $((width + 8)) '')  \n"
}

# Spinner für länger laufende Befehle
spinner() {
    local pid=$1
    local label="$2"
    local spin_chars='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local i=0

    while kill -0 "$pid" 2>/dev/null; do
        local char="${spin_chars:$i:1}"
        printf "\r    ${CYAN}${char}${NC} ${label}..."
        i=$(( (i + 1) % ${#spin_chars} ))
        sleep 0.1
    done

    wait "$pid" 2>/dev/null
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        printf "\r    ${GREEN}✓${NC} ${label}                              \n"
    else
        printf "\r    ${RED}✗${NC} ${label} ${RED}(Fehler!)${NC}              \n"
        return $exit_code
    fi
}

# Schritt-Header ausgeben
step_header() {
    local step_num=$1
    local total=$2
    local title="$3"
    echo ""
    echo -e "  ${BG_BLUE}${WHITE}${BOLD} SCHRITT ${step_num}/${total} ${NC}  ${BOLD}${title}${NC}"
    echo -e "  ${DIM}$(printf '%.0s─' {1..50})${NC}"
}

# Betriebssystem erkennen
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "windows"
    elif grep -qi "microsoft" /proc/version 2>/dev/null; then
        echo "wsl"
    elif [ -f /etc/arch-release ] || grep -qi "cachyos\|endeavour\|manjaro" /etc/os-release 2>/dev/null; then
        echo "arch"
    elif [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/fedora-release ] || grep -qi "fedora" /etc/os-release 2>/dev/null; then
        echo "fedora"
    elif [ -f /etc/SuSE-release ] || grep -qi "opensuse\|suse" /etc/os-release 2>/dev/null; then
        echo "suse"
    else
        echo "unknown"
    fi
}

# ── Banner ──────────────────────────────────────────────────
clear 2>/dev/null || true
echo ""
echo -e "  ${BLUE}${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}                                                  ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}   ${WHITE}${BOLD}♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜${NC}                            ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}   ${WHITE}${BOLD}♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟${NC}                            ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}                                                  ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}   ${YELLOW}${BOLD}Multiplayer Schach${NC}                              ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}   ${DIM}HTL Abschlussarbeit – Installer v2.0${NC}          ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}                                                  ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}   ${DIM}♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙${NC}                            ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}   ${DIM}♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖${NC}                            ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}║${NC}                                                  ${BLUE}${BOLD}║${NC}"
echo -e "  ${BLUE}${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# ── System erkennen ─────────────────────────────────────────
OS_TYPE=$(detect_os)

case "$OS_TYPE" in
    arch)    OS_LABEL="Arch Linux / CachyOS" ;;
    debian)  OS_LABEL="Debian / Ubuntu" ;;
    fedora)  OS_LABEL="Fedora" ;;
    suse)    OS_LABEL="openSUSE" ;;
    macos)   OS_LABEL="macOS" ;;
    windows) OS_LABEL="Windows (Git Bash)" ;;
    wsl)     OS_LABEL="Windows Subsystem for Linux" ;;
    *)       OS_LABEL="Unbekanntes System" ;;
esac

echo -e "  ${DIM}System erkannt:${NC} ${CYAN}${BOLD}${OS_LABEL}${NC}"
echo -e "  ${DIM}Datum:${NC}          ${CYAN}$(date '+%d.%m.%Y – %H:%M Uhr')${NC}"
echo ""

CURRENT_STEP=0
draw_overall_progress $CURRENT_STEP $TOTAL_STEPS "Initialisierung..."
echo ""

# ════════════════════════════════════════════════════════════
#  SCHRITT 1: System-Abhängigkeiten
# ════════════════════════════════════════════════════════════
CURRENT_STEP=1
step_header $CURRENT_STEP $TOTAL_STEPS "System-Abhängigkeiten installieren"

install_packages() {
    case "$OS_TYPE" in
        arch)
            echo -e "    ${DIM}→ pacman -S --needed ...${NC}"
            sudo pacman -S --needed --noconfirm git python python-pygame >/dev/null 2>&1
            ;;
        debian)
            echo -e "    ${DIM}→ apt update && apt install ...${NC}"
            sudo apt update -qq >/dev/null 2>&1
            sudo apt install -y -qq git python3 python3-pip python3-pygame >/dev/null 2>&1
            ;;
        fedora)
            echo -e "    ${DIM}→ dnf install ...${NC}"
            sudo dnf install -y -q git python3 python3-pip python3-pygame >/dev/null 2>&1
            ;;
        suse)
            echo -e "    ${DIM}→ zypper install ...${NC}"
            sudo zypper --non-interactive --quiet install git python3 python3-pip python3-pygame >/dev/null 2>&1
            ;;
        macos)
            if ! command -v brew &>/dev/null; then
                echo -e "    ${YELLOW}⚠ Homebrew nicht gefunden. Installiere Homebrew...${NC}"
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" </dev/null >/dev/null 2>&1
            fi
            echo -e "    ${DIM}→ brew install ...${NC}"
            brew install git python3 pygame >/dev/null 2>&1 || true
            ;;
        windows)
            echo -e "    ${YELLOW}⚠ Windows erkannt.${NC}"
            echo -e "    ${DIM}Stelle sicher, dass Python 3 und Git installiert sind.${NC}"
            echo -e "    ${DIM}→ https://www.python.org/downloads/${NC}"
            if command -v pip &>/dev/null || command -v pip3 &>/dev/null; then
                (pip install pygame 2>/dev/null || pip3 install pygame 2>/dev/null) >/dev/null 2>&1 || true
            fi
            ;;
        wsl)
            echo -e "    ${DIM}→ apt update && apt install ... (WSL)${NC}"
            sudo apt update -qq >/dev/null 2>&1
            sudo apt install -y -qq git python3 python3-pip python3-pygame >/dev/null 2>&1
            ;;
        *)
            echo -e "    ${YELLOW}⚠ Unbekanntes System!${NC}"
            echo -e "    ${DIM}Bitte installiere manuell: git, python3, pygame${NC}"
            ;;
    esac
}

install_packages &
spinner $! "Systempakete werden installiert"

draw_overall_progress $CURRENT_STEP $TOTAL_STEPS "Pakete installiert"
echo ""

# ════════════════════════════════════════════════════════════
#  SCHRITT 2: Python prüfen
# ════════════════════════════════════════════════════════════
CURRENT_STEP=2
step_header $CURRENT_STEP $TOTAL_STEPS "Python-Umgebung prüfen"

PYTHON_CMD=""
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
fi

if [ -n "$PYTHON_CMD" ]; then
    PY_VERSION=$($PYTHON_CMD --version 2>&1)
    echo -e "    ${GREEN}✓${NC} ${PY_VERSION} gefunden"
else
    echo -e "    ${RED}✗${NC} Python wurde nicht gefunden!"
    echo -e "    ${DIM}Bitte installiere Python 3: https://www.python.org/downloads/${NC}"
    exit 1
fi

progress_bar "Python-Umgebung verifiziert" 0.5

draw_overall_progress $CURRENT_STEP $TOTAL_STEPS "Python bereit"
echo ""

# ════════════════════════════════════════════════════════════
#  SCHRITT 3: Repository klonen
# ════════════════════════════════════════════════════════════
CURRENT_STEP=3
step_header $CURRENT_STEP $TOTAL_STEPS "Repository herunterladen"

REPO_URL="https://github.com/Sandroexe/schach.git"

if [ -d "schach" ]; then
    echo -e "    ${YELLOW}→${NC} Ordner ${CYAN}'schach'${NC} existiert bereits."
    echo -e "    ${DIM}  Aktualisiere Repository...${NC}"
    (cd schach && git pull --quiet 2>/dev/null) &
    spinner $! "Repository aktualisieren"
else
    git clone --progress "$REPO_URL" schach 2>&1 | while IFS= read -r line; do
        if [[ "$line" == *"Receiving objects:"* || "$line" == *"Resolving deltas:"* ]]; then
            # Git-Fortschritt extrahieren
            percent=$(echo "$line" | grep -oP '\d+(?=%)' | tail -1)
            if [ -n "$percent" ]; then
                local_width=30
                filled=$(( percent * local_width / 100 ))
                empty=$(( local_width - filled ))
                bar=""
                for (( j=0; j<filled; j++ )); do bar+="█"; done
                for (( j=0; j<empty; j++ )); do bar+="░"; done
                printf "\r    ${CYAN}Herunterladen${NC} ${DIM}[${NC}${BLUE}${bar}${NC}${DIM}]${NC} ${WHITE}${percent}%%${NC}"
            fi
        fi
    done
    echo -e "\r    ${GREEN}✓${NC} Repository erfolgreich geklont                              "
fi

draw_overall_progress $CURRENT_STEP $TOTAL_STEPS "Repository bereit"
echo ""

# ════════════════════════════════════════════════════════════
#  SCHRITT 4: Ins Projektverzeichnis wechseln & pip-Pakete
# ════════════════════════════════════════════════════════════
CURRENT_STEP=4
step_header $CURRENT_STEP $TOTAL_STEPS "Python-Abhängigkeiten installieren"

cd schach

if [ -f "requirements.txt" ]; then
    (pip install -r requirements.txt --break-system-packages -q 2>/dev/null || \
     pip3 install -r requirements.txt --break-system-packages -q 2>/dev/null || \
     pip install -r requirements.txt -q 2>/dev/null || \
     pip3 install -r requirements.txt -q 2>/dev/null || true) &
    spinner $! "Pip-Pakete installieren"
else
    echo -e "    ${DIM}Keine requirements.txt gefunden – überspringe.${NC}"
    progress_bar "Abhängigkeiten geprüft" 0.3
fi

draw_overall_progress $CURRENT_STEP $TOTAL_STEPS "Abhängigkeiten bereit"
echo ""

# ════════════════════════════════════════════════════════════
#  SCHRITT 5: Abschluss & Verifizierung
# ════════════════════════════════════════════════════════════
CURRENT_STEP=5
step_header $CURRENT_STEP $TOTAL_STEPS "Installation abschließen"

progress_bar "Konfiguration finalisieren" 0.4
progress_bar "Berechtigungen setzen" 0.2

draw_overall_progress $CURRENT_STEP $TOTAL_STEPS "Fertig!"
echo ""

# ── Abschluss-Banner ───────────────────────────────────────
echo ""
echo -e "  ${GREEN}${BOLD}╔══════════════════════════════════════════════════╗${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}                                                  ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}   ${WHITE}${BOLD}🎉  INSTALLATION ERFOLGREICH!${NC}                   ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}                                                  ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}   ${DIM}Starte das Spiel mit:${NC}                          ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}                                                  ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}   ${CYAN}${BOLD}  cd schach${NC}                                    ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}   ${CYAN}${BOLD}  python3 schach.py${NC}                             ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}                                                  ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}   ${DIM}Projektordner: $(pwd)${NC}"
echo -e "  ${GREEN}${BOLD}║${NC}                                                  ${GREEN}${BOLD}║${NC}"
echo -e "  ${GREEN}${BOLD}╚══════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${DIM}Viel Spaß beim Spielen! ♟️${NC}"
echo ""
