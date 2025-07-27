#!/usr/bin/env python3
"""
🐉 Dragon's Lair Folder Icon Setup Script
=========================================

This script helps you set up the dragon icon for the pygame_organized folder.
It creates the necessary files and provides instructions for different operating systems.

FOR NOVICE CODERS:
This script makes it easy to give your game folder a cool dragon icon!
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    """Main setup function"""
    print("🐉 Dragon's Lair Folder Icon Setup")
    print("=" * 40)
    
    # Get the current directory (where this script is located)
    current_dir = Path(__file__).parent
    assets_dir = current_dir / "assets"
    
    # Check if assets folder exists
    if not assets_dir.exists():
        print("❌ Error: assets folder not found!")
        print("Make sure this script is in the pygame_organized folder.")
        return
    
    # Check if icon files exist
    ico_file = assets_dir / "folder_icon.ico"
    png_file = assets_dir / "folder_icon.png"
    
    if not ico_file.exists():
        print("❌ Error: folder_icon.ico not found in assets folder!")
        return
    
    if not png_file.exists():
        print("❌ Error: folder_icon.png not found in assets folder!")
        return
    
    print("✅ Icon files found!")
    print(f"ICO file: {ico_file}")
    print(f"PNG file: {png_file}")
    print()
    
    # Detect operating system
    if sys.platform.startswith('win'):
        setup_windows(ico_file)
    elif sys.platform.startswith('darwin'):  # macOS
        setup_macos(png_file)
    else:  # Linux
        setup_linux(png_file)
    
    print("\n🎉 Setup complete!")
    print("You may need to refresh your file explorer to see the changes.")

def setup_windows(ico_file):
    """Setup for Windows"""
    print("🪟 Windows Setup Instructions:")
    print("1. Right-click on the 'pygame_organized' folder")
    print("2. Select 'Properties'")
    print("3. Click the 'Customize' tab")
    print("4. Click 'Change Icon'")
    print(f"5. Browse to: {ico_file}")
    print("6. Select the icon and click 'OK'")
    print("7. Click 'Apply' and 'OK'")
    print()
    
    # Create desktop.ini file
    desktop_ini_content = f"""[.ShellClassInfo]
IconResource={ico_file.absolute()},0
[ViewState]
Mode=
Vid=
FolderType=Generic
"""
    
    desktop_ini_path = Path("desktop.ini")
    with open(desktop_ini_path, "w") as f:
        f.write(desktop_ini_content)
    
    print("📄 Created desktop.ini file")
    print("💡 Tip: You may need to refresh your file explorer")

def setup_macos(png_file):
    """Setup for macOS"""
    print("🍎 macOS Setup Instructions:")
    print("1. Right-click on the 'pygame_organized' folder")
    print("2. Select 'Get Info'")
    print("3. Click the folder icon in the top-left corner")
    print(f"4. Select: {png_file}")
    print("5. Close the info window")
    print()
    print("💡 Tip: You may need to refresh Finder")

def setup_linux(png_file):
    """Setup for Linux"""
    print("🐧 Linux Setup Instructions:")
    print("1. Right-click on the 'pygame_organized' folder")
    print("2. Select 'Properties'")
    print("3. Click the folder icon")
    print(f"4. Browse to: {png_file}")
    print("5. Click 'OK'")
    print()
    print("💡 Tip: The exact steps may vary depending on your file manager")

if __name__ == "__main__":
    main() 