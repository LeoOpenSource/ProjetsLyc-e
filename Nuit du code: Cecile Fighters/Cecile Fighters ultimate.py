# -*- coding: utf-8 -*-
"""
Created on Wed May 29 12:20:38 2024

@author: LILARI

Appuyer sur W pour lancer le jeu une fois le script exécuté
"""
import pyxel
import random


class Ennemie:
    def __init__(self, x):
        self.x = x
        self.y = random.randint(10, 80)
        self.pv = 3
        self.skin = [0, 120, -16, 16]
        self.died_skin = [0, 168, 16, -16]
        self.speedx = -1
        self.targetted = False

    def update(self):
        self.x += self.speedx
        if self.x < 0:
            self.pv = 0

    def draw(self):
        if self.pv > 0:
            pyxel.blt(self.x, self.y, 0, self.skin[0], self.skin[1],
                      self.skin[2], self.skin[3], 5)
        if self.pv <= 0:
            self.speedx = 0
            pyxel.blt(self.x, self.y, 0, self.died_skin[0], self.died_skin[1],
                      self.died_skin[2], self.died_skin[3], 5)


class Fast_Ennemie(Ennemie):
    def __init__(self, x):
        super().__init__(x)
        self.skin = [80, 120, -16, 16]
        self.pv = 3
        self.speedx = -1.5
        self.targetted = False


class Tir:
    def __init__(self, sol_x, sol_y):
        self.sol_x = sol_x
        self.x = sol_x + 15
        self.y = sol_y + 7

    def update(self, portee):
        if self.x < self.sol_x + portee:
            self.x += 0.5

    def draw(self, portee):
        if self.x < self.sol_x + portee:
            pyxel.blt(self.x, self.y, 0, 32, 16, 8, 8, 5)

class SGtir(Tir):
    def draw(self, portee):
        if self.x < self.sol_x + portee:
            pyxel.blt(self.x, self.y, 0, 32, 8, 8, 8, 5)
            pyxel.blt(self.x, self.y+3, 0, 32, 8, 8, 8, 5)
            pyxel.blt(self.x, self.y-3, 0, 32, 8, 8, 8, 5)

class Sntir(Tir):
    
    def draw(self, portee):
        self.bullet = None
    
        if self.x < self.sol_x + portee and self.bullet == None:
            pyxel.blt(self.x, self.y, 0, 32, 48, 8, 8, 5)
            self.bullet = 0
        
        if self.x < self.sol_x + portee and self.bullet == 0:
            pyxel.blt(self.x, self.y, 0, 40, 48, 8, 8, 5)
            self.bullet = 1
        if self.x < self.sol_x + portee and self.bullet == 1:
            pyxel.blt(self.x, self.y, 0, 48, 48, 8, 8, 5)
            self.bullet = 2
        if self.x < self.sol_x + portee and self.bullet == 2:
            pyxel.blt(self.x, self.y, 0, 56, 48, 8, 8, 5)
            self.bullet = None
        

class RTtir(Tir):
    def draw(self, portee):
        if self.x < self.sol_x + portee:
            pyxel.blt(self.x, self.y, 0, 48, 56, 16, 16, 5)

class GTtir(Tir):
    def draw(self, portee):
        if self.x < self.sol_x + portee:
            pyxel.blt(self.x, self.y, 0, 129, 104, 8, 8, 5)




class Soldier:
    def __init__(self, x, y):
        self.bullet = None
        self.pv = 3
        self.range = 64
        self.damage = 2
        self.ammo = 3
        self.delay = 0.5
        self.reload = 1
        self.animation = 1
        self.default_skin = [0, 8, 16, 16]
        self.shoot_skin = [16, 8, 16, 16]
        self.skin = self.default_skin
        self.x = x
        self.y = y
        self.tirs = []
        self.can_shoot = True
        self.can_reload = True
        self.target = None

        self.status = None
        self.status_y = self.y

        self.frame_reload = -10000000
        self.frame_delay = -1000000
        self.frame_animation = -1000000

    def status_animation(self):
        if self.status_y > self.y - 2:
            self.status_y -= 0.05
        if self.status_y < self.y - 1.9:
            self.status_y += 2

    def find_nearest(self, ennemy):
        if (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            if ennemy.targetted is False:
                self.target = ennemy
                self.target.targetted = True

                self.move()

    def verify_range(self, ennemy):
        if not (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            self.target.targetted = False
            self.target = None

    def move(self):
        self.y = self.target.y

    def hurt(self):
        self.target.pv -= self.damage

    def shoot(self):
        self.tirs.append(Tir(self.x, self.y))
        self.skin = self.shoot_skin
        self.hurt()

    def update(self, frame_count):
        # Shoot Handler
        if (self.target is not None and self.ammo > 0
                and self.can_shoot is True ):
            if self.target.pv > 0:
                self.ammo -= 1
                self.shoot()
                self.can_shoot = False
                self.frame_delay = frame_count
                self.frame_animation = frame_count
            else:
                self.target = None
        
        if self.target is not None:
            if self.target.pv == 0:
                self.target = None

        # Status Handler
        if self.ammo == 0:
            self.status = "need ammos"
            if self.can_reload is True:
                self.frame_reload = frame_count
                self.can_reload = False
            self.status_animation()
        elif self.pv == 1:
            self.status = "low health"
        else:
            self.status = None

        # Frames handler
        if self.frame_animation + self.animation * 30 == frame_count:
            self.skin = self.default_skin
        if self.frame_delay + self.delay * 30 == frame_count:
            self.can_shoot = True
        if self.frame_reload + self.reload*30 == frame_count:
            self.ammo = 3
            self.can_reload = True

        # Shoots handler
        for tir in self.tirs:
            tir.update(self.range)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.skin[0], self.skin[1], self.skin[2],
                  self.skin[3], 5)

        for tir in self.tirs:
            tir.draw(self.range)

        if self.status == "need ammos":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 160, 184, 16,
                  16, 5)
        if self.status == "low health":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 208, 200, 16,
                  16, 5)
            
class Shot_Gun:
    def __init__(self, x, y):
        self.pv = 8
        self.range = 30
        self.damage = 0.5
        self.ammo = 6
        self.delay = 0.3
        self.reload = 1
        self.animation = 1
        self.default_skin = [16, 56, 16, 16]
        self.shoot_skin = [0, 56, 16, 16]
        self.skin = self.default_skin
        self.x = x
        self.y = y
        self.tirs = []
        self.can_shoot = True
        self.can_reload = True
        self.target = None

        self.status = None
        self.status_y = self.y

        self.frame_reload = -10000000
        self.frame_delay = -1000000
        self.frame_animation = -1000000

    def status_animation(self):
        if self.status_y > self.y - 2:
            self.status_y -= 0.05
        if self.status_y < self.y - 1.9:
            self.status_y += 2

    def find_nearest(self, ennemy):
        if (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            if ennemy.targetted is False:
                self.target = ennemy
                self.target.targetted = True
                print(self.target)
                self.move()

    def verify_range(self, ennemy):
        if not (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            self.target.targetted = False
            self.target = None

    def move(self):
        self.y = self.target.y

    def hurt(self):
        self.target.pv -= self.damage

    def shoot(self):
        self.tirs.append(SGtir(self.x, self.y))
        self.skin = self.shoot_skin
        self.hurt()

    def update(self, frame_count):
        # Shoot Handler
        if (self.target is not None and self.ammo > 0
                and self.can_shoot is True ):
            if self.target.pv > 0:
                self.ammo -= 1
                self.shoot()
                self.can_shoot = False
                self.frame_delay = frame_count
                self.frame_animation = frame_count
            else:
                self.target = None
        
        if self.target is not None:
            if self.target.pv <= 0:
                self.target = None

        # Status Handler
        if self.ammo == 0:
            self.status = "need ammos"
            if self.can_reload is True:
                self.frame_reload = frame_count
                self.can_reload = False
            self.status_animation()
        elif self.pv == 1:
            self.status = "low health"
        else:
            self.status = None

        # Frames handler
        if self.frame_animation + self.animation * 30 == frame_count:
            self.skin = self.default_skin
        if self.frame_delay + self.delay * 30 == frame_count:
            self.can_shoot = True
        if self.frame_reload + self.reload*30 == frame_count:
            self.ammo = 3
            self.can_reload = True

        # Shoots handler
        for tir in self.tirs:
            tir.update(self.range)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.skin[0], self.skin[1], self.skin[2],
                  self.skin[3], 5)

        for tir in self.tirs:
            tir.draw(self.range)

        if self.status == "need ammos":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 160, 184, 16,
                  16, 5)
        if self.status == "low health":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 208, 200, 16,
                  16, 5)


class Sniper:
    def __init__(self, x, y):
        self.bullet = None
        self.pv = 2
        self.range = 128
        self.damage = 8
        self.ammo = 1
        self.delay = 0.7
        self.reload = 1.5
        self.animation = 1
        self.default_skin = [0, 40, 16, 16]
        self.shoot_skin = [16, 40, 16, 16]
        self.skin = self.default_skin
        self.x = x
        self.y = y
        self.tirs = []
        self.can_shoot = True
        self.can_reload = True
        self.target = None

        self.status = None
        self.status_y = self.y

        self.frame_reload = -10000000
        self.frame_delay = -1000000
        self.frame_animation = -1000000

    def status_animation(self):
        if self.status_y > self.y - 2:
            self.status_y -= 0.05
        if self.status_y < self.y - 1.9:
            self.status_y += 2

    def find_nearest(self, ennemy):
        if (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            if ennemy.targetted is False:
                self.target = ennemy
                self.target.targetted = True
                print(self.target)
                self.move()

    def verify_range(self, ennemy):
        if not (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            self.target.targetted = False
            self.target = None

    def move(self):
        self.y = self.target.y

    def hurt(self):
        self.target.pv -= self.damage

    def shoot(self):
        self.tirs.append(Sntir(self.x, self.y))
        self.skin = self.shoot_skin
        self.hurt()

    def update(self, frame_count):
        # Shoot Handler
        if (self.target is not None and self.ammo > 0
                and self.can_shoot is True ):
            if self.target.pv > 0:
                self.ammo -= 1
                self.shoot()
                self.can_shoot = False
                self.frame_delay = frame_count
                self.frame_animation = frame_count
            else:
                self.target = None
        
        if self.target is not None:
            if self.target.pv <= 0:
                self.target = None

        # Status Handler
        if self.ammo == 0:
            self.status = "need ammos"
            if self.can_reload is True:
                self.frame_reload = frame_count
                self.can_reload = False
            self.status_animation()
        elif self.pv == 1:
            self.status = "low health"
        else:
            self.status = None

        # Frames handler
        if self.frame_animation + self.animation * 30 == frame_count:
            self.skin = self.default_skin
        if self.frame_delay + self.delay * 30 == frame_count:
            self.can_shoot = True
        if self.frame_reload + self.reload*30 == frame_count:
            self.ammo = 3
            self.can_reload = True

        # Shoots handler
        for tir in self.tirs:
            tir.update(self.range)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.skin[0], self.skin[1], self.skin[2],
                  self.skin[3], 5)

        for tir in self.tirs:
            tir.draw(self.range)

        if self.status == "need ammos":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 160, 184, 16,
                  16, 5)
        if self.status == "low health":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 208, 200, 16,
                  16, 5)


class Rocket_Thrower:
    def __init__(self, x, y):
        self.pv = 4
        self.range = 80
        self.damage = 5
        self.ammo = 4
        self.delay = 1.5
        self.reload = 3
        self.animation = 1
        self.default_skin = [96, 56, 16, 16]
        self.shoot_skin = [80, 56, 16, 16]
        self.skin = self.default_skin
        self.x = x
        self.y = y
        self.tirs = []
        self.can_shoot = True
        self.can_reload = True
        self.target = None

        self.status = None
        self.status_y = self.y

        self.frame_reload = -10000000
        self.frame_delay = -1000000
        self.frame_animation = -1000000

    def status_animation(self):
        if self.status_y > self.y - 2:
            self.status_y -= 0.05
        if self.status_y < self.y - 1.9:
            self.status_y += 2

    def find_nearest(self, ennemy):
        if (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            if ennemy.targetted is False:
                self.target = ennemy
                self.target.targetted = True
                print(self.target)
                self.move()

    def verify_range(self, ennemy):
        if not (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            self.target.targetted = False
            self.target = None

    def move(self):
        self.y = self.target.y

    def hurt(self):
        self.target.pv -= self.damage

    def shoot(self):
        self.tirs.append(RTtir(self.x, self.y))
        self.skin = self.shoot_skin
        self.hurt()

    def update(self, frame_count):
        # Shoot Handler
        if (self.target is not None and self.ammo > 0
                and self.can_shoot is True ):
            if self.target.pv > 0:
                self.ammo -= 1
                self.shoot()
                self.can_shoot = False
                self.frame_delay = frame_count
                self.frame_animation = frame_count
            else:
                self.target = None
        
        if self.target is not None:
            if self.target.pv <= 0:
                self.target = None

        # Status Handler
        if self.ammo == 0:
            self.status = "need ammos"
            if self.can_reload is True:
                self.frame_reload = frame_count
                self.can_reload = False
            self.status_animation()
        elif self.pv == 1:
            self.status = "low health"
        else:
            self.status = None

        # Frames handler
        if self.frame_animation + self.animation * 30 == frame_count:
            self.skin = self.default_skin
        if self.frame_delay + self.delay * 30 == frame_count:
            self.can_shoot = True
        if self.frame_reload + self.reload*30 == frame_count:
            self.ammo = 3
            self.can_reload = True

        # Shoots handler
        for tir in self.tirs:
            tir.update(self.range)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.skin[0], self.skin[1], self.skin[2],
                  self.skin[3], 5)

        for tir in self.tirs:
            tir.draw(self.range)

        if self.status == "need ammos":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 160, 184, 16,
                  16, 5)
        if self.status == "low health":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 208, 200, 16,
                  16, 5)

class Grenade_Thrower:
    def __init__(self, x, y):
        self.pv = 1
        self.range = 90
        self.damage = 5
        self.ammo = 1
        self.delay = 4
        self.reload = 3
        self.animation = 1
        self.default_skin = [16, 104, 16, 16]
        self.shoot_skin = [32, 104, 16, 16]
        self.skin = self.default_skin
        self.x = x
        self.y = y
        self.tirs = []
        self.can_shoot = True
        self.can_reload = True
        self.target = None

        self.status = None
        self.status_y = self.y

        self.frame_reload = -10000000
        self.frame_delay = -1000000
        self.frame_animation = -1000000

    def status_animation(self):
        if self.status_y > self.y - 2:
            self.status_y -= 0.05
        if self.status_y < self.y - 1.9:
            self.status_y += 2

    def find_nearest(self, ennemy):
        if (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            if ennemy.targetted is False:
                self.target = ennemy
                self.target.targetted = True
                print(self.target)
                self.move()

    def verify_range(self, ennemy):
        if not (ennemy.x < self.range + self.x and
                self.y - self.range <= ennemy.y <= self.y + self.range):
            self.target.targetted = False
            self.target = None

    def move(self):
        self.y = self.target.y

    def hurt(self):
        self.target.pv -= self.damage

    def shoot(self):
        self.tirs.append(GTtir(self.x, self.y))
        self.skin = self.shoot_skin
        self.hurt()

    def update(self, frame_count):
        # Shoot Handler
        if (self.target is not None and self.ammo > 0
                and self.can_shoot is True ):
            if self.target.pv > 0:
                self.ammo -= 1
                self.shoot()
                self.can_shoot = False
                self.frame_delay = frame_count
                self.frame_animation = frame_count
            else:
                self.target = None
        
        if self.target is not None:
            if self.target.pv <= 0:
                self.target = None

        # Status Handler
        if self.ammo == 0:
            self.status = "need ammos"
            if self.can_reload is True:
                self.frame_reload = frame_count
                self.can_reload = False
            self.status_animation()
        elif self.pv == 1:
            self.status = "low health"
        else:
            self.status = None

        # Frames handler
        if self.frame_animation + self.animation * 30 == frame_count:
            self.skin = self.default_skin
        if self.frame_delay + self.delay * 30 == frame_count:
            self.can_shoot = True
        if self.frame_reload + self.reload*30 == frame_count:
            self.ammo = 3
            self.can_reload = True

        # Shoots handler
        for tir in self.tirs:
            tir.update(self.range)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, self.skin[0], self.skin[1], self.skin[2],
                  self.skin[3], 5)

        for tir in self.tirs:
            tir.draw(self.range)

        if self.status == "need ammos":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 160, 184, 16,
                  16, 5)
        if self.status == "low health":
            pyxel.blt(self.x - 5, self.status_y-5, 0, 208, 200, 16,
                  16, 5)



class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Cecile fighters", fps=30, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load("theme3.pyxres")
        pyxel.mouse(visible=True)
        self.soldiers = [Soldier(20, 20), Soldier(20, 40)]
        self.shotguns = []
        self.snipers = []
        self.rockets = []
        self.grenades = [Grenade_Thrower(10, 60)]
        self.frame_count = 0
        self.text = None
        self.ennemies = []
        self.current_wave = 0
        self.just_died = True
        self.money = ""
        self.wave_text = ""
        
        self.health = 5
        self.soldatenplus = None
        self.conteurgrenade = 0

        pyxel.run(self.update, self.draw)

    def wave(self):
        self.wave_text = f'Wave : {self.current_wave}'
        if self.current_wave < 5:
            for i in range(5):
                self.ennemies.append(Ennemie(130))
        elif self.current_wave == 5:
            for i in range(5):
                self.ennemies.append(Ennemie(130))
            for i in range(2):
                self.ennemies.append(Fast_Ennemie(130))
        elif self.current_wave > 5 and self.current_wave < 10:
            for i in range(9):
                self.ennemies.append(Ennemie(130))
            for i in range(7):
                self.ennemies.append(Fast_Ennemie(150))
        elif self.current_wave == 10:
            for i in range(9):
                self.ennemies.append(Ennemie(130))
            for i in range(9):
                self.ennemies.append(Fast_Ennemie(150))
        elif self.current_wave > 10 and self.current_wave < 20:
            for i in range(9):
                self.ennemies.append(Ennemie(130))
            for i in range(9):
                self.ennemies.append(Ennemie(150))
            for i in range(7):
                self.ennemies.append(Ennemie(170))

    def update(self):
        self.frame_count = pyxel.frame_count
        if pyxel.btnr(pyxel.KEY_W):
            self.current_wave = 1
        if len(self.ennemies) == 0 and self.current_wave > 0:
            self.wave()
            self.current_wave += 1
        for ennemy in self.ennemies:
            ennemy.update()
            if ennemy.pv <= 0:
                self.ennemies.remove(ennemy)  
                self.money += 2
            if ennemy.x < 0:
                self.health -= 1
        if self.current_wave > 0 and len(self.ennemies) > 0:
            for ennemy in self.ennemies:
                for soldier in self.soldiers:
                    if soldier.target is None:
                        if ennemy.pv > 0:
                            soldier.find_nearest(ennemy)
                    else:
                        soldier.verify_range(ennemy)

        self.frame_count = pyxel.frame_count
        for soldier in self.soldiers:
            soldier.update(self.frame_count)
        
        self.text = None
        if self.money == '':
            self.money = 12
        else:
            None
       
        
        if 5 <= pyxel.mouse_x <= 21 and 105 <= pyxel.mouse_y <= 120:
            self.text = 0 
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) == True :
                if self.money >= 4 :
                    self.soldatenplus = 0
                    self.money -= 4
                else :
                    None
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) == True :
                if self.money >= 10 :
                    self.upgrade = 0
                    self.money -= 10
                else :
                    None
        elif 32 <= pyxel.mouse_x <= 48 and 105 <= pyxel.mouse_y <= 120:
            self.text = 1
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) == True :
                if self.money >= 5 :
                    self.soldatenplus = 1
                    self.money -= 5
                else :
                    None
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) == True :
                if self.money >= 10 :
                    self.upgrade = 1
                    self.money -= 10
                else :
                    None
        elif 56 <= pyxel.mouse_x <= 72 and 105 <= pyxel.mouse_y <= 120:
            self.text = 2
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) == True :
                if self.money >= 6 :
                    self.money -= 6
                    self.soldatenplus = 2
                else :
                    None
                
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) == True :
                if self.money >= 10 :
                    self.upgrade = 2
                    self.money -= 10
                else :
                    None
        elif 80 <= pyxel.mouse_x <= 96 and 105 <= pyxel.mouse_y <= 120:
            self.text = 3
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) == True :
                if self.money >= 12 :
                    self.soldatenplus = 3
                    self.money -= 12
                else :
                   None
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) == True :
                if self.money >= 10 :

                    self.upgrade = 3
                    self.money -= 10
                else :
                    None
        elif 104 <= pyxel.mouse_x <= 120 and 105 <= pyxel.mouse_y <= 120:
            self.text = 4
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) == True :
                if self.money >= 15 :
                    self.soldatenplus = 4
                    self.money -= 15
                else :
                    None
            if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) == True :
                if self.money >= 10 :
                    self.upgrade = 5
                    self.money -= 10
                else :
                    None
        else :
            None


    def draw(self):
        pyxel.cls(0)
        pyxel.rect(0,0,128,100,5)
        pyxel.circ(-70,45,130,7)
        pyxel.rect(0,100,128,28,0)
        pyxel.rect(2, 102, 124, 24, 9)

        for ennemy in self.ennemies:
            ennemy.draw()

        pyxel.blt(44, 92, 0, 224, 128, 32, 8, 5)
        pyxel.blt(76, 92, 0, 224, 128, 32, 8, 5)
        pyxel.blt(62, 92, 0, 208, 128, 16, 8, 5)
        pyxel.blt(44, 0, 0, 224, 128, 32, -8, 5)
        pyxel.blt(76, 0, 0, 224, 128, 32, -8, 5)
        pyxel.blt(68, 0, 0, 176, 128, 16, -15, 5)
        pyxel.blt(62, 0, 0, 208, 128, 16, -8, 5)
        pyxel.blt(90, 92, 0, 208, 128, 16, 8, 5)
        pyxel.blt(105, 92, 0, 208, 128, 16, 8, 5)
        pyxel.blt(117, 92, 0, 224, 128, 16, 8, 5)
        pyxel.blt(90, 0, 0, 224, 128, 32, -6, 5)
        pyxel.blt(105, 0, 0, 182, 128, 32, -8, 5)


        for soldier in self.soldiers:
            soldier.draw()
        for shotgun in self.shotguns:
            shotgun.draw()
        for sniper in self.snipers:
            sniper.draw()
        for rocket in self.rockets:
            rocket.draw()
        for grenade in self.grenades:
            grenade.draw()


        pyxel.blt(6, 105, 0, 0, 8, 16, 15)        
        pyxel.rectb(5, 104, 18, 17, 0)
        pyxel.blt(32, 105, 0, 16, 56, 16, 15)
        pyxel.rectb(31, 104, 18, 17, 0)
        pyxel.blt(56, 105, 0, 0, 40, 16, 15)
        pyxel.rectb(55, 104, 18, 17, 0)
        pyxel.blt(80, 105, 0, 96, 56, 16, 15)
        pyxel.rectb(79, 104, 18, 17, 0)
        pyxel.blt(104, 105, 0, 80, 104, 16, 15)
        pyxel.rectb(103, 104, 18, 17, 0)

        pyxel.text(1, 1, self.wave_text, 0)

        if self.text == 0:
            pyxel.text(16, 121, 'basic soldier    cost = 4', 7)
            pyxel.rectb(5, 104, 18, 17, 8)
        elif self.text == 1:
            pyxel.text(26, 121, 'shot gun    cost = 5', 7)
            pyxel.rectb(31, 104, 18, 17, 8)
        elif self.text == 2:
            pyxel.text(29, 121, 'sniper    cost = 6', 7)
            pyxel.rectb(55, 104, 18, 17, 8)
        elif self.text == 3:
            pyxel.text(16, 121, 'rocket thrower   cost = 12', 7)
            pyxel.rectb(79, 104, 18, 17, 8)
        elif self.text == 4:
            pyxel.text(14, 121, 'grenade thrower   cost = 15', 7)
            pyxel.rectb(103, 104, 18, 17, 8)
        else :
            None


        if self.soldatenplus == 0:
            
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0,  0, 8, 16, 15, 5)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) :
                self.soldiers.append(Soldier(pyxel.mouse_x, pyxel.mouse_y))
                
                self.soldatenplus = None
      
        if self.soldatenplus == 1:
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0,  16, 56, 16, 15, 5)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.soldiers.append(Shot_Gun(pyxel.mouse_x, pyxel.mouse_y))
                self.soldatenplus = None

        if self.soldatenplus == 2:
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0,  0, 40, 16, 15, 5)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.soldiers.append(Sniper(pyxel.mouse_x, pyxel.mouse_y))
                self.soldatenplus = None
        
        if self.soldatenplus == 3:
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0,  96, 56, 16, 15, 5)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.soldiers.append(Rocket_Thrower(pyxel.mouse_x, pyxel.mouse_y))
                self.soldatenplus = None
      
        if self.soldatenplus == 4:
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, 0,   80, 104, 16, 15, 5)
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.soldiers.append(Grenade_Thrower(pyxel.mouse_x, pyxel.mouse_y))
                self.soldatenplus = None
          
      
      
  
                



        pyxel.text(1, 94, f"cash : {self.money}" , 0)
        
        for i in range(self.health):
            
            pyxel.blt(0 + i*4, 6, 0, 48, 200, 16, 16, 5)
        if self.health == 0 :
            pyxel.text(60,60,'GAME OVER', 8)
            
            pyxel.quit()
        


Game()