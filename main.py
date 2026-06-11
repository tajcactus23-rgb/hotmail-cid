"""
HOTMAIL INBOXER - NEURAL EDITION ANDROID APP
High-tech email management with neural network UI

Neural Theme Features:
- Animated neural network background
- Glowing particles and connection lines
- Cyberpunk color scheme (cyan/magenta/purple)
- Windows 11 style UI components

Built with Kivy for Android deployment
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, ListProperty
from kivy.animation import Animation
import random
import math
import os

# ============================================
# NEURAL THEME COLORS
# ============================================
BG_PRIMARY = (0.04, 0.04, 0.07, 1)
BG_SECONDARY = (0.07, 0.07, 0.12, 1)
BG_CARD = (0.1, 0.1, 0.18, 1)
ACCENT_CYAN = (0, 0.94, 1, 1)
ACCENT_MAGENTA = (1, 0, 0.67, 1)
ACCENT_PURPLE = (0.55, 0.36, 0.96, 1)
ACCENT_GREEN = (0, 1, 0.53, 1)
ACCENT_ORANGE = (1, 0.4, 0, 1)
TEXT_PRIMARY = (1, 1, 1, 1)
TEXT_SECONDARY = (0.63, 0.63, 0.75, 1)


# ============================================
# NEURAL NETWORK BACKGROUND ANIMATION
# ============================================
class NeuralBackground(Widget):
    """Animated neural network with floating nodes, connections, and particles"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nodes = []
        self.particles = []
        self.node_count = 50
        self.connection_distance = 180
        self.node_speed = 0.8
        self.init_nodes()
        self.init_particles()
        Clock.schedule_interval(self.update, 1/60)
    
    def init_nodes(self):
        for _ in range(self.node_count):
            self.nodes.append({
                'x': random.random() * Window.width,
                'y': random.random() * Window.height,
                'vx': random.uniform(-self.node_speed, self.node_speed),
                'vy': random.uniform(-self.node_speed, self.node_speed),
                'radius': random.uniform(2, 5),
                'pulse': random.random() * math.pi * 2,
                'pulse_speed': random.uniform(0.02, 0.06),
                'glow': random.uniform(0.4, 1.0),
                'color': random.choice([ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_PURPLE])
            })
    
    def init_particles(self):
        for _ in range(30):
            self.particles.append({
                'x': random.random() * Window.width,
                'y': random.random() * Window.height,
                'vx': random.uniform(-0.4, 0.4),
                'vy': random.uniform(-0.4, 0.4),
                'size': random.uniform(1, 3),
                'life': random.uniform(0.3, 1.0),
                'decay': random.uniform(0.002, 0.005)
            })
    
    def update(self, dt):
        self.canvas.clear()
        
        with self.canvas:
            # Draw connections between nodes
            for i, n1 in enumerate(self.nodes):
                for n2 in self.nodes[i+1:]:
                    dist = math.sqrt((n1['x']-n2['x'])**2 + (n1['y']-n2['y'])**2)
                    if dist < self.connection_distance:
                        opacity = 0.5 * (1 - dist / self.connection_distance)
                        pulse = (math.sin(n1['pulse']) + math.sin(n2['pulse'])) / 2
                        Color(*n1['color'], a=opacity * (0.6 + 0.4 * pulse))
                        Line(points=[n1['x'], n1['y'], n2['x'], n2['y']], width=1)
            
            # Draw and update nodes
            for node in self.nodes:
                node['x'] += node['vx']
                node['y'] += node['vy']
                node['pulse'] += node['pulse_speed']
                
                # Bounce off edges
                if node['x'] < 0 or node['x'] > Window.width:
                    node['vx'] *= -1
                if node['y'] < 0 or node['y'] > Window.height:
                    node['vy'] *= -1
                
                # Draw glow
                glow_radius = node['radius'] * (2 + math.sin(node['pulse']))
                Color(*node['color'], a=0.25 * node['glow'])
                Ellipse(pos=(node['x']-glow_radius, node['y']-glow_radius), 
                       size=(glow_radius*2, glow_radius*2))
                
                # Draw core
                Color(*node['color'], a=0.9)
                Ellipse(pos=(node['x']-node['radius'], node['y']-node['radius']), 
                       size=(node['radius']*2, node['radius']*2))
            
            # Update and draw particles
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= p['decay']
                
                if p['life'] <= 0 or p['x'] < 0 or p['x'] > Window.width or p['y'] < 0 or p['y'] > Window.height:
                    p['x'] = random.random() * Window.width
                    p['y'] = random.random() * Window.height
                    p['life'] = random.uniform(0.5, 1.0)
                
                Color(*ACCENT_MAGENTA, a=p['life'] * 0.6)
                Ellipse(pos=(p['x']-p['size'], p['y']-p['size']), 
                       size=(p['size']*2, p['size']*2))


# ============================================
# CUSTOM WIDGETS
# ============================================
class NeuralButton(Button):
    """Futuristic button with glow effect"""
    
    def __init__(self, glow_color=ACCENT_CYAN, **kwargs):
        self.glow_color = glow_color
        super().__init__(**kwargs)
        self.background_color = (glow_color[0]*0.3, glow_color[1]*0.3, glow_color[2]*0.3, 0.8)
        self.color = TEXT_PRIMARY
        self.font_size = '14sp'
        self.bold = True


class GlassCard(BoxLayout):
    """Glassmorphism card container"""
    
    def __init__(self, glow_color=ACCENT_PURPLE, **kwargs):
        self.glow_color = glow_color
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10


# ============================================
# SCREENS
# ============================================
class SplashScreen(Screen):
    """Animated splash screen with neural network"""
    
    def on_enter(self):
        # Animate title
        title = self.ids.title
        anim = Animation(opacity=1, duration=1)
        anim.start(title)
        
        # Transition to main after 3 seconds
        Clock.schedule_once(self.go_main, 3)
    
    def go_main(self, dt):
        self.manager.current = 'main'


class MainScreen(Screen):
    """Main application screen with tabs"""
    
    pass


class CheckerScreen(Screen):
    """Email checker module"""
    
    def oauth_login(self):
        self.ids.status.text = '[color=00f0ff]🔐 Launching OAuth...[/color]'
        Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', '[color=00ff88]✓ OAuth Ready[/color]'), 2)


class IndexerScreen(Screen):
    """Email indexer module"""
    
    def load_folders(self):
        self.ids.status.text = '[color=ffcc00]📁 Loading folders...[/color]'


class ReplacerScreen(Screen):
    """Body replacer module"""
    
    def load_message(self):
        self.ids.status.text = '[color=ffcc00]✏️ Loading message...[/color]'


class DownloaderScreen(Screen):
    """Downloader module"""
    
    def start_download(self):
        self.ids.status.text = '[color=ffcc00]📥 Downloading...[/color]'


# ============================================
# MAIN APP
# ============================================
class HotmailNeuralApp(App):
    
    def build(self):
        Window.clearcolor = BG_PRIMARY
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(MainScreen(name='main'))
        
        # Start with splash
        return sm


if __name__ == '__main__':
    HotmailNeuralApp().run()