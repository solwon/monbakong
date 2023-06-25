import pyxel


class Game:
    def __init__(self):
        pyxel.init(320, 320, title="Goomkeykong")
        pyxel.load("goomkeykong.pyxres")

        self.player_x = 0
        self.player_y = 0
        self.player_dx = 0
        self.player_dy = 0
        self.is_alive = True
        self.is_falling = False

        self.goom = Goom(80, 130) #초기시작위치로 초기화
        self.mushroom = Mushroom(60,60)
        self.floor = Floor(80, 160)
        self.floor_2 = Floor_2(30, 20, True)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        
        self.goom.move()
        self.mushroom.move()

        self.floor.move()
        self.floor.is_touch(self.goom)
        
        self.floor_2.move()
        
    def draw(self):
        pyxel.cls(13)

        self.goom.draw()
        self.mushroom.draw()
        self.floor.draw()
        self.floor_2.draw()
        
class Goom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0.5
        self.direction = 1
        self.is_alive = True
        self.is_falling = False
        self.jump_cnt = 2

    def move(self):

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx += -2
            self.direction = -1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx += 2
            self.direction = 1
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.dy != 0: #가속도존재 = floor.is_touch조건달성
                
                if self.jump_cnt > 0:
                    self.dy += -25
                    
                    self.jump_cnt -= 2
            else:
                self.dy += -30
                self.jump_cnt -= 1

            #이단점프 구현필요
            
        if pyxel.btn(pyxel.KEY_DOWN): #테스트후 삭제
            self.dy += 2

        self.x += self.dx       
        self.y += self.dy
        self.dx = 0
        self.dy = 0.5
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

    def collide(self, goom: Goom):
        
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
        #접촉시 실행
        pass
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 24, 16, 16, 2)


class Floor:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
        self.direction = 0.1 if pyxel.rndi(1,3)%2 > 0 else -1

    def move(self):
        #self.x += self.direction # *random 으로 속도차이두기
        pass
        #떨어지지않는 장치구현 > is_wall
    def is_touch(self, goom: Goom):
        #위에서 아래로 충돌할경우
        if ((goom.x >= self.x and goom.x <= self.x+48) and
            (goom.y >= self.y-8 and goom.y <= self.y)):
                
                goom.dy = 0
                goom.jump_cnt = 2
                      
        
        #아래에서 위로 충돌할경우
        if ((goom.x >= self.x and goom.x <= self.x+48) and
             (goom.y >= self.y and goom.y <= self.y+8)):
                goom.y += 2
        
        #양옆에서 충돌시
        if ((goom.x >= self.x-8 and goom.x < self.x) and
            (goom.y >= self.y-8 and goom.y <= self.y+16)):
            goom.x -= 2

        if ((goom.x > self.x+40 and goom.x <= self.x+48) and
            (goom.y >= self.y-8 and goom.y <= self.y+16)):
            goom.x += 2

        
            

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 40, 48, 8, 2)

class Floor_2:
    def __init__(self, x, y, is_alive):
        self.x = x
        self.y = y
        
        self.direction = 1 if pyxel.rndi(1,3)%2 > 0 else -1

    def move(self):
        self.x += self.direction # *random 으로 속도차이두기

        #떨어지지않는 장치구현 > is_wall
        #밟으면 중력받으며 떨어지는 장치 구현
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

        #떨어지지않는 장치구현 > is_wall

    def draw(self):
        pyxel.blt()

Game()