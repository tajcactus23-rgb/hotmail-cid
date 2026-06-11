"""
HOTMAIL INBOXER - NEURAL EDITION
Android App with Animated Neural Network Background

Neural Theme Features:
- Animated neural network background with 50 nodes
- Glowing particles and pulsing connection lines
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
from kivy.graphics import Color, Line, Ellipse, Rectangle, ClearColor
from kivy.clock import Clock
from kivy.core.window import Window
import random
import math

# ============================================
# NEURAL THEME COLORS
# ============================================
BG_PRIMARY = (0.04, 0.04, 0.07, 1)
BG_SECONDARY = (0.07, 0.07, 0.12, 1)
ACCENT_CYAN = (0, 0.94, 1, 1)
ACCENT_MAGENTA = (1, 0, 0.67, 1)
ACCENT_PURPLE = (0.55, 0.36, 0.96, 1)
ACCENT_GREEN = (0, 1, 0.53, 1)
TEXT_WHITE = (1, 1, 1, 1)
TEXT_GRAY = (0.63, 0.63, 0.75, 1)


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
        self.init_nodes()
        Clock.schedule_interval(self.update, 1/60)
    
    def init_nodes(self):
        for _ in range(self.node_count):
            self.nodes.append({
                'x': random.random() * Window.width,
                'y': random.random() * Window.height,
                'vx': random.uniform(-0.5, 0.5),
                'vy': random.uniform(-0.5, 0.5),
                'radius': random.uniform(2, 5),
                'pulse': random.random() * math.pi * 2,
                'pulse_speed': random.uniform(0.02, 0.06),
                'color': random.choice([ACCENT_CYAN, ACCENT_MAGENTA, ACCENT_PURPLE])
            })
        
        for _ in range(30):
            self.particles.append({
                'x': random.random() * Window.width,
                'y': random.random() * Window.height,
                'vx': random.uniform(-0.3, 0.3),
                'vy': random.uniform(-0.3, 0.3),
                'size': random.uniform(1, 3),
                'life': random.uniform(0.3, 1.0),
                'decay': random.uniform(0.002, 0.005)
            })
    
    def update(self, dt):
        self.canvas.clear()
        
        with self.canvas:
            # Draw connections
            for i, n1 in enumerate(self.nodes):
                for n2 in self.nodes[i+1:]:
                    dist = math.sqrt((n1['x']-n2['x'])**2 + (n1['y']-n2['y'])**2)
                    if dist < self.connection_distance:
                        opacity = 0.5 * (1 - dist / self.connection_distance)
                        pulse = (math.sin(n1['pulse']) + math.sin(n2['pulse'])) / 2
                        Color(*n1['color'], a=opacity * (0.6 + 0.4 * pulse))
                        Line(points=[n1['x'], n1['y'], n2['x'], n2['y']], width=1)
            
            # Draw nodes
            for node in self.nodes:
                node['x'] += node['vx']
                node['y'] += node['vy']
                node['pulse'] += node['pulse_speed']
                
                # Bounce
                if node['x'] < 0 or node['x'] > Window.width:
                    node['vx'] *= -1
                if node['y'] < 0 or node['y'] > Window.height:
                    node['vy'] *= -1
                
                # Glow
                glow_radius = node['radius'] * (2 + math.sin(node['pulse']))
                Color(*node['color'], a=0.25)
                Ellipse(pos=(node['x']-glow_radius, node['y']-glow_radius), 
                       size=(glow_radius*2, glow_radius*2))
                
                # Core
                Color(*node['color'], a=0.9)
                Ellipse(pos=(node['x']-node['radius'], node['y']-node['radius']), 
                       size=(node['radius']*2, node['radius']*2))
            
            # Particles
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['life'] -= p['decay']
                
                if p['life'] <= 0 or p['x'] < 0 or p['x'] > Window.width:
                    p['x'] = random.random() * Window.width
                    p['y'] = random.random() * Window.height
                    p['life'] = random.uniform(0.5, 1.0)
                
                Color(*ACCENT_MAGENTA, a=p['life'] * 0.6)
                Ellipse(pos=(p['x']-p['size'], p['y']-p['size']), 
                       size=(p['size']*2, p['size']*2))


# ============================================
# CUSTOM WIDGETS
# ============================================
class GlassCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 10


class NeuralButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.1, 0.1, 0.2, 0.9)
        self.color = TEXT_WHITE
        self.font_size = '14sp'
        self.bold = True
        self.size_hint_y = None
        self.height = '50sp'


# ============================================
# SCREENS
# ============================================
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 3)


class LoginScreen(Screen):
    pass


class MainScreen(Screen):
    pass


class CheckerScreen(Screen):
    pass


class IndexerScreen(Screen):
    pass


class ReplacerScreen(Screen):
    pass


class DownloaderScreen(Screen):
    pass


# ============================================
# MAIN APP
# ============================================
class HotmailNeuralApp(App):
    
    def build(self):
        Window.clearcolor = BG_PRIMARY
        
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        
        return sm


if __name__ == '__main__':
    HotmailNeuralApp().run()