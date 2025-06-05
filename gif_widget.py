#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageGrab
import subprocess
import json
import os
import threading
import time
from collections import Counter
import colorsys

class GifWidget:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.gif_widget_config.json")
        self.root = tk.Tk()
        self.root.title("GIF Widget")
        
        # Window properties
        self.root.overrideredirect(True)  # Remove title bar
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', 1.0)  # Transparency
        self.root.configure(bg='black')
        
        # GIF variables
        self.gif_frames = []
        self.current_frame = 0
        self.is_playing = True
        self.gif_path = None
        self.animation_speed = 100
        
        # Position variables
        self.start_x = 0
        self.start_y = 0
        self.default_x = None
        self.default_y = None
        
        # Resize mode variables
        self.resize_mode = False
        self.min_size = 50
        self.max_size = 500
        
        # Menu control variable
        self.menu_open = False
        self.last_menu_position = (0, 0)  # Store last menu position
        
        # Hide when not on desktop control
        self.hide_when_not_desktop = True  # Default enabled
        
        # Border/Frame settings
        self.border_enabled = False
        self.border_style = "solid"  # solid, dotted, dashed, double, gradient
        self.border_color = "#FF0000"  # Default red
        self.border_width = 3
        self.border_opacity = 1.0
        
        # Available border styles
        self.border_styles = {
            "None": {"enabled": False},
            "Classic Red": {"enabled": True, "style": "solid", "color": "#FF0000", "width": 3},
            "Neon Blue": {"enabled": True, "style": "solid", "color": "#00FFFF", "width": 2},
            "Gold Frame": {"enabled": True, "style": "double", "color": "#FFD700", "width": 4},
            "Green Glow": {"enabled": True, "style": "solid", "color": "#00FF00", "width": 2},
            "Purple Magic": {"enabled": True, "style": "dashed", "color": "#8A2BE2", "width": 3},
            "Rainbow": {"enabled": True, "style": "gradient", "color": "#FF0000", "width": 4}
        }
        self.current_border_name = "None"
        
        # Wallpaper sync configuration
        self.wallpaper_sync_enabled = False
        self.last_wallpaper_analysis_pos = None
        self.wallpaper_analysis_thread = None
        self.wallpaper_update_interval = 2.0  # seconds
        self.wallpaper_dominant_color = "#000000"
        
        # Widget size
        self.widget_width = 150
        self.widget_height = 150
        
        # Create label
        self.label = tk.Label(self.root, bg='black', bd=0, highlightthickness=0)
        self.label.pack()
        
        # Event bindings
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)
        self.label.bind('<Double-Button-1>', self.reset_position)
        self.label.bind('<Button-3>', self.show_menu)  # Right click menu
        self.label.bind('<Control-Button-1>', self.start_resize)  # Ctrl + Left click for resizing
        self.label.bind('<Control-B1-Motion>', self.on_resize)  # Ctrl + Drag for resizing
        
        # Add click handler to main window (to close menu)
        self.root.bind('<Button-1>', self.close_menu_if_open)
        
        # Load configuration
        self.load_config()
        
        # Apply initial border
        self.apply_border()
        
        # Desktop check thread - RE-ENABLED
        self.desktop_check_thread = threading.Thread(target=self.check_desktop_status, daemon=True)
        self.desktop_check_thread.start()
        
        # If no gif exists, ask to select one
        if not self.gif_path or not os.path.exists(self.gif_path):
            self.select_gif()
        else:
            self.load_gif()
        
        # Set default position
        self.set_default_position()
        
        # Start wallpaper sync if enabled
        if self.wallpaper_sync_enabled:
            self.start_wallpaper_sync_thread()
        
    def load_config(self):
        """Load settings from configuration file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.gif_path = config.get('gif_path')
                    self.default_x = config.get('default_x')
                    self.default_y = config.get('default_y')
                    self.widget_width = config.get('width', 150)
                    self.widget_height = config.get('height', 150)
                    self.animation_speed = config.get('speed', 100)
                    self.hide_when_not_desktop = config.get('hide_when_not_desktop', True)
                    # Load border settings
                    self.border_enabled = config.get('border_enabled', False)
                    self.border_style = config.get('border_style', 'solid')
                    self.border_color = config.get('border_color', '#FF0000')
                    self.border_width = config.get('border_width', 3)
                    self.current_border_name = config.get('current_border_name', 'None')
                    # Load wallpaper sync settings
                    self.wallpaper_sync_enabled = config.get('wallpaper_sync_enabled', False)
                    self.wallpaper_dominant_color = config.get('wallpaper_dominant_color', '#000000')
        except Exception as e:
            print(f"Config loading error: {e}")
    
    def save_config(self):
        """Save configuration to file"""
        try:
            config = {
                'gif_path': self.gif_path,
                'default_x': self.default_x,
                'default_y': self.default_y,
                'width': self.widget_width,
                'height': self.widget_height,
                'speed': self.animation_speed,
                'hide_when_not_desktop': self.hide_when_not_desktop,
                # Save border settings
                'border_enabled': self.border_enabled,
                'border_style': self.border_style,
                'border_color': self.border_color,
                'border_width': self.border_width,
                'current_border_name': self.current_border_name,
                # Save wallpaper sync settings
                'wallpaper_sync_enabled': self.wallpaper_sync_enabled,
                'wallpaper_dominant_color': self.wallpaper_dominant_color
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Config saving error: {e}")
    
    def set_default_position(self):
        """Set default position to bottom right corner of screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Account for dash-to-panel height (usually 48px)
        panel_height = 48
        
        # Always recalculate bottom right corner
        self.default_x = screen_width - self.widget_width - 10  # 10 pixels from right edge
        self.default_y = screen_height - self.widget_height - panel_height - 10  # Panel height + 10 pixels from bottom edge
        
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{self.default_x}+{self.default_y}")
    
    def select_gif(self):
        """GIF file selection"""
        # Stop current animation
        was_playing = self.is_playing
        self.is_playing = False
        
        self.root.withdraw()  # Hide main window
        
        file_path = filedialog.askopenfilename(
            title="Select GIF file",
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        
        if file_path:
            self.gif_path = file_path
            self.load_gif()
            self.save_config()
        else:
            # If no gif is selected and there are no existing gifs, close the app
            if not self.gif_frames:
                self.root.quit()
                return
            else:
                # Continue old animation
                self.is_playing = was_playing
                if self.is_playing:
                    self.animate_gif()
            
        self.root.deiconify()  # Show main window again
    
    def load_gif(self):
        """Load GIF and split into frames"""
        try:
            if not self.gif_path or not os.path.exists(self.gif_path):
                return
            
            # Stop animation and clear frames
            self.is_playing = False
            old_frames = self.gif_frames
            self.gif_frames = []
            self.current_frame = 0
            
            gif = Image.open(self.gif_path)
            new_frames = []
            
            # Determine resampling method based on PIL version
            try:
                # For new PIL versions
                resample_method = Image.Resampling.LANCZOS
            except AttributeError:
                try:
                    # For old PIL versions
                    resample_method = Image.LANCZOS
                except AttributeError:
                    # For very old versions
                    resample_method = 1  # LANCZOS numeric value
            
            try:
                frame_count = 0
                while True:
                    # Resize frame
                    frame = gif.copy()
                    frame = frame.resize((self.widget_width, self.widget_height), resample_method)
                    photo = ImageTk.PhotoImage(frame)
                    new_frames.append(photo)
                    frame_count += 1
                    gif.seek(frame_count)
            except EOFError:
                pass
            
            # Safely assign new frames
            if new_frames:
                self.gif_frames = new_frames
                self.is_playing = True
                self.animate_gif()
            else:
                # Restore old frames
                self.gif_frames = old_frames
                print("Could not load GIF file, keeping old GIF!")
                
        except Exception as e:
            print(f"GIF loading error: {e}")
            # Keep old frames in case of error
            if not hasattr(self, 'gif_frames') or not self.gif_frames:
                self.gif_frames = []
    
    def animate_gif(self):
        """Run GIF animation"""
        if self.gif_frames and self.is_playing and len(self.gif_frames) > 0:
            # Make sure frame index is valid
            if self.current_frame >= len(self.gif_frames):
                self.current_frame = 0
            
            try:
                self.label.config(image=self.gif_frames[self.current_frame])
                self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            except (IndexError, tk.TclError) as e:
                # In case of index error or TCL error, go to beginning
                print(f"Animation error: {e}")
                self.current_frame = 0
                if len(self.gif_frames) > 0:
                    try:
                        self.label.config(image=self.gif_frames[0])
                    except:
                        # If still error, stop animation
                        self.is_playing = False
                        return
            
            self.root.after(self.animation_speed, self.animate_gif)
    
    def start_drag(self, event):
        """Start dragging"""
        self.start_x = event.x
        self.start_y = event.y
    
    def on_drag(self, event):
        """During dragging"""
        x = self.root.winfo_x() + event.x - self.start_x
        y = self.root.winfo_y() + event.y - self.start_y
        self.root.geometry(f"+{x}+{y}")
        
        # If wallpaper sync is enabled, trigger immediate analysis when dragging
        if self.wallpaper_sync_enabled:
            self.root.after(100, self.update_wallpaper_sync_border)
    
    def reset_position(self, event):
        """Double-click to return to default position"""
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{self.default_x}+{self.default_y}")
    
    def reset_position_menu(self):
        """Return to default position from menu"""
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{self.default_x}+{self.default_y}")
    
    def show_menu(self, event):
        """Show right-click menu"""
        self.menu_open = True  # Mark menu as open
        self.last_menu_position = (event.x_root, event.y_root)  # Store menu position
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Select New GIF", command=self.select_gif)
        menu.add_command(label="Play/Pause Animation", command=self.toggle_animation)
        menu.add_separator()
        
        # Resize mode menu
        resize_text = "Exit Resize Mode" if self.resize_mode else "Resize Mode"
        menu.add_command(label=resize_text, command=self.toggle_resize_mode)
        
        menu.add_separator()
        
        # Hide when not on desktop option
        hide_text = "✓ Hide when not on desktop" if self.hide_when_not_desktop else "Hide when not on desktop"
        menu.add_command(label=hide_text, command=self.toggle_hide_mode)
        
        menu.add_separator()
        
        # Border/Frame submenu
        border_menu = tk.Menu(menu, tearoff=0)
        for style_name in self.border_styles.keys():
            # Add checkmark if this is the current style
            display_name = f"✓ {style_name}" if style_name == self.current_border_name else style_name
            border_menu.add_command(
                label=display_name, 
                command=lambda name=style_name: self.set_border_style_and_refresh_menu(name)
            )
        
        menu.add_cascade(label="Border Style", menu=border_menu)
        menu.add_command(label="Next Border", command=self.cycle_border_style_and_refresh_menu)
        
        # Wallpaper sync option
        wallpaper_sync_text = "✓ Wallpaper Sync Border" if self.wallpaper_sync_enabled else "Wallpaper Sync Border"
        menu.add_command(label=wallpaper_sync_text, command=self.toggle_wallpaper_sync)
        
        menu.add_separator()
        menu.add_command(label="Reset Position", command=self.reset_position_menu)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.root.quit)
        
        # Menü kapandığında callback
        def on_menu_close():
            self.menu_open = False
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError as e:
            print(f"Menu popup error: {e}")
        finally:
            # Menü kapandıktan sonra flag'i sıfırla
            self.root.after(200, on_menu_close)
    
    def toggle_animation(self):
        """Stop/start animation"""
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.animate_gif()
    
    def toggle_resize_mode(self):
        """Toggle resize mode on/off"""
        self.resize_mode = not self.resize_mode
        if self.resize_mode:
            # Add border when in resize mode
            self.label.config(highlightbackground="red", highlightthickness=2)
            self.root.configure(bg='red')
            # Show info on widget instead of messagebox
            self.show_resize_info()
        else:
            # Return to normal mode - restore original border instead of black
            self.apply_border()  # This will restore the user's chosen border
            
            # If size changed, reload GIF and save settings
            if self.gif_path and os.path.exists(self.gif_path):
                self.load_gif()
            
            # Position widget in bottom right corner
            self.set_default_position()
            self.save_config()
    
    def toggle_hide_mode(self):
        """Toggle hide when not on desktop mode on/off"""
        self.hide_when_not_desktop = not self.hide_when_not_desktop
        self.save_config()
        
        # If hide mode is turned off and widget is hidden, show it
        if not self.hide_when_not_desktop:
            if not self.root.winfo_viewable():
                self.root.deiconify()
                self.root.attributes('-topmost', True)
    
    def close_menu_if_open(self, event):
        """Close menu if open"""
        if self.menu_open:
            self.menu_open = False
            # If this is not a drag operation (click on same point)
            return
        # Start normal drag operation
        self.start_drag(event)
    
    def show_resize_info(self):
        """Show resize info on widget"""
        # Create temporary info label
        info_label = tk.Label(self.root, text="Resize Mode On\nCtrl+Drag", 
                             bg='red', fg='white', font=('Arial', 8))
        info_label.place(x=5, y=5)
        
        # Remove info after 3 seconds
        self.root.after(3000, info_label.destroy)
    
    def start_resize(self, event):
        """Start resizing"""
        if self.resize_mode:
            self.start_x = event.x
            self.start_y = event.y
    
    def on_resize(self, event):
        """During resizing"""
        if self.resize_mode:
            # Calculate distance mouse moved
            delta_x = event.x - self.start_x
            delta_y = event.y - self.start_y
            
            # Take average change (for both x and y)
            delta = (delta_x + delta_y) // 2
            
            # Calculate new size
            new_width = max(self.min_size, min(self.max_size, self.widget_width + delta))
            new_height = max(self.min_size, min(self.max_size, self.widget_height + delta))
            
            # Only process if size actually changed
            if new_width != self.widget_width or new_height != self.widget_height:
                # Save old size
                old_width = self.widget_width
                old_height = self.widget_height
                
                # Update size
                self.widget_width = new_width
                self.widget_height = new_height
                
                # Adjust position to stay fixed in bottom right corner
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                panel_height = 48
                
                # Calculate new position (bottom right corner fixed)
                new_x = screen_width - self.widget_width - 10
                new_y = screen_height - self.widget_height - panel_height - 10
                
                # Update window size and position
                self.root.geometry(f"{self.widget_width}x{self.widget_height}+{new_x}+{new_y}")
                
                # Update default position
                self.default_x = new_x
                self.default_y = new_y
                
                # Update start point
                self.start_x = event.x
                self.start_y = event.y
    
    def check_desktop_status(self):
        """Check desktop status"""
        while True:
            try:
                # Skip check if menu is open
                if self.menu_open:
                    time.sleep(0.5)
                    continue
                
                # Skip check if hide mode is disabled
                if not self.hide_when_not_desktop:
                    time.sleep(0.5)
                    continue
                
                # Check active window
                result = subprocess.run(['xdotool', 'getactivewindow', 'getwindowname'], 
                                      capture_output=True, text=True)
                
                # Check if on desktop
                is_on_desktop = False
                
                if result.returncode != 0:
                    # If no active window, we're on desktop
                    is_on_desktop = True
                else:
                    window_name = result.stdout.strip().lower()
                    # Desktop window names
                    desktop_windows = ['desktop', 'masaüstü', 'nautilus-desktop', 'gnome-shell']
                    
                    # Empty name or desktop window names
                    is_on_desktop = (window_name == '' or 
                                   any(desktop_word in window_name for desktop_word in desktop_windows))
                
                # Show/hide widget
                self.root.after(0, self.toggle_visibility, is_on_desktop)
                
            except Exception as e:
                # Silent error handling to avoid spam
                pass
            
            time.sleep(0.5)  # Check every 0.5 seconds
    
    def toggle_visibility(self, show):
        """Toggle widget visibility"""
        try:
            # Don't hide widget if menu is open
            if self.menu_open:
                return
                
            # If hide when not on desktop is disabled, always show
            if not self.hide_when_not_desktop:
                if not self.root.winfo_viewable():
                    self.root.deiconify()
                    self.root.attributes('-topmost', True)
                return
                
            if show:
                if not self.root.winfo_viewable():
                    self.root.deiconify()
                    self.root.attributes('-topmost', True)
            else:
                if self.root.winfo_viewable():
                    self.root.withdraw()
        except Exception as e:
            print(f"Visibility toggle error: {e}")
            # Hata durumunda widget'ı göster
            try:
                self.root.deiconify()
                self.root.attributes('-topmost', True)
            except:
                pass
    
    def apply_border(self):
        """Apply the current border style to the widget"""
        if not self.border_enabled:
            # No border
            self.label.config(highlightthickness=0, bd=0)
            self.root.configure(bg='black')
            return
        
        # Apply border based on style
        if self.border_style == "solid":
            self.label.config(
                highlightbackground=self.border_color,
                highlightcolor=self.border_color,
                highlightthickness=self.border_width,
                bd=0
            )
            self.root.configure(bg=self.border_color)
        
        elif self.border_style == "double":
            # Create double border effect
            self.label.config(
                highlightbackground=self.border_color,
                highlightcolor=self.border_color,
                highlightthickness=self.border_width,
                bd=self.border_width//2,
                relief='raised'
            )
            self.root.configure(bg=self.border_color)
        
        elif self.border_style == "dashed":
            # For dashed effect, use a different approach
            self.label.config(
                highlightbackground=self.border_color,
                highlightcolor=self.border_color,
                highlightthickness=self.border_width,
                bd=1,
                relief='ridge'
            )
            self.root.configure(bg=self.border_color)
        
        elif self.border_style == "gradient":
            # Rainbow gradient effect
            self.rainbow_border()
        
        else:
            # Default solid
            self.label.config(
                highlightbackground=self.border_color,
                highlightcolor=self.border_color,
                highlightthickness=self.border_width,
                bd=0
            )
            self.root.configure(bg=self.border_color)
    
    def rainbow_border(self):
        """Create animated rainbow border effect"""
        colors = ['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', '#0000FF', '#4B0082', '#9400D3']
        
        def change_color():
            if self.border_style == "gradient" and self.border_enabled:
                import random
                color = random.choice(colors)
                self.label.config(
                    highlightbackground=color,
                    highlightcolor=color,
                    highlightthickness=self.border_width
                )
                self.root.configure(bg=color)
                # Change color every 500ms
                self.root.after(500, change_color)
        
        change_color()
    
    def set_border_style(self, style_name):
        """Set border style by name"""
        if style_name in self.border_styles:
            style_config = self.border_styles[style_name]
            self.border_enabled = style_config["enabled"]
            
            if self.border_enabled:
                self.border_style = style_config["style"]
                self.border_color = style_config["color"]
                self.border_width = style_config["width"]
            
            self.current_border_name = style_name
            self.apply_border()
            self.save_config()
    
    def cycle_border_style(self):
        """Cycle through available border styles"""
        styles = list(self.border_styles.keys())
        current_index = styles.index(self.current_border_name)
        next_index = (current_index + 1) % len(styles)
        next_style = styles[next_index]
        self.set_border_style(next_style)
    
    def set_border_style_and_refresh_menu(self, style_name):
        """Set border style and refresh menu to keep it open"""
        self.set_border_style(style_name)
        # Refresh menu after a short delay
        self.root.after(100, self.refresh_menu)
    
    def cycle_border_style_and_refresh_menu(self):
        """Cycle through border styles and refresh menu to keep it open"""
        self.cycle_border_style()
        # Refresh menu after a short delay
        self.root.after(100, self.refresh_menu)
    
    def refresh_menu(self):
        """Refresh the menu at the last position"""
        if hasattr(self, 'last_menu_position'):
            # Create a fake event with the stored position
            class FakeEvent:
                def __init__(self, x_root, y_root):
                    self.x_root = x_root
                    self.y_root = y_root
            
            fake_event = FakeEvent(self.last_menu_position[0], self.last_menu_position[1])
            self.show_menu(fake_event)

    def get_dominant_color_from_area(self, x, y, width, height):
        """Get dominant color from a specific screen area"""
        try:
            # Take screenshot of the specific area
            bbox = (x, y, x + width, y + height)
            screenshot = ImageGrab.grab(bbox)
            
            # Resize for faster processing
            screenshot = screenshot.resize((50, 50), Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS)
            
            # Get pixel colors
            pixels = list(screenshot.getdata())
            
            # Filter out very dark and very light colors (likely not wallpaper)
            filtered_pixels = []
            for pixel in pixels:
                r, g, b = pixel[:3]
                brightness = (r + g + b) / 3
                if 30 < brightness < 225:  # Avoid pure black/white
                    filtered_pixels.append(pixel)
            
            if not filtered_pixels:
                filtered_pixels = pixels  # Fallback to all pixels
            
            # Get most common color
            color_count = Counter(filtered_pixels)
            most_common = color_count.most_common(5)  # Get top 5 colors
            
            # Calculate weighted average of top colors for smoother result
            total_weight = sum(count for _, count in most_common)
            weighted_r = sum(color[0] * count for color, count in most_common) / total_weight
            weighted_g = sum(color[1] * count for color, count in most_common) / total_weight
            weighted_b = sum(color[2] * count for color, count in most_common) / total_weight
            
            # Convert to hex
            hex_color = "#{:02x}{:02x}{:02x}".format(int(weighted_r), int(weighted_g), int(weighted_b))
            return hex_color
            
        except Exception as e:
            print(f"Color analysis error: {e}")
            return "#000000"  # Fallback to black
    
    def enhance_color_for_border(self, hex_color):
        """Enhance color to make it more suitable for borders"""
        try:
            # Convert hex to RGB
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            # Convert to HSV for easier manipulation
            h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
            
            # Enhance saturation and ensure good visibility
            s = min(1.0, s * 1.3)  # Increase saturation
            v = max(0.4, min(0.9, v * 1.2))  # Ensure good brightness
            
            # Convert back to RGB
            enhanced_r, enhanced_g, enhanced_b = colorsys.hsv_to_rgb(h, s, v)
            
            # Convert to hex
            return "#{:02x}{:02x}{:02x}".format(
                int(enhanced_r * 255),
                int(enhanced_g * 255),
                int(enhanced_b * 255)
            )
        except:
            return hex_color  # Return original if enhancement fails
    
    def analyze_wallpaper_at_position(self):
        """Analyze wallpaper color at current widget position"""
        try:
            # Get current widget position
            widget_x = self.root.winfo_x()
            widget_y = self.root.winfo_y()
            
            # Analyze area around the widget (slightly larger area for better sampling)
            sample_width = self.widget_width + 40
            sample_height = self.widget_height + 40
            sample_x = max(0, widget_x - 20)
            sample_y = max(0, widget_y - 20)
            
            # Get dominant color
            dominant_color = self.get_dominant_color_from_area(sample_x, sample_y, sample_width, sample_height)
            
            # Enhance color for better border visibility
            enhanced_color = self.enhance_color_for_border(dominant_color)
            
            return enhanced_color
            
        except Exception as e:
            print(f"Wallpaper analysis error: {e}")
            return "#000000"
    
    def update_wallpaper_sync_border(self):
        """Update border color based on wallpaper analysis"""
        if not self.wallpaper_sync_enabled:
            return
            
        try:
            # Get current position
            current_pos = (self.root.winfo_x(), self.root.winfo_y())
            
            # Only analyze if position changed significantly or first time
            if (self.last_wallpaper_analysis_pos is None or 
                abs(current_pos[0] - self.last_wallpaper_analysis_pos[0]) > 20 or
                abs(current_pos[1] - self.last_wallpaper_analysis_pos[1]) > 20):
                
                # Analyze wallpaper color
                new_color = self.analyze_wallpaper_at_position()
                
                if new_color != self.wallpaper_dominant_color:
                    self.wallpaper_dominant_color = new_color
                    
                    # Apply the new color as border
                    self.border_enabled = True
                    self.border_style = "solid"
                    self.border_color = new_color
                    self.border_width = 3
                    self.current_border_name = "Wallpaper Sync"
                    
                    self.apply_border()
                    self.save_config()
                
                self.last_wallpaper_analysis_pos = current_pos
                
        except Exception as e:
            print(f"Wallpaper sync update error: {e}")
    
    def start_wallpaper_sync_thread(self):
        """Start wallpaper sync monitoring thread"""
        if self.wallpaper_analysis_thread and self.wallpaper_analysis_thread.is_alive():
            return
            
        def wallpaper_sync_loop():
            while self.wallpaper_sync_enabled:
                try:
                    self.root.after(0, self.update_wallpaper_sync_border)
                    time.sleep(self.wallpaper_update_interval)
                except Exception as e:
                    print(f"Wallpaper sync thread error: {e}")
                    time.sleep(1)
        
        self.wallpaper_analysis_thread = threading.Thread(target=wallpaper_sync_loop, daemon=True)
        self.wallpaper_analysis_thread.start()
    
    def toggle_wallpaper_sync(self):
        """Toggle wallpaper sync mode on/off"""
        self.wallpaper_sync_enabled = not self.wallpaper_sync_enabled
        
        if self.wallpaper_sync_enabled:
            # Start wallpaper sync
            self.start_wallpaper_sync_thread()
            # Immediate analysis
            self.update_wallpaper_sync_border()
        else:
            # Return to previous border style
            if self.current_border_name == "Wallpaper Sync":
                self.current_border_name = "None"
                self.border_enabled = False
                self.apply_border()
        
        self.save_config()

    def run(self):
        """Run the widget"""
        self.root.mainloop()

if __name__ == "__main__":
    # Check if xdotool is installed
    try:
        subprocess.run(['which', 'xdotool'], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("xdotool is not installed. Please install it with 'sudo apt install xdotool'.")
        exit(1)
    
    widget = GifWidget()
    widget.run()
