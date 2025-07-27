from .character import CharacterBase
import math
import random
import pygame
from config.constants import *

class Mage(CharacterBase):
    """
    Mage character class. Handles all drawing, animation, and stat logic unique to Mage.
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
        # --- Full Mage drawing code from monolithic Character class ---
        offset_x = self.animation_offset
        offset_y = self.animation_offset
        
        if self.attack_animation > 0:
            offset_y -= 5 * (1 - self.attack_animation / 10)
                
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
        
        # Mystical Elementalist - Ethereal and otherworldly
        # Robe (flowing and ethereal)
        robe_color = (75, 0, 130)  # Deep purple
        robe_highlight = (138, 43, 226)  # Bright purple
        robe_shadow = (47, 0, 82)  # Dark purple
        robe_detail = (147, 112, 219)  # Medium purple
        
        # Main robe (flowing and mystical)
        robe_points = [
            (x + 4, y + 16), (x + PLAYER_SIZE - 4, y + 16),  # Top
            (x + PLAYER_SIZE - 2, y + 20), (x + PLAYER_SIZE, y + 28),  # Right curve
            (x + PLAYER_SIZE - 2, y + 36), (x + 2, y + 36),  # Bottom
            (x, y + 28), (x + 2, y + 20)  # Left curve
        ]
        pygame.draw.polygon(surface, robe_color, robe_points)
        pygame.draw.polygon(surface, robe_highlight, [
            (x + 6, y + 18), (x + PLAYER_SIZE - 6, y + 18),
            (x + PLAYER_SIZE - 8, y + 24), (x + 8, y + 24)
        ])
        pygame.draw.polygon(surface, robe_shadow, [
            (x + 4, y + 16), (x + 2, y + 20), (x, y + 28),
            (x + 2, y + 36), (x + 4, y + 36)
        ])
        
        # Mystical symbols and runes
        for i in range(4):
            rune_x = x + 10 + i * 6
            rune_y = y + 22
            # Star symbols
            star_points = [
                (rune_x, rune_y - 2), (rune_x + 1, rune_y), (rune_x + 2, rune_y - 2),
                (rune_x, rune_y + 2), (rune_x - 1, rune_y), (rune_x - 2, rune_y + 2)
            ]
            pygame.draw.polygon(surface, robe_detail, star_points)
            pygame.draw.polygon(surface, robe_highlight, [
                (rune_x, rune_y - 1), (rune_x + 1, rune_y), (rune_x + 1, rune_y - 1),
                (rune_x, rune_y + 1), (rune_x - 1, rune_y), (rune_x - 1, rune_y + 1)
            ])
        
        # Head (ethereal and mystical)
        head_center_x = x + PLAYER_SIZE // 2
        head_center_y = y + 10
        # Head shadow
        pygame.draw.circle(surface, (180, 140, 100), (head_center_x + 1, head_center_y + 1), 9)
        # Head base (slightly smaller, more ethereal)
        pygame.draw.ellipse(surface, (240, 200, 150), (head_center_x - 8, head_center_y - 6, 16, 18))
        # Head highlight
        pygame.draw.ellipse(surface, (255, 220, 180), (head_center_x - 6, head_center_y - 4, 12, 14))
        # Head outline
        pygame.draw.ellipse(surface, (200, 150, 100), (head_center_x - 8, head_center_y - 6, 16, 18), 1)
        
        # Mystical eyes (glowing)
        pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x - 5, head_center_y - 2, 4, 3))
        pygame.draw.ellipse(surface, (50, 50, 50), (head_center_x + 1, head_center_y - 2, 4, 3))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x - 4, head_center_y - 3, 2, 2))
        pygame.draw.ellipse(surface, (255, 255, 255), (head_center_x + 2, head_center_y - 3, 2, 2))
        pygame.draw.circle(surface, (138, 43, 226), (head_center_x - 3, head_center_y - 1), 1)  # Purple eyes
        pygame.draw.circle(surface, (138, 43, 226), (head_center_x + 3, head_center_y - 1), 1)
        
        # Mystical hood (flowing)
        hood_color = (47, 0, 82)  # Dark purple
        hood_highlight = (75, 0, 130)
        hood_points = [
            (head_center_x - 8, head_center_y - 6), (head_center_x + 8, head_center_y - 6),
            (head_center_x + 10, head_center_y - 8), (head_center_x + 8, head_center_y - 12),
            (head_center_x + 4, head_center_y - 16), (head_center_x, head_center_y - 18),
            (head_center_x - 4, head_center_y - 16), (head_center_x - 8, head_center_y - 12),
            (head_center_x - 10, head_center_y - 8)
        ]
        pygame.draw.polygon(surface, hood_color, hood_points)
        pygame.draw.polygon(surface, hood_highlight, [
            (head_center_x - 6, head_center_y - 8), (head_center_x + 6, head_center_y - 8),
            (head_center_x + 8, head_center_y - 10), (head_center_x + 6, head_center_y - 14),
            (head_center_x + 2, head_center_y - 16), (head_center_x - 2, head_center_y - 16),
            (head_center_x - 6, head_center_y - 14), (head_center_x - 8, head_center_y - 10)
        ])
        
        # Mystical beard (ethereal wisps)
        beard_wisps = [
            (head_center_x - 4, head_center_y + 4), (head_center_x - 6, head_center_y + 8),
            (head_center_x - 4, head_center_y + 12), (head_center_x - 2, head_center_y + 16),
            (head_center_x + 2, head_center_y + 16), (head_center_x + 4, head_center_y + 12),
            (head_center_x + 6, head_center_y + 8), (head_center_x + 4, head_center_y + 4)
        ]
        # Draw individual wisps
        for i in range(len(beard_wisps) - 1):
            pygame.draw.line(surface, (147, 112, 219), beard_wisps[i], beard_wisps[i+1], 2)
        # Beard base
        pygame.draw.ellipse(surface, (138, 43, 226), (head_center_x - 4, head_center_y + 4, 8, 8))
        pygame.draw.ellipse(surface, (147, 112, 219), (head_center_x - 3, head_center_y + 5, 6, 6))
        
        # Arms with flowing sleeves
        hat_offset = 0
        if self.attack_animation > 0:
            hat_offset = -5 * (1 - self.attack_animation / 10)
        
        hat_color = (80, 40, 160)
        hat_highlight = (120, 60, 200)
        hat_shadow = (60, 30, 120)
        hat_detail = (100, 50, 180)
        
        # Hat base (curved)
        hat_base_points = [
            (head_center_x - 12, head_center_y - 5 + hat_offset),
            (head_center_x + 12, head_center_y - 5 + hat_offset),
            (head_center_x + 10, head_center_y - 2 + hat_offset),
            (head_center_x - 10, head_center_y - 2 + hat_offset)
        ]
        pygame.draw.polygon(surface, hat_color, hat_base_points)
        pygame.draw.polygon(surface, hat_highlight, [
            (head_center_x - 10, head_center_y - 4 + hat_offset),
            (head_center_x + 10, head_center_y - 4 + hat_offset),
            (head_center_x + 8, head_center_y - 2 + hat_offset),
            (head_center_x - 8, head_center_y - 2 + hat_offset)
        ])
        
        # Hat point (curved)
        hat_point_points = [
            (head_center_x, head_center_y - 15 + hat_offset),
            (head_center_x - 8, head_center_y - 5 + hat_offset),
            (head_center_x - 6, head_center_y - 8 + hat_offset),
            (head_center_x, head_center_y - 12 + hat_offset),
            (head_center_x + 6, head_center_y - 8 + hat_offset),
            (head_center_x + 8, head_center_y - 5 + hat_offset)
        ]
        pygame.draw.polygon(surface, hat_color, hat_point_points)
        pygame.draw.polygon(surface, hat_highlight, [
            (head_center_x, head_center_y - 15 + hat_offset),
            (head_center_x - 4, head_center_y - 8 + hat_offset),
            (head_center_x, head_center_y - 11 + hat_offset),
            (head_center_x + 4, head_center_y - 8 + hat_offset)
        ])
        
        # Hat details (stars)
        for i in range(3):
            star_x = head_center_x - 8 + i * 8
            star_y = head_center_y - 3 + hat_offset
            pygame.draw.circle(surface, hat_detail, (star_x, star_y), 1)
        
        # Staff with enhanced magical glow
        staff_top_offset = 0
        if self.attack_animation > 0:
            staff_top_offset = -10 * (1 - self.attack_animation / 10)
        
        # Staff shaft (curved)
        staff_points = [
            (x + 12, y + 12), (x + 14, y + 20), (x + 12, y + 28), (x + 10, y + 36), (x + 12, y + PLAYER_SIZE)
        ]
        for i in range(len(staff_points) - 1):
            pygame.draw.line(surface, (120, 80, 40), staff_points[i], staff_points[i + 1], 4)
        
        # Staff orb with enhanced glow effect
        orb_x = x + 12
        orb_y = y + 12 + staff_top_offset
        # Outer glow
        pygame.draw.circle(surface, (80, 80, 255), (orb_x, orb_y), 10)
        # Main orb
        pygame.draw.circle(surface, (100, 100, 255), (orb_x, orb_y), 8)
        pygame.draw.circle(surface, (150, 150, 255), (orb_x, orb_y), 5)
        pygame.draw.circle(surface, (200, 200, 255), (orb_x, orb_y), 2)
        # Orb highlight
        pygame.draw.circle(surface, (255, 255, 255), (orb_x - 2, orb_y - 2), 1)
        
        # Arms with flowing sleeves (mystical)
        arm_color = (75, 0, 130)  # Deep purple
        arm_highlight = (138, 43, 226)  # Bright purple
        arm_shadow = (47, 0, 82)  # Dark purple
        
        # Left arm (flowing sleeves)
        left_arm_points = [
            (x + 2, y + 20), (x + 10, y + 20), (x + 12, y + 24), (x + 10, y + 32), (x + 2, y + 32)
        ]
        pygame.draw.polygon(surface, arm_color, left_arm_points)
        pygame.draw.polygon(surface, arm_highlight, [(x + 3, y + 21), (x + 9, y + 21), (x + 10, y + 24), (x + 9, y + 30), (x + 3, y + 30)])
        # Sleeve details
        pygame.draw.ellipse(surface, robe_detail, (x + 3, y + 24, 8, 6))
        pygame.draw.ellipse(surface, robe_highlight, (x + 4, y + 25, 6, 4))
        
        # Right arm (flowing sleeves)
        right_arm_points = [
            (x + PLAYER_SIZE - 2, y + 20), (x + PLAYER_SIZE - 10, y + 20),
            (x + PLAYER_SIZE - 12, y + 24), (x + PLAYER_SIZE - 10, y + 32), (x + PLAYER_SIZE - 2, y + 32)
        ]
        pygame.draw.polygon(surface, arm_color, right_arm_points)
        pygame.draw.polygon(surface, arm_highlight, [(x + PLAYER_SIZE - 3, y + 21), (x + PLAYER_SIZE - 9, y + 21), (x + PLAYER_SIZE - 10, y + 24), (x + PLAYER_SIZE - 9, y + 30), (x + PLAYER_SIZE - 3, y + 30)])
        # Sleeve details
        pygame.draw.ellipse(surface, robe_detail, (x + PLAYER_SIZE - 11, y + 24, 8, 6))
        pygame.draw.ellipse(surface, robe_highlight, (x + PLAYER_SIZE - 12, y + 25, 6, 4))
        
        # Mystical Staff (ethereal)
        staff_offset = 0
        if self.attack_animation > 0:
            staff_offset = -15 * (1 - self.attack_animation / 10)
        
        # Staff shaft (mystical wood)
        staff_color = (139, 69, 19)  # Brown
        staff_highlight = (160, 82, 45)
        pygame.draw.rect(surface, staff_color, (x + 14 + staff_offset, y + 16, 4, 20))
        pygame.draw.rect(surface, staff_highlight, (x + 15 + staff_offset, y + 17, 2, 18))
        
        # Staff orb (mystical crystal)
        orb_x = x + 16 + staff_offset
        orb_y = y + 12
        # Outer glow
        pygame.draw.circle(surface, (138, 43, 226), (orb_x, orb_y), 8)
        # Main orb
        pygame.draw.circle(surface, (147, 112, 219), (orb_x, orb_y), 6)
        pygame.draw.circle(surface, (186, 85, 211), (orb_x, orb_y), 4)
        pygame.draw.circle(surface, (221, 160, 221), (orb_x, orb_y), 2)
        # Orb highlight
        pygame.draw.circle(surface, (255, 255, 255), (orb_x - 1, orb_y - 1), 1)
        
        # Mystical energy around orb
        for i in range(4):
            angle = i * 90
            energy_x = orb_x + int(6 * math.cos(math.radians(angle)))
            energy_y = orb_y + int(6 * math.sin(math.radians(angle)))
            pygame.draw.circle(surface, (138, 43, 226), (energy_x, energy_y), 2)
            pygame.draw.circle(surface, (147, 112, 219), (energy_x, energy_y), 1)
        
        # Legs with flowing robes
        leg_color = (75, 0, 130)  # Deep purple
        leg_highlight = (138, 43, 226)  # Bright purple
        leg_shadow = (47, 0, 82)  # Dark purple
        
        # Left leg (flowing robe)
        left_leg_points = [
            (x + 6, y + 36), (x + 14, y + 36), (x + 15, y + 40), (x + 14, y + 48), (x + 6, y + 48)
        ]
        pygame.draw.polygon(surface, leg_color, left_leg_points)
        pygame.draw.polygon(surface, leg_highlight, [(x + 7, y + 37), (x + 13, y + 37), (x + 14, y + 40), (x + 13, y + 46), (x + 7, y + 46)])
        # Robe hem details
        pygame.draw.ellipse(surface, robe_detail, (x + 7, y + 44, 8, 6))
        pygame.draw.ellipse(surface, robe_highlight, (x + 8, y + 45, 6, 4))
        
        # Right leg (flowing robe)
        right_leg_points = [
            (x + PLAYER_SIZE - 6, y + 36), (x + PLAYER_SIZE - 14, y + 36),
            (x + PLAYER_SIZE - 15, y + 40), (x + PLAYER_SIZE - 14, y + 48), (x + PLAYER_SIZE - 6, y + 48)
        ]
        pygame.draw.polygon(surface, leg_color, right_leg_points)
        pygame.draw.polygon(surface, leg_highlight, [(x + PLAYER_SIZE - 7, y + 37), (x + PLAYER_SIZE - 13, y + 37), (x + PLAYER_SIZE - 14, y + 40), (x + PLAYER_SIZE - 13, y + 46), (x + PLAYER_SIZE - 7, y + 46)])
        # Robe hem details
        pygame.draw.ellipse(surface, robe_detail, (x + PLAYER_SIZE - 15, y + 44, 8, 6))
        pygame.draw.ellipse(surface, robe_highlight, (x + PLAYER_SIZE - 16, y + 45, 6, 4))

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