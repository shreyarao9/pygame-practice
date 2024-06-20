import pygame
from sys import exit
from random import randint

def display_score():
    global speed
    global last_increment_time
    current_time=int(pygame.time.get_ticks() / 1000) - int(start_time / 1000)
    score_surf = test_font.render(f'Score: {current_time}',False,'White')
    score_rect=score_surf.get_rect(center = (500,50))
    screen.blit(score_surf,score_rect)
    if current_time%10==0 and current_time!=0 and current_time>last_increment_time:
            last_increment_time=current_time
            speed+=1
    return current_time

def obstacle_movement(obstacle_list):
    global speed
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= speed #motion of obstacle
            #display corresponding obstacle depending on whether it's at ground level or not
            if obstacle_rect.bottom == 415: screen.blit(rock_surface,obstacle_rect)
            else: screen.blit(circle_surf,obstacle_rect)
        #remove any obstacle that's moved further left than -100
        obstacle_list= [obstacle for obstacle in obstacle_list if obstacle.x>-100]    
        return obstacle_list
    else: return []

def collisions(chara,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if chara.colliderect(obstacle_rect): return False
    return True
    
def bushes(bush_list):
    global speed
    if bush_list:
        for bush_rect in bush_list:
            bush_rect.x -= speed
            screen.blit(bush_surf,bush_rect)
        bush_list= [bush for bush in bush_list if bush.x>=-100]
        if len(bush_list)<11:
            bush_list.append(bush_surf.get_rect(bottomleft=(1000,500)))
        return bush_list
    else: return []

pygame.init()
screen=pygame.display.set_mode((1000,500)) #size of screen
pygame.display.set_caption('Hellaur slowpokes') #window name
clock=pygame.time.Clock() #starts clock
test_font=pygame.font.SysFont('couriernew',30) #sets font and size
game_active=False #game active is true when actively playing
start_time = 0
score=0
chara_gravity=0
count=0
speed=6
last_increment_time=0

#surfaces
sky_surface=pygame.image.load('graphics/sky.png').convert_alpha()
ground_surface=pygame.image.load('graphics/ground.png').convert_alpha()
chara_surface=pygame.image.load('graphics/snail.png').convert_alpha()
rock_surface=pygame.image.load('graphics/rock.png').convert_alpha()
game_message=test_font.render('Press spacebar to start',False,'White')
circle_surf=pygame.image.load('graphics/circ.png').convert_alpha()
bush_surf=pygame.image.load('graphics/bush.png').convert_alpha()

#rects
chara_rect=chara_surface.get_rect(midbottom=(150,410))
chara_stand_rect = chara_surface.get_rect(center = (500,150))
game_message_rect=game_message.get_rect(center=(500,300))
obstacle_rect_list= []
bush_rect_list=[]

#timer
obstacle_timer = pygame.USEREVENT + 1 #creates user-defined event
pygame.time.set_timer(obstacle_timer,1500) #repeatedly creates obstacle_timer event every 1500ms

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            #places chara above ground on left mouseclick on chara
            if event.type== pygame.MOUSEBUTTONDOWN:
                if chara_rect.collidepoint(event.pos) and chara_rect.bottom==410:
                    chara_gravity=-14 
            #places chara above ground on spacebar
            if event.type==pygame.KEYDOWN and chara_rect.bottom==410:
                if event.key==pygame.K_SPACE: 
                    chara_gravity=-14 
            #random obstacle generator whenever obstacle_timer event is created
            if event.type==obstacle_timer:
                if randint(0,2): #generates either 0 or 1, which is equivalent to false or true
                    obstacle_rect_list.append(rock_surface.get_rect(midbottom=(randint(1000,1400),415)))
                else:
                    obstacle_rect_list.append(circle_surf.get_rect(midbottom=(randint(1000,1400),340)))
        else:
            #to start the game when it's not active
            if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                start_time = pygame.time.get_ticks() #sets start time of the game, so that score can be claculated

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,400))
        score=display_score()

        chara_gravity+=1 #though this may seem redundant, there are cases when gravity= -14 which is basically when the chara "jumps"
        chara_rect.y +=chara_gravity #downward motion of chara
        if chara_rect.bottom>410: chara_rect.bottom=410 #to force the chara to not go below the ground level
        screen.blit(chara_surface,chara_rect)
        
        bush_rect_list=bushes(bush_rect_list)
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active=collisions(chara_rect,obstacle_rect_list)

    else:
        screen.fill('#2f2f2f')
        screen.blit(chara_surface,chara_stand_rect)
        screen.blit(game_message,game_message_rect)
        obstacle_rect_list= []
        bush_rect_list=[]
        chara_rect.midbottom=(150,410) #sets chara's pos at ground level. it's useful since game may end when chara is mid-air
        chara_gravity=0
        speed=6
        for i in range(0,1101,100):
            bush_rect_list.append(bush_surf.get_rect(bottomleft=(i,500)))
        if score!=0: #this isn't displayed when game is played for the first time
            end_surf=test_font.render(f'You got rekt lmao, you scored {score} points this time',False,'White')
            end_rect=end_surf.get_rect(center=(500,250))
            screen.blit(end_surf,end_rect)

    pygame.display.update()
    clock.tick(60)