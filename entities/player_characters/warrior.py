from .character import CharacterBase
import math
import random
import pygame
from config.constants import *

class Warrior(CharacterBase):
    """
    Warrior character class. Handles all drawing, animation, and stat logic unique to Warrior.
    """
    def __init__(self, base_character):
        self.__dict__.update(base_character.__dict__)

    def update_animation(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * 0.005) * 2
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1

    def draw(self, surface):
        # --- Full Warrior drawing code from monolithic Character class ---
        offset_x = self.animation_offset
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            offset_x = 5 * math.sin(self.attack_animation * 0.2)
                
        if self.hit_animation > 0:
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
        
        x = self.x + offset_x
        y = self.y + offset_y
        
        # Draw shadow first
        pygame.draw.ellipse(surface, (0, 0, 0), (x + 2, y + 45, PLAYER_SIZE - 4, 8))
        
        # Draw character outline for better visibility
        outline_points = [
            (x + 2, y + 8), (x + PLAYER_SIZE - 2, y + 8),  # Top
            (x + PLAYER_SIZE, y + 15), (x + PLAYER_SIZE, y + 35),  # Right
            (x + PLAYER_SIZE - 2, y + 45), (x + 2, y + 45),  # Bottom
            (x, y + 35), (x, y + 15)  # Left
        ]
        pygame.draw.polygon(surface, (0, 0, 0), outline_points, 2)
        
        # Paladin - Noble and righteous
        # Torso (armored and noble)
        torso_color = (192, 192, 192)  # Silver armor
        torso_highlight = (220, 220, 220)  # Bright silver
        torso_shadow = (160, 160, 160)  # Dark silver
        
        # Main torso (armored)
        torso_points = [
            (x + 6, y + 10), (x + PLAYER_SIZE - 6, y + 10),  # Top
            (x + PLAYER_SIZE - 4, y + 18), (x + PLAYER_SIZE - 2, y + 30),  # Right curve
            (x + PLAYER_SIZE - 4, y + 38), (x + 4, y + 38),  # Bottom
            (x + 2, y + 30), (x + 4, y + 18)  # Left curve
        ]
        pygame.draw.polygon(surface, torso_color, torso_points)
        pygame.draw.polygon(surface, torso_highlight, [
            (x + 8, y + 12), (x + PLAYER_SIZE - 8, y + 12),
            (x + PLAYER_SIZE - 10, y + 20), (x + 10, y + 20)
        ])
        pygame.draw.polygon(surface, torso_shadow, [
            (x + 6, y + 10), (x + 4, y + 18), (x + 2, y + 30),
            (x + 4, y + 38), (x + 6, y + 38)
        ])
        
        # Armor plates and details
        # Chest plate
        pygame.draw.ellipse(surface, (160, 160, 160), (x + 10, y + 14, PLAYER_SIZE - 20, 12))
        pygame.draw.ellipse(surface, (180, 180, 180), (x + 11, y + 15, PLAYER_SIZE - 22, 10))
        # Armor trim
        pygame.draw.ellipse(surface, (139, 69, 19), (x + 8, y + 8, PLAYER_SIZE - 16, 8))
        pygame.draw.ellipse(surface, (160, 82, 45), (x + 10, y + 9, PLAYER_SIZE - 20, 6))
        # Belt
        pygame.draw.ellipse(surface, (139, 69, 19), (x + 6, y + 32, PLAYER_SIZE - 12, 6))
        pygame.draw.ellipse(surface, (160, 82, 45), (x + 8, y + 33, PLAYER_SIZE - 16, 4))
        
        # Head (noble and righteous)
        head_center_x = x + PLAYER_SIZE // 2
        head_center_y = y + 8
        # Head shadow
        pygame.draw.circle(surface, (180, 140, 100), (head_center_x + 1, head_center_y + 1), 10)
        # Head base (noble)
        pygame.draw.ellipse(surface, (240, 200, 150), (head_center_x - 10, head_center_y - 8, 20, 22))
        # Head highlight
        pygame.draw.ellipse(surface, (255, 220, 180), (head_center_x - 8, head_center_y - 6, 16, 18))
        # Head outline
        pygame.draw.ellipse(surface, (200, 150, 100), (head_center_x - 10, head_center_y - 8, 20, 22), 1)
        
        # Noble hair (flowing and well-groomed)
        hair_color = (139, 69, 19)  # Brown
        hair_highlight = (160, 82, 45)
        # Hair base
        pygame.draw.ellipse(surface, hair_color, (head_center_x - 8, head_center_y - 6, 16, 8))
        pygame.draw.ellipse(surface, hair_highlight, (head_center_x - 6, head_center_y - 5, 12, 6))
        # Flowing hair strands
        hair_strands = [
            (head_center_x - 6, head_center_y - 6), (head_center_x - 4, head_center_y - 10),
            (head_center_x - 2, head_center_y - 8), (head_center_x, head_center_y - 12),
            (head_center_x + 2, head_center_y - 10), (head_center_x + 4, head_center_y - 12),
            (head_center_x + 6, head_center_y - 8)
        ]
        for i in range(len(hair_strands) - 1):
            pygame.draw.line(surface, hair_color, hair_strands[i], hair_strands[i+1], 2)
        
        # Noble eyes (determined and righteous)
        pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x - 6, head_center_y - 2, 4, 3))
        pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x + 2, head_center_y - 2, 4, 3))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 5, head_center_y - 3, 2, 2))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x + 3, head_center_y - 3, 2, 2))
        pygame.draw.circle(surface, (0, 150, 255), (head_center_x - 4, head_center_y - 1), 1)  # Blue eyes
        pygame.draw.circle(surface, (0, 150, 255), (head_center_x + 4, head_center_y - 1), 1)
        
        # Noble features
        pygame.draw.ellipse(surface, (220, 180, 140), (head_center_x - 1, head_center_y + 1, 2, 3))  # Nose
        
        # Noble beard (well-groomed)
        beard_points = [
            (head_center_x - 4, head_center_y + 4), (head_center_x - 6, head_center_y + 8),
            (head_center_x - 4, head_center_y + 12), (head_center_x, head_center_y + 14),
            (head_center_x + 4, head_center_y + 12), (head_center_x + 6, head_center_y + 8),
            (head_center_x + 4, head_center_y + 4)
        ]
        pygame.draw.polygon(surface, hair_color, beard_points)
        pygame.draw.polygon(surface, hair_highlight, [
            (head_center_x - 2, head_center_y + 6), (head_center_x - 4, head_center_y + 10),
            (head_center_x, head_center_y + 12), (head_center_x + 4, head_center_y + 10),
            (head_center_x + 2, head_center_y + 6)
        ])
        
        # Arms (armored)
        arm_color = (192, 192, 192)  # Silver armor
        arm_highlight = (220, 220, 220)  # Bright silver
        arm_shadow = (160, 160, 160)  # Dark silver
        
        # Left arm (armored)
        left_arm_points = [
            (x + 2, y + 16), (x + 10, y + 16), (x + 12, y + 20), (x + 10, y + 32), (x + 2, y + 32)
        ]
        pygame.draw.polygon(surface, arm_color, left_arm_points)
        pygame.draw.polygon(surface, arm_highlight, [(x + 3, y + 17), (x + 9, y + 17), (x + 10, y + 20), (x + 9, y + 30), (x + 3, y + 30)])
        # Armor details
        pygame.draw.ellipse(surface, (160, 160, 160), (x + 3, y + 20, 8, 6))
        pygame.draw.ellipse(surface, (180, 180, 180), (x + 4, y + 21, 6, 4))
        
        # Right arm (armored)
        right_arm_points = [
            (x + PLAYER_SIZE - 2, y + 16), (x + PLAYER_SIZE - 10, y + 16), 
            (x + PLAYER_SIZE - 12, y + 20), (x + PLAYER_SIZE - 10, y + 32), (x + PLAYER_SIZE - 2, y + 32)
        ]
        pygame.draw.polygon(surface, arm_color, right_arm_points)
        pygame.draw.polygon(surface, arm_highlight, [(x + PLAYER_SIZE - 3, y + 17), (x + PLAYER_SIZE - 9, y + 17), (x + PLAYER_SIZE - 10, y + 20), (x + PLAYER_SIZE - 9, y + 30), (x + PLAYER_SIZE - 3, y + 30)])
        # Armor details
        pygame.draw.ellipse(surface, (160, 160, 160), (x + PLAYER_SIZE - 11, y + 20, 8, 6))
        pygame.draw.ellipse(surface, (180, 180, 180), (x + PLAYER_SIZE - 12, y + 21, 6, 4))
        
        # Holy Sword (noble and righteous)
        sword_offset = 0
        if self.attack_animation > 0:
            sword_offset = -12 * (1 - self.attack_animation / 10)
        
        # Sword handle (ornate)
        pygame.draw.rect(surface, (139, 69, 19), (x + 32 + sword_offset, y + 16, 4, 10))
        pygame.draw.rect(surface, (160, 82, 45), (x + 33 + sword_offset, y + 17, 2, 8))
        # Handle grip
        pygame.draw.rect(surface, (101, 67, 33), (x + 33 + sword_offset, y + 20, 2, 4))
        pygame.draw.rect(surface, (139, 69, 19), (x + 33 + sword_offset, y + 21, 2, 2))
        
        # Sword guard (ornate cross)
        guard_points = [
            (x + 28 + sword_offset, y + 18), (x + 40 + sword_offset, y + 18),
            (x + 39 + sword_offset, y + 20), (x + 29 + sword_offset, y + 20)
        ]
        pygame.draw.polygon(surface, (192, 192, 192), guard_points)
        pygame.draw.polygon(surface, (220, 220, 220), [
            (x + 29 + sword_offset, y + 18), (x + 39 + sword_offset, y + 18),
            (x + 38 + sword_offset, y + 19), (x + 30 + sword_offset, y + 19)
        ])
        # Cross detail
        pygame.draw.rect(surface, (160, 160, 160), (x + 32 + sword_offset, y + 16, 4, 4))
        pygame.draw.rect(surface, (180, 180, 180), (x + 33 + sword_offset, y + 17, 2, 2))
        
        # Sword blade (holy and gleaming)
        blade_points = [
            (x + 30 + sword_offset, y + 12), (x + 34 + sword_offset, y + 12),
            (x + 35 + sword_offset, y + 18), (x + 34 + sword_offset, y + 24),
            (x + 30 + sword_offset, y + 24)
        ]
        pygame.draw.polygon(surface, (220, 220, 240), blade_points)
        pygame.draw.polygon(surface, (180, 180, 200), blade_points, 1)
        # Blade edge
        pygame.draw.line(surface, (255, 255, 255), (x + 30 + sword_offset, y + 12), (x + 34 + sword_offset, y + 12), 2)
        
        # Sword tip (pointed)
        pygame.draw.polygon(surface, (200, 200, 220), [
            (x + 30 + sword_offset, y + 12), (x + 36 + sword_offset, y + 6),
            (x + 32 + sword_offset, y + 12)
        ])
        pygame.draw.polygon(surface, (220, 220, 240), [
            (x + 30 + sword_offset, y + 12), (x + 34 + sword_offset, y + 8),
            (x + 32 + sword_offset, y + 12)
        ])
        
        # Holy glow effect
        glow_points = [
            (x + 32 + sword_offset, y + 8), (x + 34 + sword_offset, y + 8),
            (x + 35 + sword_offset, y + 10), (x + 34 + sword_offset, y + 12),
            (x + 32 + sword_offset, y + 12)
        ]
        pygame.draw.polygon(surface, (255, 255, 200), glow_points)
        pygame.draw.polygon(surface, (255, 255, 255), [
            (x + 32 + sword_offset, y + 9), (x + 34 + sword_offset, y + 9),
            (x + 34 + sword_offset, y + 11), (x + 32 + sword_offset, y + 11)
        ])
        
        # Legs (armored)
        leg_color = (192, 192, 192)  # Silver armor
        leg_highlight = (220, 220, 220)  # Bright silver
        leg_shadow = (160, 160, 160)  # Dark silver
        
        # Left leg (armored)
        left_leg_points = [
            (x + 6, y + 38), (x + 16, y + 38), (x + 17, y + 42), (x + 16, y + 50), (x + 6, y + 50)
        ]
        pygame.draw.polygon(surface, leg_color, left_leg_points)
        pygame.draw.polygon(surface, leg_highlight, [(x + 7, y + 39), (x + 15, y + 39), (x + 16, y + 42), (x + 15, y + 48), (x + 7, y + 48)])
        # Armor details
        pygame.draw.ellipse(surface, (160, 160, 160), (x + 7, y + 44, 10, 6))
        pygame.draw.ellipse(surface, (180, 180, 180), (x + 8, y + 45, 8, 4))
        
        # Right leg (armored)
        right_leg_points = [
            (x + PLAYER_SIZE - 6, y + 38), (x + PLAYER_SIZE - 16, y + 38), 
            (x + PLAYER_SIZE - 17, y + 42), (x + PLAYER_SIZE - 16, y + 50), (x + PLAYER_SIZE - 6, y + 50)
        ]
        pygame.draw.polygon(surface, leg_color, right_leg_points)
        pygame.draw.polygon(surface, leg_highlight, [(x + PLAYER_SIZE - 7, y + 39), (x + PLAYER_SIZE - 15, y + 39), (x + PLAYER_SIZE - 16, y + 42), (x + PLAYER_SIZE - 15, y + 48), (x + PLAYER_SIZE - 7, y + 48)])
        # Armor details
        pygame.draw.ellipse(surface, (160, 160, 160), (x + PLAYER_SIZE - 17, y + 44, 10, 6))
        pygame.draw.ellipse(surface, (180, 180, 180), (x + PLAYER_SIZE - 18, y + 45, 8, 4))

    def draw_stats(self, surface, x, y):
        from .character_animation import draw_stats
        draw_stats(self, surface, x, y)

    def start_attack_animation(self):
        self.attack_animation = 10

    def start_hit_animation(self):
        self.hit_animation = 5

    def move(self, dx, dy):
        new_x = self.x + dx * GRID_SIZE
        new_y = self.y + dy * GRID_SIZE
        
        # Check world boundaries (0 to WORLD_WIDTH/HEIGHT)
        if 0 <= new_x < WORLD_WIDTH:
            self.x = new_x
        if 0 <= new_y < WORLD_HEIGHT:
            self.y = new_y 