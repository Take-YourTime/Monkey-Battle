# 🐒 Monkey Battle 🐒

> [English] | [繁體中文](README-zh-TW.md)

This game is inspired by the **MapleStory** fan-made game **Maple Cut**. It uses mouse clicks to attack and the number keys 1, 2, 3, 4, 5 to switch skills.  

The game content is inspired by the author's university life. Since the author studied at the "Monkey University" in Kaohsiung, they often had to deal with monkeys in daily life, and classmates were frequently bullied by them.  
The campus was practically **invaded** by monkeys, which sparked the fun idea of "students defending the school from monkey attacks."  

Based on this concept, the author created this game.  

The game is written using Python 3 and the Pygame library, and its development was divided into two stages:  
> 1. Originally made in **July, 2024**. This stage was entirely hard-coded from scratch without using any AI tools. Link to the 2024 project:   
> 2. In **March, 2026**, following the rise of Vibe Coding, AI tools like Antigravity were used for a second round of modifications and a complete refactoring of the project architecture to improve extensibility and maintainability.   

---

## How to Play

1 2 3 4 5: Switch skills

Left Mouse Button: Cast skills

---

## Skill Descriptions
#### 1. Pencil Shooting
<img src="./player/skill_icon/pencil.png" width="10%" alt="pencil">

- Description: The most basic attack. Consumes AP to shoot a pencil toward the cursor. It can cancel out enemy projectiles upon contact.
- AP Cost: 10
- Damage: 1
- Cooldown: Limited by animation
- Level Unlocked: 1

#### 2. Throw Book
<img src="./player/skill_icon/book.png" width="10%" alt="book">

- Description: Consumes MP to throw a book toward the cursor. It eliminates all enemy projectiles upon contact (e.g., banana, stone, etc.) and inflicts a "Heavy Blow" on the hit units (except the Monkey King), temporarily paralyzing them and forcefully canceling their attack if they are in the middle of one.
- MP Cost: 10
- Damage: 3
- Cooldown: Limited by animation
- Level Unlocked: 3

#### 3. Desk and Chair Obstacle
<img src="./player/skill_icon/desk.png" width="10%" alt="desk">

- Description: Consumes MP to drop a pile of desks and chairs from the classroom building above down in front of the player. It inflicts massive damage on monkeys hit by it and creates an obstacle. Melee attacks will prioritize the obstacle, which also blocks incoming projectiles. The obstacle has HP that decays over time, disappearing when its HP reaches zero.
- MP Cost: 25
- Damage: 10
- Cooldown: 20 seconds
- HP: 15
- HP Decay per second: 1
- Level Unlocked: 6

#### 4. Rest Time
<img src="./player/skill_icon/rest.png" width="10%" alt="rest">

- Description: The player takes a rest. During this time, the player cannot take any actions and cannot be interrupted. After resting, the player recovers a certain amount of HP.
- HP Restored: 10 + Current Level
- Cooldown: 20 seconds
- Level Unlocked: 10

#### 5. Scooter Crash
<img src="./player/skill_icon/motorcycle.png" width="10%" alt="motorcycle">

- Description: Fight fire with fire (or monkeys with monkeys). Consumes 75% of maximum AP and 75% of maximum MP to start a scooter and charge forward. Upon hitting a monkey, it explodes and deals massive damage.
- AP Cost: 75% Maximum AP
- MP Cost: 75% Maximum MP
- Damage: 20
- Cooldown: 30 seconds
- Level Unlocked: 15

---

## How to Download
Click on **Releases** on the right side of the GitHub page to download the latest version of the `.exe` file.

---

## Architecture Overview
### loading page

- Initialization page. Preloading is performed here to load `.png`, `.wav`, and other files needed during gameplay from the Disk to RAM in advance. This prevents stutters caused by page faults during gameplay.  
- Click the screen after loading completes to proceed to the menu page.  
  
### menu page

- Main visual page of the game. Creates a twinkling effect by adjusting the opacity of the stars.
- From here, you can navigate to the setting page and the game page.

### setting page

- Allows players to adjust the frame rate.

### game page

- Gameplay stage.

### end page

- Results screen.

---

## File Structure
```
\---Monkey Battle
    |   .gitattributes
    |   .gitignore
    |   function.py
    |   LICENSE
    |   main_icon.ico
    |   MonkeyBattle.py
    |   README.md
    |   school.png
    |
    +---.agents
    |   +---rules
    |   +---skills
    |   |       SKILL.md
    |   |
    |   \---workflows
    +---angelMonkey
    |       ...
    |
    +---BGM
    |       JustAnotherMapleLeaf.mp3
    |       Motivation.mp3
    |
    +---bigWhiteMonkey
    |   |   bigWhiteMoneky.png
    |   |
    |   +---die\...
    |   |
    |   +---jumpAttack\...
    |   |   |
    |   |   \---dust\...
    |   |
    |   +---move\...
    |   |
    |   +---shootAttack\...
    |       \---seed\...
    |
    +---config
    |       settings.json (parameter control)
    |       waves.json (monster count per wave)
    |
    +---core
    |       engine.py
    |       resource_manager.py
    |       state_machine.py
    |
    +---effects
    |       animations.py
    |
    +---entities (sprite code)
    |       angel_monkey.py
    |       base.py
    |       big_white_monkey.py
    |       magician.py
    |       menu_objects.py
    |       monkey.py
    |       monkey_king.py
    |       player.py
    |       projectiles.py
    |
    +---magician
    |       ...
    |
    +---menu
    |       ...
    |
    +---monkey
    |   |   ... 
    |   |
    |   \---banana
    |           ...
    |
    +---monkeyKing
    |   |   ...
    |   |
    |   \---banana
    |          ...
    |
    +---player (player animations and sound effects)
    |   |   ...
    |   |
    |   \---attack
    |           ...
    |
    +---states (game flow stages)
    |       base.py
    |       end_page.py
    |       game_page.py
    |       loading_page.py
    |       menu_page.py
    |       setting_page.py
    |   
    |
    +---_unuse_material_\   # some resource that is not used
    |
    \---__pycache__
            function.cpython-312.pyc
```
