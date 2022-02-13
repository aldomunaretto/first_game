from turtle import back
import pygame
from sys import exit
from random import randint, choice


# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.gravity = 0
        self.player_index = 0
        player_walk1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1,player_walk2]
        self.player_jump_surface = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
        
        self.image = self.player_walk[self.player_index] # Must contain image attribute
        self.rect = self.image.get_rect(midbottom = (80,300)) # Must contain rect attribute

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump_surface
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): 
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'fly':
            fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1,fly_frame2]
            y_pos = 210
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1,snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): 
                self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.right < 0:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()


# Functions
def display_time():
    current_time = pygame.time.get_ticks() - start_time
    time_surface = font.render(f'Time: {round(current_time/1000,1)} sec', False, (64,64,64))
    time_rectangle = time_surface.get_rect(center = (400,50))
    screen.blit(time_surface,time_rectangle)
    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True    


# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Luciano's Runner")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
background_music = pygame.mixer.Sound('audio/dynamite.mp3')
background_music.set_volume(0.2)
background_music.play(loops = -1)


# Variables initialization
game_active = False
start_time = 0
time = 0


# Groups
## Player
player = pygame.sprite.GroupSingle()
player.add(Player())

## Obstacles
obstacle_group = pygame.sprite.Group()


# Init Screen
start_surface = font.render('Click to Start', False, 'Darkred')
start_rectangle = start_surface.get_rect(midbottom = (400,350))

title_surface = font.render("Luciano's First Pixel Runner", False, 'Darkblue')
title_rectangle = title_surface.get_rect(midbottom = (400,50))

player_init_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_init_surface = pygame.transform.rotozoom(player_init_surface,0,2)
player_init_rectangle = player_init_surface.get_rect(center = (400,200))


# Game Screen
sky_surface = pygame.image.load('graphics/background/sky.png').convert()
ground_surface = pygame.image.load('graphics/background/ground.png').convert()


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rectangle.collidepoint(event.pos):
                game_active = True
                start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        
        time = display_time()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collisions
        game_active = collisions()

    else:
        screen.fill((90,129,162))
        last_time_message_surface = font.render(f'Your last run took {round(time/1000,1)} sec',False,(11,196,169))
        last_time_message_rectangle = last_time_message_surface.get_rect(midtop = (400,360))
        if time != 0: screen.blit(last_time_message_surface,last_time_message_rectangle) 
        screen.blit(start_surface,start_rectangle)
        screen.blit(title_surface,title_rectangle)
        screen.blit(player_init_surface,player_init_rectangle)

    pygame.display.update()
    clock.tick(60)