import pygame
from sys import exit
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


pygame.init()

screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("DUNO the Runner")
clock = pygame.time.Clock()
font = pygame.font.Font(os.path.join(BASE_DIR, "Font", "Pixeltype.ttf"), 50)


surface_sky = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Sky.png")).convert()


surface_ground = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "ground.png")).convert()



# text surfaces and rectangles
surface_DUNO = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "DUNO2.png")).convert_alpha()
DUNO_resized = pygame.transform.rotozoom(surface_DUNO, 0, 0.3)
DUNO_rectangle = DUNO_resized.get_rect(center = (400, 107))

rect1 = pygame.Rect(330, 150, 140, 50)
surface_font = font.render("CLICK DUNO TO RUN", False, "black")
surface_font_2 = font.render("REPLAY", False, "black")
font_rectangle = surface_font.get_rect(center = (400, 370))
font_2_rectangle = surface_font_2.get_rect(center = (400, 180))

rect2 = pygame.Rect(355, 70, 90, 60)
starting_time = 0
def score_counter():
    minutes = pygame.time.get_ticks()
    total_score = minutes//3000
    return total_score

surface_gameover = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "GAME OVER2.png")).convert_alpha()
gameover_resized = pygame.transform.rotozoom(surface_gameover, 0, 1)
gameover_rectangle = gameover_resized.get_rect(midbottom = (400, 525))




# obstacles
obstacle_snail1_rect_list = []
obstacle_fly1_rect_list = []
obstacle_position_change = 4

def obstacle_movement(obstacle_change, obstacle_list, surface):
    for obstacle_rect in obstacle_list:
        obstacle_change += 0.000005
        obstacle_rect.x -= obstacle_change

        screen.blit(surface, obstacle_rect)
    if obstacle_list == None:
        return obstacle_change, []
    else: 
        obstacle_list = [obstacle_rect for obstacle_rect in obstacle_list if obstacle_rect.x > -100]
        return obstacle_change, obstacle_list


surface_snail1 = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Snail", "snail1.png")).convert_alpha()
surface_snail2 = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Snail", "snail2.png")).convert_alpha()

surface_fly1 = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Fly", "Fly1.png")).convert_alpha()
surface_fly2 = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Fly", "Fly2.png")).convert_alpha()




# the player
surface_player_stand = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Player", "player_stand.png")).convert_alpha()
surface_player_walk_1 = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Player", "player_walk_1.png")).convert_alpha()
surface_player_walk_2 = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Player", "player_walk_2.png")).convert_alpha()
surface_player_jump = pygame.image.load(os.path.join(BASE_DIR, "Graphics", "Player", "jump.png")).convert_alpha()

player_ground_rectangle = surface_player_stand.get_rect(bottomleft = (120, 300))
player_stand_resized = pygame.transform.rotozoom(surface_player_stand, 0, 2)
player_ground_rectangle_2 = player_stand_resized.get_rect(center = (400, 215))
player_gravity = 6/31
player_speed = 0
is_jumping = False


game_active = False
first_time_playing = True
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

walk_1 = True
walk_timer = pygame.USEREVENT + 2
pygame.time.set_timer(walk_timer, 250)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_speed = 6
                is_jumping = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not game_active:
                if first_time_playing and player_ground_rectangle_2.collidepoint(mouse_pos):
                    game_active = True
                    starting_time = pygame.time.get_ticks()//3000
                    first_time_playing = False
                elif rect1.collidepoint(mouse_pos):
                    game_active = True
                    starting_time = pygame.time.get_ticks()//3000
        if game_active:
            if event.type == walk_timer:
                walk_1 = not walk_1
            if event.type == obstacle_timer:
                if random.randint(0,2):
                    obstacle_snail1_rect_list.append(surface_snail1.get_rect(bottomleft = (random.randint(900, 1200), 300)))
                else:
                    obstacle_fly1_rect_list.append(surface_fly1.get_rect(bottomleft = (random.randint(900, 1200), 200)))
       


    mouse_pos = pygame.mouse.get_pos()
    screen.blit(surface_sky, (0, 0))
    screen.blit(surface_ground, (0, 300))

    if first_time_playing:
        screen.blit(surface_font, font_rectangle)
        screen.blit(DUNO_resized, DUNO_rectangle)
        screen.blit(player_stand_resized, player_ground_rectangle_2)



    elif game_active:

        
        total_score = f"{score_counter()-starting_time}" 
        surface_score = font.render(total_score, False, "black")
        score_rectangle = surface_font.get_rect(center = (536.5-(len(total_score)*5), 103.25))
        screen.blit(surface_score, score_rectangle)
        pygame.draw.rect(screen, (0,0,0), rect2, 5, 15)

            

        if is_jumping:
            screen.blit(surface_player_jump, player_ground_rectangle)
            player_speed -= player_gravity
            player_ground_rectangle.bottom -= player_speed
            if player_ground_rectangle.bottom >= 300:
                player_ground_rectangle.bottom = 300
                is_jumping = False
                player_speed = 0
        else:
            if walk_1:
                screen.blit(surface_player_walk_1, player_ground_rectangle)
            else:
                screen.blit(surface_player_walk_2, player_ground_rectangle)

        if walk_1:
            obstacle_position_change, obstacle_snail1_rect_list = obstacle_movement(obstacle_position_change, obstacle_snail1_rect_list, surface_snail1)
            obstacle_position_change, obstacle_fly1_rect_list = obstacle_movement(obstacle_position_change, obstacle_fly1_rect_list, surface_fly1)
        else:
            obstacle_position_change, obstacle_snail1_rect_list = obstacle_movement(obstacle_position_change, obstacle_snail1_rect_list, surface_snail2)
            obstacle_position_change, obstacle_fly1_rect_list = obstacle_movement(obstacle_position_change, obstacle_fly1_rect_list, surface_fly2)

        for obstacle_rect in obstacle_snail1_rect_list:
                if player_ground_rectangle.colliderect(obstacle_rect):
                    game_active = False
                    obstacle_snail1_rect_list = []
                    obstacle_fly1_rect_list = []
                    obstacle_position_change = 4
                    player_ground_rectangle.bottom = 300
                    is_jumping = False

        for obstacle_rect in obstacle_fly1_rect_list:
            if player_ground_rectangle.colliderect(obstacle_rect):
                    game_active = False
                    obstacle_fly1_rect_list = []
                    obstacle_snail1_rect_list = []
                    obstacle_position_change = 4
                    player_ground_rectangle.bottom = 300
                    is_jumping = False




    else:
        pygame.draw.rect(screen, (0,0,0), rect1, 5, 20)
        screen.blit(surface_font_2, font_2_rectangle)    
        screen.blit(gameover_resized, gameover_rectangle)
        resultant_score = font.render(f"YOUR SCORE : {total_score}", False, "black")
        screen.blit(resultant_score, resultant_score.get_rect(center = (400, 100)))




    pygame.display.update()
    clock.tick(60)
