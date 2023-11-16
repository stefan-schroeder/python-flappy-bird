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
speed = 2 
tube_gap = 70  # times 2 for total gap
score = 0
high_score = 0
#window
win_width = 551
win_height = 720
birdPos = (251,300)

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
        if self.rect.y < 720:
            self.rect.y += self.vel
        if self.vel > -2:
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
        if birdPos[0] > self.rect.topleft[0] and not self.passed:
            self.enter = True
        if birdPos[0] > self.rect.topright[0] and self.enter:
            self.passed = True
        if self.enter and self.passed:
            self.exit = True
            score += 1
            self.exit, self.enter, self.passed = False, False, False


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
    global speed
    groundx = 0
    groundy = 520
    tube_gap = 70
    
    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipes = pygame.sprite.Group()
    pipes.add(Pipe(551,-570,top_pipeImg, "top"))
    pipes.add(Pipe(551,370,bottom_pipeImg, "bottom"))
    
    grounds = pygame.sprite.Group()
    grounds.add(Ground(groundx,groundy))

    pygame.display.update()
    speed = 2
    running = True
    
    #once space key is hit, run game
    while running:
        clock.tick(fps)
        ifQuit()
        user_input = pygame.key.get_pressed()
        #blit background
        screen.blit(backgroundImg,(0,0))
        #drawing ground, pipes, and bird
        grounds.draw(screen)
        bird.draw(screen)
        pipes.draw(screen)
        #update all
        font = pygame.font.Font(None, 50)
        score_text = font.render(f'Score: {score}', True, (255,255,255))
        screen.blit(score_text, (win_width//2 - 60, 50))
        #add ground
        if len(grounds) <= 2:
            #-23 to align lines
            grounds.add(Ground(win_width-23,groundy))
        for pipe in pipes:
            if pipe.rect.x == 321:
                pipes.add(Pipe(551,-570,top_pipeImg, "top"))
                pipes.add(Pipe(551,370,bottom_pipeImg, "bottom"))
        pygame.display.update()
main()