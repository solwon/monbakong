import pyxel
import time


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

        self.fps = str(pyxel.frame_count)

        self.goom = Goom(80, 150) #초기시작위치로 초기화
        self.mushroom = Mushroom(60,60)
        self.floor = Floor(80, 160)
        self.floor_2 = Floor(80, 130)

        self.floor_3 = Floor_2(100, 5) #test

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        
        self.goom.move()
        self.mushroom.move()

        self.floor.move()
        self.floor.detect_collision(self.goom)
        
        self.floor_2.detect_collision(self.goom)
        #self.floor_2.update(self.goom)

        self.floor_3.detect_collision(self.goom) #test
        self.floor_3.update(self.goom) #test
        
    def draw(self):
        pyxel.cls(13)

        self.goom.draw()
        self.mushroom.draw()
        self.floor.draw()
        self.floor_2.draw()

        self.floor_3.draw() #test

        pyxel.text(100,125, self.fps , 0)
        
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
            self.dx += -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx += 2
            self.direction = 1
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.dy != 0:
                
                if self.jump_cnt > 0:
                    self.dy = -5
                    
                    self.jump_cnt -= 2
            else:
                self.dy = -5
                self.jump_cnt -= 1
            
            #이단점프 구현필요
            
        if pyxel.btn(pyxel.KEY_DOWN): #테스트후 삭제
            self.dy = 2
     
        self.x += self.dx
        self.dx = 0
        self.y += self.dy
    
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
    def __init__(self, x, y, is_alive):
        self.x = x
        self.y = y
        self.is_alive = True
    
    def gameclear():
        pyxel.text(100, 125, 'GAME CLEAR', 0)
        #접촉시 실행
        pass
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 24, 16, 16, 2)


class Floor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 0
        
        
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1

    def move(self):
        # if self.speed == 0 :
        #     self.speed = pyxel.rndf(0,1)
        # self.x += self.direction * self.speed
        pass
        #떨어지지않는 장치구현 > is_wall
    def detect_collision(self, goom: Goom):
        #윗면충돌
        if ((goom.y+8 >= self.y-2) and (goom.y+8 <= self.y)):
            if (((goom.x+8 > self.x+4) and (goom.x+8 <self.x+44)) or
                ((goom.x >= self.x) and (goom.x <=self.x+48))):
                goom.dy = 0
                goom.y = self.y-8
                goom.jump_cnt = 2
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

class Floor_2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_alive = True
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1

    def update(self, goom:Goom):
        if self.detect_collision(goom) == True:
            self.is_alive = False
        
        if self.is_alive == True:
            self.dx = 0
            self.dy = 0
        else:
            
            self.dx = 0
            self.dy = 0
        
        self.x += self.dx
        self.y += self.dy
        #떨어지지않는 장치구현 > is_wall
        #밟으면 중력받으며 떨어지는 장치 구현

    def detect_collision(self, goom: Goom):
        #위아래양옆 경우마다 충돌지점 포인트 다름 다시작성
        #왼쪽충돌
        if ((goom.x+8 == self.x) and
            ((goom.y+8 >= self.y and goom.y+8 <= self.y+8)or
            (goom.y >= self.y and goom.y <= self.y+8))):
            goom.dx = 0
        
        #오른쪽충돌
        if ((goom.x == self.x+48) and
            ((goom.y+8 >= self.y and goom.y+8 <= self.y+8)or
            (goom.y >= self.y and goom.y <= self.y+8))):
            goom.dx = 0
        
        #윗면충돌
        if (((goom.x >= self.x and goom.x <= self.x+48)or
            (goom.x+8 >= self.x and goom.x+8 <= self.x+48)) and
            (goom.y+8 == self.y)):
            goom.dy =0
            return True
        
        #아랫면충돌
        if (((goom.x >= self.x and goom.x <= self.x+48)or
            (goom.x+8 >= self.x and goom.x+8 <= self.x+48)) and
            (goom.y == self.y+8)):
            goom.dy = GRAVITY

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 48, 48, 8, 2)


class Bomb:
    def __init__(self, x, y, is_alive):
        self.x = x
        self.y = y
        self.dx = 0
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1

    def update(self):
        self.dx = self.direction

        #떨어지지않는 장치구현 > is_wall

    def draw(self):
        pyxel.blt()

class Step:
    def __init__(self, x, y, is_alive):
        self.x = x
        self.y = y
        self.dx = 0
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1

    def update(self):
        self.dx = self.direction

    def draw(self):
        pyxel.blt()


Game()