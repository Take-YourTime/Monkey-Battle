# 🐒 Monkey Battle

This game is inspired by the concept of a fan-made game, which is called **Maple Cut**, it is an action game set in **MapleStory**.  
Fight endless waves of monkeys, dodge attacks, and defeat the powerful Monkey King boss!  

> Original made in **July, 2024**.  
> Edit with Antigravity in **March, 2026**.  

---

## ✨ Features
- **Player character** with movement, shooting (pencil projectiles), and skill animations
- **Enemy monkeys** that move and attack the player
- **Angel Monkey** — a special flying enemy variant
- **Magician** — a magic-wielding enemy
- **Monkey King** — a powerful boss enemy
- **Menu system** with animated title, buttons, and star effects
- **BGM & sound effects** for shooting, hits, and background music
- **Loading/start page** with fade-in effect

---

## 🚀 How to Run
1. Open this folder in **VS Code**.
2. Make sure **Pygame** is installed:
   ```bash
   pip install pygame
   ```
3. Run the main file:
   ```bash
   python MonkeyBattle.py
   ```

---

## 🕹️ Controls
| Key / Input | Action |
|-------------|--------|
| Left Mouse Button | Shoot |
---

## 🗒️ Notes
- The game runs at **60 FPS** in default.
- Default window size: **1366 × 768**.
- This is a fan-made game — all characters and concepts are inspired by *MapleStory*.

---

## 📁 File Structure
```
\---Monkey Battle
    |   .gitattributes
    |   .gitignore
    |   function.py
    |   LICENSE
    |   main_icon.ico
    |   MonkeyBattle.py
    |   README.md
    |   school.png
    |
    +---.agents
    |   +---rules
    |   +---skills
    |   |       SKILL.md
    |   |
    |   \---workflows
    +---angelMonkey
    |       ...
    |
    +---BGM
    |       JustAnotherMapleLeaf.mp3
    |       Motivation.mp3
    |
    +---bigWhiteMonkey
    |   |   bigWhiteMoneky.png
    |   |
    |   +---die\...
    |   |
    |   +---jumpAttack\...
    |   |   |
    |   |   \---dust\...
    |   |
    |   +---move\...
    |   |
    |   +---shootAttack\...
    |       \---seed\...
    |
    +---config
    |       settings.json
    |       waves.json
    |
    +---core
    |       engine.py
    |       resource_manager.py
    |       state_machine.py
    |
    +---effects
    |       animations.py
    |
    +---entities
    |       angel_monkey.py
    |       base.py
    |       big_white_monkey.py
    |       magician.py
    |       menu_objects.py
    |       monkey.py
    |       monkey_king.py
    |       player.py
    |       projectiles.py
    |
    +---magician
    |       ...
    |
    +---menu
    |       ...
    |
    +---monkey
    |   |   ... 
    |   |
    |   \---banana
    |           ...
    |
    +---monkeyKing
    |   |   ...
    |   |
    |   \---banana
    |          ...
    |
    +---player
    |   |   ...
    |   |
    |   \---attack
    |           ...
    |
    +---states
    |       base.py
    |       end_page.py
    |       game_page.py
    |       loading_page.py
    |       menu_page.py
    |       setting_page.py
    |   
    |
    +---_unuse_material_\   # some resource that is not used
    |
    \---__pycache__
            function.cpython-312.pyc
```
