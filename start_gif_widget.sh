#!/bin/bash
# filepath: /home/kutay/Desktop/viusalcode/projeler/start_gif_widget.sh
# GIF Widget Başlatma Scripti

# Script'in bulunduğu dizini al
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# xdotool kurulu mu kontrol et
if ! command -v xdotool &> /dev/null; then
    echo "❌ xdotool kurulu değil!"
    echo "📦 Kurmak için: sudo apt install xdotool"
    exit 1
fi

# Python3 kurulu mu kontrol et
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 kurulu değil!"
    echo "📦 Kurmak için: sudo apt install python3"
    exit 1
fi

# PIL (Pillow) kurulu mu kontrol et
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "❌ PIL (Pillow) kurulu değil!"
    echo "📦 Kurmak için: pip3 install Pillow"
    exit 1
fi

echo "🎭 GIF Widget başlatılıyor..."
echo "📂 Dizin: $SCRIPT_DIR"

# GIF Widget'ı başlat
cd "$SCRIPT_DIR"
python3 gif_widget.py

# Hata kontrolü
if [ $? -ne 0 ]; then
    echo "❌ GIF Widget başlatılamadı!"
    echo "🔍 Hata detayları için: python3 gif_widget.py"
    exit 1
fi

echo "✅ GIF Widget başarıyla kapatıldı."