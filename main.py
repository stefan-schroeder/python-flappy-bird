import pygame
import random
from pygame.sprite import Sprite

#initialize pygame
pygame.init()

#images
bird_Imgs = [pygame.image.load('images/bird_up.png'),
               pygame.image.load('images/bird_mid.png'),
               pygame.image.load('images/bird_down.png')]
backgroundImg = pygame.image.load("images/background.png")
game_overImg = pygame.image.load('images/game_over.png')
groundImg = pygame.image.load('images/ground.png')
bottom_pipeImg = pygame.image.load('images/pipe_bottom.png')
top_pipeImg = pygame.image.load('images/pipe_top.png')
startImg = pygame.image.load('images/start.png')


#global variables
fps = 60
speed = 2
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
birdPos = (251,300)
gamestate = 'start'
#window
win_width = 551
win_height = 720
screen = pygame.display.set_mode((win_width,win_height))

#bird class

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = bird_Imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = birdPos[0]
        self.rect.y = birdPos[1]
        self.vel = 0
        self.index = 0
        self.flap = False

    def update(self,user_input):
        #animate bird 
        self.index += 1
        if self.index >=30:
            self.index = 0
        self.image = bird_Imgs[self.index//10]

        self.image = pygame.transform.rotate(self.image, self.vel * -7)
    
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y += self.vel
        if self.vel ==0:
            self.flap = False           
        
        if user_input[pygame.K_SPACE] and not self.flap:
            self.vel = -7
            self.flap = True       
        


#pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pipeImg, pipeType):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipeImg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = pipeType
        self.enter, self.exit, self.passed = False, False, False
    def update(self):
        self.rect.x -= speed
        if self.rect.x <= -50:
            self.kill()
        #score
        global score
        if self.type == 'top':
            
            if birdPos[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if birdPos[0] > self.rect.topright[0] and self.enter:
                self.passed = True
            if self.enter and self.passed and not self.exit:
                self.exit = True
                score += 1
                print(score)    

#ground class
class Ground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        Sprite.__init__(self)
        self.image = groundImg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    # will be constantly updated in main loop
    def update(self):
        self.rect.x -= speed
        #reset the ground to original position
        if self.rect.x <-win_width:
            self.kill()



# function to handle quitting.
def ifQuit():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def main():
    pygame.display.set_caption("Flappy Bird!")
    clock = pygame.time.Clock()
    
    # initialize all
    # add to game
    groundx, groundy = 0,520
    grounds = pygame.sprite.Group()
    grounds.add(Ground(groundx,groundy))

    #init bird
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipe_clock = 0
    pipes = pygame.sprite.Group()
    
    global gamestate
    global score

    #start screen
    while gamestate == 'start':
        clock.tick(fps)
        ifQuit()
        user_input = pygame.key.get_pressed()
        screen.blit(backgroundImg,(0,0))
        screen.blit(startImg,(win_width//2-100,win_height//2-100))
        if user_input [pygame.K_SPACE]:
            gamestate = 'play'
        pygame.display.update()

    
    #once space key is hit, run game
    while gamestate == 'play':
        clock.tick(fps)
        ifQuit()
        user_input = pygame.key.get_pressed()
        #blit background
        screen.blit(backgroundImg,(0,0))
        #drawing ground, pipes, and bird
        grounds.draw(screen)
        bird.draw(screen)
        pipes.draw(screen)
        #update sprites
        pipes.update()
        bird.update(user_input)
        grounds.update()
        #update score
        score_text = font.render(f'Score: {score}', True, (255,255,255))
        screen.blit(score_text, (10,10))
        
        #check for collision/end game
        collision_pipes = pygame.sprite.spritecollide(bird.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(bird.sprites()[0], grounds, False)
        if collision_pipes or collision_ground or bird.sprites()[0].rect.y < 0 or bird.sprites()[0].rect.y > 500:
            gamestate = 'end'
            screen.blit(game_overImg,(win_width//2-100,win_height//2-100))
        
        #add ground
        if len(grounds) <= 2:
            #-23 to align lines
            grounds.add(Ground(win_width-23,groundy))

        #add pipes
        if pipe_clock <= 0 and bird.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-600, -480)
            y_bottom = y_top + random.randint(90, 130) + bottom_pipeImg.get_height()
            pipes.add(Pipe(x_top, y_top, top_pipeImg, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_pipeImg, 'bottom'))
            pipe_clock = random.randint(180, 250)
        pipe_clock -= 1
        #update screen
        pygame.display.update()
    while gamestate == 'end':
        clock.tick(fps)
        ifQuit()
        user_input = pygame.key.get_pressed()
        screen.blit(backgroundImg,(0,0))
        screen.blit(game_overImg,(win_width//2-100,win_height//2-100))
        score_text = font.render(f'Score: {score}', True, (255,255,255))
        screen.blit(score_text, (10,10))
        pygame.display.update()
        if user_input[pygame.K_r]:
            gamestate = 'start'
            main()
            
main()