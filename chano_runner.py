import pygame
import sys

def display_time():
    current_time = pygame.time.get_ticks() - start_time
    time_surface = font.render(f'Time: {round(current_time/1000,1)} seg.', False, (64,64,64))
    time_rectangle = time_surface.get_rect(center = (400,50))
    screen.blit(time_surface,time_rectangle)
    return current_time

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Luciano's Runner")
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)

game_active = False
start_time = 0
time =0

# test_surface = pygame.Surface((100,200))
# test_surface.fill('darkblue')
# test_font = pygame.font.Font(None,50)

sky_surface = pygame.image.load('graphics/background/sky.png').convert()
ground_surface = pygame.image.load('graphics/background/ground.png').convert()

# score_surface = font.render('My game', False, (64,64,64))
# score_rectangle = score_surface.get_rect(center = (400,50))

snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rectangle = snail_surface.get_rect(midbottom = (600,300))

player_surface = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80,300))
player_gravity = 0


# Init Screen
start_surface = font.render('Start', False, 'Darkblue')
start_rectangle = start_surface.get_rect(midbottom = (400,50))

quit_surface = font.render('Quit', False, 'Darkred')
quit_rectangle = quit_surface.get_rect(midbottom = (400,100))

player_init_surface = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_init_surface = pygame.transform.rotozoom(player_init_surface,0,2)
player_init_rectangle = player_init_surface.get_rect(center = (400,250))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rectangle.collidepoint(event.pos):
                game_active = True
                snail_rectangle.x = 600
                player_rectangle.bottom = 300
                start_time = pygame.time.get_ticks()
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_rectangle.collidepoint(event.pos):
                pygame.quit()
                sys.exit()

        if player_rectangle.bottom == 300:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gravity = -20

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        
        # pygame.draw.rect(screen,'#c0e8ec',score_rectangle)
        # pygame.draw.rect(screen,'#c0e8ec',score_rectangle,10)

        # screen.blit(score_surface,score_rectangle)
        time = display_time()
        
        snail_rectangle.right -= 4
        if snail_rectangle.right < 0: snail_rectangle.left = 800
        screen.blit(snail_surface,snail_rectangle)

        player_gravity += 1
        player_rectangle.bottom += player_gravity
        if player_rectangle.bottom > 300: player_rectangle.bottom = 300
        screen.blit(player_surface,player_rectangle)

        if player_rectangle.colliderect(snail_rectangle):
            game_active = False

    else:
        screen.fill((90,129,162))
        screen.blit(start_surface,start_rectangle)
        screen.blit(quit_surface,quit_rectangle)
        screen.blit(player_init_surface,player_init_rectangle)

    pygame.display.update()
    clock.tick(60)