"""
DRAGON'S LAIR RPG - Battle Screen Module
========================================

This module contains the complete BattleScreen class for turn-based combat.
It integrates with battle_actions.py, battle_effects.py, battle_log.py, and battle_ui.py
for organized functionality.

The BattleScreen handles:
- Turn-based combat between player and enemy
- Character-specific attack animations (Warrior, Mage, Rogue)
- Projectile effects (fireballs, knives)
- Screen shake and visual effects
- Battle log and UI management
- Victory/defeat conditions
"""

import pygame
import random
import math
from config.constants import *
from ui.button import Button
from systems.particle_system import ParticleSystem

# Import extracted battle components
from ui.battle_actions import execute_attack, execute_magic, execute_item, execute_run
from ui.battle_effects import add_screen_shake, start_attack_animation, start_magic_animation
from ui.battle_log import add_log
from ui.battle_ui import create_battle_buttons


class BattleScreen:
    """
    Turn-based combat system with attack, magic, item, and run options.
    Handles battle animations, damage calculations, and victory/defeat conditions.
    
    This class integrates all battle-related functionality including:
    - Player and enemy combat turns
    - Character-specific attack animations and effects
    - Projectile systems (fireballs, knives)
    - Visual effects (screen shake, particles)
    - Battle log and UI management
    """
    
    def __init__(self, player, enemy):
        """
        Initialize the battle screen with player and enemy.
        
        Args:
            player: The player character object
            enemy: The enemy character object
        """
        self.player = player
        self.enemy = enemy
        self.state = "player_turn"
        self.battle_log = ["Battle started!", "It's your turn!"]
        
        # Create battle buttons using the extracted UI helper
        self.buttons = create_battle_buttons()
        
        self.selected_option = 0
        self.battle_ended = False
        self.result = None
        self.transition_alpha = 0
        self.transition_state = "in"
        self.transition_speed = 8
        self.show_summary = False
        self.damage_effect_timer = 0
        self.damage_target = None
        self.damage_amount = 0
        self.action_cooldown = 0
        self.action_delay = 30
        self.log_page = 0
        self.log_lines_per_page = 3
        self.waiting_for_continue = False
        self.action_steps = []
        self.particle_system = ParticleSystem()
        self.screen_shake = 0
        self.attack_effect_timer = 0
        
        # Magic effect system
        self.magic_effect = {
            'active': False,
            'x': 0, 'y': 0,
            'radius': 0,
            'max_radius': 50,
            'color': MAGIC_COLORS[0]
        }
        
        # Check if this is a boss battle
        self.is_boss = hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type
        self.pending_elemental_effect = None
        self.elemental_effect_timer = 0
        
    def start_transition(self):
        """Start the battle transition animation."""
        self.transition_state = "in"
        self.transition_alpha = 0
        
    def draw(self, surface):
        """
        Draw the complete battle screen including characters, UI, and effects.
        
        Args:
            surface: The pygame surface to draw on
        """
        # Calculate screen shake offset
        shake_offset_x = 0
        shake_offset_y = 0
        if self.screen_shake > 0:
            shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.screen_shake -= 1
        
        # Create temporary surface for drawing
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        temp_surface.fill((20, 10, 40))  # Dark purple background
        
        # Draw player and enemy avatars
        player_x, player_y = 200 + shake_offset_x, 350 + shake_offset_y
        enemy_x, enemy_y = 700 + shake_offset_x, 250 + shake_offset_y
        
        # Draw the player using the same character drawing method as overworld
        # Temporarily set the player's position for battle drawing
        original_x, original_y = self.player.x, self.player.y
        self.player.x, self.player.y = player_x, player_y
        
        # Draw the player directly to the battle surface
        self.player.draw(temp_surface)
        
        # Restore original position
        self.player.x, self.player.y = original_x, original_y
        
        # Draw enemy based on type
        self._draw_enemy(temp_surface, enemy_x, enemy_y)
        
        # Draw character-specific attack effects
        self._draw_attack_effects(temp_surface, player_x, player_y, enemy_x, enemy_y)
        
        # Draw magic effect
        self._draw_magic_effect(temp_surface)
        
        # Draw projectiles
        self._draw_projectiles(temp_surface)
        
        # Draw UI elements
        self._draw_ui_elements(temp_surface, player_x, player_y, enemy_x, enemy_y)
        
        # Draw particles
        self.particle_system.draw(temp_surface)
        
        # Draw transition overlay if active
        if self.transition_state != "none":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, self.transition_alpha))
            temp_surface.blit(overlay, (0, 0))
            
        # Show summary after battle
        if self.battle_ended and self.show_summary:
            self._draw_battle_summary(temp_surface)
        
        # Draw the temporary surface to the screen
        surface.blit(temp_surface, (0, 0))

    def _draw_enemy(self, surface, enemy_x, enemy_y):
        """Draw the enemy based on its type."""
        if hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type:
            # Draw the boss using its own draw method
            boss_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            self.enemy.x = enemy_x
            self.enemy.y = enemy_y
            self.enemy.draw(boss_surf)
            surface.blit(boss_surf, (0, 0))
        elif self.enemy.enemy_type == "fiery":
            # Draw fiery enemy
            pygame.draw.ellipse(surface, (220, 80, 0), (enemy_x, enemy_y, 60, 60))
            for i in range(12):
                angle = i * math.pi / 6
                flame_length = random.randint(10, 20)
                flame_x = enemy_x + 30 + math.cos(angle) * flame_length
                flame_y = enemy_y + 30 + math.sin(angle) * flame_length
                flame_color = random.choice(FIRE_COLORS)
                pygame.draw.line(surface, flame_color, 
                               (enemy_x + 30, enemy_y + 30),
                               (flame_x, flame_y), 3)
            pygame.draw.circle(surface, (255, 255, 0), (enemy_x + 20, enemy_y + 25), 6)
            pygame.draw.circle(surface, (255, 255, 0), (enemy_x + 40, enemy_y + 25), 6)
        elif self.enemy.enemy_type == "shadow":
            # Draw shadow enemy
            pygame.draw.ellipse(surface, (30, 30, 60), (enemy_x, enemy_y, 60, 60))
            for i in range(10):
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                size = random.randint(5, 15)
                alpha = random.randint(50, 150)
                smoke_surf = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
                pygame.draw.circle(smoke_surf, (70, 70, 120, alpha), (size, size), size)
                surface.blit(smoke_surf, (enemy_x + 30 - size + offset_x, enemy_y + 30 - size + offset_y))
            pygame.draw.circle(surface, (0, 255, 255), (enemy_x + 20, enemy_y + 25), 7)
            pygame.draw.circle(surface, (0, 255, 255), (enemy_x + 40, enemy_y + 25), 7)
        else:  # Ice enemy
            # Draw ice enemy
            pygame.draw.ellipse(surface, (180, 230, 255), (enemy_x, enemy_y, 60, 60))
            for i in range(8):
                angle = i * math.pi / 4
                crystal_length = random.randint(10, 20)
                crystal_x = enemy_x + 30 + math.cos(angle) * crystal_length
                crystal_y = enemy_y + 30 + math.sin(angle) * crystal_length
                pygame.draw.line(surface, (220, 240, 255), 
                               (enemy_x + 30, enemy_y + 30),
                               (crystal_x, crystal_y), 3)
            pygame.draw.circle(surface, (0, 100, 200), (enemy_x + 20, enemy_y + 25), 6)
            pygame.draw.circle(surface, (0, 100, 200), (enemy_x + 40, enemy_y + 25), 6)

    def _draw_attack_effects(self, surface, player_x, player_y, enemy_x, enemy_y):
        """Draw character-specific attack effects."""
        if self.attack_effect_timer > 0:
            if self.player.type == "Warrior":
                # Holy slash effect for Warrior/Paladin
                effect_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                
                # Multiple holy slashes with different angles and colors
                slash_angles = [0, 15, -15, 30, -30]
                for i, angle in enumerate(slash_angles):
                    # Calculate slash start and end points
                    start_x = player_x + 25
                    start_y = player_y + 15
                    end_x = start_x + math.cos(math.radians(angle)) * 80
                    end_y = start_y + math.sin(math.radians(angle)) * 80
                    
                    # Holy slash colors (gold, white, light blue)
                    slash_colors = [(255, 215, 0, 200), (255, 255, 255, 180), (173, 216, 230, 160)]
                    color = slash_colors[i % len(slash_colors)]
                    
                    # Draw the slash with glow effect
                    for width in range(8, 2, -2):
                        alpha = color[3] - (8 - width) * 20
                        glow_color = (*color[:3], max(0, alpha))
                        pygame.draw.line(effect_surf, glow_color, (start_x, start_y), (end_x, end_y), width)
                
                # Add enemy-side slash effect
                enemy_slash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                
                # Draw impact slashes on enemy
                impact_angles = [0, 20, -20, 40, -40]
                for i, angle in enumerate(impact_angles):
                    # Calculate impact slash points
                    center_x = enemy_x + 30
                    center_y = enemy_y + 30
                    start_x = center_x - math.cos(math.radians(angle)) * 25
                    start_y = center_y - math.sin(math.radians(angle)) * 25
                    end_x = center_x + math.cos(math.radians(angle)) * 25
                    end_y = center_y + math.sin(math.radians(angle)) * 25
                    
                    # Impact slash colors (brighter versions)
                    impact_colors = [(255, 255, 100, 250), (255, 255, 255, 220), (200, 230, 255, 200)]
                    color = impact_colors[i % len(impact_colors)]
                    
                    # Draw impact slash with glow
                    for width in range(10, 3, -2):
                        alpha = color[3] - (10 - width) * 25
                        glow_color = (*color[:3], max(0, alpha))
                        pygame.draw.line(enemy_slash_surf, glow_color, (start_x, start_y), (end_x, end_y), width)
                
                surface.blit(effect_surf, (0, 0))
                surface.blit(enemy_slash_surf, (0, 0))
            
            self.attack_effect_timer -= 1

    def _draw_magic_effect(self, surface):
        """Draw magic effect circles."""
        if self.magic_effect['active']:
            radius = self.magic_effect['radius']
            max_radius = self.magic_effect['max_radius']
            
            for i in range(3, 0, -1):
                r = radius * (i/3)
                alpha = 150 * (1 - r/max_radius)
                color = (*self.magic_effect['color'][:3], int(alpha))
                pygame.draw.circle(surface, color, 
                                 (self.magic_effect['x'], self.magic_effect['y']), 
                                 int(r), 2)
            
            pygame.draw.circle(surface, self.magic_effect['color'], 
                             (self.magic_effect['x'], self.magic_effect['y']), 8)

    def _draw_projectiles(self, surface):
        """Draw fireball and knife projectiles."""
        # Draw fireball projectile
        if hasattr(self, 'fireball_projectile') and self.fireball_projectile['active'] and not self.fireball_projectile.get('hit', False):
            # Draw fireball with glow effect
            x, y = int(self.fireball_projectile['x']), int(self.fireball_projectile['y'])
            size = self.fireball_projectile['size']
            color = self.fireball_projectile['color']
            
            # Outer glow
            for i in range(3, 0, -1):
                glow_size = size + i * 3
                glow_alpha = 100 - i * 30
                glow_color = (*color[:3], glow_alpha)
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
                surface.blit(glow_surf, (x - glow_size, y - glow_size))
            
            # Main fireball
            pygame.draw.circle(surface, color, (x, y), size)
            pygame.draw.circle(surface, (255, 255, 200), (x, y), size // 2)
        
        # Draw knife projectile
        if hasattr(self, 'knife_projectile') and self.knife_projectile['active'] and not self.knife_projectile.get('hit', False):
            x, y = int(self.knife_projectile['x']), int(self.knife_projectile['y'])
            size = self.knife_projectile['size']
            rotation = self.knife_projectile['rotation']
            color = self.knife_projectile['color']
            
            # Create knife surface for rotation
            knife_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            
            # Draw knife blade (pointed oval) - scaled for larger size
            blade_points = [
                (size, 0),  # Tip
                (size - 4, size // 2),  # Top edge
                (size - 2, size),  # Bottom edge
                (size + 2, size),  # Bottom edge
                (size + 4, size // 2),  # Top edge
            ]
            pygame.draw.polygon(knife_surf, color, blade_points)
            
            # Draw knife handle - scaled for larger size
            handle_rect = pygame.Rect(size - 2, size, 4, size // 2)
            pygame.draw.rect(knife_surf, (139, 69, 19), handle_rect)  # Brown handle
            
            # Add metallic shine to blade
            shine_points = [
                (size, 2),  # Tip shine
                (size - 2, size // 2 - 2),  # Top shine
                (size + 2, size // 2 - 2),  # Top shine
            ]
            pygame.draw.polygon(knife_surf, (200, 200, 200), shine_points)
            
            # Rotate and draw
            rotated_knife = pygame.transform.rotate(knife_surf, rotation)
            knife_rect = rotated_knife.get_rect(center=(x, y))
            surface.blit(rotated_knife, knife_rect)

    def _draw_ui_elements(self, surface, player_x, player_y, enemy_x, enemy_y):
        """Draw UI elements like health bars, battle log, and buttons."""
        # Draw health bars
        player_health_width = 150 * (self.player.health / max(1, self.player.max_health))
        pygame.draw.rect(surface, (30, 30, 50), (180, 410, 160, 20))
        pygame.draw.rect(surface, HEALTH_COLOR, (182, 412, player_health_width, 16))
        player_text = font_small.render(f"{self.player.health}/{self.player.max_health}", True, TEXT_COLOR)
        text_rect = player_text.get_rect(center=(180 + 80, 410 + 10))
        surface.blit(player_text, text_rect)
        
        # Only draw enemy health bar and name if not a boss dragon
        if not (hasattr(self.enemy, 'enemy_type') and "boss_dragon" in self.enemy.enemy_type):
            enemy_health_width = 150 * (self.enemy.health / max(1, self.enemy.max_health))
            pygame.draw.rect(surface, (30, 30, 50), (680, 310, 160, 20))
            pygame.draw.rect(surface, HEALTH_COLOR, (682, 312, enemy_health_width, 16))
            enemy_text = font_small.render(f"{self.enemy.health}/{self.enemy.max_health}", True, TEXT_COLOR)
            text_rect = enemy_text.get_rect(center=(680 + 80, 310 + 10))
            surface.blit(enemy_text, text_rect)
            
            # Draw enemy name (not for boss)
            enemy_name = font_small.render(self.enemy.name, True, (255, 215, 0))
            name_rect = enemy_name.get_rect(midtop=(enemy_x + 30, enemy_y - 25))
            surface.blit(enemy_name, name_rect)
        
        # Draw battle log
        pygame.draw.rect(surface, UI_BG, (100, 50, 800, 100), border_radius=8)
        pygame.draw.rect(surface, UI_BORDER, (100, 50, 800, 100), 3, border_radius=8)
        
        start_idx = max(0, len(self.battle_log) - self.log_lines_per_page)
        end_idx = min(len(self.battle_log), start_idx + self.log_lines_per_page)
        
        for i, log in enumerate(self.battle_log[start_idx:end_idx]):
            log_text = font_small.render(log, True, TEXT_COLOR)
            surface.blit(log_text, (120, 70 + i * 30))
        
        if self.waiting_for_continue:
            continue_text = font_small.render("(Press ENTER to continue...)", True, (255, 215, 0))
            surface.blit(continue_text, (120, 70 + self.log_lines_per_page * 30))
        
        # Draw buttons
        if self.state == "player_turn" and not self.waiting_for_continue:
            for i, button in enumerate(self.buttons):
                button.selected = (i == self.selected_option)
                button.draw(surface)
        
        # Draw damage effect
        if self.damage_effect_timer > 0:
            effect_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            if self.damage_target == "player":
                pygame.draw.rect(effect_surf, (255, 0, 0, 100), (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))
            elif self.damage_target == "enemy":
                pygame.draw.rect(effect_surf, (255, 0, 0, 100), (enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))
            
            damage_text = font_medium.render(f"-{self.damage_amount}", True, (255, 50, 50))
            if self.damage_target == "player":
                surface.blit(damage_text, (player_x + 20, player_y - 30))
            elif self.damage_target == "enemy":
                surface.blit(damage_text, (enemy_x + 20, enemy_y - 30))
                
            surface.blit(effect_surf, (0, 0))
            self.damage_effect_timer -= 1

    def _draw_battle_summary(self, surface):
        """Draw the battle summary overlay."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        if self.result == "win":
            summary = [
                "VICTORY!",
                f"EXP GAINED: 25",
                f"KILLS: {self.player.kills}",
                "Press ENTER to continue..."
            ]
        elif self.result == "lose":
            summary = [
                "DEFEAT...",
                "Press ENTER to continue..."
            ]
        elif self.result == "escape":
            summary = [
                "You Escaped!",
                "Press ENTER to continue..."
            ]
            
        for i, line in enumerate(summary):
            text = font_large.render(line, True, TEXT_COLOR)
            surface.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 250 + i*60))

    def update(self):
        """
        Update the battle screen state, animations, and effects.
        
        Returns:
            bool: True if battle has ended, False otherwise
        """
        self.player.update_animation()
        self.enemy.update_animation()
        self.particle_system.update()
        
        # Update magic effect
        if self.magic_effect['active']:
            self.magic_effect['radius'] += 3
            if self.magic_effect['radius'] > self.magic_effect['max_radius']:
                self.magic_effect['active'] = False
                self.magic_effect['radius'] = 0
        
        # Update fireball projectile
        if hasattr(self, 'fireball_projectile') and self.fireball_projectile['active']:
            # Update timer
            self.fireball_projectile['timer'] += 1
            
            if self.fireball_projectile['timer'] < self.fireball_projectile['max_timer']:
                # Calculate direction to target
                dx = self.fireball_projectile['target_x'] - self.fireball_projectile['x']
                dy = self.fireball_projectile['target_y'] - self.fireball_projectile['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Move fireball towards target
                    self.fireball_projectile['x'] += (dx / distance) * self.fireball_projectile['speed']
                    self.fireball_projectile['y'] += (dy / distance) * self.fireball_projectile['speed']
                
                # Add trail particles
                for _ in range(2):
                    angle = random.uniform(0, math.pi*2)
                    dist = random.uniform(0, 6)
                    px = self.fireball_projectile['x'] + math.cos(angle) * dist
                    py = self.fireball_projectile['y'] + math.sin(angle) * dist
                    self.particle_system.add_particle(
                        px, py, self.fireball_projectile['color'],
                        (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)),
                        2, 15
                    )
            else:
                # Timer expired - fireball hits target and explodes
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30,  # Enemy center position
                    self.fireball_projectile['color'], count=30, size_range=(3, 8), 
                    speed_range=(2, 6), lifetime_range=(20, 35)
                )
                self.fireball_projectile['active'] = False
                self.fireball_projectile['hit'] = True  # Mark as hit
                # Add a small delay to ensure projectile is removed before next frame
                self.action_cooldown = 2
        
        # Clean up hit projectiles
        if hasattr(self, 'fireball_projectile') and self.fireball_projectile.get('hit', False):
            delattr(self, 'fireball_projectile')
        if hasattr(self, 'knife_projectile') and self.knife_projectile.get('hit', False):
            delattr(self, 'knife_projectile')
        
        # Update knife projectile
        if hasattr(self, 'knife_projectile') and self.knife_projectile['active']:
            # Update timer
            self.knife_projectile['timer'] += 1
            
            if self.knife_projectile['timer'] < self.knife_projectile['max_timer']:
                # Calculate direction to target
                dx = self.knife_projectile['target_x'] - self.knife_projectile['x']
                dy = self.knife_projectile['target_y'] - self.knife_projectile['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > 0:
                    # Move knife towards target
                    self.knife_projectile['x'] += (dx / distance) * self.knife_projectile['speed']
                    self.knife_projectile['y'] += (dy / distance) * self.knife_projectile['speed']
                    self.knife_projectile['rotation'] += 60  # Spin the knife faster (4x speed)
                
                # Add trail particles
                for _ in range(1):
                    angle = random.uniform(0, math.pi*2)
                    dist = random.uniform(0, 4)
                    px = self.knife_projectile['x'] + math.cos(angle) * dist
                    py = self.knife_projectile['y'] + math.sin(angle) * dist
                    self.particle_system.add_particle(
                        px, py, (120, 120, 120),
                        (random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3)),
                        1, 10
                    )
            else:
                # Timer expired - knife hits target and explodes
                self.particle_system.add_explosion(
                    700 + 30, 250 + 30,  # Enemy center position
                    (80, 80, 80), count=20, size_range=(2, 6), 
                    speed_range=(1, 4), lifetime_range=(15, 25)
                )
                self.knife_projectile['active'] = False
                self.knife_projectile['hit'] = True  # Mark as hit
                # Add a small delay to ensure projectile is removed before next frame
                self.action_cooldown = 2
        
        # Update transition
        if self.transition_state == "in":
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                self.transition_state = "out"
        elif self.transition_state == "out":
            self.transition_alpha -= self.transition_speed
            if self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transition_state = "none"
                
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
            return False
        
        # Check for battle end conditions
        if self.enemy.health <= 0:
            self.battle_ended = True
            self.result = "win"
            self.add_log("You defeated the enemy!")
            self.show_summary = True
            return True
        elif self.player.health <= 0:
            self.battle_ended = True
            self.result = "lose"
            self.add_log("You were defeated...")
            self.show_summary = True
            return True
        
        # Update elemental effect
        if self.elemental_effect_timer > 0:
            self.elemental_effect_timer -= 1
            if self.elemental_effect_timer == 0:
                self.pending_elemental_effect = None
        
        # Process current action steps
        if self.action_steps:
            step = self.action_steps.pop(0)
            step()
            return False
            
        # Handle enemy turn if no actions are queued
        if self.state == "enemy_turn" and not self.battle_ended and not self.waiting_for_continue:
            damage = max(1, self.enemy.strength - self.player.defense // 3)
            self.player.health -= damage
            self.add_log(f"{self.enemy.name} attacks for {damage} damage!")
            self.damage_target = "player"
            self.damage_amount = damage
            self.damage_effect_timer = 20
            self.enemy.start_attack_animation()
            self.player.start_hit_animation()
            self.add_screen_shake(3, 5)
            # Elemental effect after dialog
            self.pending_elemental_effect = self.enemy.enemy_type
            self.elemental_effect_timer = 20
            self.state = "player_turn"
            self.add_log("It's your turn!")
            self.action_cooldown = self.action_delay
            
        return False
    
    def handle_input(self, event, game=None):
        """
        Handle input events for the battle screen.
        
        Args:
            event: The pygame event to handle
            game: Optional game object for sound effects
        """
        if self.waiting_for_continue:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                self.waiting_for_continue = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.waiting_for_continue = False
            return
            
        if self.battle_ended and self.show_summary:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                if self.result == "escape" and game:
                    self.show_summary = False
                    game.state = "overworld"
                    game.battle_screen = None
                else:
                    self.show_summary = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.result == "escape" and game:
                    self.show_summary = False
                    game.state = "overworld"
                    game.battle_screen = None
                else:
                    self.show_summary = False
        elif self.state == "player_turn" and not self.battle_ended and self.action_cooldown == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.selected_option = (self.selected_option + 1) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.selected_option = (self.selected_option - 1) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_option = (self.selected_option - 2) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_option = (self.selected_option + 2) % 4
                    if game and hasattr(game, 'SFX_ARROW') and game.SFX_ARROW: game.SFX_ARROW.play()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if game and hasattr(game, 'SFX_ENTER') and game.SFX_ENTER: game.SFX_ENTER.play()
                    self.handle_action(game)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.buttons):
                    if button.rect.collidepoint(mouse_pos):
                        self.selected_option = i
                        if game and hasattr(game, 'SFX_ENTER') and game.SFX_ENTER: game.SFX_ENTER.play()
                        self.handle_action(game)
    
    def handle_action(self, game=None):
        """
        Handle the selected action (attack, magic, item, run).
        
        Args:
            game: Optional game object for sound effects
        """
        if self.state != "player_turn" or self.battle_ended or self.action_cooldown > 0:
            return
        if self.selected_option == 0:  # Attack
            if game and hasattr(game, 'SFX_ATTACK') and game.SFX_ATTACK: game.SFX_ATTACK.play()
            self.action_steps = [
                lambda: self.add_log("You attack!"),
                lambda: self.start_attack_animation(),
                lambda: self.execute_attack()
            ]
        elif self.selected_option == 1:  # Magic
            if self.player.mana >= 20:
                if game and hasattr(game, 'SFX_MAGIC') and game.SFX_MAGIC: game.SFX_MAGIC.play()
                self.action_steps = [
                    lambda: self.add_log("You cast a fireball!"),
                    lambda: self.start_magic_animation(),
                    lambda: self.execute_magic()
                ]
            else:
                if game and hasattr(game, 'SFX_CLICK') and game.SFX_CLICK: game.SFX_CLICK.play()
                self.add_log("Not enough mana!")
        elif self.selected_option == 2:  # Item
            if game and hasattr(game, 'SFX_ITEM') and game.SFX_ITEM: game.SFX_ITEM.play()
            self.action_steps = [
                lambda: self.add_log("You used a health potion!"),
                lambda: self.execute_item()
            ]
        elif self.selected_option == 3:  # Run
            if game and hasattr(game, 'SFX_CLICK') and game.SFX_CLICK: game.SFX_CLICK.play()
            self.action_steps = [
                lambda: self.add_log("You attempt to escape..."),
                lambda: self.execute_run()
            ] 