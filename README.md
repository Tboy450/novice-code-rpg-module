# 🐉 Dragon's Lair RPG - A Retro-Style Adventure Game

**🎮 A complete Python RPG game with dragon battles, chiptune music, and procedurally generated worlds!**

This is a modular version of the Dragon's Lair RPG game, organized into separate packages and modules for better maintainability and code organization. The project is now a proper Python package that can be uploaded and distributed.

## 🚀 Quick Start (For Everyone!)

### 🎯 For Complete Beginners
```bash
# 1. Download this folder
# 2. Open a command prompt/terminal in this folder
# 3. Run the game:
python main.py
```

### 🛠️ For Developers
```bash
# Install the game as a package
pip install -e .

# Run the game
python main.py
# or
dragons-lair-rpg
```

## 🐉 How to Set the Dragon Folder Icon

### Windows Users:
1. **Right-click** on the `pygame_organized` folder
2. Select **"Properties"**
3. Click the **"Customize"** tab
4. Click **"Change Icon"**
5. Browse to `assets/folder_icon.ico` in this folder
6. Click **"OK"** and **"Apply"**

### macOS/Linux Users:
- Use `assets/folder_icon.png` through your file manager's folder properties

## 📦 Package Features

- **🐉 Dragon-themed folder icon** - Custom dragon icon for the project folder
- **📦 Upload-ready** - Complete Python package structure with setup files
- **🎮 Ready to install** - Can be installed via pip: `pip install dragons-lair-rpg`
- **🏷️ Professional metadata** - Proper versioning, licensing, and documentation

## 📁 File Guide (What Each File Does)

### 🚪 **main.py** - The Game's Front Door
- **What it does**: Starts the game when you run it
- **For beginners**: This is like the "ON" button for the game
- **How to use**: Just run `python main.py`

### 📖 **README.md** - This File (The Manual)
- **What it does**: Explains how to use the game and understand the code
- **For beginners**: Read this first to understand what everything does

### 📋 **TODO.md** - What's Being Worked On
- **What it does**: Lists current tasks and future improvements
- **For beginners**: Shows what features are planned or being fixed

### 🎨 **assets/** - Pictures and Icons
- **What it does**: Contains the dragon folder icon and related files
- **For beginners**: This is where the folder's dragon icon comes from

### 🏗️ **build/** - Package Setup Files
- **What it does**: Contains files needed to install the game as a package
- **For beginners**: You don't need to touch these files

### 📚 **docs/** - Extra Documentation
- **What it does**: Contains detailed technical documentation
- **For beginners**: Read these if you want to understand the code deeply

### 🧪 **tests/** - Testing Files
- **What it does**: Contains code that tests if the game works correctly
- **For beginners**: These help make sure the game doesn't break

### 📜 **legacy/** - Old Version
- **What it does**: Contains the original 5523-line file (for reference)
- **For beginners**: This shows how the code looked before it was organized

### 🎮 **Game Folders** (config/, core/, world/, entities/, ui/, audio/, systems/, utils/)
- **What they do**: Each folder contains a specific part of the game
- **For beginners**: Think of these like chapters in a book - each chapter has a specific topic

## What This Game Is
This is a retro-style RPG game built with Python and Pygame. It features:
- A 3x3 world map with different areas (forest, desert, mountain, swamp, volcano, town)
- Turn-based combat with three character classes (Warrior, Mage, Rogue)
- Procedurally generated chiptune music that changes based on where you are
- Particle effects and visual effects
- An opening cutscene and story elements
- Boss battles and a progression system

## For Novice Coders
This project is organized into **modules** - think of them like chapters in a book:
- Each module has a specific job
- They work together to create the complete game
- This makes the code easier to understand and modify

## Project Structure

```
pygame_organized/
├── main.py                 # 🚪 Main entry point (start the game here)
├── README.md              # 📖 This documentation file
├── TODO.md                # 📋 Current to-do list and priorities
├── .gitignore             # 🚫 Git ignore rules
├── __init__.py            # 📦 Package initialization
├── build/                 # 📦 Build and distribution files
│   ├── __init__.py
│   ├── setup.py           # 🏗️ Package configuration
│   ├── pyproject.toml     # 📋 Modern Python packaging
│   ├── MANIFEST.in        # 📄 Package file inclusion
│   ├── LICENSE            # ⚖️ MIT license
│   ├── VERSION            # 🏷️ Version tracking
│   ├── requirements.txt   # 📋 Dependencies
│   └── build_package.py   # 🔨 Build automation
├── docs/                  # 📚 Documentation files
│   ├── __init__.py
│   ├── PACKAGE_READY.md   # ✅ Package distribution status
│   ├── MODULARIZATION_STATUS.md # 📊 Modularization progress
│   └── STRUCTURE_COMPLETE.md # ✅ Structure completion
├── tests/                 # 🧪 Test files
│   ├── __init__.py
│   ├── test_boss_system.py # 🐉 Boss system tests
│   ├── test_dark_knight.py # ⚔️ Dark knight tests
│   └── test_guard_entities.py # 🛡️ Guard entity tests
├── assets/                # 🎨 Assets and icons
│   ├── __init__.py
│   ├── folder_icon.ico    # 🐉 Windows folder icon
│   ├── folder_icon.png    # 🐉 PNG folder icon
│   ├── dragon_icon.txt    # 🐉 ASCII dragon art
│   ├── create_folder_icon.py # 🎨 Icon generation script
│   ├── setup_folder_icon.bat # ⚙️ Windows icon setup
│   └── desktop.ini        # ⚙️ Windows folder customization
├── legacy/                # 📜 Legacy files
│   ├── __init__.py
│   └── organized pycore whole 2.py # 📜 Original 5523-line file
├── config/                # ⚙️ Configuration and constants
│   ├── __init__.py
│   └── constants.py       # 🎨 Game constants, colors, fonts
├── core/                  # 🧠 Core game systems
│   ├── __init__.py
│   ├── game.py           # 🎮 Main Game class (the "brain")
│   ├── game_events.py    # 📡 Event handling
│   ├── game_ui.py        # 🖥️ UI setup and management
│   ├── game_state.py     # 🔄 Game state constants
│   └── game_utils.py     # 🛠️ Utility functions
├── world/                 # 🌍 World and area management
│   ├── __init__.py
│   ├── world_area.py     # 🏞️ Individual area management
│   ├── world_map.py      # 🗺️ 3x3 world grid management
│   └── town_layout.py    # 🏘️ Town layout generation
├── entities/              # 👥 Game entities (characters and objects)
│   ├── __init__.py
│   ├── enemy.py          # 👹 Base enemy class
│   ├── boss_dragons.py   # 🐉 Boss dragon classes
│   ├── item.py           # 💎 Item class
│   ├── dragon.py         # 🐲 Dragon class
│   └── player_characters/ # 🧙‍♂️ Player character classes
│       ├── __init__.py
│       ├── character.py  # 👤 Base character class
│       ├── character_actions.py # ⚔️ Character actions
│       ├── character_animation.py # 🎭 Character animations
│       ├── character_stats.py # 📊 Character stats
│       ├── warrior.py    # ⚔️ Warrior class
│       ├── mage.py       # 🧙‍♀️ Mage class
│       └── rogue.py      # 🗡️ Rogue class
├── ui/                    # 🖥️ User interface components
│   ├── __init__.py
│   ├── button.py         # 🔘 Button UI component
│   ├── start_screen.py   # 🏠 Start menu with dragon animations
│   ├── battle_screen.py  # ⚔️ Battle interface (main)
│   ├── battle_actions.py # ⚔️ Battle action logic
│   ├── battle_effects.py # ✨ Battle effects and animations
│   ├── battle_log.py     # 📝 Battle log management
│   ├── battle_ui.py      # 🖥️ Battle UI helpers
│   └── opening_cutscene.py # 🎬 Story cutscene
├── audio/                 # 🎵 Audio system
│   ├── __init__.py
│   └── music_system.py   # 🎼 Procedural music generation
├── systems/               # ⚙️ Game systems
│   ├── __init__.py
│   └── particle_system.py # ✨ Particle effects
└── utils/                 # 🛠️ Utility functions
    ├── __init__.py
    └── android_utils.py  # 📱 Android-specific utilities
```

## 🚀 Quick Start

### Installation
```bash
# Install the game
pip install dragons-lair-rpg

# Run the game
dragons-lair-rpg
```

### Development Setup
```bash
# Clone and install in development mode
git clone <repository-url>
cd pygame_organized
pip install -e .

# Run directly
python main.py
```

## 🐉 Folder Icon Setup

The project includes a custom dragon icon for the folder:

### Windows
1. Run the setup script: `setup_folder_icon.bat`
2. Or manually:
   - Copy `folder_icon.ico` to a permanent location
   - Right-click the folder → Properties → Customize → Change Icon
   - Browse to `folder_icon.ico`

### macOS/Linux
- Use `folder_icon.png` through your file manager's folder properties

## Current Status

**🎯 Modularization Progress: 100% Complete**

The project has been successfully modularized from a 5523-line monolithic file into a clean, organized structure. 

- ✅ **19/19 classes fully extracted** (100%)
- ✅ **31/31 modules created** (100%)
- ✅ **All modules complete and functional**
- ✅ **Cross-referenced with main.py and README.md**
- ✅ **Character positioning fixed** - World coordinate conversion implemented
- ✅ **Town grass fixed** - Made grass more dense and larger to look like solid grass instead of particles
- ✅ **Town red dirt texture fixed** - Corrected path texture implementation to match original
- ✅ **Town ground base fixed** - Added solid ground base color fill for proper solid appearance
- ✅ **Town ground texture enhanced** - Added scattered dirt spots for natural texture
- ✅ **Town grass made static** - Fixed grass positions to prevent animation/movement
- ✅ **Town background tower spacing fixed** - Adjusted tower positions for better visual spacing
- ✅ **Town guard cutscene fixed** - Implemented detailed guard cutscene with proper dialogue and animations
- ✅ **Dragon knight guard enhanced** - Added dragon-style helmet flares and crest for authentic dragon knight appearance
- ✅ **Item drawing fixed** - Proper animations and details for health/mana items
- ✅ **Enemy drawing fixed** - Detailed enemy graphics with proper animations and effects
- ✅ **Character visibility improved** - Added outlines for better visibility
- ✅ **All game features working** - Start screen, cutscene, character selection, overworld

**📋 See [TODO.md](TODO.md) for final testing and cleanup tasks.**

## How to Run

1. Navigate to the pygame_organized directory
2. Run the main.py file:
   ```bash
   python main.py
   ```

**✅ Note:** All modules have been completed and the game should now be fully functional with the modular structure.

## Module Descriptions

### 🚪 Main Entry Point
- **main.py**: The "front door" to the game. This is where you start the game. It's intentionally simple - it just creates a Game object and runs it.

### ⚙️ Config Module
- **constants.py**: Like a "settings menu" for the entire game. Contains all colors, screen sizes, fonts, and other settings that don't change during gameplay.

### 🧠 Core Module
- **game.py**: The "brain" of the game. This is the main Game class that coordinates everything - it manages game states, handles input, updates objects, and draws everything to the screen.

### 🌍 World Module
- **world_area.py**: Manages individual areas in the 3x3 world grid. Each area (forest, desert, town, etc.) has its own terrain, buildings, and visual style.
- **world_map.py**: Handles the overall world map and area transitions. When you move between areas, this manages the transition.

### 👥 Entities Module
- **character.py**: Player character factory - creates Warrior, Mage, or Rogue based on your selection.
- **enemy.py**: Base enemy class with regular enemy types (fiery, shadow, ice enemies).
- **boss_dragons.py**: Special boss dragon classes (DragonBoss and BossDragon) with enhanced graphics and abilities.
- **dark_knight.py**: DarkKnight entity with black armor, red accents, and dark dragon helmet flares.
- **guard.py**: Original detailed dragon knight guard with complete armor, helmet, sword, and shield.
- **item.py**: Collectible items in the world (health potions, mana potions).
- **dragon.py**: Decorative dragon entities used in cutscenes and effects.

### 🖥️ UI Module
- **button.py**: Reusable button component for menus. Used throughout the game for any clickable elements.
- **start_screen.py**: Start menu with animated dragon graphics and character selection. This is what you see when you first start the game.
- **battle_screen.py**: Turn-based combat interface. This handles all the combat mechanics and displays.
- **battle_actions.py**: Extracted logic for player and enemy actions in battle (attack, magic, items, run).
- **battle_effects.py**: Extracted logic for battle animations and effects (screen shake, particle effects).
- **battle_log.py**: Extracted logic for battle log management and message display.
- **battle_ui.py**: Extracted UI helpers for the battle screen (buttons, health bars, overlays).
- **opening_cutscene.py**: Story introduction sequence. The cinematic that plays when you start a new game.

### 🎵 Audio Module
- **music_system.py**: Procedural chiptune music generation. The music changes based on what area you're in and what's happening in the game.

### ⚙️ Systems Module
- **particle_system.py**: Visual effects and particle system. Creates effects like fire, smoke, sparkles, etc.
- **boss_system.py**: Boss battle management system. Handles boss fight conditions, tracking, and logic.

### 🛠️ Utils Module
- **android_utils.py**: Android-specific utility functions. Detects if the game is running on Android and adjusts controls accordingly.

## Features

- **Modular Design**: Clean separation of concerns with each module handling specific functionality
- **Easy Maintenance**: Changes to one module don't affect others
- **Reusable Components**: UI components and systems can be easily reused
- **Clear Dependencies**: Each module clearly defines its imports and dependencies
- **Extensible**: New features can be added by creating new modules

## Game Features

- 3x3 world map with different area types (forest, desert, mountain, swamp, volcano, town)
- Turn-based combat system with multiple character classes
- Procedurally generated chiptune music
- Particle effects and visual effects
- Opening cutscene and story elements
- Boss battles and progression system

## Controls

- **Arrow Keys/WASD**: Movement in overworld
- **Enter/Space**: Confirm actions
- **Escape**: Menu navigation
- **M**: Toggle world map view

## For Developers

### Adding New Features
To add a new feature:
1. Create a new module in the appropriate directory
2. Import it in the relevant existing modules
3. Update the documentation

### Understanding the Code
- Start with `main.py` to see how the game starts
- Look at `core/game.py` to understand the main game loop
- Check `config/constants.py` to see all the game settings
- Each module has detailed comments explaining what it does

### Code Style
- All modules have detailed docstrings explaining their purpose
- Functions have clear comments explaining what they do
- Variables have descriptive names
- Constants are defined in `config/constants.py` 