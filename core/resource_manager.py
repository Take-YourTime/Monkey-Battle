import pygame
import json
import os
import sys

def resource_path(relative_path):
    """ 取得資源的絕對路徑，相容於開發環境與 PyInstaller 打包環境 """
    try:
        # PyInstaller 會將資源解壓縮到 _MEIPASS 暫存資料夾
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ResourceManager:
    _instance = None

    def __init__(self):
        if ResourceManager._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self._images = {}
            self._sounds = {}
            self._config = {}
            ResourceManager._instance = self

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls()
        return cls._instance

    def load_config(self, filepath):
        if filepath not in self._config:
            full_path = resource_path(filepath)
            with open(full_path, 'r', encoding='utf-8') as f:
                self._config[filepath] = json.load(f)
        return self._config[filepath]

    def get_image(self, filepath, alpha=True):
        if filepath not in self._images:
            full_path = resource_path(filepath)
            image = pygame.image.load(full_path)
            self._images[filepath] = image.convert_alpha() if alpha else image.convert()
        return self._images[filepath]

    def get_sound(self, filepath, volume=1.0):
        if filepath not in self._sounds:
            full_path = resource_path(filepath)
            sound = pygame.mixer.Sound(full_path)
            sound.set_volume(volume)
            self._sounds[filepath] = sound
        return self._sounds[filepath]
