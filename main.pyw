#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import sys
import time
import platform
from pathlib import Path

# Treasure hunt themes
THEMES = {
    "pirate": ["Salty", "Plundered", "Cursed", "Jolly", "Buried"],
    "temple": ["Sacred", "Lost", "Ancient", "Golden", "Forbidden"],
    "cave": ["Glowing", "Echoing", "Dark", "Crystal", "Hidden"],
    "jungle": ["Wild", "Overgrown", "Mystic", "Emerald", "Secret"],
    "ghost": ["Phantom", "Haunted", "Eerie", "Spectral", "Grim"]
}

OBJECTS = ["Treasure", "Key", "Map", "Relic", "Coin"]

# Messages for immersion
REPLICATION_MESSAGES = [
    "Shiver me timbers! The loot’s burstin’ free!",
    "The curse roars! More treasures flood the deck!",
    "Wrong chest, ye swab! The hoard doubles!",
    "Blimey! A storm o’ relics rains down!",
    " Avast! The treasure fights back—find the prize!"
]

VICTORY_MESSAGES = [
    "HOIST THE JOLLY ROGER! Ye’ve seized the ultimate haul!",
    "TREASURE CLAIMED! The curse bends to yer will!",
    "CAPTAIN’S GLORY! Ye’ve outsmarted the trap!"
]

HINT_MESSAGES = [
    "Clue: SOLUTION be the beacon in the storm...",
    "Clue: A KEY might unlock more than ye see...",
    "Clue: RIDDLES guard the deepest loot...",
    "Clue: LOCKED chests need a pirate’s cunning...",
    "Clue: The simplest name hides the grandest prize!"
]

LOCK_MESSAGES = [
    "This chest be LOCKED tight! Find a KEY, ye cur!",
    "A seal o’ magic bars the way! Seek the KEY!",
    "Locked by ancient powers! Only a KEY will do!"
]

KEY_FOUND_MESSAGES = [
    "YAR! A KEY glints in yer grasp—use it well!",
    "KEY SNAGGED! The next lock trembles!",
    "A fine find! This KEY be yer ticket to riches!"
]

RIDDLE_MESSAGES = [
    "A RIDDLE bars the way! Solve it, or be lost!",
    "The treasure whispers a RIDDLE—answer true!",
    "Prove yer wits! A RIDDLE guards this chest!"
]

# Riddles and answers (simple for quick play)
RIDDLES = [
    ("I speak without a mouth and hear without ears. What am I?", "echo"),
    ("What has a head, a tail, but no legs?", "coin"),
    ("I’m always running but never move. What am I?", "clock"),
    ("What has keys but can’t open locks?", "piano"),
    ("The more you take, the more you leave behind. What am I?", "steps")
]

TEXT_SPEED = 0.01

# Game state
WRONG_CLICKS = 0
KEYS_COLLECTED = 0
RIDDLES_SOLVED = 0

def print_with_delay(text, delay=TEXT_SPEED):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def generate_filename(theme=None, is_solution=False, is_key=False, is_locked=False, is_riddle=False):
    if theme is None:
        theme = random.choice(list(THEMES.keys()))
    adjective = random.choice(THEMES[theme])
    object_name = random.choice(OBJECTS)
    
    if is_solution:
        base_name = f"SOLUTION-{adjective}{object_name}"
    elif is_key:
        base_name = f"KEY-{adjective}{object_name}"
    elif is_locked:
        base_name = f"LOCKED-{adjective}{object_name}"
    elif is_riddle:
        base_name = f"RIDDLE-{adjective}{object_name}"
    else:
        base_name = f"{adjective}{object_name}"
    
    ext = ".pyw" if platform.system() == "Windows" else ".py"
    return f"{base_name}{ext}"

def make_executable(file_path):
    if platform.system() != "Windows":
        os.chmod(file_path, 0o755)

def create_script_content(is_solution=False, is_key=False, is_locked=False, is_riddle=False, depth=0, max_depth=2):
    script_path = os.path.abspath(__file__)
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    content = content.replace("WRONG_CLICKS = 0", f"WRONG_CLICKS = {WRONG_CLICKS}")
    content = content.replace("KEYS_COLLECTED = 0", f"KEYS_COLLECTED = {KEYS_COLLECTED}")
    content = content.replace("RIDDLES_SOLVED = 0", f"RIDDLES_SOLVED = {RIDDLES_SOLVED}")
    
    if is_solution:
        content = content.replace("is_solution = False", "is_solution = True")
    elif is_key:
        content = content.replace("is_key = False", "is_key = True")
    elif is_locked:
        content = content.replace("is_locked = False", "is_locked = True")
    elif is_riddle:
        content = content.replace("is_riddle = False", "is_riddle = True")
    
    content = content.replace("current_depth = 0", f"current_depth = {depth + 1}")
    if depth >= max_depth:
        content = content.replace("is_solution = False", "is_solution = True")
    
    return content

def cleanup_files(except_current=True):
    current_script = os.path.basename(__file__)
    py_files = list(Path(".").glob("*.py")) + list(Path(".").glob("*.pyw"))
    
    deleted_count = 0
    for file_path in py_files:
        filename = str(file_path)
        if (except_current and filename == current_script) or filename == "main.pyw":
            continue
        try:
            os.remove(filename)
            deleted_count += 1
        except Exception:
            pass
    return deleted_count

def replicate(theme=None):
    global WRONG_CLICKS, KEYS_COLLECTED, RIDDLES_SOLVED
    clear_screen()
    
    print("="*50)
    print_with_delay(random.choice(REPLICATION_MESSAGES))
    print("="*50)
    
    WRONG_CLICKS += 1
    print_with_delay(f"Wrong moves: {WRONG_CLICKS} | Keys: {KEYS_COLLECTED} | Riddles solved: {RIDDLES_SOLVED}")
    
    # Generate 5 new files: 1 solution, 1 key, 1 locked, 1 riddle, 1 distractor
    files_created = []
    types = ["solution", "key", "locked", "riddle", "distractor"]
    random.shuffle(types)
    
    for file_type in types:
        is_solution = file_type == "solution"
        is_key = file_type == "key"
        is_locked = file_type == "locked"
        is_riddle = file_type == "riddle"
        filename = generate_filename(theme, is_solution, is_key, is_locked, is_riddle)
        
        counter = 1
        base_name = filename.replace(".py", "").replace(".pyw", "")
        ext = ".pyw" if platform.system() == "Windows" else ".py"
        while os.path.exists(filename):
            filename = f"{base_name}_{counter}{ext}"
            counter += 1
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(create_script_content(is_solution, is_key, is_locked, is_riddle, current_depth, 2))
        make_executable(filename)
        files_created.append(filename)
        time.sleep(0.1)
    
    print("\n" + "="*50)
    print_with_delay(random.choice(HINT_MESSAGES))
    print("="*50 + "\n")
    
    print_with_delay("New treasures rise from the depths! Pick yer fate:")
    for i, filename in enumerate(files_created):
        print_with_delay(f"  {i+1}. {filename}")
    
    pause_at_end()

def handle_key():
    global KEYS_COLLECTED
    clear_screen()
    
    print("="*50)
    print_with_delay(random.choice(KEY_FOUND_MESSAGES))
    KEYS_COLLECTED += 1
    print_with_delay(f"Keys collected: {KEYS_COLLECTED}")
    print("="*50)
    
    print_with_delay("\nThis key gleams with promise! Seek the locked hoard!")
    pause_at_end()

def handle_locked():
    global KEYS_COLLECTED
    clear_screen()
    
    print("="*50)
    print_with_delay(random.choice(LOCK_MESSAGES))
    if KEYS_COLLECTED > 0:
        print_with_delay("Yer key fits the lock! Turnin’ it now...")
        KEYS_COLLECTED -= 1
        time.sleep(1)
        print_with_delay("The chest creaks open—a SOLUTION be inside!")
        show_victory()
    else:
        print_with_delay("No keys, no glory! Hunt fer one, ye bilge rat!")
    print("="*50)
    pause_at_end()

def handle_riddle():
    global RIDDLES_SOLVED
    clear_screen()
    
    print("="*50)
    print_with_delay(random.choice(RIDDLE_MESSAGES))
    riddle, answer = random.choice(RIDDLES)
    print_with_delay(f"\nRiddle: {riddle}")
    print("="*50)
    
    user_answer = input("\nYer answer, captain: ").strip().lower()
    if user_answer == answer:
        RIDDLES_SOLVED += 1
        print_with_delay("\nYAR! Riddle cracked! The chest reveals a SOLUTION!")
        show_victory()
    else:
        print_with_delay("\nWrong, ye landlubber! The chest seals tighter!")
        replicate(theme="ghost")  # Ghost theme for failure
    pause_at_end()

def show_victory():
    clear_screen()
    
    print("="*50)
    print_with_delay(random.choice(VICTORY_MESSAGES))
    print("="*50)
    
    print_with_delay("\nRaisin’ the spoils in:")
    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(0.5)
    
    print_with_delay("\nScourin’ the seas o’ all but the main bounty...")
    deleted_count = cleanup_files(except_current=False)
    
    print_with_delay(f"\n{deleted_count} treasures hauled away!")
    print_with_delay("The tale ends here—ye be a legend, captain!")
    pause_at_end()

def show_intro():
    clear_screen()
    intro = """
    ====================================================
             THE CURSE OF THE REPLICATING HOARD
    ====================================================
    Avast, brave soul! Ye’ve stumbled into a cursed trove
    where treasures multiply, riddles taunt, and keys unlock
    secrets. Only the SOLUTION can break the spell!
    """
    for line in intro.split("\n"):
        print_with_delay(line)
    
    instructions = """
    YER MISSION:
    1. Open files to face their fate
    2. KEYS unlock LOCKED chests
    3. RIDDLES test yer wits fer treasure
    4. SOLUTION files end the curse (main.pyw stays)
    5. Wrong moves spawn more loot—beware!
    
    Hoist yer courage, captain—the hunt begins!
    """
    for line in instructions.split("\n"):
        print_with_delay(line)
    
    print("\nPress Enter to dive into the fray...")
    input()

def pause_at_end():
    if platform.system() == "Windows":
        print("\nPress Enter to sail onward...")
        input()

if __name__ == "__main__":
    is_solution = False  # Default: replicator
    is_key = False       # Default: not a key
    is_locked = False    # Default: not locked
    is_riddle = False    # Default: not a riddle
    current_depth = 0    # Replication depth
    
    if current_depth == 0:
        show_intro()
    
    if is_solution:
        show_victory()
    elif is_key:
        handle_key()
    elif is_locked:
        handle_locked()
    elif is_riddle:
        handle_riddle()
    else:
        if current_depth >= 2:
            show_victory()
        else:
            replicate()
    pause_at_end()