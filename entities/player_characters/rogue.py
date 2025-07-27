from .character import CharacterBase
import math
import random
import pygame
from config.constants import *

class Rogue(CharacterBase):
    """
    Rogue character class. Handles all drawing, animation, and stat logic unique to Rogue.
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
        # --- Full Rogue drawing code from monolithic Character class ---
        offset_x = self.animation_offset
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            offset_x = -5 * math.sin(self.attack_animation * 0.2)
                
        if self.hit_animation > 0:
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
        
        x = self.x + offset_x
        y = self.y + offset_y
        
        # Draw shadow first
        pygame.draw.ellipse(surface, (0, 0, 0), (x + 2, y + 50, PLAYER_SIZE - 4, 8))
        
        # Draw character outline for better visibility
        outline_points = [
            (x + 2, y + 8), (x + PLAYER_SIZE - 2, y + 8),  # Top
            (x + PLAYER_SIZE, y + 15), (x + PLAYER_SIZE, y + 35),  # Right
            (x + PLAYER_SIZE - 2, y + 45), (x + 2, y + 45),  # Bottom
            (x, y + 35), (x, y + 15)  # Left
        ]
        pygame.draw.polygon(surface, (0, 0, 0), outline_points, 2)
        
        # Stealthy Assassin - Dark and mysterious
        # Leather armor (dark and sleek)
        armor_color = (40, 40, 40)  # Dark gray
        armor_highlight = (80, 80, 80)  # Light gray
        armor_shadow = (20, 20, 20)  # Very dark gray
        armor_detail = (60, 60, 60)  # Medium gray
        
        # Main armor (sleek and form-fitting)
        armor_points = [
            (x + 4, y + 16), (x + PLAYER_SIZE - 4, y + 16),  # Top
            (x + PLAYER_SIZE - 2, y + 20), (x + PLAYER_SIZE, y + 28),  # Right curve
            (x + PLAYER_SIZE - 2, y + 36), (x + 2, y + 36),  # Bottom
            (x, y + 28), (x + 2, y + 20)  # Left curve
        ]
        pygame.draw.polygon(surface, armor_color, armor_points)
        pygame.draw.polygon(surface, armor_highlight, [
            (x + 6, y + 18), (x + PLAYER_SIZE - 6, y + 18),
            (x + PLAYER_SIZE - 8, y + 24), (x + 8, y + 24)
        ])
        pygame.draw.polygon(surface, armor_shadow, [
            (x + 4, y + 16), (x + 2, y + 20), (x, y + 28),
            (x + 2, y + 36), (x + 4, y + 36)
        ])
        
        # Armor details (straps and buckles)
        for i in range(3):
            strap_x = x + 8 + i * 8
            strap_y = y + 22
            pygame.draw.rect(surface, armor_detail, (strap_x, strap_y, 4, 2))
            pygame.draw.rect(surface, armor_highlight, (strap_x + 1, strap_y + 1, 2, 1))
            # Buckles
            pygame.draw.rect(surface, (139, 69, 19), (strap_x + 1, strap_y - 1, 2, 4))
            pygame.draw.rect(surface, (160, 82, 45), (strap_x + 1, strap_y, 2, 2))
        
        # Leather straps and buckles
        for i in range(2):
            strap_x = x + 10 + i * 12
            strap_y = y + 22
            pygame.draw.rect(surface, armor_detail, (strap_x, strap_y, 8, 2))
            pygame.draw.rect(surface, (60, 60, 60), (strap_x + 2, strap_y, 4, 2))
        
        # Head (hidden and mysterious)
        head_center_x = x + PLAYER_SIZE // 2
        head_center_y = y + 10
        # Head shadow
        pygame.draw.circle(surface, (180, 140, 100), (head_center_x + 1, head_center_y + 1), 8)
        # Head base (smaller, more hidden)
        pygame.draw.ellipse(surface, (240, 200, 150), (head_center_x - 7, head_center_y - 5, 14, 16))
        # Head highlight
        pygame.draw.ellipse(surface, (255, 220, 180), (head_center_x - 5, head_center_y - 3, 10, 12))
        # Head outline
        pygame.draw.ellipse(surface, (200, 150, 100), (head_center_x - 7, head_center_y - 5, 14, 16), 1)
        
        # Dark hood (mysterious)
        hood_color = (20, 20, 20)  # Very dark
        hood_highlight = (40, 40, 40)
        hood_points = [
            (head_center_x - 8, head_center_y - 5), (head_center_x + 8, head_center_y - 5),
            (head_center_x + 10, head_center_y - 7), (head_center_x + 8, head_center_y - 11),
            (head_center_x + 4, head_center_y - 15), (head_center_x, head_center_y - 17),
            (head_center_x - 4, head_center_y - 15), (head_center_x - 8, head_center_y - 11),
            (head_center_x - 10, head_center_y - 7)
        ]
        pygame.draw.polygon(surface, hood_color, hood_points)
        pygame.draw.polygon(surface, hood_highlight, [
            (head_center_x - 6, head_center_y - 7), (head_center_x + 6, head_center_y - 7),
            (head_center_x + 8, head_center_y - 9), (head_center_x + 6, head_center_y - 13),
            (head_center_x + 2, head_center_y - 15), (head_center_x - 2, head_center_y - 15),
            (head_center_x - 6, head_center_y - 13), (head_center_x - 8, head_center_y - 9)
        ])
        
        # Hood stitching (stealth details)
        for i in range(3):
            stitch_x = head_center_x - 5 + i * 5
            stitch_y = head_center_y - 9
            pygame.draw.line(surface, (10, 10, 10), (stitch_x, stitch_y), (stitch_x, stitch_y + 2), 1)
        
        # Eyes (hidden in shadow, mysterious)
        pygame.draw.ellipse(surface, (10, 10, 10), (head_center_x - 4, head_center_y - 2, 5, 3))
        pygame.draw.ellipse(surface, (10, 10, 10), (head_center_x - 1, head_center_y - 2, 5, 3))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 3, head_center_y - 3, 2, 2))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x, head_center_y - 3, 2, 2))
        pygame.draw.circle(surface, (0, 255, 0), (head_center_x - 2, head_center_y - 1), 1)  # Green eyes
        pygame.draw.circle(surface, (0, 255, 0), (head_center_x + 1, head_center_y - 1), 1)
        pygame.draw.ellipse(surface, (255, 255, 0), (head_center_x - 1, head_center_y - 2, 4, 3))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 2, head_center_y - 3, 2, 2))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x, head_center_y - 3, 2, 2))
        pygame.draw.circle(surface, (0, 0, 0), (head_center_x - 1, head_center_y - 1), 1)
        pygame.draw.circle(surface, (0, 0, 0), (head_center_x + 1, head_center_y - 1), 1)
        
        # Daggers with enhanced detail
        dagger_offset = 0
        if self.attack_animation > 0:
            dagger_offset = -15 * (1 - self.attack_animation / 10)
        
        # Left dagger (curved blade)
        left_dagger_points = [
            (x + 18 + dagger_offset, y + 22), (x + 22 + dagger_offset, y + 18),
            (x + 25 + dagger_offset, y + 20), (x + 26 + dagger_offset, y + 22),
            (x + 25 + dagger_offset, y + 24), (x + 22 + dagger_offset, y + 22)
        ]
        pygame.draw.polygon(surface, (200, 200, 220), left_dagger_points)
        pygame.draw.polygon(surface, (180, 180, 200), left_dagger_points, 1)
        # Dagger handle (wrapped)
        pygame.draw.rect(surface, (120, 80, 40), (x + 20 + dagger_offset, y + 22, 4, 6))
        for i in range(2):
            pygame.draw.line(surface, (100, 60, 20), (x + 20 + dagger_offset, y + 24 + i*2), (x + 24 + dagger_offset, y + 24 + i*2), 1)
        
        # Right dagger (curved blade)
        right_dagger_points = [
            (x + PLAYER_SIZE - 18 - dagger_offset, y + 22), (x + PLAYER_SIZE - 22 - dagger_offset, y + 18),
            (x + PLAYER_SIZE - 25 - dagger_offset, y + 20), (x + PLAYER_SIZE - 26 - dagger_offset, y + 22),
            (x + PLAYER_SIZE - 25 - dagger_offset, y + 24), (x + PLAYER_SIZE - 22 - dagger_offset, y + 22)
        ]
        pygame.draw.polygon(surface, (200, 200, 220), right_dagger_points)
        pygame.draw.polygon(surface, (180, 180, 200), right_dagger_points, 1)
        # Dagger handle (wrapped)
        pygame.draw.rect(surface, (120, 80, 40), (x + PLAYER_SIZE - 24 - dagger_offset, y + 22, 4, 6))
        for i in range(2):
            pygame.draw.line(surface, (100, 60, 20), (x + PLAYER_SIZE - 24 - dagger_offset, y + 24 + i*2), (x + PLAYER_SIZE - 20 - dagger_offset, y + 24 + i*2), 1)
        
        # Arms with organic shape
        arm_color = (100, 0, 0)
        arm_highlight = (140, 0, 0)
        arm_shadow = (80, 0, 0)
        
        # Left arm (curved)
        left_arm_points = [
            (x + 2, y + 25), (x + 8, y + 25), (x + 10, y + 28), (x + 8, y + 35), (x + 2, y + 35)
        ]
        pygame.draw.polygon(surface, arm_color, left_arm_points)
        pygame.draw.polygon(surface, arm_highlight, [(x + 3, y + 26), (x + 7, y + 26), (x + 9, y + 28), (x + 7, y + 33), (x + 3, y + 33)])
        
        # Right arm (curved)
        right_arm_points = [
            (x + PLAYER_SIZE - 2, y + 25), (x + PLAYER_SIZE - 8, y + 25),
            (x + PLAYER_SIZE - 10, y + 28), (x + PLAYER_SIZE - 8, y + 35), (x + PLAYER_SIZE - 2, y + 35)
        ]
        pygame.draw.polygon(surface, arm_color, right_arm_points)
        pygame.draw.polygon(surface, arm_highlight, [(x + PLAYER_SIZE - 3, y + 26), (x + PLAYER_SIZE - 7, y + 26), (x + PLAYER_SIZE - 9, y + 28), (x + PLAYER_SIZE - 7, y + 33), (x + PLAYER_SIZE - 3, y + 33)])
        
        # Legs with organic shape
        leg_color = (80, 0, 0)
        leg_highlight = (120, 0, 0)
        leg_shadow = (60, 0, 0)
        
        # Left leg (curved)
        left_leg_points = [
            (x + 6, y + 35), (x + 14, y + 35), (x + 15, y + 38), (x + 14, y + 45), (x + 6, y + 45)
        ]
        pygame.draw.polygon(surface, leg_color, left_leg_points)
        pygame.draw.polygon(surface, leg_highlight, [(x + 7, y + 36), (x + 13, y + 36), (x + 14, y + 38), (x + 13, y + 43), (x + 7, y + 43)])
        
        # Right leg (curved)
        right_leg_points = [
            (x + PLAYER_SIZE - 14, y + 35), (x + PLAYER_SIZE - 6, y + 35),
            (x + PLAYER_SIZE - 5, y + 38), (x + PLAYER_SIZE - 6, y + 45), (x + PLAYER_SIZE - 14, y + 45)
        ]
        pygame.draw.polygon(surface, leg_color, right_leg_points)
        pygame.draw.polygon(surface, leg_highlight, [(x + PLAYER_SIZE - 13, y + 36), (x + PLAYER_SIZE - 7, y + 36), (x + PLAYER_SIZE - 6, y + 38), (x + PLAYER_SIZE - 7, y + 43), (x + PLAYER_SIZE - 13, y + 43)])
        
        # Belt with buckle
        pygame.draw.rect(surface, (40, 40, 40), (x + 2, y + 35, PLAYER_SIZE - 4, 3))
        # Belt buckle
        buckle_x = x + PLAYER_SIZE // 2 - 3
        buckle_y = y + 35
        pygame.draw.rect(surface, (80, 80, 80), (buckle_x, buckle_y, 6, 3))
        pygame.draw.rect(surface, (120, 120, 120), (buckle_x + 1, buckle_y + 1, 4, 1))

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