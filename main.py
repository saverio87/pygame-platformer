import pygame
from os import path
import pickle
from pygame.locals import *
from utils import SCREEN_SIZE, TILE_SIZE, FPS, main_menu, game_over, scale, flipX, sun_img, bg_img, restart_img, start_img, exit_img


level = 1
maxlevels = 8


def reset_level(level):

    player.reset(100, SCREEN_SIZE[1] - 130)
    blob_group.empty()
    lava_group.empty()
    exit_group.empty()
    platform_group.empty()

    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        WORLD_DATA = pickle.load(pickle_in)
        return World(WORLD_DATA)


pygame.init()

# For scaling sprites


screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption('Platformer')
clock = pygame.time.Clock()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.clicked = False

    def draw(self):

        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                # We're looking for left clicks
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/blob.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 2
        self.counter = 0

    def update(self):

        self.rect.x += self.vel_x

        self.counter += self.vel_x

        if abs(self.counter) > 50:

            self.vel_x *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png').convert_alpha()
        self.image = scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/exit.png').convert_alpha()
        self.image = scale(img, (TILE_SIZE, int(TILE_SIZE * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/platform_x.png').convert_alpha()
        self.image = scale(img, (TILE_SIZE, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = velocity
        self.counter = 0
        self.move_x = move_x
        self.move_y = move_y

    def update(self):

        if self.move_x:
            self.rect.x += self.velocity
        elif self.move_y:
            self.rect.y += self.velocity

        self.counter += self.velocity

        if abs(self.counter) >= 50:
            self.velocity *= -1


# def update(self):

#     self.rect.x += self.vel_x
#     self.counter += self.vel_x

#     if abs(self.counter) > 50:

#         self.vel_x *= -1


class World:
    def __init__(self, data):
        self.tile_list = []

        row_count = 0

        dirt_img = pygame.image.load('img/dirt.png').convert_alpha()
        dirt_img = scale(dirt_img, (TILE_SIZE, TILE_SIZE))
        grass_img = pygame.image.load('img/grass.png').convert_alpha()
        grass_img = scale(grass_img, (TILE_SIZE, TILE_SIZE))

        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    dirt_rect = dirt_img.get_rect()
                    dirt_rect.x = col_count * TILE_SIZE
                    dirt_rect.y = row_count * TILE_SIZE

                    # Creates a tuple
                    tile = (dirt_img, dirt_rect)
                    self.tile_list.append(tile)

                if tile == 2:
                    grass_rect = grass_img.get_rect()
                    grass_rect.x = col_count * TILE_SIZE
                    grass_rect.y = row_count * TILE_SIZE

                    tile = (grass_img, grass_rect)
                    self.tile_list.append(tile)

                if tile == 3:
                    blob = Enemy(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    blob_group.add(blob)

                if tile == 4:
                    platform = Platform(
                        col_count * TILE_SIZE, row_count * TILE_SIZE, 3, True, False)
                    platform_group.add(platform)

                if tile == 5:

                    platform = Platform(
                        col_count * TILE_SIZE, row_count * TILE_SIZE, 3, False, True)
                    platform_group.add(platform)

                if tile == 6:
                    lava = Lava(col_count * TILE_SIZE, row_count *
                                TILE_SIZE + TILE_SIZE // 2)
                    lava_group.add(lava)

                if tile == 8:

                    exit = Exit(col_count * TILE_SIZE, row_count *
                                TILE_SIZE - TILE_SIZE // 2)

                    exit_group.add(exit)

                col_count += 1

            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


class Player:
    def __init__(self, x, y):

        self.reset(x, y)

    def jump(self):

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -20
            self.jumped = True
        # This is to avoid that the character keeps jumping
        # when keeping the space key pressed
        if key[pygame.K_SPACE] == False:
            self.jumped = False

        # ADDING GRAVITY

        if self.vel_y >= 15:
            self.vel_y = 15

        self.vel_y += 1

        # # decreasing y velocity at every frame
        # self.vel_y += 1
        # # gravity is set at vel_y = 15, meaning the speed at which the character falls down is capped at 15
        # if self.vel_y >= 10:
        #     self.vel_y = 10

    def walk_anim(self):

        # handle animation

        # walk_counter gets incremented by 1 every time the user
        # presses the left/right arrow, and it is only once it
        # gets to 10 (the value of walk_cooldown) that the index
        # gets incremented. This helps slow down an otherwise too
        # fast animation.
        # The bigger the cooldown number, the slower the animation

        walk_cooldown = 10

        if self.walk_counter > walk_cooldown:
            self.walk_counter = 0
            # incrementing the index by 1 and assigning a new image
            # to self.image using the new index each time
            # walk_anim is invoked
            self.walk_index += 1
            if self.walk_index >= len(self.walk_right_img):
                self.walk_index = 0

            if self.walk_direction == -1:
                self.image = self.walk_left_img[self.walk_index]
            else:
                self.image = self.walk_right_img[self.walk_index]

    def update(self, game_over):

        dx = 0
        dy = 0

        collision_treshold = 20

        # CONDITIONAL STATEMENT (game_over == 0)

        if game_over == 0:

            # get keypresses and edit delta x / y
            key = pygame.key.get_pressed()

            if key[pygame.K_LEFT]:
                dx -= 8
                self.walk_counter += 1
                self.walk_direction = -1
            if key[pygame.K_RIGHT]:
                dx += 8
                self.walk_counter += 1
                self.walk_direction = 1

            # When the player stops moving
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                self.walk_counter = 0
                self.walk_index = 0

                if self.walk_direction == -1:
                    self.image = self.walk_left_img[self.walk_index]
                else:
                    self.image = self.walk_right_img[self.walk_index]

            self.walk_anim()
            self.jump()
            dy += self.vel_y

            # check for collisions

            # We need to set it to true every time it re-renders / updates
            # as the variable is set to False whenever the player touches
            # the ground

            self.in_air = True

            for tile in world.tile_list:

                # Check for collisions on x axis

                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                # Check for collisions on the y axis

                # We use a virtual rectangle that we send in for
                # exploration before the actual player rectangle's x and
                # get updated and player gets moved

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y >= 0:

                        # above the ground
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

                    if self.vel_y < 0:

                        # below the ground, hits the head
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0

            # check for collision with enemies

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                    # if player below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < collision_treshold:
                        self.vel_y = 5
                        # this (dy) will be a negative number - limiting
                        # the distance the player can jump
                        dy = platform.rect.bottom - self.rect.top

                    # if player above platform

                    elif abs((self.rect.bottom + dy) - platform.rect.top) < collision_treshold:
                        self.rect.bottom = platform.rect.top
                        self.rect.y += platform.velocity
                        # player will float just above the platform
                        self.in_air = False
                        dy = 0

                        if platform.move_x:
                            self.rect.x += platform.velocity

                    # hits = pygame.sprite.spritecollide(
                    #     self, platform_group, False)

                    # for platform in hits:

                    #     if self.vel_y >= 0:

                    #         self.rect.bottom = platform.rect.top
                    #         self.in_air = False

                    #         self.rect.x += platform.velocity

                    #     if self.vel_y < 0:

                    #         # below the ground, hits the head
                    #         dy = platform.rect.bottom - self.rect.top
                    #         self.vel_y = 0

                    # update player coordinates (and move him)

            self.rect.x += dx
            self.rect.y += dy

            # END OF CONDITIONAL STATEMENT (game_over == 0)

        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 100:
                self.rect.y -= 5

        # draw player onto screen
        screen.blit(self.image, self.rect)
        #pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        self.walk_right_img = []
        self.walk_left_img = []
        self.walk_index = 0
        self.walk_counter = 0
        self.walk_direction = 0

        for num in range(1, 5):
            img_right = pygame.image.load(
                f'img/guy{num}.png').convert_alpha()
            img_right = scale(img_right, (30, 60))
            self.walk_right_img.append(img_right)
            img_left = pygame.image.load(f'img/guy{num}.png').convert_alpha()
            img_left = flipX(scale(img_left, (30, 60)))
            #img_left = flipX(img_left)
            self.walk_left_img.append(img_left)

        # setting the default image for the sprite (self.walk_index = 0, first item on the list -> guy1.png -> character not moving)

        self.image = self.walk_right_img[self.walk_index]
        dead_image = pygame.image.load('img/ghost.png').convert_alpha()
        self.dead_image = dead_image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.in_air = True

        self.vel_y = 0
        self.jumped = False


# def draw_grid():
#     #SCREEN_SIZE[0] = width,
#     #SCREEN_SIZE[1] = height
#     for line in range(0, 20):
#         pygame.draw.line(screen, (255, 255, 255), (0, line * TILE_SIZE),
#                          (SCREEN_SIZE[0], line * TILE_SIZE))
#         # 0 -------------- 1000
#         pygame.draw.line(screen, (255, 255, 255), (line * TILE_SIZE, 0),
#                          (line * TILE_SIZE, SCREEN_SIZE[1]))
run = True

# Groups

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
exit_group = pygame.sprite.GroupSingle()
platform_group = pygame.sprite.Group()

# Create world and player instances

pickle_in = open(f'level{level}_data', 'rb')
world = World(pickle.load(pickle_in))

player = Player(130, SCREEN_SIZE[1] - 100)

# Create button instances

restart_btn = Button(SCREEN_SIZE[0] // 2 - 50,
                     SCREEN_SIZE[1] // 2 - 200, restart_img)

start_btn = Button(SCREEN_SIZE[0] // 2 - 300,
                   SCREEN_SIZE[1] // 2 - 100, start_img)

exit_btn = Button(SCREEN_SIZE[0] // 2 + 50,
                  SCREEN_SIZE[1] // 2 - 100, exit_img)

while run:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu == True:
        # .draw() returns a boolean, evaluates to True if the button
        # has been clicked
        if start_btn.draw():
            main_menu = False

        if exit_btn.draw():
            run = False
    else:

        world.draw()

        # Monsters

        if game_over == 0:
            blob_group.update()
            platform_group.update()

        blob_group.draw(screen)
        lava_group.draw(screen)
        exit_group.draw(screen)
        platform_group.draw(screen)

        # if player dies
        if game_over == -1:
            # .draw() returns 'action', which has a boolean value
            if restart_btn.draw() == True:
                world = reset_level(level)
                game_over = 0

        if game_over == 1:

            level += 1

            if level < maxlevels:

                world = reset_level(level)
                game_over = 0

            # if we finished the game
            else:

                level = 1
                # reset level
                world = reset_level(level)
                game_over = 0

        # draw_grid()

        # Update player sprite

        # by assigning the value returned by .update() to the variable
        # game_over we create a constant loop where the variable updates
        # itself if a collision with an enemy is triggered, thereby ending
        # the game
        game_over = player.update(game_over)

    pygame.display.update()

pygame.quit()
