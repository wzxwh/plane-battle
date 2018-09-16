# -*- coding: utf-8 -*-
"""
Created on Sun Dec 10 20:35:24 2017

@author: 19230
"""

import pygame
import random
from sys import exit



class Bullet():
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.png').convert_alpha()
        self.active = False
        
    def move(self):
        if self.active:
            self.y -= 3
        if self.y < 0:
            self.active = False
            
    def restart(self):
        mouseX,mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width()/2
        self.y = mouseY - self.image.get_height()/2
        self.active = True
        
        
class Bulletleft(Bullet):
    def move(self):
        if self.active:
            self.y -= 3
            self.x -= 1.5
        if self.y < 0 or self.x < 0:
            self.active = False
            
            
class Bulletright(Bullet):
    def move(self):
        if self.active:
            self.y -= 3
            self.x += 1.5
        if self.y < 0 or self.x > 450:
            self.active = False
        
            
class Enemy():
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()
        
    def move(self):
        if self.y < 800:
            self.y += self.speed
        else:
            self.restart()
            
    def restart(self):
        self.x = random.randint(50,400)
        self.y = random.randint(-200,-50)
        self.speed = random.random() + 0.1
        
        
class Plane():
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()
        
    def restart(self):
        self.x = 200
        self.y = 600
        
    def move(self):
        x,y = pygame.mouse.get_pos()
        x -= self.image.get_width()/2
        y -= self.image.get_height()/2
        self.x = x
        self.y = y
        
        
class Boss():
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('boss.png').convert_alpha()
        
    def restart(self):
        self.x = 150
        self.y = 25
        self.speed = 0.1
        self.life = 100
        self.right = True
        self.left = False
        self.up = True
        self.down = False
        
    def move(self):
        if self.right:
            self.x += self.speed
            if self.x >=  250:
                self.right = False
                self.left = True
        if self.left:
            self.x -= self.speed
            if self.x <= 50:
                self.right = True
                self.left = False
        if self.up:
            self.y += self.speed
            if self.y >= 50:
                self.up = False
                self.down = True
        if self.down:
            self.y -= self.speed
            if self.y <= 25:
                self.up = True
                self.down = False
                
    def get_pos(self):
        x = self.x + self.image.get_width()/2
        y = self.y + self.image.get_height()/2
        return x , y
                
    
class Bossbullet():
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bossbullet.png').convert_alpha()
        self.active = False
        
    def restart(self):
        boss_x , boss_y = boss.get_pos()
        self.x = boss_x - self.image.get_width()/2
        self.y = boss_y - self.image.get_height()/2
        self.active = True
    
    def move(self):
        if self.active:
            self.y += 0.5
        if self.y > 800:
            self.active = False
            
            
class Bossbulletleft(Bossbullet):
    def move(self):
        if self.active:
            self.y += 0.5
            self.x -= 0.5
        if self.y > 800 or self.x < 0:
            self.active = False
            
            
class Bossbulletright(Bossbullet):
    def move(self):
        if self.active:
            self.y += 0.5
            self.x += 0.5
        if self.y > 800 or self.x > 450:
            self.active = False
            

class Redbuff():
    def __init__(self):
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('redbuff.png').convert_alpha()
        self.active = False
        
    def restart(self):
        self.x = random.randint(50,400)
        self.y = random.randint(-200,-50)
        self.speed = 0.1
        self.active = True
        
    def move(self):
        if self.y < 850:
            self.y += self.speed
            
        
              
def checkHit(enemy,bullet):
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
    return False


def checkHitplane(plane,bossbullet):
    if (bossbullet.x > plane.x and bossbullet.x < plane.x + plane.image.get_width()) and (bossbullet.y > plane.y and bossbullet.y < plane.y + plane.image.get_height()):
        return True
    return False

    
def checkHitboss(boss,bullet):
    if (bullet.x > boss.x and bullet.x < boss.x + boss.image.get_width()) and (bullet.y > boss.y and bullet.y < boss.y + boss.image.get_height()):
        boss.life -= 1
        bullet.active = False
        
    
def checkCrash(enemy,plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False


def checkCrashboss(boss,plane):
    if (plane.x + 0.7*plane.image.get_width() > boss.x) and (plane.x + 0.3*plane.image.get_width() < boss.x + boss.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > boss.y) and (plane.y + 0.3*plane.image.get_height() < boss.y + boss.image.get_height()):
        return True
    return False


def checkGetbuff(buff,plane):
    if (plane.x + 0.7*plane.image.get_width() > buff.x) and (plane.x + 0.3*plane.image.get_width() < buff.x + buff.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > buff.y) and (plane.y + 0.3*plane.image.get_height() < buff.y + buff.image.get_height()):
        return True
    return False

    
    
pygame.init()
screen = pygame.display.set_mode((450,800),0,32)
pygame.display.set_caption('biubiubiu~')
background = pygame.image.load('background.png').convert()
plane = Plane()
boss = Boss()

bullets = []
for i in range(5):
    bullets.append(Bullet())
count_b = len(bullets)
index_b = 0
interval_b = 0

bulletsleft = []
for i in range(5):
    bulletsleft.append(Bulletleft())
count_bl = len(bulletsleft)
index_bl = 0
interval_bl = 0

bulletsright = []
for i in range(5):
    bulletsright.append(Bulletright())
count_br = len(bulletsright)
index_br = 0
interval_br = 0

bossbullets = []
for i in range(5):
    bossbullets.append(Bossbullet())
count_bb = len(bossbullets)
index_bb = 0
interval_bb = 0

bossbulletsleft = []
for i in range(5):
    bossbulletsleft.append(Bossbulletleft())
count_bbl = len(bossbulletsleft)
index_bbl = 0
interval_bbl = 200

bossbulletsright = []
for i in range(5):
    bossbulletsright.append(Bossbulletright())
count_bbr = len(bossbulletsright)
index_bbr = 0
interval_bbr = 400

enemies = []
for i in range(5):
    enemies.append(Enemy())
    
redbuff = Redbuff()
interval_redbuff = 10000
    
gameover = False
begin = False
checkboss = False
win = False
checkredbuff = False
score = 0

font = pygame.font.Font(None,32)
font2 = pygame.font.Font(None,32)
font3 = pygame.font.Font(None,32)
font4 = pygame.font.Font(None,32)
font5 = pygame.font.Font(None,32)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if gameover and event.type == pygame.MOUSEBUTTONUP:
            pygame.mixer.music.unpause()
            plane.restart()
            boss.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            for bl in bulletsleft:
                bl.active = False
            for br in bulletsright:
                br.active = False
            for bb in bossbullets:
                bb.active = False
            for bbl in bossbulletsleft:
                bbl.active = False
            for bbr in bossbulletsright:
                bbr.active = False
            score = 0
            interval_redbuff = 10000
            checkredbuff = False
            gameover = False
            win = False
            begin = True
            checkboss = False
            
        if not begin and event.type == pygame.MOUSEBUTTONUP:
            screen.blit(background,(0,0))
            pygame.mixer.music.load('game_music.mp3')
            pygame.mixer.music.play(loops = -1)
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            boss.life = 100
            score = 0
            begin = True
            win = False
            checkboss = False
            gameover = False
            
        if win and event.type == pygame.MOUSEBUTTONUP:
            screen.blit(background,(0,0))
            pygame.mixer.music.unpause()
            plane.restart()
            for e in enemies:
                e.restart()
            for b in bullets:
                b.active = False
            boss.life = 100
            score = 0
            win = False
            checkboss = False
            begin = True
            gameover = False
            
    screen.blit(background,(0,0))
    
    if not gameover and begin and not win:
        interval_b -= 1
        if interval_b < 0:
            bullets[index_b].restart()
            interval_b = 100
            index_b = (index_b + 1) % count_b
        interval_redbuff -= 1
        if interval_redbuff < 0:
            redbuff.restart()
            interval_redbuff = 10000
        if redbuff.active:
            redbuff.move()
            screen.blit(redbuff.image,(redbuff.x,redbuff.y))
        for b in bullets:
            if b.active:
                for e in enemies:
                    if checkHit(e,b):
                        score += 100
                b.move()
                screen.blit(b.image,(b.x,b.y))
        for e in enemies:
            if checkCrash(e,plane):
                gameover = True
            if e.y >= 800:
                score -= 50
            e.move()
            screen.blit(e.image,(e.x,e.y))
            
        if checkGetbuff(redbuff,plane):
            checkredbuff = True
            redbuff.active = False
            bufftime = 5000
        if checkredbuff and bufftime > 0:
            bufftime -= 1
            interval_bl -= 1
            if interval_bl < 0:
                bulletsleft[index_bl].restart()
                interval_bl = 100
                index_bl = (index_bl + 1) % count_bl
            for bl in bulletsleft:
                if bl.active:
                    for e in enemies:
                        if checkHit(e,bl):
                            score += 100
                    bl.move()
                    screen.blit(bl.image,(bl.x,bl.y))
            interval_br -= 1
            if interval_br < 0:
                bulletsright[index_br].restart()
                interval_br = 100
                index_br = (index_br + 1) % count_br
            for br in bulletsright:
                if br.active:
                    for e in enemies:
                        if checkHit(e,br):
                            score += 100
                    br.move()
                    screen.blit(br.image,(br.x,br.y))

        if score >= 10000:
            checkboss = True
        if checkboss:
            interval_bb -= 1
            interval_bbl -= 1
            interval_bbr -= 1
            if interval_bb < 0:
                bossbullets[index_bb].restart()
                interval_bb = 500
                index_bb = (index_bb + 1) % count_bb
            if interval_bbl < 0:
                bossbulletsleft[index_bbl].restart()
                interval_bbl = 500
                index_bbl = (index_bbl + 1) % count_bbl
            if interval_bbr < 0:
                bossbulletsright[index_bbr].restart()
                interval_bbr = 500
                index_bbr = (index_bbr + 1) % count_bbr
            for bb in bossbullets:
                if bb.active:
                    if checkHitplane(plane,bb):
                        gameover = True
                    bb.move()
                    screen.blit(bb.image,(bb.x,bb.y))
            for bbl in bossbulletsleft:
                if bbl.active:
                    if checkHitplane(plane,bbl):
                        gameover = True
                    bbl.move()
                    screen.blit(bbl.image,(bbl.x,bbl.y))
            for bbr in bossbulletsright:
                if bbr.active:
                    if checkHitplane(plane,bbr):
                        gameover = True
                    bbr.move()
                    screen.blit(bbr.image,(bbr.x,bbr.y))
            for b in bullets:
                if b.active:
                    checkHitboss(boss,b)
                    if boss.life <= 0:
                        win = True
            for bl in bulletsleft:
                if bl.active:
                    checkHitboss(boss,bl)
                    if boss.life <= 0:
                        win = True
            for br in bulletsright:
                if br.active:
                    checkHitboss(boss,br)
                    if boss.life <= 0:
                        win = True
                        
            if checkCrashboss(boss,plane):
                gameover = True
            boss.move()
            screen.blit(boss.image,(boss.x,boss.y))
            
        plane.move()
        screen.blit(plane.image,(plane.x,plane.y))
        text = font.render("Score: %d" % score,1,(0,0,0))
        screen.blit(text,(0,0))
        
    if gameover:
        pygame.mixer.music.pause()
        text = font.render("Score: %d" % score,1,(0,0,0))
        logo = font2.render("GAME OVER",1,(255,0,0))
        screen.blit(logo,(150,300))
        screen.blit(text,(160,350))
        
    if win:
        pygame.mixer.music.pause()
        wintext = font5.render("YOU WIN!!!",1,(255,0,0))
        screen.blit(wintext,(160,350))
        
    if not begin:
        text = font.render("biubiubiu~",1,(0,0,96))
        instruction = font.render("click to start",1,(0,0,0))
        screen.blit(text,(170,300))
        screen.blit(instruction,(160,350))
        
    pygame.display.update()