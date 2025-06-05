#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess
import json
import os
import threading
import time

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
        
        # Hide when not on desktop control
        self.hide_when_not_desktop = True  # Default enabled
        
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
        
        # Desktop check thread
        self.desktop_check_thread = threading.Thread(target=self.check_desktop_status, daemon=True)
        self.desktop_check_thread.start()
        
        # If no gif exists, ask to select one
        if not self.gif_path or not os.path.exists(self.gif_path):
            self.select_gif()
        else:
            self.load_gif()
        
        # Set default position
        self.set_default_position()
        
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
                'hide_when_not_desktop': self.hide_when_not_desktop
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
    
    def reset_position(self, event):
        """Double-click to return to default position"""
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{self.default_x}+{self.default_y}")
    
    def reset_position_menu(self):
        """Return to default position from menu"""
        self.root.geometry(f"{self.widget_width}x{self.widget_height}+{self.default_x}+{self.default_y}")
    
    def show_menu(self, event):
        """Show right-click menu"""
        self.menu_open = True  # Mark menu as open
        
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
        menu.add_command(label="Reset Position", command=self.reset_position_menu)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.root.quit)
        
        # Menü kapandığında callback
        def on_menu_close():
            self.menu_open = False
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        except tk.TclError:
            pass
        finally:
            # Menü kapandıktan sonra flag'i sıfırla
            self.root.after(500, on_menu_close)
    
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
            # Return to normal mode
            self.label.config(highlightthickness=0)
            self.root.configure(bg='black')
            
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
                print(f"Desktop check error: {e}")
            
            time.sleep(0.5)  # Check every 0.5 seconds (more responsive)
    
    def toggle_visibility(self, show):
        """Toggle widget visibility"""
        try:
            # Don't hide widget if menu is open
            if self.menu_open:
                return
                
            # If hide when not on desktop is disabled, do nothing
            if not self.hide_when_not_desktop:
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
