"""
Boss System Module
==================

This module contains the BossSystem class that handles all boss fight conditions,
tracking, and logic extracted from the pycore whole 2 file.

RESOURCE: This module provides boss battle management for the game.
"""

import pygame
from config.constants import *
from entities.boss_dragons import DragonBoss, BossDragon

class BossSystem:
    """
    Boss System - Manages boss battle conditions and tracking
    
    This class handles all boss-related logic including:
    - Boss battle triggering conditions
    - Boss tracking and cooldowns
    - Boss battle win/lose logic
    - Boss music and effects
    
    Attributes:
        boss_battle_triggered (bool): Whether a boss battle is currently triggered
        boss_defeated (bool): Whether the final boss has been defeated
        boss_cooldown (bool): Whether boss battles are on cooldown
        last_boss_level (int): Last boss level encountered
    """
    
    def __init__(self):
        """Initialize the boss system"""
        self.boss_battle_triggered = False
        self.boss_defeated = False
    
    def check_boss_battle_trigger(self, player):
        """
        Check if a boss battle should be triggered
        
        Args:
            player: The player character object
            
        Returns:
            tuple: (should_trigger, boss_enemy) or (False, None)
        """
        # Check for boss battle after level up
        if (
            player.just_leveled_up and
            player.level > 1 and
            not player.boss_cooldown and
            player.level > player.last_boss_level
        ):
            # At level 10, spawn Malakor, else progressive boss
            if player.level == 10:
                return True, BossDragon()
            else:
                return True, DragonBoss(player.level)
        
        return False, None
    
    def start_boss_battle(self, player, boss_enemy):
        """
        Start a boss battle
        
        Args:
            player: The player character object
            boss_enemy: The boss enemy to fight
            
        Returns:
            bool: True if boss battle started successfully
        """
        if boss_enemy:
            # Set boss cooldown to prevent immediate retrigger
            player.boss_cooldown = True
            player.just_leveled_up = False
            self.boss_battle_triggered = True
            return True
        return False
    
    def handle_boss_battle_win(self, player, boss_enemy, game):
        """
        Handle boss battle victory
        
        Args:
            player: The player character object
            boss_enemy: The boss enemy that was defeated
            game: The game object for state management
        """
        if hasattr(boss_enemy, 'enemy_type') and "boss_dragon" in boss_enemy.enemy_type:
            player.just_leveled_up = False
            player.kills += 1
            player.gain_exp(45)  # Boss gives more exp than regular enemies (25)
            game.score += 25  # Boss gives more score too
            player.boss_cooldown = True  # Set cooldown after boss battle
            player.last_boss_level = player.level  # Set after the fight
            
            if boss_enemy.enemy_type == "boss_dragon":
                # Final boss defeated
                self.boss_defeated = True
                game.state = "victory"
                print("Final boss defeated - Victory!")
            else:
                # Progressive boss defeated
                print(f"Boss battle ended - transitioning to overworld")
                game.state = "overworld"
    
    def handle_boss_battle_lose(self, game):
        """
        Handle boss battle defeat
        
        Args:
            game: The game object for state management
        """
        game.state = "game_over"
        print("Boss battle lost - Game Over!")
    
    def handle_boss_battle_escape(self, player, game):
        """
        Handle boss battle escape
        
        Args:
            player: The player character object
            game: The game object for state management
        """
        player.exp = 0
        player.just_leveled_up = False
        player.boss_cooldown = True  # Set cooldown after boss battle
        player.last_boss_level = player.level  # Set after the fight
        print(f"Boss battle escaped - transitioning to overworld")
        game.state = "overworld"
    
    def is_boss_battle(self, battle_screen):
        """
        Check if current battle is a boss battle
        
        Args:
            battle_screen: The current battle screen
            
        Returns:
            bool: True if this is a boss battle
        """
        if battle_screen and battle_screen.enemy:
            return hasattr(battle_screen.enemy, 'enemy_type') and "boss_dragon" in battle_screen.enemy.enemy_type
        return False
    
    def reset_boss_state(self):
        """Reset boss system state for new game"""
        self.boss_battle_triggered = False
        self.boss_defeated = False
    
    def get_boss_battle_music_state(self, battle_screen):
        """
        Get boss battle music state for music system
        
        Args:
            battle_screen: The current battle screen
            
        Returns:
            bool: True if boss music should be playing
        """
        return self.is_boss_battle(battle_screen) 