#!/bin/bash
set -e

echo ""
echo "========================================="
echo "  Multiplayer Schach - Installer"
echo "  HTL Abschlussarbeit"
echo "========================================="
echo ""

# --- Betriebssystem erkennen ---
OS="unknown"
if [ "$(uname)" = "Darwin" ]; then
    OS="macos"
elif [ -f /etc/arch-release ] || grep -qi "cachyos\|endeavour\|manjaro" /etc/os-release 2>/dev/null; then
    OS="arch"
elif [ -f /etc/debian_version ]; then
    OS="debian"
elif [ -f /etc/fedora-release ]; then
    OS="fedora"
elif grep -qi "opensuse\|suse" /etc/os-release 2>/dev/null; then
    OS="suse"
elif grep -qi "microsoft" /proc/version 2>/dev/null; then
    OS="debian"
fi

echo "[1/4] Systempakete installieren..."

case "$OS" in
    arch)
        echo "  -> Arch Linux / CachyOS erkannt"
        sudo pacman -S --needed --noconfirm git python python-pygame >/dev/null 2>&1
        ;;
    debian)
        echo "  -> Debian / Ubuntu erkannt"
        sudo apt update -qq >/dev/null 2>&1
        sudo apt install -y -qq git python3 python3-pip python3-pygame >/dev/null 2>&1
        ;;
    fedora)
        echo "  -> Fedora erkannt"
        sudo dnf install -y -q git python3 python3-pip python3-pygame >/dev/null 2>&1
        ;;
    suse)
        echo "  -> openSUSE erkannt"
        sudo zypper --non-interactive --quiet install git python3 python3-pip python3-pygame >/dev/null 2>&1
        ;;
    macos)
        echo "  -> macOS erkannt"
        if ! command -v brew >/dev/null 2>&1; then
            echo "  -> Homebrew wird installiert..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" </dev/null >/dev/null 2>&1
        fi
        brew install git python3 pygame >/dev/null 2>&1 || true
        ;;
    *)
        echo "  -> Unbekanntes System. Bitte installiere git, python3 und pygame manuell."
        ;;
esac
echo "  Fertig."
echo ""

echo "[2/4] Python pruefen..."
PYTHON_CMD=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

if [ -n "$PYTHON_CMD" ]; then
    echo "  -> $($PYTHON_CMD --version 2>&1) gefunden"
else
    echo "  FEHLER: Python nicht gefunden!"
    echo "  Bitte installiere Python 3: https://www.python.org/downloads/"
    exit 1
fi
echo ""

echo "[3/4] Repository herunterladen..."
if [ -d "schach" ]; then
    echo "  -> Ordner 'schach' existiert bereits, aktualisiere..."
    cd schach
    git pull --quiet 2>/dev/null || true
else
    echo "  -> Klone von GitHub..."
    git clone --quiet https://github.com/Sandroexe/schach.git
    cd schach
fi
echo "  Fertig."
echo ""

echo "[4/4] Python-Abhaengigkeiten..."
if [ -f "requirements.txt" ]; then
    echo "  -> Installiere requirements.txt..."
    pip install -r requirements.txt --break-system-packages -q 2>/dev/null || \
    pip3 install -r requirements.txt --break-system-packages -q 2>/dev/null || \
    pip install -r requirements.txt -q 2>/dev/null || \
    pip3 install -r requirements.txt -q 2>/dev/null || true
    echo "  Fertig."
else
    echo "  -> Keine requirements.txt gefunden, ueberspringe."
fi
echo ""

echo "========================================="
echo "  Installation abgeschlossen!"
echo ""
echo "  Starte das Spiel mit:"
echo "    cd schach"
echo "    python3 schach.py"
echo ""
echo "  Projektordner: $(pwd)"
echo "========================================="
echo ""
