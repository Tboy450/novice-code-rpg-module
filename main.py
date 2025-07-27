"""
DRAGON'S LAIR RPG - Main Game Entry Point
=========================================

This is the main entry point for the modular Dragon's Lair RPG game.
It imports all the necessary modules and starts the game.

WHAT THIS FILE DOES:
===================
This file is the "front door" to the game. When you run this file, it:
1. Imports all the game modules (like loading all the game parts)
2. Creates a new Game object (starts the game engine)
3. Runs the game loop (keeps the game running)

RESOURCE INITIALIZATION FLOW:
============================
1. MODULE IMPORTS:
   - core.game.Game: Main game controller (the "brain" of the game)
   - config.constants.*: All game constants, colors, fonts, screen setup

2. PYGAME INITIALIZATION:
   - Pygame is initialized in config.constants
   - Screen is created with SCREEN_WIDTH x SCREEN_HEIGHT
   - Fonts are loaded (fallback to system fonts if needed)
   - Audio system is initialized

3. GAME STARTUP:
   - Game() constructor initializes all systems
   - StartScreen module creates animated dragon and UI
   - MusicSystem generates procedural chiptune music
   - WorldMap creates 3x3 world grid
   - ParticleSystem initializes visual effects

4. RESOURCE ALLOCATION:
   - Background: Dark blue (config.constants.BACKGROUND)
   - UI Colors: Hot pink borders, cyan text
   - Fonts: Large, medium, small, tiny sizes
   - Audio: Procedural chiptune music
   - Graphics: Procedurally generated (no external files)

5. MODULE DEPENDENCIES:
   - Game class coordinates all other modules
   - Each module handles its specific functionality
   - Clean separation of concerns

ENTRY POINT EXPLANATION:
=======================
- main() function creates Game instance and runs it
- Game.run() starts the main game loop
- All resource management handled by individual modules
- No external files required - everything is procedurally generated

FOR NOVICE CODERS:
==================
This file is intentionally simple - it just starts the game.
All the complex logic is in other modules:
- core/game.py: Contains the main game logic
- config/constants.py: Contains all the game settings
- ui/start_screen.py: Contains the title screen
- world/world_area.py: Contains the world areas
- entities/: Contains all the game characters and objects
"""

from core.game import Game
from config.constants import *

def main():
    """
    Main game entry point - this is where the game starts!
    
    WHAT THIS FUNCTION DOES:
    - Prints a startup message
    - Creates a new Game object (this starts the game engine)
    - Calls game.run() to start the main game loop
    
    FOR NOVICE CODERS:
    This is like turning on a car - you just need to start it,
    and all the complex parts (engine, transmission, etc.) work together.
    """
    print("Starting Dragon's Lair RPG...")
    game = Game()
    game.run()

if __name__ == "__main__":
    main() 