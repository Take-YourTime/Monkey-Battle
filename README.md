# 🐒 Monkey Battle

This game is inspired by the concept of a fan-made game, which is called **Maple Cut**, it is an action game set in **MapleStory**.  
Fight endless waves of monkeys, dodge attacks, and defeat the powerful Monkey King boss!  

> Made in **July, 2024**.

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

## 📁 File Structure
```
Monkey Battle/
├── MonkeyBattle.py      # 🎮 Main entry point — run this to start the game
├── Player.py            # Player class (movement, shooting, abilities)
├── Monkey.py            # Monkey enemy class
├── MonkeyKing.py        # Boss enemy class
├── Magician.py          # Magician enemy class
├── Menu.py              # Menu UI (buttons, title, stars)
├── function.py          # Shared constants and window setup
├── angelMonkey/         # Angel monkey sprite frames
├── banana/              # Banana projectile sprite frames
├── menu/                # Menu assets (fonts, music, images)
├── monkey/              # Monkey enemy sprite frames
├── monkeyKing/          # Boss monkey sprite frames
├── player/              # Player character sprite frames
├── school.png           # Background image
├── sunset.jpg           # Alternative background
├── Motivation.mp3       # Background music
├── wind_path.mp3        # Wind sound effect
├── hit.wav              # Hit sound effect
└── shoot.wav            # Shoot sound effect
```

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
| Arrow Keys / WASD | Move the player |
| Left Mouse Button | Shoot |
| Right Mouse Button | Special skill |

---

## 🗒️ Notes
- The game runs at **120 FPS**.
- Window size: **1280 × 720**.
- This is a fan-made game — all characters and concepts are inspired by *MapleStory*.

