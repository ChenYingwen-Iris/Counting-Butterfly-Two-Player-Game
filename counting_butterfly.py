import pygame
import sys
import random
import time
import math
import os
from enum import Enum

# Initialize pygame
pygame.init()
# Initialize audio system
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# Game state enumeration
class GameState(Enum):
    START_SCREEN = 0
    COUNTDOWN = 1
    GAME_PLAY = 2
    INPUT_PHASE = 3
    RESULT_SCREEN = 4
    GAME_OVER = 5
    PAUSED = 6  # Paused state

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60
BUTTERFLY_HEIGHT = 36  # Unified butterfly height (pixels), adjustable

# Color definitions - Red and Blue contrast
RED = (255, 50, 50)
BLUE = (50, 100, 255)
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BACKGROUND = (240, 240, 240)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Counting Butterfly!")
clock = pygame.time.Clock()

# Load font - Use Press Start 2P pixel font
try:
    font_large = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)  # Pixel font recommended to use smaller sizes
    font_medium = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
    font_small = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
    print("✓ Successfully loaded Press Start 2P font!")
except:
    # If font loading fails, try using system font
    try:
        font_large = pygame.font.Font("freesansbold.ttf", 48)
        font_medium = pygame.font.Font("freesansbold.ttf", 32)
        font_small = pygame.font.Font("freesansbold.ttf", 24)
        print("Using default system font")
    except:
        font_large = pygame.font.SysFont(None, 48)
        font_medium = pygame.font.SysFont(None, 32)
        font_small = pygame.font.SysFont(None, 24)
        print("Using pygame default font")

# Load background image (optional)
def load_background_image():
    try:
        img = pygame.image.load("assets/images/background1.png").convert()
        return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception:
        return None

# Load audio files
def load_sounds():
    """Load background music and sound effects"""
    sounds = {
        'bgm': None,
        'countdown': None,
        'start': None,
        'beep': None,
        'success': None,
        'wrong': None
    }
    
    try:
        # Try to load background music (electronic style)
        if os.path.exists("assets/audio/bgm.mp3") or os.path.exists("assets/audio/bgm.ogg") or os.path.exists("assets/audio/bgm.wav"):
            for ext in ['mp3', 'ogg', 'wav']:
                if os.path.exists(f"assets/audio/bgm.{ext}"):
                    pygame.mixer.music.load(f"assets/audio/bgm.{ext}")
                    pygame.mixer.music.set_volume(0.5)
                    print(f"✓ Successfully loaded background music: bgm.{ext}")
                    sounds['bgm'] = True
                    break
        else:
            print("⚠ BGM music file not found (supported: bgm.mp3, bgm.ogg, bgm.wav)")
    except Exception as e:
        print(f"✗ Failed to load background music: {e}")
    
    try:
        # Try to load countdown sound effect
        for ext in ['wav', 'ogg', 'mp3']:
            if os.path.exists(f"assets/audio/countdown.{ext}"):
                sounds['countdown'] = pygame.mixer.Sound(f"assets/audio/countdown.{ext}")
                sounds['countdown'].set_volume(0.7)
                print(f"✓ Successfully loaded countdown sound: countdown.{ext}")
                break
        if not sounds['countdown']:
            print("⚠ Countdown sound file not found (supported: countdown.wav, countdown.ogg, countdown.mp3)")
    except Exception as e:
        print(f"✗ Failed to load countdown sound: {e}")
    
    try:
        # Try to load start sound effect
        for ext in ['wav', 'ogg', 'mp3']:
            if os.path.exists(f"assets/audio/start.{ext}"):
                sounds['start'] = pygame.mixer.Sound(f"assets/audio/start.{ext}")
                sounds['start'].set_volume(0.8)
                print(f"✓ Successfully loaded start sound: start.{ext}")
                break
        if not sounds['start']:
            print("⚠ Start sound file not found (supported: start.wav, start.ogg, start.mp3)")
    except Exception as e:
        print(f"✗ Failed to load start sound: {e}")
    
    try:
        # Try to load keypress sound effect
        for ext in ['wav', 'ogg', 'mp3']:
            if os.path.exists(f"assets/audio/beep.{ext}"):
                sounds['beep'] = pygame.mixer.Sound(f"assets/audio/beep.{ext}")
                sounds['beep'].set_volume(0.4)
                print(f"✓ Successfully loaded keypress sound: beep.{ext}")
                break
    except Exception as e:
        print(f"✗ Failed to load keypress sound: {e}")
    
    try:
        # Try to load success sound effect
        for ext in ['wav', 'ogg', 'mp3']:
            if os.path.exists(f"assets/audio/success.{ext}"):
                sounds['success'] = pygame.mixer.Sound(f"assets/audio/success.{ext}")
                sounds['success'].set_volume(0.6)
                print(f"✓ Successfully loaded success sound: success.{ext}")
                break
    except Exception as e:
        print(f"✗ Failed to load success sound: {e}")
    
    try:
        # Try to load error sound effect
        for ext in ['wav', 'ogg', 'mp3']:
            if os.path.exists(f"assets/audio/wrong.{ext}"):
                sounds['wrong'] = pygame.mixer.Sound(f"assets/audio/wrong.{ext}")
                sounds['wrong'].set_volume(0.5)
                print(f"✓ Successfully loaded error sound: wrong.{ext}")
                break
    except Exception as e:
        print(f"✗ Failed to load error sound: {e}")
    
    return sounds

# Helper function: Draw text with white outline
def draw_text_with_outline(surface, text, font, color, x, y, outline_color=(255, 255, 255), outline_width=2):
    """
    Draw text with outline
    :param surface: Drawing surface
    :param text: Text content
    :param font: Font
    :param color: Text color
    :param x: X coordinate
    :param y: Y coordinate
    :param outline_color: Outline color
    :param outline_width: Outline width
    :return: Text surface object
    """
    # Draw outline (8 directions)
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                surface.blit(outline_surface, (x + dx, y + dy))
    
    # Draw main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
    return text_surface

# Pixel-style butterfly class
class Butterfly:
    # Static image loading
    blue_img = None
    red_img = None
    @staticmethod
    def load_images():
        if Butterfly.blue_img is None:
            try:
                Butterfly.blue_img = pygame.image.load("butterfly_blue.png").convert_alpha()
            except Exception:
                Butterfly.blue_img = None
        if Butterfly.red_img is None:
            try:
                Butterfly.red_img = pygame.image.load("butterfly_red.png").convert_alpha()
            except Exception:
                Butterfly.red_img = None

    def __init__(self, x, y, style=None, moving=False):
        self.x = x
        self.y = y
        self.size = 64  # Butterfly display size
        self.spawn_time = time.time()
        self.lifetime = random.uniform(1.8, 3.0)  # Shorten single butterfly lifetime
        self.wing_phase = random.uniform(0, math.pi * 2)
        Butterfly.load_images()
        # Alternate blue and red
        if style is not None:
            self.style = style
        else:
            self.style = random.choice(["blue", "red"])
        self.img = Butterfly.blue_img if self.style == "blue" else Butterfly.red_img
        
        # Movement attributes (Level 3)
        self.moving = moving
        if self.moving:
            # Random direction (360 degrees)
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 1.5)  # Random speed
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        else:
            self.vx = 0
            self.vy = 0

    def update(self):
        # If butterfly is moving, update position
        if self.moving:
            self.x += self.vx
            self.y += self.vy
            
            # Bounce off boundaries
            if self.x < 60 or self.x > SCREEN_WIDTH - 60:
                self.vx = -self.vx
                self.x = max(60, min(SCREEN_WIDTH - 60, self.x))
            if self.y < 40 or self.y > SCREEN_HEIGHT - 100:
                self.vy = -self.vy
                self.y = max(40, min(SCREEN_HEIGHT - 100, self.y))
        
        self.wing_phase += 0.3
        return time.time() - self.spawn_time > self.lifetime

    def draw(self, surface):
        if self.img:
            # Maintain original aspect ratio, max side is self.size
            bob = int(8 * math.sin(self.wing_phase))
            w, h = self.img.get_width(), self.img.get_height()
            if w > h:
                scale_w = self.size
                scale_h = int(h * self.size / w)
            else:
                scale_h = self.size
                scale_w = int(w * self.size / h)
            img = pygame.transform.smoothscale(self.img, (scale_w, scale_h))
            surface.blit(img, (self.x - scale_w//2, self.y - scale_h//2 + bob))
        else:
            # If image loading fails, use fallback pixel art drawing
            s = self.size
            wing_offset = int(s * 0.18 * abs(pygame.math.Vector2(1, 0).rotate(self.wing_phase * 30).x))
            pygame.draw.rect(surface, (50, 50, 50), (self.x - s//16, self.y, s//8, s//2))
            for dx, dy, w, h in [(-s//2-wing_offset, -s//4, s//2, s//2), (s//4+wing_offset, -s//4, s//2, s//2), (-s//3-wing_offset, s//8, s//3, s//3), (s//6+wing_offset, s//8, s//3, s//3)]:
                pygame.draw.ellipse(surface, (0,0,0), (self.x+dx-3, self.y+dy-3, w+6, h+6), 0)
                pygame.draw.ellipse(surface, (0, 80, 255) if self.style=="blue" else (255, 50, 50), (self.x+dx, self.y+dy, w, h), 0)

# Load character sprite images
def load_player_sprites():
    sprites = {}
    try:
        # Load sprite file (preserve alpha channel)
        red_stand = pygame.image.load("assets/images/red_player_stand.png").convert_alpha()
        red_walk = pygame.image.load("assets/images/red_player_walk.png").convert_alpha()
        blue_stand = pygame.image.load("assets/images/blue_player_stand.png").convert_alpha()
        blue_walk = pygame.image.load("assets/images/blue_player_walk.png").convert_alpha()

        print(f"Loaded sprite size: {red_stand.get_size()}")

        def auto_crop_surface(surf: pygame.Surface) -> pygame.Surface:
            """Auto-crop transparent margins using pixel mask, return cropped Surface. Return original if failed."""
            try:
                mask = pygame.mask.from_surface(surf)
                rect = mask.get_bounding_rect()
                if rect.width > 0 and rect.height > 0:
                    return surf.subsurface(rect).copy()
            except Exception:
                pass
            return surf

        def extract_and_scale_sprite(sprite, frame_index=0):
            """Use entire sprite image, auto-crop transparent margins then scale up"""
            cropped = auto_crop_surface(sprite)
            sprite_width, sprite_height = cropped.get_size()
            target_height = 130
            target_width = max(1, int(sprite_width * target_height / max(1, sprite_height)))
            scaled = pygame.transform.scale(cropped, (target_width, target_height))
            print(
                f"Crop and scale: original({sprite.get_width()}x{sprite.get_height()}) -> cropped({sprite_width}x{sprite_height}) -> scaled({target_width}x{target_height})"
            )
            return scaled

        # Extract red character - use entire image
        sprites['red_stand'] = extract_and_scale_sprite(red_stand, 0)
        sprites['red_walk1'] = extract_and_scale_sprite(red_walk, 0)
        sprites['red_walk2'] = extract_and_scale_sprite(red_walk, 0)
        sprites['red_walk3'] = extract_and_scale_sprite(red_walk, 0)

        # Extract blue character - use entire image
        sprites['blue_stand'] = extract_and_scale_sprite(blue_stand, 0)
        sprites['blue_walk1'] = extract_and_scale_sprite(blue_walk, 0)
        sprites['blue_walk2'] = extract_and_scale_sprite(blue_walk, 0)
        sprites['blue_walk3'] = extract_and_scale_sprite(blue_walk, 0)

        print("✓ Successfully loaded all character sprites!")
    except Exception as e:
        print(f"✗ Failed to load sprite files: {e}")
        print("Will use fallback drawing method")
    return sprites

background_image = load_background_image()
player_sprites = load_player_sprites()
game_sounds = load_sounds()  # Load audio files


# Load butterfly images (two styles, optional)
def load_butterfly_images():
    bases = []
    try:
        def auto_crop_surface(surf: pygame.Surface) -> pygame.Surface:
            try:
                mask = pygame.mask.from_surface(surf)
                rect = mask.get_bounding_rect()
                if rect.width > 0 and rect.height > 0:
                    return surf.subsurface(rect).copy()
            except Exception:
                pass
            return surf

        # Load blue and red butterfly images
        for name in ["assets/images/butterfly_blue.png", "assets/images/butterfly_red.png"]:
            try:
                s = pygame.image.load(name).convert()
                arr = pygame.surfarray.pixels3d(s)
                alpha = pygame.surfarray.pixels_alpha(s)
                # Make near-white pixels transparent
                threshold = 240
                mask = (arr[:,:,0] > threshold) & (arr[:,:,1] > threshold) & (arr[:,:,2] > threshold)
                alpha[:,:][mask] = 0
                del arr, alpha
                s = s.convert_alpha()
                s = auto_crop_surface(s)
                bases.append(s)
            except Exception:
                pass
    except Exception:
        pass
    # No longer load images, return empty list, draw all with pixel art
    print("All butterflies are pixel-style procedurally drawn!")
    return []
    self.sprite = None
    self.style_index = None
    # No longer load images, draw all with pixel art
        
    def update(self):
        # Flapping effect (not dependent on assets, can be shared)
        self.wing_phase += 0.3
        return time.time() - self.spawn_time > self.lifetime

    def draw(self, surface):
        if self.sprite is not None:
            # Slight vertical oscillation, simulate flight
            bob = int(3 * math.sin(self.wing_phase))
            sx = self.x - self.sprite.get_width() // 2
            sy = self.y - self.sprite.get_height() // 2 + bob
            surface.blit(self.sprite, (sx, sy))
            return

        # Fallback: Draw pixel-art butterfly
        wing_offset = int(5 * abs(pygame.math.Vector2(1, 0).rotate(self.wing_phase * 30).x))
        pygame.draw.rect(surface, (50, 50, 50), (self.x, self.y, 4, 10))
        pygame.draw.ellipse(surface, self.color, (self.x - 8 - wing_offset, self.y - 5, 10, 8))
        pygame.draw.ellipse(surface, self.color, (self.x + 2 + wing_offset, self.y - 5, 10, 8))
        pygame.draw.ellipse(surface, self.color, (self.x - 6 - wing_offset, self.y + 2, 8, 6))
        pygame.draw.ellipse(surface, self.color, (self.x + 2 + wing_offset, self.y + 2, 8, 6))

# Player class
class Player:
    def __init__(self, x, color, controls):
        self.x = x
        self.y = 0  # Initialize y position
        self.color = color
        self.score = 0
        self.input_value = 0
        self.controls = controls  # (up_key, down_key, submit_key)
        self.submitted = False
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_counter = 0
        self.is_moving = False
        
    def animate(self):
        """Continuous animation: switch between 0/1 every fixed frames, no key press required."""
        self.animation_timer += 1
        if self.animation_timer > 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2

    def update(self, events):
        # Handle input - can enter any number
        self.is_moving = False
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == self.controls[0]:  # Up key/W key
                    self.input_value += 1  # Increase by 1 each time
                    self.is_moving = True
                    # Play keypress sound
                    if game_sounds['beep']:
                        game_sounds['beep'].play()
                elif event.key == self.controls[1]:  # Down key/S key
                    if self.input_value > 0:  # Ensure not less than 0
                        self.input_value -= 1  # Decrease by 1 each time
                        self.is_moving = True
                        # Play keypress sound
                        if game_sounds['beep']:
                            game_sounds['beep'].play()
                elif event.key == self.controls[2]:  # Submit key
                    self.submitted = True
                    self.is_moving = True
                    
    def reset_input(self):
        self.input_value = 0
        self.submitted = False
        
    def draw(self, surface, y):
        # Larger butterfly size with black outline
        # ...existing code...
        # If corresponding sprite exists, use it
        sprite_key = ""
        if self.color == RED:
            sprite_key = "red_stand" if self.animation_frame == 0 else "red_walk1"
        else:  # BLUE
            sprite_key = "blue_stand" if self.animation_frame == 0 else "blue_walk1"
        if sprite_key in player_sprites and player_sprites[sprite_key]:
            try:
                sprite = player_sprites[sprite_key]
                sprite_x = self.x - sprite.get_width() // 2
                sprite_y = y - sprite.get_height()
                surface.blit(sprite, (sprite_x, sprite_y))
                return
            except Exception as e:
                print(f"Sprite drawing error: {e}")
        self.draw_fallback(surface, y)
        # If corresponding sprite exists, use it
        if sprite_key in player_sprites and player_sprites[sprite_key]:
            try:
                sprite = player_sprites[sprite_key]
                
                # Draw sprite centered (no border/background)
                sprite_x = self.x - sprite.get_width() // 2
                sprite_y = y - sprite.get_height()
                surface.blit(sprite, (sprite_x, sprite_y))
                
                return  # Successfully drew sprite, exit
                
            except Exception as e:
                print(f"Sprite drawing error: {e}")
        
        # If sprite loading fails, use fallback method
        self.draw_fallback(surface, y)
    
    def draw_fallback(self, surface, y):
        # Enhanced fallback drawing - larger more visible character
        size = 60  # Increase base size
        
        # First draw visible background border
        bg_rect = pygame.Rect(self.x - size//2 - 5, y - size - 5, size + 10, size + 10)
        pygame.draw.rect(surface, (255, 255, 255), bg_rect)  # White background
        pygame.draw.rect(surface, (0, 0, 0), bg_rect, 3)      # Black border
        
        # Head - large circle
        pygame.draw.circle(surface, self.color, (self.x, y - 40), 18)
        pygame.draw.circle(surface, (255, 255, 255), (self.x, y - 40), 18, 2)
        
        # Eyes
        pygame.draw.circle(surface, (255, 255, 255), (self.x - 6, y - 42), 3)
        pygame.draw.circle(surface, (255, 255, 255), (self.x + 6, y - 42), 3)
        pygame.draw.circle(surface, (0, 0, 0), (self.x - 6, y - 42), 1)
        pygame.draw.circle(surface, (0, 0, 0), (self.x + 6, y - 42), 1)
        
        # Body - rectangle
        body_rect = pygame.Rect(self.x - 12, y - 20, 24, 35)
        pygame.draw.rect(surface, self.color, body_rect)
        def draw(self, surface, y):
            # Only draw player, not butterflies
            sprite_key = ""
            if self.color == RED:
                sprite_key = "red_stand" if self.animation_frame == 0 else "red_walk1"
            else:  # BLUE
                sprite_key = "blue_stand" if self.animation_frame == 0 else "blue_walk1"
            if sprite_key in player_sprites and player_sprites[sprite_key]:
                try:
                    sprite = player_sprites[sprite_key]
                    sprite_x = self.x - sprite.get_width() // 2
                    sprite_y = y - sprite.get_height()
                    surface.blit(sprite, (sprite_x, sprite_y))
                    return
                except Exception as e:
                    print(f"Sprite drawing error: {e}")
            self.draw_fallback(surface, y)

# Main game class
class ButterflyGame:
    def __init__(self):
        self.state = GameState.START_SCREEN
        self.level = 1
        self.butterflies = []
        self.total_butterflies = 0
        self.current_butterflies = 0
        self.level_target = 0
        self.last_spawn_time = 0
        self.input_timer = 0
        self.correct_answer = 0
        self.countdown_timer = 0  # Countdown
        self.countdown_start_time = 0
        self.last_countdown_sound = 0  # Last number for countdown sound played
        self.paused = False  # Pause flag
        self.previous_state = None  # State before pause
        
        # Create players (red on right, blue on left, keys match positions)
        # player1 = red, on right, uses UP/DOWN/ENTER
        self.player1 = Player(SCREEN_WIDTH * 3 // 4, RED, (pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))
        # player2 = blue, on left, uses W/S/SPACE
        self.player2 = Player(SCREEN_WIDTH // 4, BLUE, (pygame.K_w, pygame.K_s, pygame.K_SPACE))
        
        # Play background music at game start
        if game_sounds['bgm']:
            pygame.mixer.music.play(-1)  # -1 means loop playback
            print("♪ Background music started (initial screen)")
        
    def start_level(self):
        # Level 3 target count is half
        if self.level == 3:
            base_target = 12  # Half of 24
            self.level_target = random.randint(base_target - 2, base_target + 2)
        else:
            self.level_target = random.randint([8, 15, 24][self.level-1] - 2, 
                                              [8, 15, 24][self.level-1] + 2)
        self.total_butterflies = 0
        self.current_butterflies = 0
        self.butterflies = []
        self.last_spawn_time = time.time()
        # Start countdown
        self.countdown_timer = 3
        self.countdown_start_time = time.time()
        self.last_countdown_sound = 0
        self.state = GameState.COUNTDOWN
        
    def spawn_butterflies(self):
        current_time = time.time()
        if current_time - self.last_spawn_time > 1.5 and self.total_butterflies < self.level_target:
            # Generate 1-4 butterflies randomly across screen (not divided by color)
            count = random.randint(1, min(4, self.level_target - self.total_butterflies))
            player_y = SCREEN_HEIGHT - 60  # Player base height
            
            # Count blue/red butterflies, ensure balanced generation
            blue_count = sum(1 for b in self.butterflies if b.style == "blue")
            red_count = sum(1 for b in self.butterflies if b.style == "red")
            
            # Alternate blue and red butterflies
            for i in range(count):
                # Try to find non-overlapping position
                attempts = 0
                while attempts < 20:
                    # X-axis: Random across screen width (not divided by color)
                    px = random.randint(60, SCREEN_WIDTH - 60)  # At least 60 pixels from edge
                    # Y-axis: 150-320 pixels above player (further from characters)
                    py = player_y - random.randint(150, 320)
                    py = max(40, min(SCREEN_HEIGHT - 100, py))  # Ensure within screen boundaries
                    
                    # Check overlap with existing butterflies (min spacing 70px)
                    is_overlapping = False
                    for b in self.butterflies:
                        distance = math.sqrt((px - b.x)**2 + (py - b.y)**2)
                        if distance < 70:
                            is_overlapping = True
                            break
                    
                    if not is_overlapping:
                        break
                    attempts += 1
                
                # Prioritize generating fewer color, ensure balance
                if blue_count <= red_count:
                    style = "blue"
                    blue_count += 1
                else:
                    style = "red"
                    red_count += 1
                
                # Level 3 butterflies move
                is_moving = (self.level == 3)
                self.butterflies.append(Butterfly(px, py, style=style, moving=is_moving))
                self.total_butterflies += 1
            self.last_spawn_time = current_time
            
    def update_countdown(self, dt):
        """Update countdown"""
        elapsed = time.time() - self.countdown_start_time
        remaining = 3 - elapsed
        
        if remaining <= 0:
            # Countdown finished, start game
            self.state = GameState.GAME_PLAY
            self.last_spawn_time = time.time()
            # Play start sound
            if game_sounds['start']:
                try:
                    game_sounds['start'].play()
                except Exception as e:
                    print(f"Failed to play start sound: {e}")
        else:
            current_number = int(remaining) + 1  # 3, 2, 1
            self.countdown_timer = current_number
            
            # Play countdown sound when number changes
            if current_number != self.last_countdown_sound and game_sounds['countdown']:
                self.last_countdown_sound = current_number
                try:
                    game_sounds['countdown'].play()
                except Exception as e:
                    print(f"Failed to play countdown sound: {e}")
            
    def update_gameplay(self):
        # Generate butterflies
        self.spawn_butterflies()
        
        # Update butterflies
        self.butterflies = [b for b in self.butterflies if not b.update()]
        self.current_butterflies = len(self.butterflies)
        
        # Level 3: Check if moving butterflies overlap, bounce if too close
        if self.level == 3:
            for i, b1 in enumerate(self.butterflies):
                for b2 in self.butterflies[i+1:]:
                    distance = math.sqrt((b1.x - b2.x)**2 + (b1.y - b2.y)**2)
                    if distance < 70:  # Minimum spacing 70 pixels
                        # Calculate bounce direction
                        dx = b2.x - b1.x
                        dy = b2.y - b1.y
                        if distance > 0:
                            # Normalize
                            dx /= distance
                            dy /= distance
                            # Bounce (swap and reverse velocity components)
                            b1.vx, b2.vx = -b2.vx, -b1.vx
                            b1.vy, b2.vy = -b2.vy, -b1.vy
                            # Separate overlapping butterflies
                            overlap = 70 - distance
                            b1.x -= dx * overlap / 2
                            b1.y -= dy * overlap / 2
                            b2.x += dx * overlap / 2
                            b2.y += dy * overlap / 2
        
        # Check if all butterflies disappeared
        if self.total_butterflies >= self.level_target and len(self.butterflies) == 0:
            self.correct_answer = self.total_butterflies
            self.start_input_phase()
            
    def start_input_phase(self):
        self.state = GameState.INPUT_PHASE
        self.input_timer = 10  # 10 seconds input time
        self.player1.reset_input()
        self.player2.reset_input()
        self.show_result = False  # Whether to show result
        self.result_display_timer = 0  # Result display timer
        
    def update_input_phase(self, events, dt):
        # If showing result, countdown then next level
        if self.show_result:
            self.result_display_timer -= dt
            if self.result_display_timer <= 0:
                if self.level < 3:
                    self.level += 1
                    self.start_level()
                else:
                    self.state = GameState.GAME_OVER
            return
        
        # Update input timer
        self.input_timer -= dt
        
        # Update player input
        self.player1.update(events)
        self.player2.update(events)
        
        # Check if time's up or both players submitted
        if self.input_timer <= 0 or (self.player1.submitted and self.player2.submitted):
            self.calculate_results()
            self.show_result = True
            self.result_display_timer = 4  # Show results for 4 seconds
            
    def calculate_results(self):
        # Calculate scores
        p1_correct = self.player1.input_value == self.correct_answer
        p2_correct = self.player2.input_value == self.correct_answer
        
        # Play sound effects
        if p1_correct or p2_correct:
            # At least one correct, play success sound
            if game_sounds['success']:
                game_sounds['success'].play()
        else:
            # Both wrong, play error sound
            if game_sounds['wrong']:
                game_sounds['wrong'].play()
        
        if p1_correct and p2_correct:
            # Both correct, first submitter gets 10 pts, second gets 5 pts
            if self.player1.submitted and not self.player2.submitted:
                self.player1.score += 10
                self.player2.score += 5
            elif not self.player1.submitted and self.player2.submitted:
                self.player1.score += 5
                self.player2.score += 10
            else:
                # Both submitted or both not submitted but answer correct
                self.player1.score += 10
                self.player2.score += 10
        elif p1_correct:
            self.player1.score += 10
        elif p2_correct:
            self.player2.score += 10
        
        # No longer switch to RESULT_SCREEN, results displayed directly in INPUT_PHASE
        
    def update_result_screen(self, dt):
        self.result_timer -= dt
        if self.result_timer <= 0:
            if self.level < 3:
                self.level += 1
                self.start_level()
            else:
                self.state = GameState.GAME_OVER
                
    def draw_start_screen(self):
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND)
        
        # Draw decorative butterflies (floating effect)
        time_offset = time.time()
        for i in range(8):
            x = 100 + (i % 4) * 200 + int(30 * math.sin(time_offset + i))
            y = 80 + (i // 4) * 280 + int(20 * math.cos(time_offset * 0.8 + i))
            
            # Random colored decorative butterflies
            deco_color = [(255, 180, 200), (200, 180, 255), (255, 220, 150), (180, 255, 200)][i % 4]
            wing_phase = time_offset * 3 + i
            wing_offset = int(8 * abs(math.sin(wing_phase)))
            
            # Butterfly body
            pygame.draw.ellipse(screen, (100, 100, 100), (x - 2, y - 8, 4, 16))
            # Upper wings
            pygame.draw.ellipse(screen, deco_color, (x - 12 - wing_offset, y - 8, 14, 12))
            pygame.draw.ellipse(screen, deco_color, (x + wing_offset, y - 8, 14, 12))
            # Lower wings
            pygame.draw.ellipse(screen, deco_color, (x - 10 - wing_offset, y + 2, 11, 9))
            pygame.draw.ellipse(screen, deco_color, (x + wing_offset, y + 2, 11, 9))
        
        # Game title - colorful gradient effect
        title_text = "Counting Butterfly!"
        colors = [(255, 100, 100), (255, 180, 100), (255, 220, 100), (100, 255, 150), 
                  (100, 200, 255), (180, 150, 255), (255, 150, 200)]
        
        # Calculate total width for centering
        total_width = sum(font_large.render(char, True, BLACK).get_width() for char in title_text)
        x_offset = SCREEN_WIDTH//2 - total_width//2
        
        # Draw colorful title (different color for each character)
        for i, char in enumerate(title_text):
            color = colors[i % len(colors)]
            char_surface = font_large.render(char, True, color)
            # Add shadow
            shadow = font_large.render(char, True, (80, 80, 80))
            screen.blit(shadow, (x_offset + 3, 153))
            screen.blit(char_surface, (x_offset, 150))
            x_offset += char_surface.get_width()
        
        # Add colorful decoration line below title
        pygame.draw.rect(screen, (255, 100, 150), (SCREEN_WIDTH//2 - 150, 200, 60, 4))
        pygame.draw.rect(screen, (255, 200, 100), (SCREEN_WIDTH//2 - 80, 200, 60, 4))
        pygame.draw.rect(screen, (100, 200, 255), (SCREEN_WIDTH//2 - 10, 200, 60, 4))
        pygame.draw.rect(screen, (150, 255, 150), (SCREEN_WIDTH//2 + 60, 200, 60, 4))
        
        # Advance animation and draw player characters (bigger and more visible)
        self.player1.animate()
        self.player2.animate()
        
        # Display two characters in center, standing left and right
        player_y = SCREEN_HEIGHT//2 + 60
        
        # Draw character platform/base
        pygame.draw.ellipse(screen, (200, 200, 200), (SCREEN_WIDTH//4 - 40, player_y + 20, 80, 15))
        pygame.draw.ellipse(screen, (200, 200, 200), (SCREEN_WIDTH*3//4 - 40, player_y + 20, 80, 15))
        
        # Player base position, more separated left/right, moved down overall
        player_y = SCREEN_HEIGHT - 80
        player_x_left = SCREEN_WIDTH // 4 - 60
        player_x_right = SCREEN_WIDTH * 3 // 4 + 60
        self.player2.x = player_x_left
        self.player1.x = player_x_right
        self.player2.draw(screen, player_y)
        self.player1.draw(screen, player_y)
        
        # Start hint - colorful blinking effect, SPACE in distinct color
        if int(time.time() * 2) % 2 == 0:
            start_text_str = "Press SPACE to Start"
            colors_start = [(255, 100, 100), (255, 180, 100), (255, 220, 100), (100, 255, 150), 
                           (100, 200, 255), (180, 150, 255), (255, 150, 200)]
            
            # Calculate total width for centering
            total_width = sum(font_medium.render(char, True, BLACK).get_width() for char in start_text_str)
            x_offset = SCREEN_WIDTH//2 - total_width//2
            
            # Draw colorful start hint, "SPACE" in bright yellow
            char_index = 0
            for i, char in enumerate(start_text_str):
                # Check if in "SPACE" word (position 6-10)
                if 6 <= i <= 10:
                    color = (255, 255, 50)  # Bright yellow, eye-catching
                else:
                    color = colors_start[char_index % len(colors_start)]
                    char_index += 1
                char_surface = font_medium.render(char, True, color)
                screen.blit(char_surface, (x_offset, SCREEN_HEIGHT - 80))
                x_offset += char_surface.get_width()
        
        # Small decoration at bottom
        for i in range(5):
            x = 100 + i * 150
            pygame.draw.circle(screen, (220, 220, 220), (x, SCREEN_HEIGHT - 20), 5)
            pygame.draw.circle(screen, (180, 180, 180), (x + 75, SCREEN_HEIGHT - 20), 3)
            
    def draw_countdown(self):
        """Draw countdown screen"""
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND)
        
        # Draw level info - more vibrant colors
        level_text = font_medium.render(f"Level {self.level}", True, (255, 50, 150))  # Vivid pink
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 20))
        
        # Draw large countdown numbers with animation effect
        countdown_num = str(self.countdown_timer)
        # Calculate animation scale effect
        elapsed = time.time() - self.countdown_start_time
        scale_progress = (elapsed % 1.0)  # Loop from 0 to 1
        base_size = 120
        scale = 1.0 + (1.0 - scale_progress) * 0.5  # Scale from 1.5 to 1.0
        
        # Create extra large font for countdown
        countdown_font = pygame.font.Font("PressStart2P-Regular.ttf", int(base_size * scale)) if os.path.exists("PressStart2P-Regular.ttf") else pygame.font.SysFont(None, int(base_size * scale * 2))
        
        # Colored numbers: 3=red, 2=yellow, 1=green
        colors = {3: (255, 50, 50), 2: (255, 220, 50), 1: (50, 255, 100)}
        countdown_color = colors.get(self.countdown_timer, (255, 255, 255))
        
        countdown_surface = countdown_font.render(countdown_num, True, countdown_color)
        countdown_rect = countdown_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        # Draw shadow
        shadow_surface = countdown_font.render(countdown_num, True, (50, 50, 50))
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH//2 + 5, SCREEN_HEIGHT//2 + 5))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(countdown_surface, countdown_rect)
        
        # Draw hint text - use vivid purple with white outline
        hint_x = SCREEN_WIDTH//2 - font_small.render("Get Ready!", True, (200, 50, 255)).get_width()//2
        draw_text_with_outline(screen, "Get Ready!", font_small, (200, 50, 255), hint_x, SCREEN_HEIGHT//2 + 100)
        
        # Advance animation and draw players
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
            
    def draw_gameplay(self):
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND)
        
        # Draw level info - more vibrant colors
        level_text = font_medium.render(f"Level {self.level}", True, (255, 50, 150))  # Vivid pink
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, 20))
        
        # Draw butterflies
        for butterfly in self.butterflies:
            butterfly.draw(screen)
        
        # Advance animation and draw players
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
        
    def draw_input_phase(self):
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND)
        
        # Draw timer - more vivid colors, turns red when time is low
        timer_color = (255, 50, 50) if self.input_timer <= 3 else (50, 200, 255)  # Red if less than 3 seconds, otherwise bright blue
        timer_text = font_medium.render(f"Time: {int(self.input_timer)}", True, timer_color)
        screen.blit(timer_text, (SCREEN_WIDTH//2 - timer_text.get_width()//2, 20))
        
        # If results not shown yet, display hint text
        if not self.show_result:
            hint_text = font_small.render("The faster you type, the higher the score you get!", True, (255, 215, 0))
            screen.blit(hint_text, (SCREEN_WIDTH//2 - hint_text.get_width()//2, 55))
        
        # Red/blue box position: aligned with player horizontal position, vertically above character head
        # Blue player on left side (SCREEN_WIDTH//4)
        blue_x = SCREEN_WIDTH//4
        # Red player on right side (SCREEN_WIDTH*3//4)
        red_x = SCREEN_WIDTH*3//4
        
        # Input box position: above character head (character bottom 420, head 290, box around 200)
        box_y = 180
        
        # Draw players input boxes (red/blue swapped)
        pygame.draw.rect(screen, BLUE, (blue_x - 50, box_y - 25, 100, 50), 3)
        pygame.draw.rect(screen, RED, (red_x - 50, box_y - 25, 100, 50), 3)
        
        # Draw players input values (red/blue swapped) - use text with white outline
        p1_x = red_x - font_large.render(str(self.player1.input_value), True, RED).get_width()//2
        p1_y = box_y - font_large.render(str(self.player1.input_value), True, RED).get_height()//2
        p2_x = blue_x - font_large.render(str(self.player2.input_value), True, BLUE).get_width()//2
        p2_y = box_y - font_large.render(str(self.player2.input_value), True, BLUE).get_height()//2
        
        draw_text_with_outline(screen, str(self.player2.input_value), font_large, BLUE, p2_x, p2_y)
        draw_text_with_outline(screen, str(self.player1.input_value), font_large, RED, p1_x, p1_y)
        
        # Blue player (left) - W ▲ [box] ▼ S layout, SPACE below
        # W outside above box
        w_label = font_small.render("W", True, BLUE)
        screen.blit(w_label, (blue_x - w_label.get_width()//2, box_y - 55))
        # Up triangle ▲ outside above box
        pygame.draw.polygon(screen, BLUE, [(blue_x, box_y - 40), (blue_x - 10, box_y - 30), (blue_x + 10, box_y - 30)])
        # Down triangle ▼ outside below box
        pygame.draw.polygon(screen, BLUE, [(blue_x, box_y + 40), (blue_x - 10, box_y + 30), (blue_x + 10, box_y + 30)])
        # S outside below box
        s_label = font_small.render("S", True, BLUE)
        screen.blit(s_label, (blue_x - s_label.get_width()//2, box_y + 45))
        # SPACE below
        space_hint_bottom = font_small.render("SPACE", True, (255, 255, 50))
        screen.blit(space_hint_bottom, (blue_x - space_hint_bottom.get_width()//2, box_y + 70))
        
        # Red player (right) - UP ▲ [box] ▼ DOWN layout, ENTER below
        # UP outside above box
        up_label = font_small.render("UP", True, RED)
        screen.blit(up_label, (red_x - up_label.get_width()//2, box_y - 55))
        # Up triangle ▲ outside above box
        pygame.draw.polygon(screen, RED, [(red_x, box_y - 40), (red_x - 10, box_y - 30), (red_x + 10, box_y - 30)])
        # Down triangle ▼ outside below box
        pygame.draw.polygon(screen, RED, [(red_x, box_y + 40), (red_x - 10, box_y + 30), (red_x + 10, box_y + 30)])
        # DOWN outside below box
        down_label = font_small.render("DOWN", True, RED)
        screen.blit(down_label, (red_x - down_label.get_width()//2, box_y + 45))
        # ENTER below
        enter_hint_bottom = font_small.render("ENTER", True, (255, 255, 50))
        screen.blit(enter_hint_bottom, (red_x - enter_hint_bottom.get_width()//2, box_y + 70))
        
        # Draw submission status - only show when results not displayed
        if not self.show_result:
            if self.player2.submitted:
                # Submission marker - no background, directly show text with outline
                submit_x = blue_x - font_small.render("Submitted!", True, BLUE).get_width()//2
                draw_text_with_outline(screen, "Submitted!", font_small, BLUE, submit_x, box_y - 90)
                
            if self.player1.submitted:
                # Submission marker - no background, directly show text with outline
                submit_x = red_x - font_small.render("Submitted!", True, RED).get_width()//2
                draw_text_with_outline(screen, "Submitted!", font_small, RED, submit_x, box_y - 90)
        
        # If showing results, display more detailed information
        if self.show_result:
            # Show correct answer - moved to higher position to avoid occlusion, use large font with white outline
            answer_x = SCREEN_WIDTH//2 - font_large.render(f"Answer: {self.correct_answer}", True, (255, 255, 50)).get_width()//2
            draw_text_with_outline(screen, f"Answer: {self.correct_answer}", font_large, (255, 255, 50), answer_x, 100)
            
            # Calculate scores
            p1_correct = self.player1.input_value == self.correct_answer
            p2_correct = self.player2.input_value == self.correct_answer
            
            # Show blue player result
            if p2_correct:
                score_gain = 10 if not self.player1.submitted or self.player2.submitted else 5
                score_text = font_large.render(f"+{score_gain}", True, (50, 255, 100))
                screen.blit(score_text, (blue_x - score_text.get_width()//2, box_y + 100))
            else:
                wrong_text = font_large.render("X", True, (255, 50, 50))
                screen.blit(wrong_text, (blue_x - wrong_text.get_width()//2, box_y + 100))
            
            # Show red player result
            if p1_correct:
                score_gain = 10 if not self.player2.submitted or self.player1.submitted else 5
                score_text = font_large.render(f"+{score_gain}", True, (50, 255, 100))
                screen.blit(score_text, (red_x - score_text.get_width()//2, box_y + 100))
            else:
                wrong_text = font_large.render("X", True, (255, 50, 50))
                screen.blit(wrong_text, (red_x - wrong_text.get_width()//2, box_y + 100))
            
            # Show current total score - moved to screen bottom, avoid character occlusion, use outlined text
            p2_total_x = blue_x - font_medium.render(f"Total: {self.player2.score}", True, BLUE).get_width()//2
            p1_total_x = red_x - font_medium.render(f"Total: {self.player1.score}", True, RED).get_width()//2
            draw_text_with_outline(screen, f"Total: {self.player2.score}", font_medium, BLUE, p2_total_x, SCREEN_HEIGHT - 60)
            draw_text_with_outline(screen, f"Total: {self.player1.score}", font_medium, RED, p1_total_x, SCREEN_HEIGHT - 60)
            
            # Show next level hint - use more vivid colors with white outline, larger font
            if self.level < 3:
                next_text_str = f"Next: Level {self.level+1}"
                next_x = SCREEN_WIDTH//2 - font_medium.render(next_text_str, True, (255, 200, 0)).get_width()//2
                draw_text_with_outline(screen, next_text_str, font_medium, (255, 200, 0), next_x, SCREEN_HEIGHT - 100)
            else:
                final_x = SCREEN_WIDTH//2 - font_medium.render("Final Results!", True, (255, 150, 255)).get_width()//2
                draw_text_with_outline(screen, "Final Results!", font_medium, (255, 150, 255), final_x, SCREEN_HEIGHT - 100)
        
        # If both players submitted but results not shown yet, display simple feedback
        elif self.player1.submitted and self.player2.submitted:
            # Show correct answer
            answer_text = font_medium.render(f"Answer: {self.correct_answer}", True, (255, 255, 50))
            screen.blit(answer_text, (SCREEN_WIDTH//2 - answer_text.get_width()//2, 60))
            
            # Calculate scores
            p1_correct = self.player1.input_value == self.correct_answer
            p2_correct = self.player2.input_value == self.correct_answer
            
            # Show blue player score
            if p2_correct:
                score_gain = 10 if not self.player1.submitted or self.player2.submitted else 5
                score_text = font_medium.render(f"+{score_gain}", True, (50, 255, 100))
                screen.blit(score_text, (blue_x - score_text.get_width()//2, box_y + 100))
            else:
                wrong_text = font_medium.render("X", True, (255, 50, 50))
                screen.blit(wrong_text, (blue_x - wrong_text.get_width()//2, box_y + 100))
            
            # Show red player score
            if p1_correct:
                score_gain = 10 if not self.player2.submitted or self.player1.submitted else 5
                score_text = font_medium.render(f"+{score_gain}", True, (50, 255, 100))
                screen.blit(score_text, (red_x - score_text.get_width()//2, box_y + 100))
            else:
                wrong_text = font_medium.render("X", True, (255, 50, 50))
                screen.blit(wrong_text, (red_x - wrong_text.get_width()//2, box_y + 100))
        
        # Advance animation and draw players
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
        
    def draw_result_screen(self):
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND)
        
        # Show correct answer
        answer_text = font_medium.render(f"Correct answer: {self.correct_answer}", True, BLACK)
        screen.blit(answer_text, (SCREEN_WIDTH//2 - answer_text.get_width()//2, 100))
        
        # Show player answers and scores
        p1_answer = font_small.render(f"Player 1: {self.player1.input_value}", True, RED)
        p2_answer = font_small.render(f"Player 2: {self.player2.input_value}", True, BLUE)
        # Red/blue positions swapped
        screen.blit(p2_answer, (SCREEN_WIDTH//4 - p2_answer.get_width()//2, 200))
        screen.blit(p1_answer, (SCREEN_WIDTH*3//4 - p1_answer.get_width()//2, 200))
        
        # Show score
        p1_score = font_small.render(f"Score: {self.player1.score}", True, RED)
        p2_score = font_small.render(f"Score: {self.player2.score}", True, BLUE)
        # Red/blue positions swapped
        screen.blit(p2_score, (SCREEN_WIDTH//4 - p2_score.get_width()//2, 250))
        screen.blit(p1_score, (SCREEN_WIDTH*3//4 - p1_score.get_width()//2, 250))
        
        # Show next level hint
        if self.level < 3:
            next_text = font_small.render(f"Next: Level {self.level+1}", True, BLACK)
            screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 350))
        else:
            next_text = font_small.render("Final Results!", True, BLACK)
            screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, 350))
        
    def draw_game_over(self):
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BACKGROUND)
        
        # Show Game Over title - rainbow gradient effect
        title_text = "GAME OVER!"
        title_colors = [(255, 100, 100), (255, 180, 100), (255, 220, 100), (100, 255, 150), 
                       (100, 200, 255), (180, 150, 255), (255, 150, 200), (255, 100, 150),
                       (255, 150, 100), (255, 200, 100), (200, 255, 100)]
        
        # Calculate total title width for centering
        title_width = sum(font_large.render(char, True, BLACK).get_width() for char in title_text)
        x_offset = SCREEN_WIDTH//2 - title_width//2
        
        # Draw colorful title (each character different color, with shadow)
        for i, char in enumerate(title_text):
            color = title_colors[i % len(title_colors)]
            # Shadow
            shadow = font_large.render(char, True, (60, 60, 60))
            screen.blit(shadow, (x_offset + 4, 84))
            # Main text
            char_surface = font_large.render(char, True, color)
            screen.blit(char_surface, (x_offset, 80))
            x_offset += char_surface.get_width()
        
        # Show final score - use outlined text and larger font
        # Blue player (left)
        blue_score_text = f"BLUE: {self.player2.score}"
        blue_score_x = SCREEN_WIDTH//4 - font_medium.render(blue_score_text, True, BLUE).get_width()//2
        draw_text_with_outline(screen, blue_score_text, font_medium, BLUE, blue_score_x, 200)
        
        # Red player (right)
        red_score_text = f"RED: {self.player1.score}"
        red_score_x = SCREEN_WIDTH*3//4 - font_medium.render(red_score_text, True, RED).get_width()//2
        draw_text_with_outline(screen, red_score_text, font_medium, RED, red_score_x, 200)
        
        # Show winner - use outlined text with larger more eye-catching style
        if self.player1.score > self.player2.score:
            winner_text = "RED WINS!"
            winner_color = RED
        elif self.player2.score > self.player1.score:
            winner_text = "BLUE WINS!"
            winner_color = BLUE
        else:
            winner_text = "IT'S A TIE!"
            winner_color = (255, 200, 0)  # Gold
        
        winner_x = SCREEN_WIDTH//2 - font_large.render(winner_text, True, winner_color).get_width()//2
        # Add extra shadow effect to make victory text more prominent
        for dx, dy in [(5, 5), (4, 4), (3, 3), (2, 2)]:
            shadow = font_large.render(winner_text, True, (80, 80, 80))
            screen.blit(shadow, (winner_x + dx, 285 + dy))
        draw_text_with_outline(screen, winner_text, font_large, winner_color, winner_x, 280)
        
        # Restart hint - use more obvious color
        restart_x = SCREEN_WIDTH//2 - font_small.render("Press SPACE to play again", True, (100, 255, 100)).get_width()//2
        draw_text_with_outline(screen, "Press SPACE to play again", font_small, (100, 255, 100), restart_x, 400, (50, 50, 50), 1)
        
        # Advance animation and draw players
        self.player1.animate()
        self.player2.animate()
        self.player1.draw(screen, SCREEN_HEIGHT - 60)
        self.player2.draw(screen, SCREEN_HEIGHT - 60)
    
    def draw_pause_screen(self):
        """Draw pause screen"""
        # Draw semi-transparent black overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw "PAUSED" title
        paused_text = font_large.render("PAUSED", True, (255, 255, 100))
        paused_x = SCREEN_WIDTH//2 - paused_text.get_width()//2
        # Add shadow
        shadow = font_large.render("PAUSED", True, (100, 100, 100))
        screen.blit(shadow, (paused_x + 4, 154))
        screen.blit(paused_text, (paused_x, 150))
        
        # Draw hint message
        hint1 = font_small.render("Press ESC to resume", True, (200, 200, 200))
        hint1_x = SCREEN_WIDTH//2 - hint1.get_width()//2
        screen.blit(hint1, (hint1_x, 250))
        
        # Show current level and scores
        level_text = font_small.render(f"Level {self.level}", True, (150, 200, 255))
        level_x = SCREEN_WIDTH//2 - level_text.get_width()//2
        screen.blit(level_text, (level_x, 320))
        
        score_text = font_small.render(f"RED: {self.player1.score}  BLUE: {self.player2.score}", True, (200, 200, 200))
        score_x = SCREEN_WIDTH//2 - score_text.get_width()//2
        screen.blit(score_text, (score_x, 360))
        
    def run(self):
        last_time = time.time()
        
        while True:
            # Calculate time delta
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # ESC key toggle pause
                        if self.state in [GameState.GAME_PLAY, GameState.INPUT_PHASE, GameState.COUNTDOWN]:
                            self.paused = not self.paused
                            if self.paused:
                                self.previous_state = self.state
                                self.state = GameState.PAUSED
                                pygame.mixer.music.pause()  # Pause music
                            else:
                                self.state = self.previous_state
                                pygame.mixer.music.unpause()  # Resume music
                        elif self.state == GameState.PAUSED:
                            self.paused = False
                            self.state = self.previous_state
                            pygame.mixer.music.unpause()
                        elif self.state in [GameState.START_SCREEN, GameState.GAME_OVER]:
                            pygame.quit()
                            sys.exit()
                    elif self.state == GameState.START_SCREEN and event.key == pygame.K_SPACE:
                        self.start_level()
                    elif self.state == GameState.GAME_OVER and event.key == pygame.K_SPACE:
                        # Reset game
                        self.__init__()
                        self.state = GameState.START_SCREEN
            
            # If paused, skip update
            if self.state == GameState.PAUSED:
                # Draw pause screen
                self.draw_pause_screen()
                pygame.display.flip()
                clock.tick(FPS)
                continue
            
            # Update game state
            if self.state == GameState.COUNTDOWN:
                self.update_countdown(dt)
            elif self.state == GameState.GAME_PLAY:
                self.update_gameplay()
            elif self.state == GameState.INPUT_PHASE:
                self.update_input_phase(events, dt)
            elif self.state == GameState.RESULT_SCREEN:
                self.update_result_screen(dt)
            
            # Draw game
            if self.state == GameState.START_SCREEN:
                self.draw_start_screen()
            elif self.state == GameState.COUNTDOWN:
                self.draw_countdown()
            elif self.state == GameState.GAME_PLAY:
                self.draw_gameplay()
            elif self.state == GameState.INPUT_PHASE:
                self.draw_input_phase()
            elif self.state == GameState.RESULT_SCREEN:
                self.draw_result_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            clock.tick(FPS)

# Run game
if __name__ == "__main__":
    try:
        game = ButterflyGame()
        game.run()
    except Exception as e:
        print(f"Game runtime error: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()