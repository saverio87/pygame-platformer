

from os import path
import pygame


SCREEN_SIZE = (800, 800)
TILE_SIZE = 40
FPS = 60
level = 1


# WORLD_DATA = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 5, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], [1, 0, 0, 0, 0, 0, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1], [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 3, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 2, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [
#     1, 0, 0, 4, 0, 0, 0, 3, 0, 0, 0, 2, 2, 2, 0, 0, 0, 3, 0, 1], [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 0, 2, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1], [1, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 2, 1, 1, 1, 2, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 1, 1, 1, 1, 1, 1, 2, 0, 1], [1, 2, 2, 2, 2, 2, 6, 2, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 2, 1]]


# GLOBAL VARIABLES

main_menu = True
game_over = 0


def scale(surface, scale_size):
  # scale_size should be a tuple
    return pygame.transform.scale(surface, scale_size)


def flipX(surface):
    return pygame.transform.flip(surface, True, False)

# Background


sun_img = pygame.image.load('img/sun.png')
bg_img = scale(pygame.image.load('img/sky.png'), SCREEN_SIZE)
dirt_img = scale(pygame.image.load(
    'img/dirt.png'), (TILE_SIZE, TILE_SIZE))
grass_img = scale(pygame.image.load(
    'img/grass.png'), (TILE_SIZE, TILE_SIZE))
restart_img = pygame.image.load('img/restart_btn.png')

start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')


# AUDIO_PATHS = {
#     'bgm': os.path.join(os.getcwd(), 'resources/audios/bgm.mp3'),
#     'get': os.path.join(os.getcwd(), 'resources/images/get.wav')
# }
