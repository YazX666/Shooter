from pygame import *
from random import randint
from time import time as timer
font.init()
font1=font.SysFont('Arial',36)
victory=font1.render('YOU WIN!',True,(255,255,255))
lose=font1.render('YOU LOSE!',True,(180,0,0))
font2=font.SysFont('Arial',36)
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sfx=mixer.Sound('fire.ogg')
font.init()
font2=font.SysFont('Arial',36)
img_bg="galaxy.jpg"
img_bullet="bullet.png"
img_hero="rocket.png"
img_enemy="ufo.png"
img_ast="asteroid.png"
score=0
goal=10
lost=0
max_lost=3
life=3
class GameSprite(sprite.Sprite):
    def __init__(self,p_img,p_x,p_y,size_x,size_y,p_spd):
        sprite.Sprite.__init__(self)
        self.image=transform.scale(image.load(p_img),(size_x,size_y))
        self.spd=p_spd
        self.rect=self.image.get_rect()
        self.rect.x=p_x
        self.rect.y=p_y
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x>5:
            self.rect.x-=self.spd
        if keys[K_RIGHT] and self.rect.x<win_width-80:
            self.rect.x+=self.spd
    def fire(self):
        bullet=Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.spd
        global lost
        if self.rect.y>win_height:
            self.rect.x=randint(80,win_width-80)
            self.rect.y=0
            lost+=1
class Bullet(GameSprite):
    def update(self):
        self.rect.y+=self.spd
        if self.rect.y<0:
            self.kill()
win_width=700
win_height=500
display.set_caption("Shooter")
win=display.set_mode((win_width,win_height))
bg=transform.scale(image.load(img_bg),(win_width,win_height))
ship=Player(img_hero,5,win_height-100,80,100,10)
monsters=sprite.Group()
for i in range(1,6):
    monster=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    monsters.add(monster)
asteroids=sprite.Group()
for i in range(1,3):
    asteroid=Enemy(img_ast,randint(30,win_width-30),-40,80,50,randint(1,7))
    asteroids.add(asteroid)
bullets=sprite.Group()
finish=False
run=True
rel_time=False
fired=0
while run:
    for e in event.get():
        if e.type==QUIT:
            run=False
        elif e.type==KEYDOWN:
            if e.key==K_SPACE:
                if fired<5 and rel_time==False:
                    fired+=1
                    fire_sfx.play()
                    ship.fire()
                if fired>=5 and rel_time==False:
                    last_time=timer()
                    rel_time=True
    if not finish:
        win.blit(bg,(0,0))
        ship.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        ship.reset()
        monsters.draw(win)
        asteroids.draw(win)
        bullets.draw(win)
        if rel_time==True:
            now_time=timer()
            if now_time-last_time<3:
                reload=font2.render('Reload in progress...',1,(150,0,0))
                win.blit(reload,(260,460))
            else:
                fired=0
                rel_time=False
        collides=sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score=score+1
            monster=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life-=1
        if life==0 or lost>=max_lost:
            finish=True
            win.blit(lose,(200,200))
        if score>=goal:
            finish=True
            win.blit(victory,(200,200))
        text=font2.render("Score: "+str(score),1,(255,255,255))
        win.blit(text,(10,20))
        text_ls=font2.render("Missed: "+str(lost),1,(255,255,255))
        win.blit(text_ls,(10,50))
        if life==3:
            life_color=(0,150,0)
        if life==2:
            life_color=(150,150,0)
        if life==1:
            life_color=(150,0,0)
        text_life=font2.render(str(life),1,life_color)
        win.blit(text_life,(650,10))
        display.update()
    else:
        finish=False
        score=0
        lost=0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1,6):
            monster=Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monsters.add(monster)
        for i in range(1,3):
            asteroid=Enemy(img_ast,randint(30,win_width-30),-40,80,50,randint(1,7))
            asteroids.add(asteroid)
    time.delay(50)