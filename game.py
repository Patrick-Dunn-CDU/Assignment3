# Import the pygame module
import pygame
import random
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
RLEACCEL,
K_z,
K_UP,
K_DOWN,
K_LEFT,
K_RIGHT,
K_ESCAPE,
K_RETURN,
KEYDOWN,
QUIT,
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet1.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/4,(5*SCREEN_HEIGHT)/6))
        
        self.jforce=30
        self.speed=8
        self.g=0
        self.jump=False
        self.cjf= -self.jforce
        self.facing=1
        self.pdelay=10
        self.cdelay=self.pdelay
        self.mhp=10
        self.hp=self.mhp
        self.lives=3
    
    def update(self, pressed_keys):
        if self.hp <= 0:
            self.lives -=1
            self.hp = self.mhp
        
        if self.g<=5:
            self.g+=1
        if self.jump==False:
            self.cjf= -self.jforce
        if self.cdelay>0:
            self.cdelay-=1
            
        self.rect.move_ip(0,self.g)
        if pressed_keys[K_UP]:
            if self.jump==False:
                self.jump=True
        if self.jump:
            self.rect.move_ip(0,self.cjf)
            self.cjf+=2
            #move_up_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
            self.facing= -1
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
            self.facing=1
        #if pressed_keys[K_DOWN]:
            #self.rect=pygame.rect()
        if pressed_keys[K_z]:
            if self.cdelay==0:
                new_proj=Projectile(self.facing)
                projectiles.add(new_proj)
                all_sprites.add(new_proj)
                self.cdelay=self.pdelay
        
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH/2:
            self.rect.right = SCREEN_WIDTH/2
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT-20:
            self.rect.bottom = SCREEN_HEIGHT-20
            self.g=0
            self.jump=False
    
    def reset(self):
        self.rect.center=(SCREEN_WIDTH/4,(5*SCREEN_HEIGHT)/6)
        self.g=0
        self.jump=False
        self.cjf= -self.jforce
        self.facing=1
        self.cdelay=self.pdelay
        self.hp=self.mhp
        self.lives=3
    
    def __str__(self):
        return("Player")
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("jet3.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH + 200*enemy_num,
                SCREEN_HEIGHT-(180*random.randint(0, 1))-20,
            )
        )
        self.speed = 5
        self.mhp = 2
        self.hp = self.mhp

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
        if self.hp==1:
            self.surf = pygame.image.load("jet2.png").convert()
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        if self.hp <= 0:
            self.kill()
    
    def reset(self):
        self.kill()

class Projectile(pygame.sprite.Sprite):
    def __init__(self,facing):
        super(Projectile,self).__init__()
        
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(player.rect.centerx,player.rect.centery))
        
        self.facing=facing
        self.speed=10
    
    def update(self):
        self.rect.move_ip(self.speed*self.facing,0)
        
        if self.rect.left < 0:
            self.kill()
        if self.rect.right > SCREEN_WIDTH:
            self.kill()
        if self.rect.top <= 0:
            self.kill()
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.kill()
    
    def reset(self):
        self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self,life,x,y):
        super(Collectible, self).__init__()
        self.life=life
        if self.life:
            self.surf = pygame.image.load("heart1.png").convert()
        else:
            self.surf = pygame.image.load("heart2.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(x,y)
        )
        self.speed = 1

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    #def update(self):   
    
    def reset(self):
        self.kill()
        

# Setup for sounds. Defaults are good.
pygame.mixer.init()
pygame.font.init()
# Initialize pygame
pygame.init()
pygame.display.set_caption("Jet Game")
f=pygame.font.SysFont('Copperplate',40)

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

player=Player()
all_sprites.add(player)



# Fill the screen with black
screen.fill((0, 0, 0))
# Draw all sprites
for entity in all_sprites:
    screen.blit(entity.surf, entity.rect)
# Update the display
pygame.display.flip()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

run=True
alive=True
load=True
score=1000
enemy_num=0
won=False
while run:
    if alive:
        if load:
            for i in range(10):
                if i%5==0:
                    new_collectible=Collectible(True,800*(i+1),SCREEN_HEIGHT-110)
                else:
                    new_collectible=Collectible(False,800*(i+1),SCREEN_HEIGHT-110)
                collectibles.add(new_collectible)
                all_sprites.add(new_collectible)
            load=False
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
            elif event.type==ADDENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                enemy_num+=1
        
    # Get all the keys currently pressed
        pressed_keys = pygame.key.get_pressed()
    # Update the player sprite based on user keypresses
        player.update(pressed_keys)
        enemies.update()
        projectiles.update()

    # Fill the screen with black
        screen.fill((135, 206, 235))
    # Draw all sprites
        for entity in all_sprites:
            if player.rect.right>=SCREEN_WIDTH/2:
                if player.facing==1:
                    if str(entity) !="Player":
                        entity.rect.move_ip(-player.speed,0)
            screen.blit(entity.surf, entity.rect)
        if player.rect.right>=SCREEN_WIDTH/2:
            player.rect.move_ip(-1,0)
        
        for i in range(10):
            if i < player.hp:
                surf = pygame.image.load("heart1.png").convert()
            else:
                surf = pygame.image.load("heart2.png").convert()
            surf.set_colorkey((255, 255, 255), RLEACCEL)
            rect = surf.get_rect(center=(SCREEN_WIDTH/2-225+(50*i),20))
            screen.blit(surf,rect)
        
        Lives=f.render(f'Lives: {player.lives}',False,(255,255,255))
        showScore=f.render(f'Score: {score}',False,(255,255,255))
        screen.blit(Lives,(10,10))
        screen.blit(showScore,(10,50))
        instr=f.render(f'Collect all the hearts to win!',False,(255,255,255))
        screen.blit(instr,(SCREEN_WIDTH/2-190,150))
        
        shot_list=pygame.sprite.groupcollide(enemies, projectiles,False,True)
        for hit in shot_list:
            hit.hp -= 1
            score += 100
        hit_list= pygame.sprite.spritecollide(player, enemies,True)
        for hit in hit_list:
            player.hp-=1
        if player.lives <= 0:
            alive=False
            load=True
        collect_list= pygame.sprite.spritecollide(player, collectibles,True)
        for collect in collect_list:
            if collect.life==True:
                if player.lives<3:
                    player.lives+=1
            elif collect.life==False:
                if player.hp<player.mhp:
                    player.hp+=1
            if len(collectibles)==0:
                alive=False
                won=True
    else:
    # Fill the screen with black
        screen.fill((0, 0, 0))
        if won:
            wp=f.render(f'YOU WIN!',False,(255,255,255))
            screen.blit(wp,(SCREEN_WIDTH/2-90,SCREEN_HEIGHT/2-70))
            pa=f.render(f'Press ENTER to play again',False,(255,255,255))
            screen.blit(pa,(SCREEN_WIDTH/2-170,SCREEN_HEIGHT/2+10))
        else:
            go=f.render(f'GAME OVER',False,(255,255,255))
            screen.blit(go,(SCREEN_WIDTH/2-90,SCREEN_HEIGHT/2-70))
            ta=f.render(f'Press ENTER to try again',False,(255,255,255))
            screen.blit(ta,(SCREEN_WIDTH/2-170,SCREEN_HEIGHT/2+10))
        seeScore=f.render(f'Score: {score}',False,(255,255,255))
        screen.blit(seeScore,(SCREEN_WIDTH/2-90,SCREEN_HEIGHT/2-30))
        for event in pygame.event.get():
            if event.type==KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                if event.key == K_RETURN:
                    alive = True
                    score=0
                    enemy_num=0
                    won=False
                    for entity in all_sprites:
                        print(entity)
                        entity.reset()
            elif event.type == QUIT:
                run = False
        
    # Update the display
    pygame.display.flip()
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(60)


pygame.quit()