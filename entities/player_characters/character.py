"""
DRAGON'S LAIR RPG - Player Character Main Class
==============================================

This module contains the Character factory class for player characters.
Depending on char_type, it instantiates Warrior, Mage, or Rogue.
All logic for actions, animation, and stats is split into separate modules in this package.

Interface Note:
---------------
CharacterBase defines the required interface for animation and action methods.
Battle and UI modules (e.g., battle_screen, battle_actions, battle_effects) will call these methods to trigger or update character animations.
"""

import pygame
import math
import random
from config.constants import *
from abc import ABC, abstractmethod
# Import character classes (avoiding circular imports)
# These will be imported when needed

class CharacterBase(ABC):
    """
    Abstract base class for all player character types.
    Provides the interface for animation and action methods used by battle/UI modules.
    """
    @abstractmethod
    def start_attack_animation(self):
        """Trigger the character's attack animation (called by battle modules)."""
        pass

    @abstractmethod
    def start_hit_animation(self):
        """Trigger the character's hit animation (called by battle modules)."""
        pass

    @abstractmethod
    def update_animation(self):
        """Update the character's animation state (called every frame)."""
        pass

    @abstractmethod
    def draw(self, surface):
        """Draw the character sprite (called by UI/battle modules)."""
        pass

    @abstractmethod
    def draw_stats(self, surface, x, y):
        """Draw the character's stats (HP, MP, EXP, etc.) on the given surface."""
        pass

class Character:
    """
    Character factory/wrapper. Instantiates the correct subclass (Warrior, Mage, Rogue) based on char_type.
    Implements the CharacterBase interface for use in battle/UI modules.
    """
    def __new__(cls, char_type="Warrior"):
        base = object.__new__(cls)
        # Set up base attributes
        base.type = char_type
        base.level = 1
        base.exp = 0
        base.exp_to_level = 100
        if char_type == "Warrior":
            base.max_health = 120
            base.max_mana = 50
            base.strength = 15
            base.defense = 10
            base.speed = 7
        elif char_type == "Mage":
            base.max_health = 80
            base.max_mana = 120
            base.strength = 8
            base.defense = 6
            base.speed = 8
        else:  # Rogue
            base.max_health = 100
            base.max_mana = 70
            base.strength = 12
            base.defense = 8
            base.speed = 12
        base.health = base.max_health
        base.mana = base.max_mana
        base.x = SCREEN_WIDTH // 2
        base.y = SCREEN_HEIGHT // 2
        base.attack_cooldown = 0
        base.kills = 0
        base.items_collected = 0
        base.animation_offset = 0
        base.attack_animation = 0
        base.hit_animation = 0
        base.last_boss_level = 0  # Track the last boss level encountered
        base.just_leveled_up = False
        base.boss_cooldown = False  # Prevent boss battles during cooldown
        # Instantiate the correct subclass
        if char_type == "Warrior":
            from .warrior import Warrior
            return Warrior(base)
        elif char_type == "Mage":
            from .mage import Mage
            return Mage(base)
        else:
            from .rogue import Rogue
            return Rogue(base) 