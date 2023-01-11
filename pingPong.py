import random
import pygame
import sys

pygame.init()

#GAMEVARIABLES
EXITGAME = False
GAMEOVER = False
PONG_COLOR = (244, 214, 11)
CLOCK = pygame.time.Clock()
FPS = 60
SCREEN = pygame.display.set_mode((1200,600),pygame.RESIZABLE)
pygame.display.set_caption("PingPong Game - By Parth")
pygame.display.set_icon(pygame.image.load('pp.png').convert_alpha())

Survival_time = 0

#Ball
WIDTH = 1200
HEIGHT = 600
b_x = 600 
b_y = 300
x_add = True
y_add = True
b_speed = 0.01*WIDTH
counter  = 0

#Making High Score
try :
    with open('hiscore.txt') as file:
        HISCORE = int(file.read())
except Exception as e:
    f = open('hiscore.txt','w')
    f.write("0") 
    HISCORE = 0

def checkScore():
    global Survival_time,HISCORE
    if Survival_time>HISCORE:
        HISCORE = Survival_time
        return True
    
    
def loadImage(path):
    return pygame.image.load(path).convert_alpha()

def resizeImage(img,height,width):
    return pygame.transform.scale(img,(width,height))

def blitImage(img,screen,x,y):
    return screen.blit(img,(x,y))

def renderText(fontfile,text,x,y,fontsize):
    font = pygame.font.Font(fontfile,fontsize)
    font = font.render(text,True,(0,0,0),PONG_COLOR)
    SCREEN.blit(font,(x,y))


def restartGame():
    pygame.time.wait(2000)
    global y_add,x_add,b_y,b_x,GAMEOVER,b_speed,Survival_time
    x_add = True
    y_add= True
    b_x = WIDTH//2
    b_y = HEIGHT//2
    b_speed += 2
    Survival_time  = 0
    GAMEOVER = False
    with open('hiscore.txt','w') as f:
            f.write(str(HISCORE))

def checkGameOver():
    global GAMEOVER
    if b_x<=0 or b_x+2*b_radius>WIDTH:
        GAMEOVER  =  True
        




def checkMargin(y,margin,slider_height,height):
    if y <= margin:
        y = margin
    elif (y+slider_height) >= (height - margin):
        y = height - margin - slider_height

    return y

def moveBall(x,y,speed,x_add=True,y_add=True):
    if x_add:
        x+=speed
    else:
        x-=speed

    if y_add:
        y+=speed
    else:
        y-=speed

    return (x,y)


def checkyCollisons(y):
    if y<=margin:
        return True
    elif y+b_radius>=HEIGHT:
        return True
    return False

def slider_collisons(slider_rect,ball_rect):
    if pygame.Rect.colliderect(slider_rect,ball_rect):
        return True
    else:
        return False



def bounce(x_Add,y_Add,slider_rect,ball_rect,computer_slider_rect):
    def bouncey(y_a):
        if y_a:
            y_a=False
        else:
            y_a=True
        return y_a

    def bouncex(x_a):
        if x_a:
            x_a=False
        else:
            x_a=True
        return x_a

    if checkyCollisons(b_y):
        y_Add = bouncey(y_Add)
    
    elif slider_collisons(slider_rect,ball_rect):
        x_Add = bouncex(x_Add)

    elif slider_collisons(computer_slider_rect,ball_rect):
        x_Add = bouncex(x_Add)

    return (x_Add,y_Add)
    




while not EXITGAME:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            with open('hiscore.txt','w') as f:
                f.write(str(HISCORE))
            EXITGAME = True

    counter += 1


    if counter%(FPS*20)==0:
        b_speed += 2

    if counter%FPS==0:
     Survival_time  += 1

    #Height And Width
    WIDTH = pygame.display.get_window_size()[0]
    HEIGHT = pygame.display.get_window_size()[1]
    
    #Setting Background
    bgImage = loadImage('bg.png')
    bgImage = resizeImage(bgImage,HEIGHT,WIDTH)
    blitImage(bgImage,SCREEN,0,0)

    #Making Player Slider
    margin = 0.015*WIDTH
    p_x = margin
    p_height = 0.4*HEIGHT
    p_width = 0.03*WIDTH
    p_y = pygame.mouse.get_pos()[1]
    p_y = checkMargin(p_y,margin+margin/2,p_height,HEIGHT)
    
    playerSlider_RECT = pygame.Rect(p_x,p_y,p_width,p_height)
    playerSlider = pygame.draw.rect(SCREEN,PONG_COLOR,playerSlider_RECT,border_radius=2)

    
    # Making COMPUTER SLIDER
    c_height = 0.4*HEIGHT
    c_width = 0.03*WIDTH
    c_x = WIDTH - margin-c_width
    c_y = b_y -10
    c_y = checkMargin(c_y,margin+margin/2,c_height,HEIGHT)
    
    computerSlider_RECT = pygame.Rect(c_x,c_y,c_width,c_height)
    computerSlider = pygame.draw.rect(SCREEN,PONG_COLOR,computerSlider_RECT,border_radius=2)


    #Making Ball
    b_radius = 0.02*WIDTH
    try:
        x_add = bounce(x_add,y_add,playerSlider_RECT,Ball,computerSlider_RECT)[0]
        y_add = bounce(x_add,y_add,playerSlider_RECT,Ball,computerSlider_RECT)[1]
    except Exception as e:
        print(e)
    b_x = moveBall(b_x,b_y,b_speed,x_add,y_add)[0]
    b_y = moveBall(b_x,b_y,b_speed,x_add,y_add)[1]

    Ball = pygame.draw.circle(SCREEN,PONG_COLOR,(b_x,b_y),b_radius)
    

    
    #Making Custom Cursor
    pygame.mouse.set_visible(False)
    cursor_x = pygame.mouse.get_pos()[0]
    cursor_y = pygame.mouse.get_pos()[1]
    cursor_img = loadImage('cursor.png')
    cursor_img = resizeImage(cursor_img,0.05*HEIGHT,0.03*WIDTH)
    blitImage(cursor_img,SCREEN,cursor_x,cursor_y)



    
    #Checking GameOver
    checkGameOver()
    if GAMEOVER:
        restartGame()

    checkScore()

    #Rendering Survival Time
    text = f"SURVIVAL TIME  {Survival_time} secs"
    size  =  int(0.05*WIDTH//1)
    renderText("GUMDROP.ttf",text,WIDTH//2 - 5*size,10,size)

    hiscore = f" HIGHEST SURVIVAL TIME  {str(HISCORE)} secs"
    size  =  int(0.05*WIDTH//1)
    renderText("GUMDROP.ttf",hiscore,WIDTH//2 - 5*size,size+20,size)

    

    pygame.display.update()
    CLOCK.tick(FPS)
    

pygame.quit()
sys.exit("Game Exited!")
