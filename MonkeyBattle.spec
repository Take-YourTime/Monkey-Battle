# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# 定義要包含的資料檔案與資料夾
added_files = [
    ('angelMonkey', 'angelMonkey'),
    ('banana', 'banana'),
    ('config', 'config'),
    ('core', 'core'),
    ('effects', 'effects'),
    ('entities', 'entities'),
    ('menu', 'menu'),
    ('monkey', 'monkey'),
    ('monkeyKing', 'monkeyKing'),
    ('player', 'player'),
    ('states', 'states'),
    ('Motivation.mp3', '.'),
    ('hit.wav', '.'),
    ('magicion.png', '.'),
    ('pencil.png', '.'),
    ('pencil_fold.png', '.'),
    ('pencil_fold_1.png', '.'),
    ('school.png', '.'),
    ('shoot.wav', '.'),
    ('start_mark1.png', '.'),
    ('start_mark2.png', '.'),
    ('stone.png', '.'),
    ('sunset.jpg', '.'),
    ('sunset_temp.jpg', '.'),
    ('wind_path.mp3', '.'),
    ('main_icon.ico', '.')
]

a = Analysis(
    ['MonkeyBattle.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['pygame'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MonkeyBattle',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # 關閉 UPX 以提高相容性，減少 DLL 載入錯誤
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['main_icon.ico'],
)
