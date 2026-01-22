import pyautogui
import tkinter as tk
from tkinter import ttk
import threading
import time
from pathlib import Path
import math

class ImageClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Auto-Clicker")
        self.root.geometry("600x750")
        self.root.resizable(False, False)
        
        # Set custom cursor
        self.root.config(cursor="cross")
        
        # Variables
        self.is_running = False
        self.current_step = 0
        self.total_steps = 8
        self.death_count = 0
        self.max_deaths = 5
        self.animation_frame = 0
        self.particle_effects = []
        
        # Color scheme - Neon vibes
        self.color_primary = "#0a0e27"      # Dark blue
        self.color_secondary = "#1a1f3a"    # Slightly lighter
        self.color_accent1 = "#00d9ff"      # Cyan
        self.color_accent2 = "#ff006e"      # Hot pink
        self.color_accent3 = "#8338ec"      # Purple
        self.color_text = "#ffffff"
        self.color_success = "#06ffa5"      # Green
        self.color_warning = "#ffbe0b"      # Yellow
        
        # Configure root background
        self.root.config(bg=self.color_primary)
        
        # Create main canvas for animations
        self.canvas = tk.Canvas(
            self.root, 
            width=600, 
            height=750, 
            bg=self.color_primary,
            highlightthickness=0,
            cursor="cross"
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Bind window events
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.root.bind("<Configure>", self.on_configure)
        
        # Create UI Elements
        self.create_widgets()
        
        # Start animation loop
        self.animate()
    
    def create_widgets(self):
        """Create all UI elements"""
        # Title with animation
        self.title_id = self.canvas.create_text(
            300, 40,
            text="⚡ IMAGE AUTO-CLICKER ⚡",
            font=("Courier New", 20, "bold"),
            fill=self.color_accent1,
            anchor="center"
        )
        
        # Decorative lines
        self.canvas.create_line(50, 65, 550, 65, fill=self.color_accent1, width=2)
        self.canvas.create_line(50, 75, 550, 75, fill=self.color_accent2, width=1)
        
        # Settings Section
        settings_y = 110
        self.canvas.create_text(
            60, settings_y,
            text="⚙ SETTINGS",
            font=("Courier New", 12, "bold"),
            fill=self.color_accent3,
            anchor="w"
        )
        
        # Max Deaths Label
        self.canvas.create_text(
            80, settings_y + 35,
            text="Max Deaths:",
            font=("Courier New", 10),
            fill=self.color_text,
            anchor="w"
        )
        
        # Deaths Entry Box
        self.deaths_entry = tk.Entry(
            self.root,
            width=8,
            font=("Courier New", 11, "bold"),
            bg=self.color_secondary,
            fg=self.color_accent1,
            insertbackground=self.color_accent1,
            relief="flat",
            borderwidth=2
        )
        self.deaths_entry.insert(0, "5")
        
        # Create window for entry
        self.entry_window = self.canvas.create_window(
            300, settings_y + 35,
            window=self.deaths_entry,
            width=80
        )
        
        # Set Button
        self.set_button = tk.Button(
            self.root,
            text="SET",
            command=self.update_max_deaths,
            font=("Courier New", 9, "bold"),
            bg=self.color_accent3,
            fg=self.color_primary,
            relief="flat",
            borderwidth=0,
            activebackground=self.color_accent1,
            activeforeground=self.color_primary,
            cursor="hand2",
            padx=15,
            pady=5
        )
        self.set_button_window = self.canvas.create_window(
            400, settings_y + 35,
            window=self.set_button
        )
        
        # Progress Section
        progress_y = 220
        self.canvas.create_text(
            60, progress_y,
            text="📊 PROGRESS",
            font=("Courier New", 12, "bold"),
            fill=self.color_accent1,
            anchor="w"
        )
        
        # Step Counter
        self.step_label_id = self.canvas.create_text(
            300, progress_y + 40,
            text="STEP: 0 / 8",
            font=("Courier New", 14, "bold"),
            fill=self.color_accent1,
            anchor="center"
        )
        
        # Death Counter
        self.death_label_id = self.canvas.create_text(
            300, progress_y + 75,
            text="DEATHS: 0 / 5",
            font=("Courier New", 14, "bold"),
            fill=self.color_accent2,
            anchor="center"
        )
        
        # Decorative progress bar background
        self.canvas.create_rectangle(
            50, progress_y + 110, 550, progress_y + 125,
            fill=self.color_secondary,
            outline=self.color_accent1,
            width=2
        )
        
        # Animated progress bar
        self.progress_bar_id = self.canvas.create_rectangle(
            50, progress_y + 110, 50, progress_y + 125,
            fill=self.color_accent1,
            outline="",
            width=0
        )
        
        self.progress_y = progress_y
        
        # Status Section
        status_y = 380
        self.canvas.create_text(
            60, status_y,
            text="📡 STATUS",
            font=("Courier New", 12, "bold"),
            fill=self.color_accent2,
            anchor="w"
        )
        
        # Status message box
        self.status_box = self.canvas.create_rectangle(
            50, status_y + 25, 550, status_y + 80,
            fill=self.color_secondary,
            outline=self.color_accent2,
            width=2
        )
        
        self.status_label_id = self.canvas.create_text(
            300, status_y + 52,
            text="Ready to start",
            font=("Courier New", 10),
            fill=self.color_text,
            anchor="center",
            width=480
        )
        
        # Image tracking label
        self.image_label_id = self.canvas.create_text(
            300, status_y + 65,
            text="",
            font=("Courier New", 8),
            fill=self.color_accent1,
            anchor="center"
        )
        
        # Control Buttons
        button_y = 530
        
        # Start Button
        self.start_button = tk.Button(
            self.root,
            text="▶ START",
            command=self.start_process,
            font=("Courier New", 12, "bold"),
            bg=self.color_success,
            fg=self.color_primary,
            relief="flat",
            borderwidth=0,
            activebackground=self.color_accent1,
            activeforeground=self.color_primary,
            cursor="hand2",
            padx=40,
            pady=12
        )
        self.start_btn_window = self.canvas.create_window(
            200, button_y,
            window=self.start_button
        )
        
        # Stop Button
        self.stop_button = tk.Button(
            self.root,
            text="⏹ STOP",
            command=self.stop_process,
            font=("Courier New", 12, "bold"),
            bg=self.color_accent2,
            fg=self.color_primary,
            relief="flat",
            borderwidth=0,
            activebackground=self.color_accent1,
            activeforeground=self.color_primary,
            cursor="hand2",
            padx=40,
            pady=12,
            state="disabled"
        )
        self.stop_btn_window = self.canvas.create_window(
            400, button_y,
            window=self.stop_button
        )
        
        # Info text
        self.canvas.create_text(
            300, 620,
            text="Press corner of screen to abort | 1920x1080 recommended",
            font=("Courier New", 8),
            fill=self.color_accent3,
            anchor="center"
        )
        
        # Decorative bottom line
        self.canvas.create_line(50, 650, 550, 650, fill=self.color_accent1, width=2)
        self.canvas.create_line(50, 655, 550, 655, fill=self.color_accent2, width=1)
        
        # Version
        self.canvas.create_text(
            300, 680,
            text="v2.0 | NEON EDITION",
            font=("Courier New", 9, "bold"),
            fill=self.color_accent1,
            anchor="center"
        )
    
    def on_mouse_move(self, event):
        """Track mouse position for reactive effects"""
        self.mouse_x = event.x
        self.mouse_y = event.y
    
    def on_configure(self, event=None):
        """Handle window resize"""
        pass
    
    def animate_particles(self):
        """Create particle effects around cursor"""
        if hasattr(self, 'mouse_x') and hasattr(self, 'mouse_y'):
            if self.is_running and self.animation_frame % 5 == 0:
                angle = (self.animation_frame * 15) % 360
                x = self.mouse_x + math.cos(math.radians(angle)) * 30
                y = self.mouse_y + math.sin(math.radians(angle)) * 30
                
                particle = self.canvas.create_oval(
                    x-2, y-2, x+2, y+2,
                    fill=self.color_accent1,
                    outline="",
                    width=0
                )
                self.particle_effects.append((particle, 10))
    
    def update_particles(self):
        """Update and fade particle effects"""
        remaining = []
        for particle, life in self.particle_effects:
            if life > 0:
                color = self.color_accent1
                self.canvas.itemconfig(particle, fill=color)
                remaining.append((particle, life - 1))
            else:
                self.canvas.delete(particle)
        self.particle_effects = remaining
    
    def draw_reactive_background(self):
        """Draw animated reactive background"""
        # Calculate animation based on running state
        if self.is_running:
            intensity = (math.sin(self.animation_frame / 10) + 1) / 2
            
            # Draw pulsing aura circles
            for i in range(3):
                offset = (self.animation_frame + i * 20) % 100
                radius = 200 + (offset / 100) * 100
                
                # Calculate opacity effect through color
                alpha = int(20 * (1 - offset / 100))
                if alpha > 0:
                    self.canvas.create_oval(
                        300 - radius, 375 - radius,
                        300 + radius, 375 + radius,
                        fill="",
                        outline=self.color_accent1,
                        width=1
                    )
    
    def animate_title(self):
        """Animate title color"""
        colors = [self.color_accent1, self.color_accent2, self.color_accent3]
        color_index = (self.animation_frame // 15) % len(colors)
        self.canvas.itemconfig(self.title_id, fill=colors[color_index])
    
    def update_progress_bar_visual(self):
        """Update progress bar animation"""
        max_width = 500
        progress = self.current_step / self.total_steps
        bar_width = max_width * progress
        
        self.canvas.coords(
            self.progress_bar_id,
            50, self.progress_y + 110,
            50 + bar_width, self.progress_y + 125
        )
    
    def update_progress(self, step, status, image_name=""):
        """Update UI progress"""
        self.current_step = step
        self.canvas.itemconfig(
            self.step_label_id,
            text=f"STEP: {self.current_step} / {self.total_steps}"
        )
        self.canvas.itemconfig(
            self.death_label_id,
            text=f"DEATHS: {self.death_count} / {self.max_deaths}"
        )
        
        # Update status color based on status
        if "ERROR" in status or "Timeout" in status:
            status_color = self.color_accent2
            self.canvas.itemconfig(self.status_box, outline=self.color_accent2)
        elif "completed" in status:
            status_color = self.color_success
            self.canvas.itemconfig(self.status_box, outline=self.color_success)
        else:
            status_color = self.color_text
            self.canvas.itemconfig(self.status_box, outline=self.color_accent1)
        
        self.canvas.itemconfig(self.status_label_id, text=status, fill=status_color)
        
        if image_name:
            self.canvas.itemconfig(
                self.image_label_id,
                text=f"🎯 Looking for: {image_name}",
                fill=self.color_accent1
            )
        else:
            self.canvas.itemconfig(self.image_label_id, text="")
        
        self.update_progress_bar_visual()
    
    def update_max_deaths(self):
        """Update max deaths value"""
        if self.is_running:
            self.update_progress(self.current_step, "⚠ Cannot change during run!", "")
            return
        try:
            value = int(self.deaths_entry.get())
            if value > 0:
                self.max_deaths = value
                self.update_progress(0, f"✓ Max deaths set to {self.max_deaths}", "")
                self.root.after(2000, lambda: self.update_progress(
                    0, "Ready to start", ""
                ))
            else:
                self.update_progress(0, "⚠ Please enter a positive number", "")
        except ValueError:
            self.update_progress(0, "⚠ Invalid input! Enter a number", "")
    
    def start_process(self):
        """Start the clicking process"""
        if not self.is_running:
            self.is_running = True
            self.death_count = 0
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.deaths_entry.config(state="disabled")
            self.set_button.config(state="disabled")
            
            thread = threading.Thread(target=self.run_clicker, daemon=True)
            thread.start()
    
    def stop_process(self):
        """Stop the clicking process"""
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.deaths_entry.config(state="normal")
        self.set_button.config(state="normal")
        self.update_progress(0, "⏹ Stopped by user", "")
    
    def run_clicker(self):
        """Main clicking loop"""
        self.update_progress(0, "🚀 Starting...", "")
        time.sleep(1)
        
        steps = [
            (["1.png", "1_fix.png"], 1),
            ("2.png", 1),
            ("5.png", 1),
            ("3.png", 1),
            ("4.png", 1),
            ("5.png", 4),
            ("4.png", 1),
            ("7.png", 1)
        ]
        
        while self.is_running and self.death_count < self.max_deaths:
            self.update_progress(0, f"🔄 Running cycle (Death {self.death_count + 1}/{self.max_deaths})...", "")
            time.sleep(0.5)
            
            for step_num, (image_files, click_count) in enumerate(steps, start=1):
                if not self.is_running:
                    break
                
                if isinstance(image_files, str):
                    image_files_list = [image_files]
                else:
                    image_files_list = image_files
                
                for click_num in range(click_count):
                    if not self.is_running:
                        break
                    
                    if len(image_files_list) > 1:
                        file_display = " or ".join(image_files_list)
                    else:
                        file_display = image_files_list[0]
                    
                    if click_count > 1:
                        status_msg = f"Death {self.death_count + 1}/{self.max_deaths} | Step {step_num}: Searching for {file_display} ({click_num+1}/{click_count})"
                    else:
                        status_msg = f"Death {self.death_count + 1}/{self.max_deaths} | Step {step_num}: Searching for {file_display}"
                    
                    self.update_progress(step_num - 1, status_msg, file_display)
                    
                    existing_files = [f for f in image_files_list if Path(f).exists()]
                    if not existing_files:
                        self.update_progress(step_num - 1, f"ERROR: None of {image_files_list} found!", file_display)
                        self.stop_process()
                        return
                    
                    max_attempts = 60
                    found = False
                    clicked_file = None
                    
                    for attempt in range(max_attempts):
                        if not self.is_running:
                            return
                        
                        for image_file in existing_files:
                            try:
                                for confidence in [0.95, 0.9, 0.85, 0.8, 0.75, 0.7]:
                                    try:
                                        location = pyautogui.locateOnScreen(image_file, confidence=confidence)
                                        
                                        if location:
                                            center = pyautogui.center(location)
                                            pyautogui.click(center.x, center.y)
                                            clicked_file = image_file
                                            
                                            if click_count > 1:
                                                click_status = f"Death {self.death_count + 1}/{self.max_deaths} | Step {step_num}: ✓ {clicked_file} ({click_num+1}/{click_count})"
                                            else:
                                                click_status = f"Death {self.death_count + 1}/{self.max_deaths} | Step {step_num}: ✓ {clicked_file}"
                                            
                                            self.update_progress(step_num - 1, click_status, "")
                                            found = True
                                            time.sleep(0.5)
                                            break
                                    except:
                                        continue
                                
                                if found:
                                    break
                                    
                            except pyautogui.ImageNotFoundException:
                                pass
                            except Exception:
                                pass
                        
                        if found:
                            break
                        
                        time.sleep(0.5)
                    
                    if not found:
                        self.update_progress(step_num - 1, f"Timeout: Could not find {file_display}", file_display)
                        self.stop_process()
                        return
                
                self.update_progress(step_num, f"Death {self.death_count + 1}/{self.max_deaths} | Step {step_num}: ✓ Complete!", "")
                time.sleep(0.3)
            
            self.death_count += 1
            
            if self.death_count < self.max_deaths:
                self.update_progress(self.total_steps, f"💀 Death {self.death_count}/{self.max_deaths} completed! Restarting...", "")
                time.sleep(1)
        
        if self.is_running:
            self.update_progress(self.total_steps, f"🎉 All {self.max_deaths} deaths completed!", "")
            self.stop_process()
    
    def animate(self):
        """Main animation loop"""
        self.animation_frame += 1
        
        # Update animations
        self.animate_title()
        self.animate_particles()
        self.update_particles()
        self.draw_reactive_background()
        
        # Schedule next frame
        self.root.after(50, self.animate)

def main():
    screen_width, screen_height = pyautogui.size()
    print(f"Detected screen resolution: {screen_width}x{screen_height}")
    
    if screen_width != 1920 or screen_height != 1080:
        print("WARNING: Screen resolution is not 1920x1080!")
    
    pyautogui.FAILSAFE = True
    
    root = tk.Tk()
    app = ImageClickerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()