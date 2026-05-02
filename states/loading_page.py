import pygame
import os
from states.base import StateBase
from function import BLACK, WHITE
from core.resource_manager import ResourceManager, resource_path

class LoadingState(StateBase):
    def __init__(self, engine):
        super().__init__(engine)
        self.font = pygame.font.Font(resource_path("menu/Wordefta.otf"), 50)
        self.start_font = pygame.font.SysFont(None, 60)
        self.start_color = 255
        self.start_color_detect = True
        
        # Preloading variables
        self.assets_to_load = []
        self.loaded_count = 0
        self.is_loading = True

    def enter(self):
        self.assets_to_load = self._gather_assets()
        self.loaded_count = 0
        self.is_loading = True

    def _gather_assets(self):
        base_path = resource_path(".")
        ignore_dirs = {'.git', 'venv', '__pycache__', 'core', 'states', 'entities', 'effects'}
        assets = []
        for root, dirs, files in os.walk(base_path):
            # filter dirs
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.') and 'unuse' not in d.lower()]
            for file in files:
                if file.endswith(('.png', '.jpg', '.wav', '.json')):
                    rel_path = os.path.relpath(os.path.join(root, file), base_path)
                    ext = os.path.splitext(file)[1].lower()
                    if ext in ['.png', '.jpg']:
                        assets.append(("image", rel_path))
                    elif ext == '.wav':
                        assets.append(("sound", rel_path))
                    elif ext == '.json':
                        assets.append(("config", rel_path))
        return assets

    def update(self, delta_time):
        if self.is_loading:
            for _ in range(5):
                if self.loaded_count < len(self.assets_to_load):
                    asset_type, path = self.assets_to_load[self.loaded_count]
                    rm = ResourceManager.get_instance()
                    
                    try:
                        if asset_type == "image":
                            rm.get_image(path, alpha=True)
                        elif asset_type == "sound":
                            rm.get_sound(path)
                        elif asset_type == "config":
                            rm.load_config(path)
                    except Exception as e:
                        print(f"Error loading {path}: {e}")
                        
                    self.loaded_count += 1
                else:
                    self.is_loading = False
                    break
        else:
            speed = 240 * delta_time 
            if self.start_color_detect == True:
                self.start_color -= speed
                if self.start_color < 100:
                    self.start_color_detect = False
            else:
                self.start_color += speed
                if self.start_color >= 255:
                    self.start_color = 255
                    self.start_color_detect = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.is_loading: # click left mouse button
                    self.engine.state_machine.change_state("MENU")

    def draw(self, surface):
        surface.fill(BLACK)
        
        vw = self.engine.virtual_width
        vh = self.engine.virtual_height

        if self.is_loading:
            total = len(self.assets_to_load)
            progress = self.loaded_count / total if total > 0 else 1.0
            
            # Text
            loading_text = self.font.render(f"Loading Assets... {int(progress * 100)}%", True, WHITE)
            surface.blit(loading_text, (vw / 2 - loading_text.get_width() / 2, vh / 2 - 50))
            
            # Progress Bar Rect
            bar_width = 800
            bar_height = 40
            x = vw / 2 - bar_width / 2
            y = vh / 2 + 20
            
            # Border
            pygame.draw.rect(surface, WHITE, (x, y, bar_width, bar_height), 2)
            # Fill
            pygame.draw.rect(surface, WHITE, (x, y, bar_width * progress, bar_height))
        else:
            start_text_surface = self.start_font.render("Click anywhere to start the game!", True, (int(self.start_color), int(self.start_color), int(self.start_color)))
            surface.blit(start_text_surface, (vw / 2 - start_text_surface.get_width() / 2, vh / 2))
