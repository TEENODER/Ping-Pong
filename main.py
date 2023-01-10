import random
import pygame
import sys

pygame.init()

#GAMEVARIABLES
EXITGAME = False
GAMEOVER = False
PONG_COLOR = (244, 214, 11)
CLOCK = pygame.time.Clock()
FPS = 30
SCREEN = pygame.display.set_mode((1200,600),pygame.RESIZABLE)
pygame.display.set_caption("PingPong Game - By Parth")

#Ball
b_x = 600 
b_y = 300
x_add = True
y_add = True

def loadImage(path):
    return pygame.image.load(path)

def resizeImage(img,height,width):
    return pygame.transform.scale(img,(width,height))

def blitImage(img,screen,x,y):
    return screen.blit(img,(x,y))

def restartGame():
    pygame.time.wait(2000)
    global y_add,x_add,b_y,b_x,GAMEOVER,b_speed
    x_add = True
    y_add= True
    b_x = WIDTH//2
    b_y = HEIGHT//2
    b_speed += 2
    
    GAMEOVER = False

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
            EXITGAME = True


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
    b_speed = 7
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
    

    pygame.display.update()
    CLOCK.tick(FPS)
    

pygame.quit()
sys.exit("Game Exited!")
