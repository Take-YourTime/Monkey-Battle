import pygame
from random import randint
import math
from core.resource_manager import ResourceManager
from entities.base import Entity
from effects.animations import DustEffect
from entities.projectiles import Seed
from function import REFERENCE_FPS

class BigWhiteMonkey(Entity):
    def __init__(self, location_x, location_y) -> None:
        super().__init__()
        rm = ResourceManager.get_instance()
        settings = rm.load_config("config/settings.json")["big_white_monkey"]

        self.raw_image = rm.get_image("bigWhiteMonkey\\bigWhiteMoneky.png")
        
        self.shootImages = [rm.get_image(f"bigWhiteMonkey\\shootAttack\\shootAttack_{str(i).zfill(4)}.png") for i in range(1, 22)]
        self.jumpImages = [rm.get_image(f"bigWhiteMonkey\\jumpAttack\\jumpAttack_{str(i).zfill(4)}.png") for i in range(1, 11)]
        self.moveImages = [rm.get_image(f"bigWhiteMonkey\\move\\move_{str(i).zfill(4)}.png") for i in range(1, 5)]
        self.dieImages = [rm.get_image(f"bigWhiteMonkey\\die\\die_{str(i).zfill(4)}.png") for i in range(1, 9)]

        self.mask = pygame.mask.from_surface(self.raw_image)

        self.image = self.raw_image
        self.index = 0.0 # the time step, take "lower bound" to get frame index
        self.x_moving_destination = randint(settings["moving_range_min"], settings["moving_range_max"])
        
        # State machine variables
        self.state = "move"  # states: move, wait, shootAttack, jumpAttack, die
        self.energy = float(settings["energy_limit"])
        self.max_life = settings["life"]
        self.life = self.max_life
        self.seed_directions = settings["seed_directions"]
        self.jump_attack_damage = settings["jump_attack_damage"]
        self.seeds_fired = 0
        self.has_done_50_jump = False
        self.has_done_25_jump = False
        self._jump_hit_done = False  # flag for jump impact

        self.width = self.raw_image.get_width()
        self.height = self.raw_image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (location_x, location_y)
        self.x = float(location_x)

    def hurt(self, damage=1):
        if self.state == "die":
            return
        self.life -= damage
        if self.life <= 0:
            self.life = 0
            self.state = "die"
            self.index = 0.0
        elif self.life <= self.max_life * 0.25 and not self.has_done_25_jump:
            self.has_done_25_jump = True
            self.state = "jumpAttack"
            self.index = 0.0
            self._jump_hit_done = False
        elif self.life <= self.max_life * 0.5 and not self.has_done_50_jump:
            self.has_done_50_jump = True
            self.state = "jumpAttack"
            self.index = 0.0
            self._jump_hit_done = False

    def calculate_attack_angle(self, player):
        pass # Removed as per user instruction to not calculate vectors dynamically


    def update(self, delta_time, player, seed_group, seedHit_group, dust_group):
        time_step = delta_time * REFERENCE_FPS # time_step is the time step   
        if self.state == "die":
            self.die(time_step)
        elif self.state == "jumpAttack":
            self.jump_attack(time_step, player, dust_group)
        elif self.state == "shootAttack":
            self.shoot_attack(time_step, player, seed_group, seedHit_group)
        elif self.state == "move":
            self.moving(time_step)
        elif self.state == "wait":
            if self.energy >= 400:
                self.state = "shootAttack"
                self.index = 0.0
                self.seeds_fired = 0
                self.energy = 0.0
            else:
                self.energy += time_step

    def jump_attack(self, time_step, player, dust_group):
        frames_per_image = 20
        final_frame = len(self.jumpImages) * frames_per_image

        if self.index < final_frame:
            prev_img_idx = int(self.index) // frames_per_image
            self.index += time_step
            new_img_idx = min(int(self.index) // frames_per_image, len(self.jumpImages) - 1)
            self.image = self.jumpImages[new_img_idx]
            
            # Impact at image index 5 (transition detection)
            if new_img_idx >= 5 and not self._jump_hit_done:
                self._jump_hit_done = True
                player.hurt(self.jump_attack_damage)
                dust_group.add(DustEffect(player.rect.center))
        else:
            self.image = self.raw_image
            self.index = 0.0
            self.state = "wait"

    def shoot_attack(self, time_step, player, seed_group, seedHit_group):
        frames_per_image = 15
        final_frame = len(self.shootImages) * frames_per_image
        
        if self.index < final_frame:
            prev_img_idx = int(self.index) // frames_per_image
            self.index += time_step
            new_img_idx = min(int(self.index) // frames_per_image, len(self.shootImages) - 1)
            self.image = self.shootImages[new_img_idx]
            
            # Fire seeds when transitioning to specific image indices
            if new_img_idx != prev_img_idx and new_img_idx in [12, 14, 16, 18, 20] and self.seeds_fired < 5:
                direction = self.seed_directions[self.seeds_fired % len(self.seed_directions)]
                spawn_pos = (self.rect.left+125, self.rect.centery+20)
                seed_group.add(Seed(spawn_pos, direction["vx"], direction["vy"], direction["angle"], seedHit_group))
                self.seeds_fired += 1
        else:
            self.image = self.raw_image
            self.index = 0.0
            self.state = "wait"

    def moving(self, time_step):
        if self.rect.left > self.x_moving_destination:
            self.index += time_step
            if self.index >= 90:
                self.index = 0.0
            if self.index >= 70:
                self.x -= 1.5 * time_step
                self.image = self.moveImages[3]
            elif self.index >= 45:
                self.x -= 1.5 * time_step
                self.image = self.moveImages[2]
            elif self.index >= 15:
                self.x -= 2 * time_step
                self.image = self.moveImages[1]
            elif self.index >= 5:
                self.x -= 0.5 * time_step
                self.image = self.moveImages[0]
            else:
                self.x -= 0.5 * time_step
                self.image = self.raw_image
            
            self.rect.left = int(self.x)
        else:
            self.index = 0.0
            self.state = "wait"
            self.image = self.raw_image

    def die(self, time_step):
        frames_per_image = 10
        final_frame = len(self.dieImages) * frames_per_image
        
        if self.index < final_frame:
            img_idx = min(int(self.index) // frames_per_image, len(self.dieImages) - 1)
            self.image = self.dieImages[img_idx]
            self.index += time_step
        else:
            self.kill()

