#!/bin/bash
# filepath: /home/kutay/Desktop/viusalcode/projeler/start_gif_widget.sh
# GIF Widget Launcher Script

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if xdotool is installed
if ! command -v xdotool &> /dev/null; then
    echo "❌ xdotool is not installed!"
    echo "📦 To install: sudo apt install xdotool"
    exit 1
fi

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed!"
    echo "📦 To install: sudo apt install python3"
    exit 1
fi

# Check if PIL (Pillow) is installed
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "❌ PIL (Pillow) is not installed!"
    echo "📦 To install: pip3 install Pillow"
    exit 1
fi

echo "🎭 Starting GIF Widget..."
echo "📂 Directory: $SCRIPT_DIR"

# Start GIF Widget
cd "$SCRIPT_DIR"
python3 gif_widget.py

# Error check
if [ $? -ne 0 ]; then
    echo "❌ Failed to start GIF Widget!"
    echo "🔍 For error details: python3 gif_widget.py"
    exit 1
fi

echo "✅ GIF Widget closed successfully."