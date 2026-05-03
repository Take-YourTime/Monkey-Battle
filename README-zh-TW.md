# 🐒 Monkey Battle

這款遊戲的靈感來自**新楓之谷**同人小遊戲**Maple Cut**，採用滑鼠進行攻擊，並以數字鍵12345來切換技能。  
遊戲內容靈感來自作者的大學生活，因作者就讀於高雄「猴子大學」，在生活中時常需要與猴子打交道，且周遭時常有同學遭到猴子欺負，學校已然受到猴子的**入侵**，進而有了「學生保衛猴子攻擊學校」的有趣想法。  
在以此想法為基礎上，作者創作出了這款遊戲。  

遊戲使用Python 3以及Python套件─pygame來撰寫，分為兩階段製作：
> 最初製作於 **2024 年 7 月** ，這階段採用純手刻，沒有使用任何的AI工具進行輔助。2024年的作品連結： 
> 在 **2026 年 3 月** Vibe Coding流行後，使用 Antigravity 等AI工具進行二次修改，並重構整個專案架構。  

---

## 遊玩方式
12345：切換技能
滑鼠左鍵：施放技能

---

## 技能說明


---

## ✨ 遊戲特色
- **玩家角色**：具備移動、射擊（鉛筆彈幕）與技能動畫
- **敵方猴子**：會移動並攻擊玩家
- **天使猴子 (Angel Monkey)** — 一種特殊的飛行敵方變體
- **魔法使 (Magician)** — 使用魔法的敵方
- **猴子王 (Monkey King)** — 強大的 Boss 級敵人
- **選單系統**：包含標題動畫、按鈕與星星特效
- **背景音樂與音效**：包含射擊、擊中與背景音樂
- **載入/開始頁面**：具備淡入效果

---

## 🚀 如何運行
1. 在 **VS Code** 中打開此資料夾。
2. 確保已安裝 **Pygame**：
   ```bash
   pip install pygame
   ```
3. 執行主檔案：
   ```bash
   python MonkeyBattle.py
   ```

---

## 🕹️ 操作方式
| 按鍵 / 輸入 | 動作 |
|-------------|--------|
| 滑鼠左鍵 | 射擊 |

---

## 🗒️ 注意事項
- 遊戲預設以 **60 FPS** 運行。
- 預設視窗大小：**1366 × 768**。
- 這是一款同人遊戲 —— 所有角色與概念皆受到《楓之谷》（MapleStory）啟發。

---

## 📁 檔案結構
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
    |       settings.json
    |       waves.json
    |
    +---core
    |       engine.py
    |       resource_manager.py
    |       state_machine.py
    |
    +---effects
    |       animations.py
    |
    +---entities
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
    +---player
    |   |   ...
    |   |
    |   \---attack
    |           ...
    |
    +---states
    |       base.py
    |       end_page.py
    |       game_page.py
    |       loading_page.py
    |       menu_page.py
    |       setting_page.py
    |   
    |
    +---_unuse_material_\   # 部分未使用的素材資源
    |
    \---__pycache__
            function.cpython-312.pyc
```
