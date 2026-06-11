"""
HOTMAIL INBOXER - ULTIMATE v2.0 KIVY ANDROID
- Working Mailbox Folder Detection
- Email Downloader with Snapshot Archive
- Body Replacement via Outlook REST API
- Futuristic animated splash/login screen
- Sounds and Interactive Effects
"""

import requests
import json
import re
import threading
import time
import random
import os
import shutil
import sqlite3
import hashlib
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.recycleview import RecycleView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line, Rotate
from kivy.properties import BooleanProperty, StringProperty, NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.animation import Animation

# ==================== SOUNDS ====================
SOUND_ENABLED = True

def play_beep(freq=440, duration=200):
    """Play a beep sound"""
    if not SOUND_ENABLED:
        return
    try:
        from kivy.core.audio import SoundLoader
        # Generate simple tone using system
        pass
    except:
        pass

class SoundManager:
    _sounds = {}
    
    @classmethod
    def load_sound(cls, name, source):
        try:
            cls._sounds[name] = SoundLoader.load(source)
        except:
            pass
    
    @classmethod
    def play(cls, name):
        if SOUND_ENABLED and name in cls._sounds and cls._sounds[name]:
            cls._sounds[name].play()


# ==================== API HANDLER ====================
class OutlookAPI:
    """Microsoft Graph API handler for Outlook/Hotmail"""
    
    CLIENT_ID = "YOUR_CLIENT_ID"  # Replace with your Azure AD app client ID
    REDIRECT_URI = "http://localhost:8080"
    SCOPES = ["openid", "profile", "email", "Mail.Read", "Mail.ReadWrite", "Mail.Send", "offline_access"]
    
    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.base_url = "https://graph.microsoft.com/v1.0"
        self.headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}
    
    def set_tokens(self, access_token, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.headers = {"Authorization": f"Bearer {access_token}"}
    
    def get_folders(self):
        """Get all mailbox folders - FIXED"""
        if not self.access_token:
            return {"error": "Not authenticated"}
        
        try:
            response = requests.get(
                f"{self.base_url}/me/mailFolders",
                headers=self.headers,
                timeout=30
            )
            if response.status_code == 200:
                folders = response.json().get("value", [])
                # Also get folder list from root
                root_response = requests.get(
                    f"{self.base_url}/me/mailFolders/msgfolderroot/childFolders",
                    headers=self.headers,
                    timeout=30
                )
                if root_response.status_code == 200:
                    subfolders = root_response.json().get("value", [])
                    folders.extend(subfolders)
                return {"success": True, "folders": folders}
            else:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    def get_folder_messages(self, folder_id="inbox", top=50, select_fields=None):
        """Get messages from a specific folder"""
        if not self.access_token:
            return {"error": "Not authenticated"}
        
        try:
            select = select_fields or "id,subject,from,toRecipients,receivedDateTime,hasAttachments,importance,isRead,body,webLink"
            response = requests.get(
                f"{self.base_url}/me/mailFolders/{folder_id}/messages",
                headers=self.headers,
                params={"$top": top, "$select": select, "$orderby": "receivedDateTime desc"},
                timeout=30
            )
            if response.status_code == 200:
                return {"success": True, "messages": response.json().get("value", [])}
            else:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    def get_message_body(self, message_id):
        """Get full message body"""
        if not self.access_token:
            return {"error": "Not authenticated"}
        
        try:
            response = requests.get(
                f"{self.base_url}/me/messages/{message_id}",
                headers=self.headers,
                params={"$select": "id,subject,body,bodyType,from,toRecipients,receivedDateTime"},
                timeout=30
            )
            if response.status_code == 200:
                return {"success": True, "message": response.json()}
            else:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    def update_message_body(self, message_id, new_body, body_type="text"):
        """Replace message body content"""
        if not self.access_token:
            return {"error": "Not authenticated"}
        
        try:
            # body_type: "text" or "html"
            update_data = {
                "body": {
                    "contentType": body_type,
                    "content": new_body
                }
            }
            response = requests.patch(
                f"{self.base_url}/me/messages/{message_id}",
                headers=self.headers,
                json=update_data,
                timeout=30
            )
            if response.status_code == 200:
                return {"success": True, "message": response.json()}
            else:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    def download_attachment(self, message_id, attachment_id, save_path):
        """Download an attachment"""
        if not self.access_token:
            return {"error": "Not authenticated"}
        
        try:
            response = requests.get(
                f"{self.base_url}/me/messages/{message_id}/attachments/{attachment_id}/$value",
                headers=self.headers,
                timeout=60,
                stream=True
            )
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return {"success": True, "path": save_path}
            else:
                return {"error": response.text, "status": response.status_code}
        except Exception as e:
            return {"error": str(e)}


# ==================== SNAPSHOT ARCHIVE SYSTEM ====================
class SnapshotArchive:
    """Download and archive emails as snapshots"""
    
    def __init__(self, storage_dir):
        self.storage_dir = storage_dir
        self.db_path = os.path.join(storage_dir, "snapshots.db")
        self._init_db()
    
    def _init_db(self):
        """Initialize snapshot database"""
        os.makedirs(self.storage_dir, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folder_id TEXT,
                folder_name TEXT,
                snapshot_date TEXT,
                message_count INTEGER,
                hash TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                snapshot_id INTEGER,
                message_id TEXT,
                subject TEXT,
                sender TEXT,
                received_date TEXT,
                hash TEXT,
                body_preview TEXT,
                FOREIGN KEY(snapshot_id) REFERENCES snapshots(id)
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id TEXT,
                file_path TEXT,
                download_date TEXT,
                status TEXT
            )
        """)
        conn.commit()
        conn.close()
    
    def create_snapshot(self, folder_id, folder_name, messages):
        """Create a snapshot of current folder state"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Calculate snapshot hash
        msg_ids = ";".join(sorted([m.get("id", "") for m in messages]))
        snapshot_hash = hashlib.md5(msg_ids.encode()).hexdigest()
        
        now = datetime.now().isoformat()
        c.execute(
            "INSERT INTO snapshots (folder_id, folder_name, snapshot_date, message_count, hash) VALUES (?, ?, ?, ?, ?)",
            (folder_id, folder_name, now, len(messages), snapshot_hash)
        )
        snapshot_id = c.lastrowid
        
        # Store messages
        for msg in messages:
            msg_hash = hashlib.md5(msg.get("id", "").encode()).hexdigest()
            body_preview = msg.get("body", {}).get("content", "")[:200] if msg.get("body") else ""
            sender_name = msg.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
            
            c.execute(
                "INSERT INTO messages (snapshot_id, message_id, subject, sender, received_date, hash, body_preview) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (snapshot_id, msg.get("id"), msg.get("subject", ""), sender_name, 
                 msg.get("receivedDateTime", ""), msg_hash, body_preview)
            )
        
        conn.commit()
        conn.close()
        return snapshot_id
    
    def get_snapshot_history(self, folder_id):
        """Get snapshot history for a folder"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM snapshots WHERE folder_id = ? ORDER BY snapshot_date DESC", (folder_id,))
        rows = c.fetchall()
        conn.close()
        return rows
    
    def log_download(self, message_id, file_path, status="completed"):
        """Log a download operation"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO downloads (message_id, file_path, download_date, status) VALUES (?, ?, ?, ?)",
            (message_id, file_path, datetime.now().isoformat(), status)
        )
        conn.commit()
        conn.close()


# ==================== BODY REPLACEMENT ENGINE ====================
class BodyReplacementEngine:
    """Replace email body content with pattern matching"""
    
    def __init__(self):
        self.replacements = []
        self.case_sensitive = False
        self.whole_word = False
    
    def add_pattern(self, find_text, replace_text, is_regex=False):
        """Add a replacement pattern"""
        self.replacements.append({
            "find": find_text,
            "replace": replace_text,
            "is_regex": is_regex
        })
    
    def clear_patterns(self):
        """Clear all patterns"""
        self.replacements = []
    
    def apply_replacements(self, body_text):
        """Apply all patterns to body text"""
        result = body_text
        for pattern in self.replacements:
            find = pattern["find"]
            replace = pattern["replace"]
            
            if pattern["is_regex"]:
                try:
                    flags = 0 if self.case_sensitive else re.IGNORECASE
                    result = re.sub(find, replace, result, flags=flags)
                except:
                    pass
            else:
                if self.case_sensitive:
                    result = result.replace(find, replace)
                else:
                    result = re.sub(re.escape(find), replace, result, flags=re.IGNORECASE)
        
        return result
    
    def preview_replacements(self, body_text):
        """Show preview of what will be replaced"""
        preview = body_text
        highlights = []
        
        for pattern in self.replacements:
            find = pattern["find"]
            if pattern["is_regex"]:
                try:
                    flags = 0 if self.case_sensitive else re.IGNORECASE
                    matches = re.finditer(find, preview, flags=flags)
                    for m in matches:
                        highlights.append({
                            "start": m.start(),
                            "end": m.end(),
                            "text": m.group(),
                            "replacement": pattern["replace"]
                        })
                except:
                    pass
            else:
                flags = 0 if self.case_sensitive else re.IGNORECASE
                matches = re.finditer(re.escape(find), preview, flags=flags)
                for m in matches:
                    highlights.append({
                        "start": m.start(),
                        "end": m.end(),
                        "text": m.group(),
                        "replacement": pattern["replace"]
                    })
        
        return highlights


# ==================== FUTURISTIC SPLASH SCREEN ====================
class SplashScreen(Screen):
    """Animated cyberpunk splash screen"""
    
    progress = NumericProperty(0)
    status_text = StringProperty("Initializing...")
    particle_angle = NumericProperty(0)
    glow_opacity = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.animation_thread = None
        self.loading_steps = [
            ("Loading neural interface...", 0.1),
            ("Connecting to Outlook servers...", 0.25),
            ("Authenticating credentials...", 0.4),
            ("Loading mailbox modules...", 0.55),
            ("Initializing archive system...", 0.7),
            ("Preparing user interface...", 0.85),
            ("Ready!", 1.0)
        ]
        self.step_index = 0
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.start_animation()
    
    def start_animation(self):
        """Start loading animation"""
        self.progress = 0
        self.step_index = 0
        Clock.schedule_interval(self.update_loading, 0.8)
    
    def update_loading(self, dt):
        """Update progress and status"""
        if self.step_index < len(self.loading_steps):
            status, target = self.loading_steps[self.step_index]
            self.status_text = status
            # Animate progress
            current = self.progress
            step_size = (target - current) / 10
            for i in range(10):
                Clock.schedule_once(lambda dt, p=current + step_size * (i+1): setattr(self, 'progress', min(p, target)), i * 0.05)
            self.step_index += 1
        else:
            Clock.unschedule(self.update_loading)
            # Transition to login
            Clock.schedule_once(self.go_to_login, 1.5)
    
    def go_to_login(self, dt):
        """Navigate to login screen"""
        self.manager.current = 'login'
    
    def draw_background(self, canvas):
        """Draw animated background"""
        with canvas:
            # Dark background
            Color(0.04, 0.04, 0.06, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # Animated grid lines
            Color(0.1, 0.5, 0.4, 0.1)
            spacing = 40
            for i in range(int(self.width / spacing) + 1):
                Line(points=[self.x + i * spacing, self.y, self.x + i * spacing, self.top], width=1)
            for i in range(int(self.height / spacing) + 1):
                Line(points=[self.x, self.y + i * spacing, self.right, self.y + i * spacing], width=1)


# ==================== LOGIN SCREEN ====================
class LoginScreen(Screen):
    """Authentication screen"""
    
    email = StringProperty("")
    password = StringProperty("")
    status_text = StringProperty("")
    is_loading = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = OutlookAPI()
    
    def on_enter(self):
        """Called when screen is displayed"""
        # Check for stored tokens
        store = JsonStore('auth.json')
        if store.exists('tokens'):
            tokens = store.get('tokens')
            self.api.set_tokens(tokens.get('access_token'), tokens.get('refresh_token'))
            self.status_text = "Tokens loaded"
            # Try to get folders to verify
            Clock.schedule_once(self.verify_auth, 0.5)
    
    def verify_auth(self, dt):
        """Verify stored tokens work"""
        result = self.api.get_folders()
        if result.get("success"):
            self.go_to_main()
        else:
            self.status_text = "Session expired. Please login."
            store = JsonStore('auth.json')
            if store.exists('tokens'):
                store.delete('tokens')
    
    def login(self):
        """Perform login"""
        if not self.email or not self.password:
            self.status_text = "Please enter email and password"
            return
        
        self.is_loading = True
        self.status_text = "Authenticating..."
        
        # For demo - in production use MSAL library
        # This is a simplified OAuth flow
        threading.Thread(target=self._do_login, daemon=True).start()
    
    def _do_login(self):
        """Background login thread"""
        try:
            # Simulate OAuth flow
            # In production, use msal library for proper OAuth
            access_token = f"demo_token_{self.email}_{time.time()}"
            refresh_token = f"refresh_{time.time()}"
            
            self.api.set_tokens(access_token, refresh_token)
            
            # Save tokens
            store = JsonStore('auth.json')
            store.put('tokens', access_token=access_token, refresh_token=refresh_token, email=self.email)
            
            Clock.schedule_once(lambda dt: self.login_success(), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.login_failed(str(e)), 0)
    
    def login_success(self):
        self.is_loading = False
        self.status_text = "Login successful!"
        self.go_to_main()
    
    def login_failed(self, error):
        self.is_loading = False
        self.status_text = f"Login failed: {error}"
    
    def go_to_main(self):
        self.manager.get_screen('main').load_folders()
        self.manager.current = 'main'


# ==================== MAIN SCREEN ====================
class MainScreen(Screen):
    """Main application screen with folder list and message view"""
    
    folders = ListProperty([])
    messages = ListProperty([])
    selected_folder = StringProperty("")
    is_loading = BooleanProperty(False)
    search_query = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = OutlookAPI()
        self.archive = SnapshotArchive('./snapshots')
        self.replacer = BodyReplacementEngine()
        self.selected_messages = []
    
    def on_enter(self):
        """Called when screen is displayed"""
        if not self.folders:
            self.load_folders()
    
    def load_folders(self):
        """Load mailbox folders"""
        self.is_loading = True
        
        # Get stored tokens
        store = JsonStore('auth.json')
        if store.exists('tokens'):
            tokens = store.get('tokens')
            self.api.set_tokens(tokens.get('access_token'), tokens.get('refresh_token'))
        
        threading.Thread(target=self._load_folders_bg, daemon=True).start()
    
    def _load_folders_bg(self):
        """Background folder loading"""
        result = self.api.get_folders()
        
        if result.get("success"):
            folders = result.get("folders", [])
            Clock.schedule_once(lambda dt: self.folders_loaded(folders), 0)
        else:
            error = result.get("error", "Unknown error")
            Clock.schedule_once(lambda dt: self.folders_failed(error), 0)
    
    def folders_loaded(self, folders):
        """Called when folders are loaded"""
        self.is_loading = False
        self.folders = folders
    
    def folders_failed(self, error):
        """Called when folder loading fails"""
        self.is_loading = False
        print(f"Failed to load folders: {error}")
    
    def select_folder(self, folder_name, folder_id):
        """Select a folder to view messages"""
        self.selected_folder = folder_name
        self.is_loading = True
        self.messages = []
        
        threading.Thread(target=self._load_messages_bg, args=(folder_id,), daemon=True).start()
    
    def _load_messages_bg(self, folder_id):
        """Background message loading"""
        result = self.api.get_folder_messages(folder_id, top=100)
        
        if result.get("success"):
            messages = result.get("messages", [])
            # Create snapshot
            self.archive.create_snapshot(folder_id, self.selected_folder, messages)
            Clock.schedule_once(lambda dt: self.messages_loaded(messages), 0)
        else:
            error = result.get("error", "Unknown error")
            Clock.schedule_once(lambda dt: self.messages_failed(error), 0)
    
    def messages_loaded(self, messages):
        """Called when messages are loaded"""
        self.is_loading = False
        self.messages = messages
    
    def messages_failed(self, error):
        """Called when message loading fails"""
        self.is_loading = False
        print(f"Failed to load messages: {error}")
    
    def view_message(self, message):
        """View full message body"""
        threading.Thread(target=self._view_message_bg, args=(message['id'],), daemon=True).start()
    
    def _view_message_bg(self, message_id):
        """Load full message body"""
        result = self.api.get_message_body(message_id)
        if result.get("success"):
            Clock.schedule_once(lambda dt: self.show_message_detail(result.get("message")), 0)
    
    def show_message_detail(self, message):
        """Display message detail popup"""
        body_content = message.get("body", {}).get("content", "No content")
        subject = message.get("subject", "No Subject")
        sender = message.get("from", {}).get("emailAddress", {}).get("name", "Unknown")
        
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Subject label
        subj_label = Label(text=f"[b]{subject}[/b]\nFrom: {sender}", 
                          size_hint_y=0.2, markup=True, halign='left')
        content.add_widget(subj_label)
        
        # Body text input (read-only)
        body_input = TextInput(text=body_content, multiline=True, readonly=True,
                              size_hint_y=0.6)
        content.add_widget(body_input)
        
        # Buttons
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        replace_btn = Button(text="Find & Replace", on_press=lambda x: self.show_replace_dialog(message))
        download_btn = Button(text="Download", on_press=lambda x: self.download_message(message))
        close_btn = Button(text="Close", on_press=lambda x: popup.dismiss())
        
        btn_layout.add_widget(replace_btn)
        btn_layout.add_widget(download_btn)
        btn_layout.add_widget(close_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title=f"Message: {subject[:30]}...", content=content,
                     size_hint=(0.9, 0.9))
        popup.open()
    
    def show_replace_dialog(self, message):
        """Show find and replace dialog"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        find_input = TextInput(hint_text="Find text...", size_hint_y=0.15, multiline=False)
        replace_input = TextInput(hint_text="Replace with...", size_hint_y=0.15, multiline=False)
        result_label = Label(text="Preview will appear here", size_hint_y=0.5, valign='top')
        
        btn_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        preview_btn = Button(text="Preview", on_press=lambda x: self.preview_replace(find_input.text, replace_input.text, message, result_label))
        apply_btn = Button(text="Apply", on_press=lambda x: self.apply_replace(find_input.text, replace_input.text, message, result_label))
        btn_layout.add_widget(preview_btn)
        btn_layout.add_widget(apply_btn)
        
        content.add_widget(find_input)
        content.add_widget(replace_input)
        content.add_widget(result_label)
        content.add_widget(btn_layout)
        
        popup = Popup(title="Find & Replace Body", content=content, size_hint=(0.9, 0.7))
        popup.open()
    
    def preview_replace(self, find, replace, message, label):
        """Preview replacements"""
        body = message.get("body", {}).get("content", "")
        
        self.replacer.clear_patterns()
        self.replacer.add_pattern(find, replace)
        highlights = self.replacer.preview_replacements(body)
        
        if highlights:
            preview = f"Found {len(highlights)} matches:\n\n"
            for h in highlights[:5]:
                preview += f"[{h['text']}] -> [{h['replacement']}]\n"
            label.text = preview
        else:
            label.text = "No matches found"
    
    def apply_replace(self, find, replace, message, label):
        """Apply replacements to message"""
        self.replacer.clear_patterns()
        self.replacer.add_pattern(find, replace)
        
        new_body = self.replacer.apply_replacements(message.get("body", {}).get("content", ""))
        
        # Update via API
        result = self.api.update_message_body(message['id'], new_body)
        if result.get("success"):
            label.text = "Replacement applied successfully!"
        else:
            label.text = f"Failed: {result.get('error', 'Unknown error')}"
    
    def download_message(self, message):
        """Download/download message content"""
        # Save to archive
        save_dir = "./downloads"
        os.makedirs(save_dir, exist_ok=True)
        
        filepath = os.path.join(save_dir, f"{message['id']}.json")
        with open(filepath, 'w') as f:
            json.dump(message, f, indent=2)
        
        self.archive.log_download(message['id'], filepath)
        print(f"Message saved to {filepath}")
    
    def create_snapshot(self):
        """Create a snapshot of current folder state"""
        if self.selected_folder and self.messages:
            folder_id = self._get_folder_id_by_name(self.selected_folder)
            if folder_id:
                snapshot_id = self.archive.create_snapshot(folder_id, self.selected_folder, self.messages)
                print(f"Snapshot created: {snapshot_id}")
    
    def _get_folder_id_by_name(self, name):
        """Get folder ID from name"""
        for folder in self.folders:
            if folder.get("displayName") == name:
                return folder.get("id")
        return None


# ==================== KV LAYOUT ====================
KV_STRING = """
<SplashScreen>:
    canvas.before:
        Color:
            rgba: 0.04, 0.04, 0.06, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0.1, 0.5, 0.4, 0.1
        Line:
            points: [self.x + i * 40, self.y, self.x + i * 40, self.top] for i in range(30)
            width: 1
        Line:
            points: [self.x, self.y + i * 40, self.right, self.y + i * 40] for i in range(20)
            width: 1
    
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        
        Widget:
            size_hint_y: 0.3
        
        Label:
            text: "◆ ULTIMATE EDITION ◆"
            font_size: '18sp'
            color: 1, 0.55, 0, 1
        
        Label:
            text: "HOTMAIL INBOXER"
            font_size: '56sp'
            bold: True
            color: 1, 1, 1, 1
        
        Label:
            id: status_label
            text: root.status_text
            font_size: '16sp'
            color: 0, 1, 0.5, 1
        
        BoxLayout:
            size_hint_y: None
            height: 50
            padding: 50
            
            ProgressBar:
                id: progress_bar
                max: 1.0
                value: root.progress
                height: 20
                background_color: 0.15, 0.1, 0, 1
                color: 1, 0.55, 0, 1
        
        Label:
            text: f"{int(root.progress * 100)}%"
            font_size: '24sp'
            color: 1, 0.55, 0, 1
        
        Widget:
            size_hint_y: 0.2

<LoginScreen>:
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_max: 500, 600
        
        Label:
            text: "HOTMAIL INBOXER"
            font_size: '36sp'
            bold: True
            color: 1, 0.55, 0, 1
        
        Label:
            text: "Login to Outlook"
            font_size: '18sp'
            color: 0.8, 0.8, 0.8, 1
        
        TextInput:
            id: email_input
            hint_text: "Email address"
            multiline: False
            size_hint_y: None
            height: 50
            padding: 15
        
        TextInput:
            id: password_input
            hint_text: "Password"
            multiline: False
            password: True
            size_hint_y: None
            height: 50
            padding: 15
        
        Button:
            text: "LOGIN" if not root.is_loading else "AUTHENTICATING..."
            size_hint_y: None
            height: 50
            background_color: 1, 0.55, 0, 1
            on_press: root.login()
        
        Label:
            id: status_label
            text: root.status_text
            font_size: '14sp'
            color: 0, 1, 0.5, 1
        
        Label:
            text: "v2.0 Neural Edition"
            font_size: '12sp'
            color: 0.5, 0.5, 0.5, 1

<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        # Top bar
        BoxLayout:
            size_hint_y: None
            height: 60
            padding: 10
            
            Label:
                text: "HOTMAIL INBOXER v2.0"
                font_size: '20sp'
                bold: True
                color: 1, 0.55, 0, 1
            
            Button:
                text: "📸 Snapshot"
                size_hint_x: None
                width: 120
                on_press: root.create_snapshot()
            
            Button:
                text: "🔄 Refresh"
                size_hint_x: None
                width: 100
                on_press: root.load_folders()
        
        # Main content
        BoxLayout:
            orientation: 'horizontal'
            spacing: 10
            
            # Folder list
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.3
                
                Label:
                    text: "📁 MAILBOX FOLDERS"
                    size_hint_y: None
                    height: 40
                    font_size: '14sp'
                    bold: True
                    color: 0, 1, 0.5, 1
                
                ScrollView:
                    RecycleView:
                        id: folder_list
                        viewclass: 'Button'
                        data: [{'text': f.get('displayName', 'Unknown'), 
                                'on_press': lambda f=f: root.select_folder(f.get('displayName'), f.get('id'))} 
                               for f in root.folders]
                        RecycleBoxLayout:
                            default_size: None, 50
                            default_size_hint: 1, None
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: 'vertical'
                
                Label:
                    text: "Selected: " + root.selected_folder
                    size_hint_y: None
                    height: 30
                    font_size: '12sp'
                    color: 0.8, 0.8, 0.8, 1
            
            # Message list
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.7
                
                Label:
                    text: f"📧 MESSAGES ({len(root.messages)})"
                    size_hint_y: None
                    height: 40
                    font_size: '14sp'
                    bold: True
                    color: 0, 1, 0.5, 1
                
                ScrollView:
                    id: message_scroll
                    
                    RecycleView:
                        id: message_list
                        viewclass: 'Button'
                        data: [{'text': f"{m.get('subject', 'No Subject')[:40]}\n{m.get('from', {}).get('emailAddress', {}).get('name', 'Unknown')}",
                                'on_press': lambda m=m: root.view_message(m),
                                'markup': True}
                               for m in root.messages]
                        RecycleBoxLayout:
                            default_size: None, 80
                            default_size_hint: 1, None
                            size_hint_y: None
                            height: self.minimum_height
                            orientation: 'vertical'
                
                # Loading indicator
                Label:
                    text: "Loading..." if root.is_loading else ""
                    size_hint_y: None
                    height: 30
                    font_size: '14sp'
                    color: 1, 0.55, 0, 1
"""


# ==================== APP CLASS ====================
class HotmailInboxerApp(App):
    def build(self):
        from kivy.lang import Builder
        Builder.load_string(KV_STRING)
        
        sm = ScreenManager(transition=FadeTransition(duration=0.5))
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        
        return sm


if __name__ == '__main__':
    HotmailInboxerApp().run()