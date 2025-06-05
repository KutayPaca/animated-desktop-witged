# 🎭 Animated Desktop Widget

A lightweight floating GIF widget for Linux desktop with auto-hide, drag & resize functionality. Perfect for adding some life to your desktop without getting in the way!

## ✨ Features

- 🎯 **Smart auto-hide**: Optional feature to hide when other apps are active (can be toggled on/off)
- 🖱️ **Draggable**: Move the widget anywhere on your screen
- 📏 **Resizable**: Ctrl+drag to resize the widget (50px - 500px)
- 🔄 **Double-click reset**: Return to default position (bottom-right corner)
- 💾 **Memory**: Remembers your GIF choice, widget size/position, and settings
- 🎮 **Right-click menu**: Easy access to all controls
- ⚙️ **Customizable**: Toggle auto-hide behavior from the context menu
- ⚡ **Lightweight**: Minimal resource usage

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/KutayPaca/animated-desktop-witged.git
cd animated-desktop-witged
```

### 2. Easy Installation (Recommended)
```bash
chmod +x start_gif_widget.sh
./start_gif_widget.sh
```

The script will automatically:
- Check for required dependencies
- Install missing packages (with instructions)
- Launch the GIF widget

### 3. Manual Installation

#### Install Dependencies
```bash
# Install xdotool (for desktop detection)
sudo apt install xdotool

# Install Python3 (if not already installed)
sudo apt install python3

# Install Pillow (PIL) for image processing
pip3 install Pillow
```

#### Run the Widget
```bash
python3 gif_widget.py
```

## 🎮 Controls

| Action | Control |
|--------|---------|
| **Move widget** | Left-click + drag |
| **Reset position** | Double left-click |
| **Resize mode** | Right-click → "Resize Mode" |
| **Resize widget** | Ctrl + drag (in resize mode) |
| **Open menu** | Right-click |
| **Pause/Play** | Right-click → "Play/Pause Animation" |
| **Change GIF** | Right-click → "Select New GIF" |
| **Toggle auto-hide** | Right-click → "Hide when not on desktop" |

## 📋 Requirements

### System Requirements
- **OS**: Linux (tested on Ubuntu/GNOME)
- **Python**: 3.6 or higher
- **Desktop Environment**: Any (GNOME, KDE, XFCE, etc.)
- **Display Server**: X11 (recommended), Wayland (limited support)

### Tested Distributions
- **Ubuntu**: 18.04, 20.04, 22.04, 24.04 LTS and interim releases
- **Ubuntu Derivatives**: Linux Mint, Pop!_OS, Elementary OS, Zorin OS
- **Other**: KDE Neon, Kubuntu, Xubuntu, Lubuntu

### Dependencies
- `python3` - Core Python runtime
- `python3-tk` - Tkinter GUI library
- `python3-pil` or `pillow` - Image processing
- `xdotool` - Desktop window detection

### Installation Commands by Distribution

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pil xdotool
```

#### Fedora/CentOS/RHEL
```bash
sudo dnf install python3 python3-tkinter python3-pillow xdotool
```

#### Arch Linux
```bash
sudo pacman -S python python-pillow tk xdotool
```

## 🔧 Configuration

### First Run Setup
1. Run the widget for the first time
2. A file dialog will open - select your favorite GIF
3. The widget will appear in the bottom-right corner
4. Your settings are automatically saved to `~/.gif_widget_config.json`

### Configuration File Location
```
~/.gif_widget_config.json
```

### Reset Configuration
```bash
rm ~/.gif_widget_config.json
```

## 🛠️ Troubleshooting

### Widget Not Appearing
```bash
# Check if xdotool is installed
which xdotool

# Install if missing
sudo apt install xdotool

# Run with debug output
python3 gif_widget.py
```

### GIF Not Loading
- Ensure the GIF file is valid and not corrupted
- Check file permissions (readable)
- Try a different GIF file
- Supported format: `.gif` files only

### Auto-hide Not Working
- Verify xdotool is installed and working:
```bash
xdotool getactivewindow getwindowname
```
- Check if your desktop environment is supported
- Try toggling the auto-hide feature from the right-click menu
- Try restarting the widget

### Performance Issues
- Use smaller GIF files (< 5MB recommended)
- Reduce widget size if the GIF has many frames
- Close other resource-intensive applications

## 📁 Project Structure

```
animated-desktop-witged/
├── gif_widget.py           # Main application
├── start_gif_widget.sh     # Easy launcher script
├── README.md              # This file (English & Turkish)
├── gif/                   # Sample GIFs (optional)
├── .git/                  # Git repository data
└── .venv/                 # Python virtual environment (optional)
```


## 🐛 Known Issues

- May not work properly with Wayland (X11 recommended)
- Desktop detection might not work on all desktop environments (can be disabled via menu)
- Large GIFs (>10MB) may cause performance issues


## 🙏 Acknowledgments

- Built with Python and Tkinter
- Uses PIL (Pillow) for image processing
- Desktop detection powered by xdotool
- Inspired by desktop pet applications

---

**Enjoy your animated desktop! 🎉**

---

# 🎭 Animasyonlu Masaüstü Widget'ı

Otomatik gizlenme, sürükleme ve boyutlandırma özellikli Linux masaüstü için hafif yüzen GIF widget'ı. Yolunuzdan çekilirken masaüstünüzü canlandırmak için mükemmel!

## ✨ Özellikler

- 🎯 **Akıllı otomatik gizlenme**: Diğer uygulamalar aktifken gizlenme özelliği (açılıp kapatılabilir)
- 🖱️ **Sürüklenebilir**: Widget'ı ekranınızda istediğiniz yere taşıyın
- 📏 **Boyutlandırılabilir**: Ctrl+sürükle ile widget'ı yeniden boyutlandırın (50px - 500px)
- 🔄 **Çift tık sıfırlama**: Varsayılan konuma dönün (sağ alt köşe)
- 💾 **Hafıza**: GIF seçiminizi, widget boyutu/konumunu ve ayarları hatırlar
- 🎮 **Sağ tık menüsü**: Tüm kontrollere kolay erişim
- ⚙️ **Özelleştirilebilir**: Sağ tık menüsünden otomatik gizlenme davranışını değiştirin
- ⚡ **Hafif**: Minimal kaynak kullanımı

## 🚀 Hızlı Başlangıç

### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/KutayPaca/animated-desktop-witged.git
cd animated-desktop-witged
```

### 2. Kolay Kurulum (Önerilen)
```bash
chmod +x start_gif_widget.sh
./start_gif_widget.sh
```

Script otomatik olarak:
- Gerekli bağımlılıkları kontrol eder
- Eksik paketleri yükler (talimatlarla birlikte)
- GIF widget'ını başlatır

### 3. Manuel Kurulum

#### Bağımlılıkları Kurun
```bash
# xdotool'u kurun (masaüstü algılama için)
sudo apt install xdotool

# Python3'ü kurun (zaten kurulu değilse)
sudo apt install python3

# Pillow (PIL) kurun (görüntü işleme için)
pip3 install Pillow
```

#### Widget'ı Çalıştırın
```bash
python3 gif_widget.py
```

## 🎮 Kontroller

| Eylem | Kontrol |
|-------|---------|
| **Widget'ı taşı** | Sol tık + sürükle |
| **Konumu sıfırla** | Çift sol tık |
| **Boyutlandırma modu** | Sağ tık → "Boyut Düzenle" |
| **Widget'ı boyutlandır** | Ctrl + sürükle (boyutlandırma modunda) |
| **Menüyü aç** | Sağ tık |
| **Duraklat/Oynat** | Sağ tık → "Animasyonu Durdur/Başlat" |
| **GIF değiştir** | Sağ tık → "Yeni GIF Seç" |
| **Otomatik gizlenme** | Sağ tık → "Masaüstü dışında gizle" |

## 📋 Gereksinimler

### Sistem Gereksinimleri
- **İşletim Sistemi**: Linux (Ubuntu/GNOME'da test edildi)
- **Python**: 3.6 veya üzeri
- **Masaüstü Ortamı**: Herhangi biri (GNOME, KDE, XFCE, vb.)
- **Görüntü Sunucusu**: X11 (önerilen), Wayland (sınırlı destek)

### Test Edilen Dağıtımlar
- **Ubuntu**: 18.04, 20.04, 22.04, 24.04 LTS ve ara sürümler
- **Ubuntu Türevleri**: Linux Mint, Pop!_OS, Elementary OS, Zorin OS
- **Diğerleri**: KDE Neon, Kubuntu, Xubuntu, Lubuntu

### Bağımlılıklar
- `python3` - Temel Python çalışma zamanı
- `python3-tk` - Tkinter GUI kütüphanesi
- `python3-pil` veya `pillow` - Görüntü işleme
- `xdotool` - Masaüstü pencere algılama

### Dağıtıma Göre Kurulum Komutları

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-tk python3-pil xdotool
```

#### Fedora/CentOS/RHEL
```bash
sudo dnf install python3 python3-tkinter python3-pillow xdotool
```

#### Arch Linux
```bash
sudo pacman -S python python-pillow tk xdotool
```

## 🔧 Konfigürasyon

### İlk Çalıştırma Kurulumu
1. Widget'ı ilk kez çalıştırın
2. Bir dosya seçim dialogu açılacak - favori GIF'inizi seçin
3. Widget sağ alt köşede görünecek
4. Ayarlarınız otomatik olarak `~/.gif_widget_config.json`'a kaydedilir

### Konfigürasyon Dosyası Konumu
```
~/.gif_widget_config.json
```

### Konfigürasyonu Sıfırla
```bash
rm ~/.gif_widget_config.json
```

## 🛠️ Sorun Giderme

### Widget Görünmüyor
```bash
# xdotool kurulu mu kontrol edin
which xdotool

# Eksikse kurun
sudo apt install xdotool

# Debug çıktısıyla çalıştırın
python3 gif_widget.py
```

### GIF Yüklenmiyor
- GIF dosyasının geçerli ve bozuk olmadığından emin olun
- Dosya izinlerini kontrol edin (okunabilir)
- Farklı bir GIF dosyası deneyin
- Desteklenen format: Sadece `.gif` dosyaları

### Otomatik Gizlenme Çalışmıyor
- xdotool'un kurulu ve çalıştığını doğrulayın:
```bash
xdotool getactivewindow getwindowname
```
- Masaüstü ortamınızın desteklenip desteklenmediğini kontrol edin
- Sağ tık menüsünden otomatik gizlenme özelliğini açıp kapatmayı deneyin
- Widget'ı yeniden başlatmayı deneyin

### Performans Sorunları
- Daha küçük GIF dosyaları kullanın (< 5MB önerilen)
- GIF'in çok fazla frame'i varsa widget boyutunu küçültün
- Diğer kaynak yoğun uygulamaları kapatın

## 📁 Proje Yapısı

```
animated-desktop-witged/
├── gif_widget.py           # Ana uygulama
├── start_gif_widget.sh     # Kolay başlatıcı script
├── README.md              # Bu dosya (İngilizce ve Türkçe)
├── gif/                   # Örnek GIF'ler (opsiyonel)
├── .git/                  # Git repository verileri
└── .venv/                 # Python sanal ortamı (opsiyonel)
```

## 🐛 Bilinen Sorunlar

- Wayland ile düzgün çalışmayabilir (X11 önerilen)
- Masaüstü algılama tüm masaüstü ortamlarında çalışmayabilir (menüden kapatılabilir)
- Büyük GIF'ler (>10MB) performans sorunlarına neden olabilir

## 🙏 Teşekkürler

- Python ve Tkinter ile geliştirildi
- Görüntü işleme için PIL (Pillow) kullanır
- Masaüstü algılama xdotool ile desteklenir
- Masaüstü pet uygulamalarından ilham alındı

---

**Animasyonlu masaüstünüzün keyfini çıkarın! 🎉**
