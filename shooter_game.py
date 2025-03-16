#! Создай собственный Шутер!

from pygame import *
from random import randint
class GameSprite(sprite.Sprite):
    def __init__(self, img,x,y,w,h,speed):
        super().__init__()
        self.image=transform.scale(image.load(img),(w,h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.speed=speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
  
class Player(GameSprite):
    def update(self):
        key_pressed=key.get_pressed()
        if key_pressed[K_RIGHT]and self.rect.x<600:
            self.rect.x += self.speed
        if key_pressed[K_LEFT]and self.rect.x>5:
            self.rect.x -= self.speed
    def fire(self):
        bullet=Bullet('tnt.png', self.rect.centerx,self.rect.y,50,50,5)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y+=self.speed
        if self.rect.y > 500-self.rect.height:
            self.rect.x = randint(10,700-10-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed=randint(1,3)
            lost+=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y <=0:
            self.kill()

window=display.set_mode((700,500))
display.set_caption('Шутер')
background = transform.scale(image.load('backgr.png'),(700 ,500))
player=Player('creeper.png', 250,400,100,100,5)
button=GameSprite('play.png', 250,200,220,100,0)
bullets=sprite.Group()
enemy_count=6
enemys=sprite.Group()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(0)
font.init()
font1= font.SysFont('Arial',36)
clock = time.Clock()
fps=60

for i in range(enemy_count):
    enemy=Enemy('steve.png',randint(10,700-10-70),-40,50,100,randint(1,3))
    enemys.add(enemy)

game = True
lost=0
score=0
finish=True
menu=True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
        

    if menu:
        window.blit(background, (0,0))
        button.reset()
        pressed = mouse.get_pressed()
        pos=mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu=False
                finish=False
        

    if not finish:
        window.blit(background, (0,0))
        player.reset()
        player.update()
        enemys.update()
        enemys.draw(window)
        bullets.update()
        bullets.draw(window)

        lost_enemy=font1.render('Потрачено: '+str(lost),1,(255,255,255))
        window.blit(lost_enemy,(10,10))

        score_enemy=font1.render('Взорвано: '+str(score),1,(255,255,255))
        window.blit(score_enemy,(500,10))

        sprite_list=sprite.groupcollide(enemys,bullets,True,True)
        for i in range(len(sprite_list)):
            score += 1
            enemy=Enemy('steve.png',randint(10,700-10-70),-40,50,100,randint(1,3))
            enemys.add(enemy)          

        if score >=10:
            finish=True
            text_win=font1.render('Молодец, возьми с полки огурец', 1, (255,255,255))
            window.blit(text_win, (100,250))

        sprite_list = sprite.spritecollide(player,enemys, True)
        if lost >=10 or len(sprite_list)>0:
            finish=True
            text_lose=font1.render('ПОТРАЧЕНО', 1, (255,0,0))
            window.blit(text_lose, (250,250))
    
    display.update()
    clock.tick(fps)
