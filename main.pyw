#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import sys
import time
import platform
import shutil
from pathlib import Path

# Define themes for file names with adjectives
THEMES = {
    "treasure": ["Golden", "Hidden", "Ancient", "Mystic", "Cursed"],
    "mystery": ["Secret", "Enigma", "Mystery", "Cryptic", "Shadow"],
    "magical": ["Wizard", "Spell", "Magic", "Enchanted", "Rune"],
    "space": ["Cosmic", "Star", "Galactic", "Nebula", "Void"],
    "haunted": ["Ghost", "Haunted", "Eerie", "Phantom", "Spirit"]
}

# Objects to pair with adjectives
OBJECTS = ["Chest", "Orb", "Key", "Scroll", "Gem", "Map", "Amulet", "Crystal", "Box", "Relic"]

# Dialogues for different events
REPLICATION_MESSAGES = [
    "Uh oh! You've triggered the replication! The files are multiplying!",
    "Nice try, but I'm multiplying now! Can you find the right one?",
    "Wrong choice! Watch as I divide and conquer! Muhahaha!",
    "Oops! More puzzles for you to solve now! Good luck!",
    "Hahaha! You thought it would be that easy? Think again!"
]

VICTORY_MESSAGES = [
    "CONGRATULATIONS! YOU'VE WON! All files have been cleaned up!",
    "WELL DONE, DETECTIVE! You solved the puzzle and stopped the replication!",
    "VICTORY! You found the right file and stopped the madness!"
]

HINT_MESSAGES = [
    "Hint: The solution might be hiding in plain sight...",
    "Hint: Sometimes the obvious choice is the right one...",
    "Hint: Look for patterns that seem out of place...",
    "Hint: The treasure is where X marks the spot...",
    "Hint: The key is sometimes labeled as such..."
]

# New twists and challenges
TWIST_MESSAGES = [
    "The files are getting smarter! Some will now try to hide their true nature!",
    "Oh no! The puzzle is evolving! Names are now becoming scrambled!",
    "Warning: Some files are now disguising themselves as the solution!",
    "Difficulty increasing! File names may no longer be truthful!",
    "Caution! The puzzle has deployed decoys to trick you!"
]

# Text speed - FASTER as requested
TEXT_SPEED = 0.01  # Reduced from 0.03 to 0.01

# Track wrong clicks for increasing difficulty
WRONG_CLICKS = 0

# Flag to determine if this file should create distraction folders
CREATE_DISTRACTIONS = False

def print_with_delay(text, delay=TEXT_SPEED):
    """Print text with a typewriter effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def generate_filename(theme=None, is_solution=False):
    """Generate a themed filename with proper extension for double-clicking"""
    global WRONG_CLICKS
    
    if theme is None:
        theme = random.choice(list(THEMES.keys()))
    
    adjective = random.choice(THEMES[theme])
    object_name = random.choice(OBJECTS)
    
    # After a few wrong clicks, start applying twists to filenames
    if WRONG_CLICKS >= 2 and random.random() < 0.3:
        # Sometimes scramble words
        adjective = ''.join(random.sample(adjective, len(adjective)))
    
    if WRONG_CLICKS >= 3 and random.random() < 0.25 and not is_solution:
        # Sometimes false solutions appear
        base_name = f"SOLUTION-{adjective}{object_name}" 
    else:
        # Mark the solution file clearly as requested
        base_name = f"SOLUTION-{adjective}{object_name}" if is_solution else f"{adjective}{object_name}"
    
    # Use .pyw extension on Windows for no-console execution
    if platform.system() == 'Windows':
        return f"{base_name}.pyw"
    else:
        return f"{base_name}.py"

def make_executable(file_path):
    """Make the file executable on Unix systems"""
    if platform.system() != 'Windows':
        os.chmod(file_path, 0o755)

def create_folder_mayhem():
    """Create random folders when wrong clicks accumulate"""
    folder_names = [
        "DONT_OPEN_ME", "CLICK_HERE", "SECRET_FILES", "SYSTEM32", 
        "IMPORTANT_DATA", "BACKUP", "CLUES", "PUZZLE_PIECES"
    ]
    
    num_folders = random.randint(2, 10)
    created_folders = []
    
    for _ in range(num_folders):
        folder_name = random.choice(folder_names)
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            created_folders.append(folder_name)
            
            # Sometimes create Python files inside folders
            if random.random() < 0.5:
                filename = generate_filename(is_solution=False)
                file_path = os.path.join(folder_name, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(create_script_content(is_solution=False, depth=2, max_depth=2))
                make_executable(file_path)
    
    return created_folders

def create_decoy_files():
    """Create non-Python decoy files to add confusion"""
    decoy_extensions = [".txt", ".log", ".dat", ".cfg", ".tmp"]
    decoy_names = [
        "README", "IMPORTANT", "CLUE", "SOLUTION", "HINT", 
        "DECRYPT_ME", "PASSWORD", "MAP", "INSTRUCTIONS", "SECRETS"
    ]
    
    num_decoys = random.randint(2, 4)
    for _ in range(num_decoys):
        name = random.choice(decoy_names)
        ext = random.choice(decoy_extensions)
        filename = f"{name}{ext}"
        
        # Create a decoy file with misleading content
        with open(filename, 'w', encoding='utf-8') as f:
            if ext == ".txt":
                f.write("This might be a clue... or a trap!\nThe solution is hidden " + 
                        "where you least expect it.\nMaybe check file properties?")
            else:
                f.write("01001000 01101001 01100100 01100100 01100101 01101110\n" + 
                        "01001101 01100101 01110011 01110011 01100001 01100111 01100101")

def create_script_content(is_solution=False, depth=0, max_depth=2):
    """Generate the content for new script files with double-click compatibility"""
    script_path = os.path.abspath(__file__)
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # For Windows, add a pause at the end to keep window open
    if platform.system() == 'Windows':
        if "input('Press Enter to exit...')" not in content:
            # Make sure we have input() at the end to keep console window open
            content = content.replace("# Main execution", 
                                     """# Ensure script pauses at the end on Windows
def pause_at_end():
    if platform.system() == 'Windows':
        print("\\nPress Enter to exit...")
        input()
        
# Main execution""")
            content = content.replace("    show_victory()", "    show_victory()\n    pause_at_end()")
            content = content.replace("            replicate()", "            replicate()\n    pause_at_end()")
    
    # Make sure wrong clicks counter is preserved
    content = content.replace("WRONG_CLICKS = 0", f"WRONG_CLICKS = {WRONG_CLICKS}")
    
    # Set CREATE_DISTRACTIONS flag for 3 out of 5 files
    create_distractions = random.random() < 0.6  # 60% chance (3 out of 5)
    content = content.replace("CREATE_DISTRACTIONS = False", f"CREATE_DISTRACTIONS = {create_distractions}")
    
    # Different logic based on whether this is a solution file or a replicator
    if is_solution:
        return content.replace('is_solution = False', 'is_solution = True')
    else:
        if depth >= max_depth:
            # At max depth, make all files solutions to prevent infinite growth
            return content.replace('is_solution = False', 'is_solution = True')
        else:
            return content.replace('current_depth = 0', f'current_depth = {depth + 1}')

def increase_difficulty():
    """Apply difficulty changes based on wrong clicks"""
    global WRONG_CLICKS
    WRONG_CLICKS += 1
    
    # Apply increasingly difficult twists
    if WRONG_CLICKS == 2:
        print_with_delay("\n" + "="*50, TEXT_SPEED)
        print_with_delay(random.choice(TWIST_MESSAGES), TEXT_SPEED)
        print_with_delay("="*50 + "\n", TEXT_SPEED)
    
    if WRONG_CLICKS == 3:
        create_decoy_files()
    
    # Create distraction folders based on the flag
    if CREATE_DISTRACTIONS and (WRONG_CLICKS >= 4 and WRONG_CLICKS % 2 == 0):
        folders = create_folder_mayhem()
        if folders:
            print_with_delay(f"\nMysterious folders have appeared: {', '.join(folders)}", TEXT_SPEED)
    
    # If they've failed too many times, make the next one easier to find
    if WRONG_CLICKS >= 6:
        return True
    return False

def replicate(theme=None):
    """Create replicas of this script with variations"""
    global WRONG_CLICKS
    clear_screen()
    
    # Display a random replication message
    print("="*50)
    print(random.choice(REPLICATION_MESSAGES))
    print("="*50)
    time.sleep(0.5)  # Faster as requested
    
    print_with_delay("Creating new challenges for you...", TEXT_SPEED)
    
    # Make it easier after too many wrong clicks
    make_obvious = increase_difficulty()
    
    # Create 5 new files (1 solution, 4 replicators)
    solution_index = random.randint(0, 4)
    
    files_created = []
    for i in range(5):
        is_solution = (i == solution_index)
        
        # Make the solution more obvious if they've had too many failures
        if make_obvious and is_solution:
            new_filename = "SOLUTION-TheRealOne.pyw" if platform.system() == 'Windows' else "SOLUTION-TheRealOne.py"
        else:
            new_filename = generate_filename(theme, is_solution)
        
        # Ensure we don't overwrite existing files with the same name
        counter = 1
        base_name = new_filename.replace('.py', '').replace('.pyw', '')
        ext = '.pyw' if platform.system() == 'Windows' else '.py'
        while os.path.exists(new_filename):
            new_filename = f"{base_name}_{counter}{ext}"
            counter += 1
        
        # Create the new file
        with open(new_filename, 'w', encoding='utf-8') as f:
            f.write(create_script_content(is_solution, current_depth, 2))
        
        # Make it executable
        make_executable(new_filename)
        
        files_created.append(new_filename)
        time.sleep(0.1)  # Faster delay for effect
    
    # Display a hint
    print("\n" + "="*50)
    print_with_delay(random.choice(HINT_MESSAGES), TEXT_SPEED)
    print("="*50 + "\n")
    
    print_with_delay("New files have been created. Choose wisely...", TEXT_SPEED)
    
    # List the new files with a fun presentation
    print("\nNEW FILES CREATED:")
    for i, filename in enumerate(files_created):
        print_with_delay(f"  {i+1}. {filename}", TEXT_SPEED)
    
    # Make sure the console stays open on Windows
    if platform.system() == 'Windows':
        print("\nPress Enter to close this window and continue the game...")
        input()
    
    return files_created

def cleanup_files(except_current=True):
    """Delete all script files in the current directory except the currently running one, main.py, and main.pyw"""
    current_script = os.path.basename(__file__)
    
    # Get all Python files in the current directory
    py_files = list(Path('.').glob('*.py')) + list(Path('.').glob('*.pyw'))
    
    deleted_count = 0
    for file_path in py_files:
        filename = str(file_path)
        # Skip the current file if requested and always skip main.py and main.pyw
        if (except_current and filename == current_script) or filename == "main.py" or filename == "main.pyw":
            continue
        try:
            os.remove(filename)
            deleted_count += 1
        except Exception:
            pass
    
    # Also clean up decoy files and folders
    for ext in [".txt", ".log", ".dat", ".cfg", ".tmp"]:
        for file_path in Path('.').glob(f'*{ext}'):
            try:
                os.remove(file_path)
                deleted_count += 1
            except Exception:
                pass
    
    # Clean up folders
    folder_names = ["DONT_OPEN_ME", "CLICK_HERE", "SECRET_FILES", "SYSTEM32", 
                  "IMPORTANT_DATA", "BACKUP", "CLUES", "PUZZLE_PIECES"]
    for folder in folder_names:
        if os.path.exists(folder):
            try:
                shutil.rmtree(folder)
            except Exception:
                pass
    
    return deleted_count

def show_victory():
    """Display victory message and clean up"""
    clear_screen()
    
    # Victory message
    print("="*50)
    print(random.choice(VICTORY_MESSAGES))
    print("="*50)
    
    # Create suspense with a countdown
    print_with_delay("\nCleaning up the chaos in:", TEXT_SPEED)
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.5)  # Faster countdown
    
    print_with_delay("\nSweeping away all the copied files...", TEXT_SPEED)
    
    # Delete all the generated files
    deleted_count = cleanup_files(except_current=False)
    
    time.sleep(0.5)  # Faster as requested
    print_with_delay(f"\n{deleted_count} files have been removed!", TEXT_SPEED)
    print_with_delay("\nGame Over! Thanks for playing!", TEXT_SPEED)
    
    # Keep the console window open on Windows
    if platform.system() == 'Windows':
        print("\nPress Enter to exit...")
        input()

# Add a fun intro sequence
def show_intro():
    """Display an intro animation/message"""
    clear_screen()
    
    intro = """
    ====================================================
                THE SELF-REPLICATING PUZZLE
    ====================================================
    
    Welcome, player! You're about to embark on a
    challenging puzzle of replicating files.
    """
    
    for line in intro.split('\n'):
        print_with_delay(line, TEXT_SPEED)
    
    time.sleep(0.3)  # Faster delay
    
    instructions = """
    INSTRUCTIONS:
    
    1. Each time you run a file, it will create 5 new files
    2. Four will create more files when clicked
    3. One will solve the puzzle and clean everything up
    4. Your goal is to find the solution file
    5. WARNING: The more wrong choices you make, the harder it gets!
    
    Are you ready to begin? The game starts now!
    """
    
    for line in instructions.split('\n'):
        print_with_delay(line, TEXT_SPEED)
    
    print("\nPress Enter to start the game...")
    input()

# Ensure script pauses at the end on Windows
def pause_at_end():
    if platform.system() == 'Windows':
        print("\nPress Enter to exit...")
        input()

# Add Windows double-click compatibility
if __name__ == "__main__":
    # Configuration
    is_solution = False  # Change this to True to make this the solution file
    current_depth = 0    # Track replication depth to prevent infinite replication
    
    # Only show intro for the initial run
    if current_depth == 0:
        show_intro()
    
    if is_solution:
        show_victory()
    else:
        # If we've reached the maximum depth, make this a solution anyway
        if current_depth >= 2:
            show_victory()
        else:
            replicate()
    pause_at_end()