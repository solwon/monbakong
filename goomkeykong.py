import pyxel
import time
import random

FPS = 30
GRAVITY = 3

    
class Game:
    def __init__(self):
        pyxel.init(320, 320, title="Goomkeykong", fps=FPS)
        pyxel.load("goomkeykong.pyxres")

        self.player_x = 0
        self.player_y = 0
        self.player_dx = 0
        self.player_dy = 0
        self.is_alive = True
        self.is_falling = False
        
        self.floor = [Floor(-48 if pyxel.rndi(1,3)%2 == 1 else 140, pyxel.rndi(10, 130), True)]

        self.goom = Goom(80, 150) #초기시작위치로 초기화
        self.mushroom = Mushroom(60,60)
        # self.floor = []
        # for i in 10:
        #     self.floor.append(Floor(i,pyxel.rndi(10, 140), True))
        #self.floor_2 = Floor(80, 130)

        self.temp_floor_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.mario = Mario(80, 30)

        self.bomb = [Bomb(self.floor[0])]
        # self.floor_3 = Floor_2(100, 120) #test
        self.floor_num = len(self.floor)
        # for i in range(1,4):
        #     i = pyxel.rndi(1,11)
        #     self.bomb = Bomb(self.floor[i])
        #     self.temp_floor_num -= i
            



        
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        
        self.goom.move()
        self.mushroom.move()

        # self.floor.update()
        # self.floor.detect_collision(self.goom)
        if len(self.floor) < 10 :
            floor = Floor(60 if pyxel.rndi(1,3)%2 == 1 else 200, pyxel.rndi(10, 200), True)
            self.floor.append(floor)

        # self.floor_2.detect_collision(self.goom)
        # self.floor_2.update()
        for floor in self.floor:
            floor.update()
            floor.detect_collision(self.goom)

        if len(self.bomb) < 4:
            i = pyxel.rndi(1,len(self.floor))
            if i in self.temp_floor_num:
                bomb = Bomb(self.floor[i-1])
                self.temp_floor_num.remove(i)
                self.bomb.append(bomb)

        self.temp_floor_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.mario.detect_collision(self.goom)

        # self.floor_3.detect_collision(self.goom) #test
        # self.floor_3.update(self.goom) #test
        for bomb in self.bomb:
            bomb.update(floor)

        
    def draw(self):
        pyxel.cls(13)
        # # if self.gameover:
        # #     pyxel.text(100, 115, 'GAME OVER', 0)
        # if self.mario.detect_collision(self.goom) == True:
        #     pyxel.text(100, 120, 'YOU WIN', 0)
        # else:
        self.goom.draw()
        self.mushroom.draw()
        
        for floor in self.floor:
            floor.draw()
        

        # self.floor_3.draw() #test
        
        for bomb in self.bomb:
            bomb.draw()

        
        self.mario.draw()
        # if self.mario.detect_collision(self.goom) == True:
        #     pyxel.text(100, 5, 'GAME CLEAR', 0)

        
class Goom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.direction = 1
        self.is_alive = True
        self.is_falling = False
        self.jump_cnt = 2
        self.last_y = self.y

        

    def move(self):

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx = -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx = 2
            self.direction = 1
        if pyxel.btnp(pyxel.KEY_SPACE):
            # if self.dy != 0:
                
            #     if self.jump_cnt > 0:
            #         self.dy = -5
                    
            #         self.jump_cnt -= 2
            # else:
            #     self.dy = -5
            #     self.jump_cnt -= 1
            self.dy = -5
            
        if pyxel.btn(pyxel.KEY_DOWN): #테스트후 삭제
            self.dy = 2
     
        self.x += self.dx
        self.dx = 0
        self.y += self.dy
        #self.dy = 0
        self.dy = min(self.dy + 1, 3)
        #중력구현
        #좌표제한 필요
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, 8, 8, 2) #테스트용 기본상태
        #걸을때
        #기절일때 옆으로 90도


class Mushroom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1

    def move(self):
        self.x += self.direction
        #떨어지지않는 장치구현 > is_wall

    def detect_collide(self, goom: Goom):
        
        pass
        #goom과 충돌판정넣기
        #벽아래로 안떨어지도록하기

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, 2)


class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def detect_collision(self, goom: Goom):
        if ((goom.y+8 >= self.y-2) and (goom.y+8 <= self.y)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+14)) or
                ((goom.x >= self.x) and (goom.x <=self.x+16))):
                return True
        elif ((goom.y >= self.y+6) and (goom.y <= self.y+8)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+14)) or
                ((goom.x >= self.x) and (goom.x <=self.x+16))):
                return True
        elif (((goom.y+8 > self.y) and (goom.y+8 < self.y+8)) or
            ((goom.y > self.y) and (goom.y < self.y+8))):
            if (goom.x+8 >= self.x) and (goom.x+8 <= self.x+2):
                return True
            elif (goom.x >= self.x+14) and (goom.x <= self.x+16):
                return True
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 24, 16, 16, 2)


class Floor:
    def __init__(self, x, y, is_alive):
        self.x = x
        self.y = y
        self.is_alive = is_alive
        self.direction = 0.1 if pyxel.rndi(1,3)%2 > 0 else -0.1
        self.speed = 0

    def update(self):
        if self.speed == 0 :
            self.speed = pyxel.rndf(0,15) * self.direction
        self.x += self.speed
        
    def detect_collision(self, goom: Goom):
        #윗면충돌
        if ((goom.y+8 >= self.y-2) and (goom.y+8 <= self.y)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+44)) or
                ((goom.x >= self.x) and (goom.x <=self.x+48))):
                goom.dy = 0
                goom.y = self.y-8
                goom.jump_cnt = 2
                goom.dx = self.speed

        #아랫면충돌
        elif ((goom.y >= self.y+6) and (goom.y <= self.y+8)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+44)) or
                ((goom.x >= self.x) and (goom.x <=self.x+48))):
                goom.dy = GRAVITY
                goom.y = self.y+10
        
        elif (((goom.y+8 > self.y) and (goom.y+8 < self.y+8)) or
            ((goom.y > self.y) and (goom.y < self.y+8))):
            #좌측충돌
            if (goom.x+8 >= self.x) and (goom.x+8 <= self.x+2):
                goom.dx = 0
                goom.x += -2
            #우측충돌
            elif (goom.x >= self.x+46) and (goom.x <= self.x+48):
                goom.dx = 0
                goom.x += 2
        
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 40, 48, 8, 2)


#다른 floor밟으면 frame카운팅함
class Floor_2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = 0
        self.direction = 0.1 if pyxel.rndi(1,3)%2 > 0 else -0.1
        self.speed = 0
        self.temp_frame = 0

    def update(self, goom:Goom):
        if self.speed == 0 :
            self.speed = pyxel.rndf(0,1) * self.direction
        self.x += self.speed

        while self.detect_collision(goom) == False:
            self.temp_frame = pyxel.frame_count

        if self.detect_collision(goom) == True:
            if pyxel.frame_count >= self.temp_frame + 150:
                self.speed = 0
                self.dy = 5
    
        self.x += self.speed
        self.y += self.dy
        
    def detect_collision(self, goom: Goom):
        if ((goom.y+8 >= self.y-2) and (goom.y+8 <= self.y)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+44)) or
                ((goom.x >= self.x) and (goom.x <=self.x+48))):
                goom.dy = 0
                goom.y = self.y-8
                goom.jump_cnt = 2
                goom.dx = self.speed
                return True
        elif ((goom.y >= self.y+6) and (goom.y <= self.y+8)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+44)) or
                ((goom.x >= self.x) and (goom.x <=self.x+48))):
                goom.dy = GRAVITY
                goom.y = self.y+10
        elif (((goom.y+8 > self.y) and (goom.y+8 < self.y+8)) or
            ((goom.y > self.y) and (goom.y < self.y+8))):
            if (goom.x+8 >= self.x) and (goom.x+8 <= self.x+2):
                goom.dx = 0
                goom.x += -2
            elif (goom.x >= self.x+46) and (goom.x <= self.x+48):
                goom.dx = 0
                goom.x += 2

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 48, 48, 8, 2)

#폭탄이동 = 발판범위에서 좌우로 이동
#기절기능 필요
class Bomb:
    def __init__(self, floor:Floor):
        self.x = pyxel.rndf(floor.x-8, floor.x+36)
        self.y = floor.y - 12
        self.floor_x = floor.x
        self.floor_speed = floor.speed
        self.direction = 0.1 if pyxel.rndi(1,3)%2 > 0 else -0.1
        self.speed = pyxel.rndi(1,30) * self.direction
        

    def update(self, floor:Floor):
        self.left_x = floor.x
        self.right_x = floor.x +48
        if self.x <= floor.x or self.x+8 >= floor.x+48:
            self.floor_speed = -self.floor_speed
            self.speed = -self.speed
        
        self.x += self.floor_speed + self.speed
        

    def detect_collision(self, goom: Goom):
        if ((goom.y+8 >= self.y-2) and (goom.y+8 <= self.y)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+14)) or
                ((goom.x >= self.x) and (goom.x <=self.x+16))):
                return True
        elif ((goom.y >= self.y+6) and (goom.y <= self.y+8)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+14)) or
                ((goom.x >= self.x) and (goom.x <=self.x+16))):
                return True
        elif (((goom.y+8 > self.y) and (goom.y+8 < self.y+8)) or
            ((goom.y > self.y) and (goom.y < self.y+8))):
            if (goom.x+8 >= self.x) and (goom.x+8 <= self.x+2):
                return True
            elif (goom.x >= self.x+14) and (goom.x <= self.x+16):
                return True

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 16, 24, 16, 16, 2)

class Step:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1


    def update(self, goom:Goom):
        self.dx = self.direction

        if self.detect_collision() == True:
            goom.dy = -10
            goom.jump_cnt = 2

    def detect_collision(self, goom: Goom):
        if ((goom.y+8 >= self.y-2) and (goom.y+8 <= self.y)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+14)) or
                ((goom.x >= self.x) and (goom.x <=self.x+16))):
                return True
        elif ((goom.y >= self.y+6) and (goom.y <= self.y+8)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+14)) or
                ((goom.x >= self.x) and (goom.x <=self.x+16))):
                return True
        elif (((goom.y+8 > self.y) and (goom.y+8 < self.y+8)) or
            ((goom.y > self.y) and (goom.y < self.y+8))):
            if (goom.x+8 >= self.x) and (goom.x+8 <= self.x+2):
                return True
            elif (goom.x >= self.x+14) and (goom.x <= self.x+16):
                return True

    def draw(self):
        pyxel.blt()


Game()