import random
import pygame
from pygame.sprite import Sprite

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
speed =2
tube_gap = 70  # times 2 for total gap
score = 0
high_score = 0
#window
win_width = 551
win_height = 720

#bird class

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = bird_Imgs[0]
        self.rect = self.image.get_rect()
        self.rect.x = 251
        self.rect.y = 300
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
        if self.rect.y < 720:
            self.rect.y += self.vel
        if self.vel > -2:
            self.flap = False           
        
        if user_input[pygame.K_SPACE] and not self.flap:
            self.vel = -8
            self.flap = True
    # def checkScore(self):
    #     global score
    #     for pipe in Pipe:
    #         if pipe.rect.x == self.rect.x:
    #             score += 1
    def collides(self,topPipe,bottomPipe,ground):
        #check collision between bird and top pipes
        if pygame.sprite.spritecollide(self,bottomPipe,False):
            return True
        if pygame.sprite.spritecollide(self,topPipe,False):
            return True
        #check collision between bird and bottom pipes
        if pygame.sprite.spritecollide(self,ground,False):
            return True
        #check for collision between pipe and grounds
        if pygame.sprite.spritecollide(self,ground,False):
            return True
        
        


#pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pipeImg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipeImg
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        self.rect.x -= speed
        if self.rect.x <= -50:
            self.kill()


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

    #initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((win_width,win_height))
    pygame.display.set_caption("Flappy Bird!")
    clock = pygame.time.Clock()
    
    # initialize all
    groundx = 0
    groundy = 520
    tube_gap = 70
    ground = pygame.sprite.Group()
    bird = pygame.sprite.Group()
    topPipe = pygame.sprite.Group()
    bottomPipe = pygame.sprite.Group()

    # add to game
    ground.add(Ground(groundx,groundy))
    bird.add(Bird())
    topPipe.add(Pipe(win_width,-500-tube_gap,top_pipeImg))
    bottomPipe.add(Pipe(win_width,300+tube_gap,bottom_pipeImg))

    running = False
    screen.blit(backgroundImg,(0,0))
    screen.blit(startImg,(183,360))
    pygame.display.update()
    

    running = True
    
    #once space key is hit, run game
    while running:
        clock.tick(fps)
        ifQuit()
        user_input = pygame.key.get_pressed()
        #display background
        screen.blit(backgroundImg,(0,0))
        #drawing ground, pipes, and bird
        ground.draw(screen)
        bird.draw(screen)
        topPipe.draw(screen)
        bottomPipe.draw(screen)
        #update all
        topPipe.update()
        bottomPipe.update()
        bird.update(user_input)
        ground.update()
        #check for collision 
        if bird.sprites()[0].collides(topPipe.sprites(),bottomPipe.sprites(),ground.sprites()):
            screen.blit(game_overImg,(183,360))
            running = False
            pygame.display.update()
            pygame.time.delay(1000)
        #add ground
        if len(ground) <= 2:
            #-23 to align lines
            ground.add(Ground(win_width-23,groundy))
        for pipe in topPipe:
            if pipe.rect.x == 321:
                # tube_gap = tube_gap * random.randint(0,3)
                topPipe.add(Pipe(551,-570,top_pipeImg))
                bottomPipe.add(Pipe(551,370,bottom_pipeImg))
        tube_gap = 70
        #update display at end of loop
        pygame.display.update()

main()