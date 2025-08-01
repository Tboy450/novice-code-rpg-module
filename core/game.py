"""
DRAGON'S LAIR RPG - Core Game Module
====================================

This module contains the main Game class that manages all game states,
systems, and user input. It handles the complete game loop from start
menu to game over.

WHAT THIS MODULE DOES:
======================
This is the "brain" of the game. It:
1. Manages all game states (start menu, battle, overworld, etc.)
2. Handles user input (keyboard, mouse)
3. Updates all game objects (characters, enemies, items)
4. Draws everything to the screen
5. Manages the game loop (keeps the game running)

FOR NOVICE CODERS:
==================
Think of this like the "conductor" of an orchestra:
- The conductor doesn't play the instruments
- But they coordinate all the musicians
- They decide what happens when and how everything works together

RESOURCE FLOW EXPLANATION:
=========================
1. MODULE COORDINATION:
   - Game class acts as the central coordinator
   - Imports and manages all other modules
   - Handles state transitions between modules

2. START SCREEN RESOURCES:
   - Uses ui.start_screen.StartScreen for title screen
   - StartScreen handles dragon graphics, buttons, and animations
   - Background: config.constants.BACKGROUND (dark blue)
   - Music: audio.music_system.MusicSystem

3. CHARACTER SYSTEM:
   - Uses entities.player_characters.character.Character factory
   - Character creates Warrior/Mage/Rogue based on selection
   - Stats and abilities defined in character subclasses

4. WORLD SYSTEM:
   - Uses world.world_map.WorldMap for 3x3 grid
   - Uses world.world_area.WorldArea for individual areas
   - Procedural generation for terrain and buildings

5. BATTLE SYSTEM:
   - Uses ui.battle_screen.BattleScreen for combat
   - Uses entities.enemy.Enemy for regular enemies
   - Uses entities.boss_dragons.DragonBoss/BossDragon for bosses

6. AUDIO SYSTEM:
   - Uses audio.music_system.MusicSystem for procedural music
   - Music changes based on game state and area type
   - Sound effects generated procedurally

7. PARTICLE SYSTEM:
   - Uses systems.particle_system.ParticleSystem for effects
   - Area-specific particles (lava, snow, leaves, etc.)

8. UI SYSTEM:
   - Uses ui.button.Button for interactive elements
   - Uses ui.opening_cutscene.OpeningCutscene for story

DEPENDENCIES:
=============
- config.constants: All game constants, colors, fonts
- ui.start_screen: Title screen and character selection
- ui.battle_screen: Combat interface
- ui.opening_cutscene: Story introduction
- ui.button: Interactive UI elements
- entities.player_characters: Character classes
- entities.enemy: Enemy system
- entities.boss_dragons: Boss dragon classes
- entities.item: Collectible items
- entities.dragon: Decorative dragons
- world.world_map: 3x3 world grid
- world.world_area: Individual areas
- systems.particle_system: Visual effects
- audio.music_system: Procedural music
- utils.android_utils: Platform detection

GAME LOOP EXPLANATION:
======================
The game loop is like a never-ending cycle:
1. Handle Input: Check for keyboard/mouse input
2. Update: Move characters, update animations, check collisions
3. Draw: Draw everything to the screen
4. Repeat: Go back to step 1

This happens 60 times per second (FPS = 60) to create smooth animation.
"""

import pygame
import sys
import random
import math
from config.constants import *
from world.world_map import WorldMap
from world.world_area import WorldArea
from entities.player_characters.character import Character
from entities.enemy import Enemy
from entities.boss_dragons import DragonBoss, BossDragon
from entities.item import Item
from entities.dragon import Dragon
from ui.button import Button
from ui.battle_screen import BattleScreen
from ui.opening_cutscene import OpeningCutscene
from ui.start_screen import StartScreen
from systems.particle_system import ParticleSystem
from systems.boss_system import BossSystem
from audio.music_system import MusicSystem
from utils.android_utils import is_android

class Game:
    """
    Main game controller that manages all game states, systems, and user input.
    Handles the complete game loop from start menu to game over.
    
    WHAT THIS CLASS DOES:
    ====================
    This is the main "Game" class - it's like the "boss" of the entire game.
    It coordinates everything:
    - Manages game states (what screen you're on)
    - Handles user input (keyboard, mouse)
    - Updates all game objects (characters, enemies, items)
    - Draws everything to the screen
    - Manages the game loop (keeps everything running)
    
    Game States:
    - start_menu: Title screen with start/quit options
    - opening_cutscene: Story introduction sequence
    - character_select: Choose character class
    - overworld: Main gameplay area with movement and exploration
    - battle: Turn-based combat system
    - game_over: End game screen
    - victory: Win game screen
    
    FOR NOVICE CODERS:
    ==================
    This class is like a "game manager" - it doesn't do the specific work
    (like drawing characters or handling combat), but it tells other parts
    of the game when to do their jobs.
    
    Think of it like a restaurant manager:
    - The manager doesn't cook the food
    - But they coordinate the cooks, servers, and customers
    - They make sure everything happens in the right order
    """
    def __init__(self):
        self.state = "start_menu"
        self.player = None
        self.world_map = WorldMap()
        self.enemies = []
        self.items = []
        self.score = 0
        self.game_time = 0
        self.spawn_timer = 0
        self.item_timer = 0
        self.starfield = []
        self.dragon = Dragon(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 120)
        self.fire_timer = 0
        self.battle_screen = None
        self.transition_alpha = 0
        self.transition_state = "none"
        self.transition_speed = 10
        self.player_moved = False
        self.movement_cooldown = 0
        self.movement_delay = 10
        self.particle_system = ParticleSystem()
        self.opening_cutscene = OpeningCutscene()
        self.start_screen = StartScreen()
        self.boss_system = BossSystem()
        self.show_world_map = False
        
        # Initialize starfield
        for _ in range(150):
            self.starfield.append([
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.random() * 2 + 0.5
            ])
        
        # Add flying dragons
        self.flying_dragons = []
        for _ in range(5):
            self.flying_dragons.append({
                'x': random.randint(-200, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'speed': random.uniform(0.5, 2.0),
                'size': random.randint(2, 5),
                'flap': random.random() * 2 * math.pi
            })
        
        # UI Elements (StartScreen handles its own buttons)
        self.back_button = Button(20, 20, 100, 40, "BACK")
        
        # ========================================
        # AUDIO SYSTEM - Procedurally Generated Sound Effects
        # ========================================
        # Generate retro-style sound effects using mathematical waveforms
        def generate_tone(frequency=440, duration_ms=100, volume=0.5, sample_rate=44100, waveform='sine'):
            t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
            if waveform == 'sine':
                wave = np.sin(frequency * 2 * np.pi * t)
            elif waveform == 'square':
                wave = np.sign(np.sin(frequency * 2 * np.pi * t))
            elif waveform == 'sawtooth':
                wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
            elif waveform == 'noise':
                wave = np.random.uniform(-1, 1, t.shape)
            else:
                wave = np.sin(frequency * 2 * np.pi * t)
            audio = (wave * volume * 32767).astype(np.int16)
            # Make it stereo by duplicating the mono channel
            audio_stereo = np.column_stack((audio, audio))
            return pygame.sndarray.make_sound(audio_stereo)
        try:
            pygame.mixer.init()
            self.SFX_CLICK = generate_tone(frequency=800, duration_ms=60, volume=0.5, waveform='square')
            self.SFX_ATTACK = generate_tone(frequency=200, duration_ms=120, volume=0.5, waveform='square')
            self.SFX_MAGIC = generate_tone(frequency=1200, duration_ms=200, volume=0.5, waveform='sine')
            self.SFX_ITEM = generate_tone(frequency=1000, duration_ms=80, volume=0.5, waveform='sine')
            self.SFX_LEVELUP = generate_tone(frequency=1500, duration_ms=300, volume=0.5, waveform='sine')
            self.SFX_GAMEOVER = generate_tone(frequency=100, duration_ms=400, volume=0.5, waveform='sine')
            self.SFX_VICTORY = generate_tone(frequency=900, duration_ms=500, volume=0.5, waveform='sine')
            self.SFX_ARROW = generate_tone(frequency=600, duration_ms=40, volume=0.4, waveform='square')
            self.SFX_ENTER = generate_tone(frequency=1200, duration_ms=80, volume=0.5, waveform='sine')
        except Exception as e:
            print("[WARNING] Could not generate sound effects:", e)
            self.SFX_CLICK = self.SFX_ATTACK = self.SFX_MAGIC = self.SFX_ITEM = self.SFX_LEVELUP = self.SFX_GAMEOVER = self.SFX_VICTORY = None
        
        # ========================================
        # MUSIC SYSTEM - Procedural Chiptune Generation
        # ========================================
        # Dynamic music that changes based on game state and area
        self.music = MusicSystem()
        
        # Virtual button setup for Android
        self.android_buttons = {}
        if is_android():
            button_size = 80
            button_margin = 20
            screen_w, screen_h = SCREEN_WIDTH, SCREEN_HEIGHT
            # D-pad
            self.android_buttons['up'] = pygame.Rect(button_margin + button_size, screen_h - 3*button_size, button_size, button_size)
            self.android_buttons['down'] = pygame.Rect(button_margin + button_size, screen_h - button_size, button_size, button_size)
            self.android_buttons['left'] = pygame.Rect(button_margin, screen_h - 2*button_size, button_size, button_size)
            self.android_buttons['right'] = pygame.Rect(button_margin + 2*button_size, screen_h - 2*button_size, button_size, button_size)
            # Enter/Space
            self.android_buttons['enter'] = pygame.Rect(screen_w - button_margin - button_size, screen_h - 2*button_size, button_size, button_size)
            self.android_buttons['space'] = pygame.Rect(screen_w - button_margin - 2*button_size, screen_h - 2*button_size, button_size, button_size)
    
    def spawn_enemy(self):
        current_area = self.world_map.get_current_area()
        # Don't spawn enemies in town areas
        if current_area and current_area.area_type != "town" and len(current_area.enemies) < 3:
            # Spawn enemy in current area
            enemy = Enemy(self.player.level if self.player else 1)
            
            # Area-specific enemy types
            area_enemy_types = {
                "plains": ["fiery", "shadow", "ice"],
                "forest": ["shadow", "ice"],
                "mountain": ["fiery", "ice"],
                "desert": ["fiery"],
                "swamp": ["shadow", "ice"],
                "volcano": ["fiery"],
                "ice": ["ice"],
                "castle": ["shadow", "fiery"],
                "cave": ["shadow", "ice"]
            }
            
            # Set enemy type based on area
            available_types = area_enemy_types.get(current_area.area_type, ["fiery", "shadow", "ice"])
            enemy.enemy_type = random.choice(available_types)
            
            # Position enemy randomly within the current area
            area_world_x, area_world_y = current_area.get_world_position()
            enemy.x = area_world_x + random.randint(100, AREA_WIDTH - 100)
            enemy.y = area_world_y + random.randint(100, AREA_HEIGHT - 100)
            current_area.enemies.append(enemy)
            self.enemies.append(enemy)
    
    def spawn_item(self):
        current_area = self.world_map.get_current_area()
        if current_area and len(current_area.items) < 2:
            # Spawn item in current area
            item = Item()
            # Position item randomly within the current area
            area_world_x, area_world_y = current_area.get_world_position()
            item.x = area_world_x + random.randint(100, AREA_WIDTH - 100)
            item.y = area_world_y + random.randint(100, AREA_HEIGHT - 100)
            current_area.items.append(item)
            self.items.append(item)
    
    def start_transition(self):
        self.transition_state = "in"
        self.transition_alpha = 0
    
    def update(self):
        """
        Main game update loop - called every frame to update all game systems.
        Handles different update logic based on current game state.
        """
        # ========================================
        # VISUAL EFFECTS UPDATES
        # ========================================
        # Update starfield animation
        for star in self.starfield:
            star[0] -= star[2]
            if star[0] < 0:
                star[0] = SCREEN_WIDTH
                star[1] = random.randint(0, SCREEN_HEIGHT)
        
        # Update flying dragons
        for dragon in self.flying_dragons:
            dragon['x'] += dragon['speed']
            dragon['flap'] += 0.05
            if dragon['x'] > SCREEN_WIDTH + 50:
                dragon['x'] = -50
                dragon['y'] = random.randint(0, SCREEN_HEIGHT)
                dragon['speed'] = random.uniform(0.5, 2.0)
        
        # ========================================
        # SYSTEM UPDATES
        # ========================================
        # Update particle effects
        self.particle_system.update()
        
        # Update dynamic music system based on game state
        is_boss_battle = self.boss_system.get_boss_battle_music_state(self.battle_screen)
        current_area = self.world_map.get_current_area() if hasattr(self, 'world_map') else None
        self.music.update(self.state, is_boss_battle, current_area)
        
        # ========================================
        # TRANSITION EFFECTS
        # ========================================
        # Handle screen transition animations (fade in/out)
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
        
        # ========================================
        # GAME STATE-SPECIFIC UPDATES
        # ========================================
        if self.state == "start_menu":
            # Title screen with animated dragon
            self.dragon.update()
            self.fire_timer += 1
            if self.fire_timer > 120:
                self.dragon.breathe_fire()
                self.fire_timer = 0
                
            # Update StartScreen for UI interactions
            next_state = self.start_screen.update()
            if next_state:
                self.state = next_state
                
        elif self.state == "opening_cutscene":
            # Story introduction sequence
            next_state = self.opening_cutscene.update()
            if next_state:
                self.state = next_state
                
        elif self.state == "character_select":
            # Character selection screen using StartScreen module
            result = self.start_screen.update()
            if result:
                if isinstance(result, tuple):
                    self.state, character_type = result
                    if character_type:
                        self.player = Character(character_type)
                else:
                    self.state = result
                
        elif self.state == "overworld" and self.player:
            # Main gameplay area with movement and exploration
            self.game_time += 1
            self.spawn_timer += 1
            self.item_timer += 1
            self.movement_cooldown = max(0, self.movement_cooldown - 1)
            self.player.update_animation()
            
            # Update camera to follow player
            self.world_map.update_camera(self.player.x, self.player.y)
            
            # Update area transition effect
            self.world_map.update_transition()
            
            # Check for area transition
            if self.world_map.check_area_transition(self.player.x, self.player.y):
                # Area changed, update enemy and item lists
                current_area = self.world_map.get_current_area()
                self.enemies = current_area.enemies
                self.items = current_area.items
                
                # If entering town area, position player at the gate (4 squares lower)
                if current_area and current_area.area_type == "town":
                    area_world_x, area_world_y = current_area.get_world_position()
                    # Position at gate (center horizontally, 4 squares lower)
                    self.player.x = area_world_x + (AREA_WIDTH // 2)  # Center horizontally
                    self.player.y = area_world_y + 260  # 4 squares lower from top (200 + 60 = 260)
            
            # Add area-specific particle effects
            current_area = self.world_map.get_current_area()
            if current_area:
                current_area.particle_timer += 1
                if current_area.particle_timer >= current_area.particle_interval:
                    current_area.particle_timer = 0
                    
                    # Spawn area-specific particles
                    area_world_x, area_world_y = current_area.get_world_position()
                    if current_area.area_type == "volcano":
                        # Lava particles
                        for _ in range(5):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (255, 100, 0),
                                (random.uniform(-0.5, 0.5), random.uniform(-2, -0.5)),
                                6, 40
                            )
                    elif current_area.area_type == "ice":
                        # Snow particles
                        for _ in range(4):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (200, 220, 255),
                                (random.uniform(-0.3, 0.3), random.uniform(0.5, 1.5)),
                                4, 50
                            )
                    elif current_area.area_type == "swamp":
                        # Mist particles
                        for _ in range(3):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (150, 180, 150),
                                (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                5, 60
                            )
                    elif current_area.area_type == "forest":
                        # Leaf particles
                        for _ in range(4):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (100, 150, 50),
                                (random.uniform(-0.3, 0.3), random.uniform(-0.5, -0.1)),
                                5, 45
                            )
                    elif current_area.area_type == "desert":
                        # Sand particles
                        for _ in range(6):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (200, 180, 120),
                                (random.uniform(-1, 1), random.uniform(-0.5, 0.5)),
                                4, 35
                            )
                    elif current_area.area_type == "mountain":
                        # Wind particles
                        for _ in range(3):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (180, 180, 200),
                                (random.uniform(-0.8, 0.8), random.uniform(-0.3, 0.3)),
                                4, 40
                            )
                    elif current_area.area_type == "beach":
                        # Sea foam particles
                        for _ in range(4):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (220, 240, 255),
                                (random.uniform(-0.4, 0.4), random.uniform(-0.2, 0.2)),
                                5, 55
                            )
                    elif current_area.area_type == "castle":
                        # Magic sparkles
                        for _ in range(3):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (255, 215, 0),
                                (random.uniform(-0.2, 0.2), random.uniform(-0.2, 0.2)),
                                4, 50
                            )
                    elif current_area.area_type == "cave":
                        # Dust particles
                        for _ in range(2):
                            x = area_world_x + random.randint(0, AREA_WIDTH)
                            y = area_world_y + random.randint(0, AREA_HEIGHT)
                            self.particle_system.add_particle(
                                x, y, (100, 100, 120),
                                (random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1)),
                                3, 70
                            )
                    elif current_area.area_type == "town":
                        # Town-specific particles (smoke, fountain, leaves)
                        current_area.generate_town_particles(self.particle_system)
                        
                        # Check for town entrance cutscene
                        if current_area.check_entrance_cutscene(self.player.x, self.player.y):
                            print("Town entrance cutscene triggered!")
                        
                        # Update town cutscene if active
                        current_area.update_cutscene()
            
            for item in self.items:
                item.update()
            if self.spawn_timer >= 300:
                self.spawn_enemy()
                self.spawn_timer = 0
            if self.item_timer >= 600:
                self.spawn_item()
                self.item_timer = 0
            for enemy in self.enemies:
                enemy.update(self.player.x, self.player.y)
                enemy.update_animation()
            # --- Check for boss battle after level up ---
            should_trigger, boss_enemy = self.boss_system.check_boss_battle_trigger(self.player)
            if should_trigger:
                self.battle_screen = BattleScreen(self.player, boss_enemy)
                self.battle_screen.start_transition()
                self.state = "battle"
                self.boss_system.start_boss_battle(self.player, boss_enemy)
                return
            for enemy in self.enemies[:]:
                if self.player:  # Ensure player exists
                    player_rect = pygame.Rect(self.player.x, self.player.y, PLAYER_SIZE, PLAYER_SIZE)
                    enemy_rect = pygame.Rect(enemy.x, enemy.y, ENEMY_SIZE, ENEMY_SIZE)
                    if player_rect.colliderect(enemy_rect):
                        self.battle_screen = BattleScreen(self.player, enemy)
                        self.battle_screen.start_transition()
                        self.state = "battle"
                        # Remove enemy from both lists
                        self.enemies.remove(enemy)
                        current_area = self.world_map.get_current_area()
                        if current_area and enemy in current_area.enemies:
                            current_area.enemies.remove(enemy)
                        self.player_moved = False
                        break
            for item in self.items[:]:
                if self.player:  # Ensure player exists
                    item_rect = pygame.Rect(item.x, item.y, ITEM_SIZE, ITEM_SIZE)
                    player_rect = pygame.Rect(self.player.x, self.player.y, PLAYER_SIZE, PLAYER_SIZE)
                    if player_rect.colliderect(item_rect):
                        if item.type == "health":
                            self.player.health = min(self.player.max_health, self.player.health + 30)
                            for _ in range(15):
                                x = random.randint(self.player.x, self.player.x + PLAYER_SIZE)
                                y = random.randint(self.player.y, self.player.y + PLAYER_SIZE)
                                self.particle_system.add_particle(
                                    x, y, HEALTH_COLOR,
                                    (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                                    3, 30
                                )
                        else:
                            self.player.mana = min(self.player.max_mana, self.player.mana + 40)
                            for _ in range(15):
                                x = random.randint(self.player.x, self.player.x + PLAYER_SIZE)
                                y = random.randint(self.player.y, self.player.y + PLAYER_SIZE)
                                self.particle_system.add_particle(
                                    x, y, MANA_COLOR,
                                    (random.uniform(-0.5, 0.5), random.uniform(-1, -0.5)),
                                    3, 30
                                )
                        self.player.items_collected += 1
                        # Remove item from both lists
                        if item in self.items:
                            self.items.remove(item)
                        current_area = self.world_map.get_current_area()
                        if current_area and item in current_area.items:
                            current_area.items.remove(item)
    
    def draw(self, screen):
        screen.fill(BACKGROUND)
        
        # Draw starfield background
        for x, y, speed in self.starfield:
            alpha = min(255, int(speed * 100))
            pygame.draw.circle(screen, (200, 200, 255, alpha), (int(x), int(y)), 1)
        
        # Draw flying dragons
        for dragon in self.flying_dragons:
            wing_offset = math.sin(dragon['flap']) * dragon['size']
            color = (200, 200, 255, min(255, int(dragon['size'] * 40)))
            
            pygame.draw.line(
                screen, color,
                (dragon['x'], dragon['y']),
                (dragon['x'] + 5 * dragon['size'], dragon['y']),
                max(1, dragon['size'] // 2)
            )
            
            pygame.draw.line(
                screen, color,
                (dragon['x'] + 2 * dragon['size'], dragon['y']),
                (dragon['x'] + dragon['size'], dragon['y'] - 3 * dragon['size'] - wing_offset),
                max(1, dragon['size'] // 2)
            )
            pygame.draw.line(
                screen, color,
                (dragon['x'] + 2 * dragon['size'], dragon['y']),
                (dragon['x'] + dragon['size'], dragon['y'] + 3 * dragon['size'] + wing_offset),
                max(1, dragon['size'] // 2)
            )
            
            pygame.draw.line(
                screen, color,
                (dragon['x'] + 5 * dragon['size'], dragon['y']),
                (dragon['x'] + 7 * dragon['size'], dragon['y'] - dragon['size']),
                max(1, dragon['size'] // 2)
            )
        
        # ========================================
        # GAME STATE-SPECIFIC DRAWING
        # ========================================
        if self.state == "start_menu":
            # Title screen using StartScreen module
            self.start_screen.draw_start_menu(screen)
            # Draw the animated dragon
            self.dragon.draw(screen)
            
        elif self.state == "opening_cutscene":
            # Story introduction sequence
            self.opening_cutscene.draw(screen)
            
        elif self.state == "character_select":
            # Character selection screen using StartScreen module
            self.start_screen.draw_character_select(screen)
            
        elif self.state == "overworld":
            # Main gameplay area
            if self.show_world_map:
                # Draw world map view
                self.world_map.draw_world_map(screen)
            else:
                # Draw current area
                current_area = self.world_map.get_current_area()
                if current_area:
                    current_area.draw(screen, self.world_map)
                else:
                    screen.fill(BACKGROUND)
                
                # Draw grid for current area
                for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                    pygame.draw.line(screen, current_area.grid_color if current_area else GRID_COLOR, 
                                   (x, 0), (x, SCREEN_HEIGHT), 2)
                for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                    pygame.draw.line(screen, current_area.grid_color if current_area else GRID_COLOR, 
                                   (0, y), (SCREEN_WIDTH, y), 2)
                
                # Draw area boundaries more prominently
                pygame.draw.rect(screen, (255, 255, 255), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 3)
                
                # Draw player (convert world coordinates to screen coordinates)
                if self.player:
                    screen_x, screen_y = self.world_map.world_to_screen(self.player.x, self.player.y)
                    original_x, original_y = self.player.x, self.player.y
                    self.player.x, self.player.y = screen_x, screen_y
                    self.player.draw(screen)
                    self.player.x, self.player.y = original_x, original_y
                    
                    # Draw player position indicator
                    grid_x = (screen_x // GRID_SIZE) * GRID_SIZE
                    grid_y = (screen_y // GRID_SIZE) * GRID_SIZE
                    pygame.draw.rect(screen, (255, 255, 0), (grid_x, grid_y, GRID_SIZE, GRID_SIZE), 2)
                
                # Draw enemies (convert world coordinates to screen coordinates)
                for enemy in self.enemies:
                    screen_x, screen_y = self.world_map.world_to_screen(enemy.x, enemy.y)
                    if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                        original_x, original_y = enemy.x, enemy.y
                        enemy.x, enemy.y = screen_x, screen_y
                        enemy.draw(screen)
                        enemy.x, enemy.y = original_x, original_y
                
                # Draw items (convert world coordinates to screen coordinates)
                for item in self.items:
                    screen_x, screen_y = self.world_map.world_to_screen(item.x, item.y)
                    if 0 <= screen_x < SCREEN_WIDTH and 0 <= screen_y < SCREEN_HEIGHT:
                        original_x, original_y = item.x, item.y
                        item.x, item.y = screen_x, screen_y
                        item.draw(screen)
                        item.x, item.y = original_x, original_y
                
                # Draw particle effects
                self.particle_system.draw(screen, self.world_map)
                
                # Draw town entrance cutscene if active
                if current_area and current_area.cutscene_active:
                    current_area.draw_cutscene(screen)
                
                # Draw area transition effect
                if self.world_map.transitioning:
                    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, self.world_map.area_transition_alpha))
                    screen.blit(overlay, (0, 0))
                
                # Draw world map overlay
                if self.show_world_map:
                    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 180))
                    screen.blit(overlay, (0, 0))
                    
                    # Draw world map grid
                    map_size = 300
                    map_x = (SCREEN_WIDTH - map_size) // 2
                    map_y = (SCREEN_HEIGHT - map_size) // 2
                    cell_size = map_size // 3
                    
                    # Draw background
                    pygame.draw.rect(screen, UI_BG, (map_x, map_y, map_size, map_size), border_radius=8)
                    pygame.draw.rect(screen, UI_BORDER, (map_x, map_y, map_size, map_size), 3, border_radius=8)
                    
                    # Draw areas
                    for y in range(3):
                        for x in range(3):
                            area = self.world_map.areas.get((x, y))
                            if area:
                                cell_x = map_x + x * cell_size
                                cell_y = map_y + y * cell_size
                                
                                # Color based on area type and visited status
                                if area == self.world_map.get_current_area():
                                    color = (100, 255, 100)  # Current area - bright green
                                elif area.visited:
                                    color = (50, 150, 50)    # Visited area - dark green
                                else:
                                    color = (50, 50, 50)     # Unvisited area - dark gray
                                
                                pygame.draw.rect(screen, color, (cell_x + 2, cell_y + 2, cell_size - 4, cell_size - 4))
                                pygame.draw.rect(screen, UI_BORDER, (cell_x, cell_y, cell_size, cell_size), 1)
                                
                                # Draw area name
                                name_text = font_tiny.render(area.area_type[:3].upper(), True, TEXT_COLOR)
                                text_x = cell_x + (cell_size - name_text.get_width()) // 2
                                text_y = cell_y + (cell_size - name_text.get_height()) // 2
                                screen.blit(name_text, (text_x, text_y))
                    
                    # Draw player position
                    player_world_x, player_world_y = self.player.x, self.player.y
                    player_area_x = player_world_x // AREA_WIDTH
                    player_area_y = player_world_y // AREA_HEIGHT
                    if 0 <= player_area_x < 3 and 0 <= player_area_y < 3:
                        player_cell_x = map_x + player_area_x * cell_size + cell_size // 2
                        player_cell_y = map_y + player_area_y * cell_size + cell_size // 2
                        pygame.draw.circle(screen, (255, 255, 0), (player_cell_x, player_cell_y), 5)
                
                # Draw UI overlay
                self.draw_overworld_ui(screen)
                
        elif self.state == "battle":
            # Battle screen
            if self.battle_screen:
                self.battle_screen.draw(screen)
                
        elif self.state == "game_over":
            # Game over screen
            title_text = font_large.render("GAME OVER", True, (255, 100, 100))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
            screen.blit(title_text, title_rect)
            
            score_text = font_medium.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(score_text, score_rect)
            
            if self.player:
                level_text = font_medium.render(f"Level Reached: {self.player.level}", True, TEXT_COLOR)
                level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 350))
                screen.blit(level_text, level_rect)
            
            self.start_button.draw(screen)
            self.back_button.draw(screen)
            
        elif self.state == "victory":
            # Victory screen
            title_text = font_large.render("VICTORY!", True, (255, 215, 0))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 200))
            screen.blit(title_text, title_rect)
            
            subtitle_text = font_medium.render("You defeated the Dragon Lord!", True, TEXT_COLOR)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 300))
            screen.blit(subtitle_text, subtitle_rect)
            
            score_text = font_medium.render(f"Final Score: {self.score}", True, TEXT_COLOR)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 350))
            screen.blit(score_text, score_rect)
            
            self.start_button.draw(screen)
            self.back_button.draw(screen)
        
        # Draw transition overlay
        if self.transition_alpha > 0:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(self.transition_alpha)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
    
    def draw_overworld_ui(self, screen):
        """Draw the overworld UI overlay"""
        if not self.player:
            return
            
        # Draw player stats
        self.player.draw_stats(screen, 10, 10)
        
        # Draw score
        score_text = font_small.render(f"Score: {self.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 150))
        
        # Draw controls hint
        controls_text = font_tiny.render("M: Map | ESC: Menu", True, (150, 150, 150))
        screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = True
                    # Android virtual controls
                    if is_android() and self.android_buttons:
                        mx, my = event.pos
                        for name, rect in self.android_buttons.items():
                            if rect.collidepoint(mx, my):
                                if name == 'up':
                                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
                                    pygame.event.post(fake_event)
                                elif name == 'down':
                                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
                                    pygame.event.post(fake_event)
                                elif name == 'left':
                                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
                                    pygame.event.post(fake_event)
                                elif name == 'right':
                                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
                                    pygame.event.post(fake_event)
                                elif name == 'enter':
                                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
                                    pygame.event.post(fake_event)
                                elif name == 'space':
                                    fake_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
                                    pygame.event.post(fake_event)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "overworld":
                            self.state = "game_over"
                        elif self.state == "game_over":
                            self.state = "start_menu"
                        elif self.state == "character_select":
                            self.state = "start_menu"
                        elif self.state == "opening_cutscene":
                            self.opening_cutscene.skip()
                    
                    # Handle skip for cutscene
                    if self.state == "opening_cutscene":
                        self.opening_cutscene.skip()
                    
                    # Handle world map toggle
                    if self.state == "overworld" and event.key == pygame.K_m:
                        self.show_world_map = not self.show_world_map
                    
                    # Handle movement in overworld
                    if self.state == "overworld" and self.player and self.movement_cooldown <= 0:
                        # Store original position for collision detection
                        original_x = self.player.x
                        original_y = self.player.y
                        
                        if event.key in [pygame.K_UP, pygame.K_w]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(0, -1)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                        elif event.key in [pygame.K_DOWN, pygame.K_s]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(0, 1)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(-1, 0)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            if self.SFX_ARROW: self.SFX_ARROW.play()
                            self.player.move(1, 0)
                            # Check collision and revert if needed
                            current_area = self.world_map.get_current_area()
                            if current_area and current_area.check_building_collision(self.player.x, self.player.y):
                                self.player.x = original_x
                                self.player.y = original_y
                            else:
                                self.player_moved = True
                                self.movement_cooldown = self.movement_delay
                    
                    # Handle town cutscene dialogue advancement
                    if self.state == "overworld" and event.key == pygame.K_SPACE:
                        current_area = self.world_map.get_current_area()
                        if current_area and current_area.cutscene_active and current_area.guard:
                            # Advance dialogue
                            current_area.guard["current_dialogue"] += 1
                            current_area.cutscene_timer = 0
                            
                            # Check if we've reached the end of dialogue
                            if current_area.guard["current_dialogue"] >= len(current_area.guard["dialogue"]):
                                current_area.cutscene_phase = 2  # End cutscene
                    
                    # Pass input to battle screen
                    if self.state == "battle" and self.battle_screen:
                        self.battle_screen.handle_input(event, self)
            
            # Handle button clicks
            if self.state == "start_menu":
                # Update button hover states
                self.start_screen.update_buttons(mouse_pos)
                
                # Handle clicks using StartScreen module
                result = self.start_screen.handle_start_menu_clicks(mouse_pos, mouse_click)
                if result:
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    if result == "quit":
                        running = False
                    else:
                        self.state = result
                        if result == "opening_cutscene":
                            self.opening_cutscene = OpeningCutscene()  # Reset cutscene
                    
            elif self.state == "character_select":
                # Update button hover states
                self.start_screen.update_buttons(mouse_pos)
                
                # Handle clicks using StartScreen module
                result = self.start_screen.handle_character_select_clicks(mouse_pos, mouse_click)
                if result:
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    if isinstance(result, tuple):
                        self.state, character_type = result
                        if character_type:
                            self.player = Character(character_type)
                            self.start_game()
                    else:
                        self.state = result
                    
            elif self.state == "overworld":
                pass
                    
            elif self.state == "battle":
                battle_ended = self.battle_screen.update()
                
                if battle_ended:
                    # Boss battle win/lose/escape
                    if self.boss_system.is_boss_battle(self.battle_screen):
                        if self.battle_screen.result == "win":
                            self.boss_system.handle_boss_battle_win(self.player, self.battle_screen.enemy, self)
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
                        elif self.battle_screen.result == "lose":
                            self.boss_system.handle_boss_battle_lose(self)
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
                        elif self.battle_screen.result == "escape":
                            self.boss_system.handle_boss_battle_escape(self.player, self)
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
                    else:
                        if self.battle_screen.result == "win":
                            self.player.kills += 1
                            self.player.gain_exp(25)
                            self.score += 10
                            self.start_transition()
                            print(f"Battle ended - transitioning to overworld")
                            self.state = "overworld"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                        elif self.battle_screen.result == "lose":
                            self.state = "game_over"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                        elif self.battle_screen.result == "escape":
                            self.player.exp = 0
                            self.player.just_leveled_up = False
                            print(f"Battle escaped - transitioning to overworld")
                            self.state = "overworld"
                            self.battle_screen = None
                            self.music.update(self.state, False)  # Explicitly reset music state
                            continue
            
            elif self.state == "game_over":
                self.start_button.update(mouse_pos)
                self.back_button.update(mouse_pos)
                
                if self.start_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "character_select"
                    
                if self.back_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "start_menu"
                    
            elif self.state == "victory":
                self.start_button.update(mouse_pos)
                self.back_button.update(mouse_pos)
                
                if self.start_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "character_select"
                    
                if self.back_button.is_clicked(mouse_pos, mouse_click):
                    if self.SFX_CLICK: self.SFX_CLICK.play()
                    self.state = "start_menu"
            
            self.update()
            self.draw(screen)
            
            # Handle victory music completion
            if self.state == "victory" and not pygame.mixer.music.get_busy():
                # After victory music plays once, return to menu
                self.state = "start_menu"
                self.music.update(self.state)
            
            pygame.display.flip()
            clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
    
    def start_game(self):
        """Reset game state for a new game"""
        self.enemies = []
        self.items = []
        self.score = 0
        self.game_time = 0
        self.spawn_timer = 0
        self.item_timer = 0
        self.player_moved = False
        self.movement_cooldown = 0
        self.boss_system.reset_boss_state()
        
        # Reset world map
        self.world_map = WorldMap()
        
        # Position player in center area (1,1) at center position
        if self.player:
            self.player.x = AREA_WIDTH + (AREA_WIDTH // 2)
            self.player.y = AREA_HEIGHT + (AREA_HEIGHT // 2)
        
        # Spawn initial enemies and items in starting area
        for _ in range(3):
            self.spawn_enemy()
        for _ in range(2):
            self.spawn_item() 