"""
DRAGON'S LAIR RPG - Enemy Module
================================

This module contains the base Enemy class and regular enemy types.
Boss dragon classes have been moved to entities/boss_dragons.py for better organization.

The module provides:
- Base Enemy class with common enemy functionality
- Regular enemy types (fiery, shadow, ice)
- Enemy movement, combat, and animation systems
- Health bars and visual effects
"""

import pygame
import random
import math
from config.constants import *


class Enemy:
    """
    Base enemy class with common functionality for all enemy types.
    Handles movement, combat, animations, and visual effects.
    """
    
    def __init__(self, player_level):
        """Initialize enemy with stats based on player level"""
        self.size = 50
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        
        # Enemy type and stats
        self.enemy_type = random.choice(["fiery", "shadow", "ice"])
        self.name = f"{self.enemy_type.title()} Enemy"
        
        # Stats scale with player level
        self.health = self.max_health = 50 + player_level * 10
        self.strength = 8 + player_level * 2
        self.speed = 3 + player_level // 3
        
        # Visual properties
        self.color = ENEMY_COLORS.get(self.enemy_type, (255, 0, 0))
        self.animation_frame = 0
        self.attack_animation = 0
        self.hit_animation = 0
        
        # Movement properties
        self.movement_cooldown = 0
        self.movement_delay = 60
    
    def update_animation(self):
        """Update enemy animations and effects"""
        self.animation_frame += 0.1
        
        if self.attack_animation > 0:
            self.attack_animation -= 1
        if self.hit_animation > 0:
            self.hit_animation -= 1
    
    def start_attack_animation(self):
        """Start the attack animation"""
        self.attack_animation = 15
    
    def start_hit_animation(self):
        """Start the hit animation when taking damage"""
        self.hit_animation = 10
    
    def draw(self, surface):
        """Draw the enemy with detailed animations and effects"""
        offset_x = 0
        offset_y = self.animation_offset if hasattr(self, 'animation_offset') else 0
        
        if self.attack_animation > 0:
            offset_x = 5 * math.sin(self.attack_animation * 0.2)
            
        if self.hit_animation > 0:
            offset_x = random.randint(-2, 2)
            offset_y = random.randint(-2, 2)
        
        x = self.x + offset_x
        y = self.y + offset_y
        
        if self.enemy_type == "fiery":
            pygame.draw.ellipse(surface, (200, 50, 0), (x, y, self.size, self.size))
            flame_size = 15
            if self.attack_animation > 0:
                flame_size = 20 * (1 - self.attack_animation / 10)
            for i in range(8):
                angle = i * math.pi / 4
                flame_x = x + self.size//2 + math.cos(angle) * flame_size
                flame_y = y + self.size//2 + math.sin(angle) * flame_size
                pygame.draw.polygon(surface, (255, 150, 0), 
                                  [(x + self.size//2, y + self.size//2),
                                   (flame_x, flame_y),
                                   (flame_x + math.cos(angle+0.3)*5, flame_y + math.sin(angle+0.3)*5)])
            pygame.draw.circle(surface, (255, 255, 0), (x + 15, y + 15), 4)
            pygame.draw.circle(surface, (255, 255, 0), (x + self.size - 15, y + 15), 4)
            pygame.draw.arc(surface, (255, 100, 0), (x + 10, y + 20, self.size - 20, 15), 0, math.pi, 2)
            
        elif self.enemy_type == "shadow":
            pygame.draw.ellipse(surface, (40, 40, 80), (x, y, self.size, self.size))
            smoke_count = 6
            if self.attack_animation > 0:
                smoke_count = 12 * (1 - self.attack_animation / 10)
            for i in range(int(smoke_count)):
                offset_x = random.randint(-5, 5)
                offset_y = random.randint(-5, 5)
                pygame.draw.circle(surface, (70, 70, 120), 
                                 (x + self.size//2 + offset_x, y + self.size//2 + offset_y), 
                                 random.randint(3, 8))
            pygame.draw.circle(surface, (0, 255, 255), (x + 20, y + 20), 5)
            pygame.draw.circle(surface, (0, 255, 255), (x + self.size - 20, y + 20), 5)
            claw_length = 10
            if self.attack_animation > 0:
                claw_length = 15 * (1 - self.attack_animation / 10)
            pygame.draw.line(surface, (0, 200, 200), (x, y + self.size), (x - claw_length, y + self.size + claw_length), 2)
            pygame.draw.line(surface, (0, 200, 200), (x + self.size, y + self.size), (x + self.size + claw_length, y + self.size + claw_length), 2)
            
        else:  # Ice enemy
            pygame.draw.ellipse(surface, (150, 220, 255), (x, y, self.size, self.size))
            shard_length = 20
            if self.attack_animation > 0:
                shard_length = 30 * (1 - self.attack_animation / 10)
            for i in range(8):
                angle = i * math.pi / 4
                shard_x = x + self.size//2 + math.cos(angle) * shard_length
                shard_y = y + self.size//2 + math.sin(angle) * shard_length
                pygame.draw.line(surface, (200, 240, 255), 
                               (x + self.size//2, y + self.size//2),
                               (shard_x, shard_y), 2)
            pygame.draw.circle(surface, (0, 100, 200), (x + 15, y + 15), 4)
            pygame.draw.circle(surface, (0, 100, 200), (x + self.size - 15, y + 15), 4)
            breath_width = 10
            if self.attack_animation > 0:
                breath_width = 20 * (1 - self.attack_animation / 10)
            pygame.draw.arc(surface, (100, 200, 255), (x + 10, y + 25, self.size - 20, breath_width), 0, math.pi, 2)
            
        bar_width = 40
        pygame.draw.rect(surface, (20, 20, 30), (x - 5, y - 15, bar_width, 8), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (x - 4, y - 14, health_width, 6), border_radius=2)
        
                # Draw enemy name
        name_text = font_tiny.render(self.name, True, TEXT_COLOR)
        name_rect = name_text.get_rect(midtop=(x + self.size//2, y - 30))
        surface.blit(name_text, name_rect)
        
        # Health bar
        bar_width = 60
        bar_x = x - 5
        bar_y = y - 15
        pygame.draw.rect(surface, (20, 20, 30), (bar_x, bar_y, bar_width, 8), border_radius=2)
        health_width = (bar_width - 2) * (self.health / self.max_health)
        pygame.draw.rect(surface, HEALTH_COLOR, (bar_x + 1, bar_y + 1, health_width, 6), border_radius=2)
    
    def update(self, player_x, player_y):
        """Update enemy movement towards player"""
        if self.movement_cooldown > 0:
            self.movement_cooldown -= 1
            return
        
        # Move towards player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed
            
            self.x += dx
            self.y += dy
            
            # Keep enemy within screen bounds
            self.x = max(self.size//2, min(SCREEN_WIDTH - self.size//2, self.x))
            self.y = max(self.size//2, min(SCREEN_HEIGHT - self.size//2, self.y))
        
        self.movement_cooldown = self.movement_delay


# Boss dragon classes have been moved to entities/boss_dragons.py for better organization 