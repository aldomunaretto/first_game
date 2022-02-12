import pygame
from sys import exit
from random import randint

#Functions
def display_time():
    current_time = pygame.time.get_ticks() - start_time
    time_surface = font.render(f'Time: {round(current_time/1000,1)} sec', False, (64,64,64))
    time_rectangle = time_surface.get_rect(center = (400,50))
    screen.blit(time_surface,time_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.left > 0]
        return obstacle_list
    else:
        return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
    return True    

def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump_surface
    else:
        player_index += 0.1
        if player_index >= len(player_walk_surface): player_index = 0
        player_surface = player_walk_surface[int(player_index)]


# Pygame initialization
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Luciano's Runner")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)

# Vaiables initialization
game_active = False
start_time = 0
time = 0
player_index = 0
player_gravity = 0
obstacle_rect_list = []

# test_surface = pygame.Surface((100,200))
# test_surface.fill('darkblue')
# test_font = pygame.font.Font(None,50)

sky_surface = pygame.image.load('graphics/background/sky.png').convert()
ground_surface = pygame.image.load('graphics/background/ground.png').convert()

# score_surface = font.render('My game', False, (64,64,64))
# score_rectangle = score_surface.get_rect(center = (400,50))


#Obstacles
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_rectangle = snail_surface.get_rect(midbottom = (600,300))

fly_surface = pygame.image.load('graphics/fly/fly1.png').convert_alpha()

# Player
player_walk1_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk2_surface = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk_surface = [player_walk1_surface,player_walk2_surface]
player_jump_surface = pygame.image.load('graphics/player/player_jump.png').convert_alpha()
player_surface = player_walk_surface[player_index]
player_rectangle = player_surface.get_rect(midbottom = (80,300))


# Init Screen
start_surface = font.render('Click to Start', False, 'Darkred')
start_rectangle = start_surface.get_rect(midbottom = (400,350))

title_surface = font.render("Luciano's Pixel Runner", False, 'Darkblue')
title_rectangle = title_surface.get_rect(midbottom = (400,50))

player_init_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_init_surface = pygame.transform.rotozoom(player_init_surface,0,2)
player_init_rectangle = player_init_surface.get_rect(center = (400,200))

# Timer
obstacle_timer = pygame.USEREVENT +1
pygame.time.set_timer(obstacle_timer,1500)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rectangle.collidepoint(event.pos):
                game_active = True
                # snail_rectangle.x = 600
                player_rectangle.bottom = 300
                start_time = pygame.time.get_ticks()
                
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if quit_rectangle.collidepoint(event.pos):
        #         pygame.quit()
        #         sys.exit()

        if game_active:
            if player_rectangle.bottom == 300:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player_rectangle.collidepoint(event.pos):
                        player_gravity = -20

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        
        # pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
        # pygame.draw.rect(screen,'#c0e8ec',score_rectangle,10)

        # screen.blit(score_surface,score_rectangle)
        time = display_time()
        
        # snail_rectangle.right -= 4
        # if snail_rectangle.right < 0: snail_rectangle.left = 800
        # screen.blit(snail_surface,snail_rectangle)

        # Player
        player_gravity += 1
        player_rectangle.bottom += player_gravity
        if player_rectangle.bottom > 300: player_rectangle.bottom = 300
        player_animation()
        screen.blit(player_surface,player_rectangle)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rectangle, obstacle_rect_list)

    else:
        screen.fill((90,129,162))
        obstacle_rect_list.clear()
        player_rectangle.bottom = 300
        player_gravity = 0

        last_time_message_surface = font.render(f'Your last run took {round(time/1000,1)} sec',False,(11,196,169))
        last_time_message_rectangle = last_time_message_surface.get_rect(midtop = (400,360))
        if time != 0: screen.blit(last_time_message_surface,last_time_message_rectangle) 
        screen.blit(start_surface,start_rectangle)
        screen.blit(title_surface,title_rectangle)
        screen.blit(player_init_surface,player_init_rectangle)

    pygame.display.update()
    clock.tick(60)