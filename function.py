import random
import math
import pygame

WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768

VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720

REFERENCE_FPS = 120  # 基準幀率，所有動畫速度以此為基準換算

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


'''blit image that with opacity (optimized for Pygame 2.x)'''
def blit_alpha(target, source, location, opacity): # window 圖片 位置 透明度
    temp = source.copy()
    temp.set_alpha(opacity)
    target.blit(temp, location)


# 傳入 A(x0, y0) B(x1, y1)兩個座標
# 回傳 A->B 的單位向量
def get_normalize_vector(x0, y0, x1, y1):
    vector_x = x1 - x0
    vector_y = y1 - y0
    third_side = math.sqrt( vector_x ** 2 + vector_y ** 2)

    return vector_x / third_side, vector_y / third_side

def get_random_position(widow_width, window_height, image_width, image_height):
    random_x = random.randint(30, widow_width - image_width)
    random_y = random.randint(30, window_height - image_height)
    return random_x, random_y

def numberFollowTarget(current, target, rate):
    # current + (target - curerent) * rate
    #   = current + target * rate - current * rate
    #   = (1-rate) * current + rate * target
    return ( (1 - rate) * current + rate * target )