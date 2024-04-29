'''
list of some abbreviations in this code
ln - level number
kb - killblock/killbrick
plr - player
'''


import pygame as pg, random, sys, time
WIDTH, HEIGHT = 1200, 700
plr_img = pg.image.load('icon.png')
cursor = pg.Rect(0,0,1,1)

print('Only existing levels yet are 0 and 1')
lvl = input('Go to level... ')
if lvl == '':
    lvl = 0
lvl = int(lvl)

class Player:
    def __init__(self, game):
        self.game = game
        self.paused = False
        self.plr = pg.Rect(100,110,18,18)
        self.cap = 0
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()
        self.level = Level(self) 
    def instance(self):
        if cursor.colliderect(self.plr):
            if self.game.paused == 0:
                if self.cap == 0:
                    self.cap = 1
                self.mouse_x,self.mouse_y = pg.mouse.get_pos()
               
        self.game.app.sc.blit(plr_img,(self.plr.left,self.plr.top))
        self.mouse_xx, self.mouse_yy = pg.mouse.get_pos()
        cursor.left = self.mouse_xx
        cursor.top = self.mouse_yy    
        
        if self.cap == 1:  
            self.plr.left = self.mouse_x - 9
            self.plr.top = self.mouse_y - 9
        else:
            pass
    def check(self):
        for i in range(len(self.level.lvl[self.level.ln])):
            self.kb = pg.Rect(self.level.lvl[self.level.ln][i][0], self.level.lvl[self.level.ln][i][1], self.level.lvl[self.level.ln][i][2], self.level.lvl[self.level.ln][i][3])
            if self.plr.colliderect(self.kb):
                print("!")
class Level:
    def __init__(self, game, ln=lvl):
        self.game = game
        self.ln = ln # ln = level number
        self.lvl = [
                        [
                         [0,0,WIDTH,HEIGHT/14],[0,HEIGHT-HEIGHT/14+1,WIDTH,HEIGHT/14],
                         [0,0,WIDTH/20,HEIGHT],[WIDTH-WIDTH/20+1,0,WIDTH/20,HEIGHT]   # Resizable frame
                        ],
                        
                        [[500,500,50,50]]
                   ]
    def run(self,ln=1):
        for i in range(len(self.lvl[self.ln])):
            self.game.block = Obstacle(self.game, self.lvl[self.ln][i][0], self.lvl[self.ln][i][1], self.lvl[self.ln][i][2], self.lvl[self.ln][i][3])
            self.game.block.blit()
class Obstacle:
    def __init__(self, game, l=10, t=10, w=100, h=100, id=0, type="static"):
        self.game = game
        self.rect = pg.Rect(l,t,w,h)
        #print(l,t,w,h,id)
    def blit(self):
        pg.draw.rect(self.game.app.sc, (0,0,0), self.rect)
        
class Game:
    def __init__(self, app):
        self.app = app
        self.player = Player(self)
        self.level = Level(self) 
        self.paused = False
        
    def background(self):
        self.app.sc.fill((0,0,0))
        pg.draw.rect(self.app.sc,(125,150,200),(0,0,WIDTH,HEIGHT))
    def setup(self):
        pass
    
    def run(self):
        self.background()
        self.player.instance()
        self.player.check()
        self.level.run()
        
        # draw objects
        self.setup()
        
        # Ball moving
        #self.obj.check_collision()
        
        
        # move
        key = pg.key.get_pressed()
        if key[pg.K_UP]:
            self.player.plr.left -= 20
            self.player.plr.right -= 20
            r = 0
            
        if key[pg.K_LEFT]:
            pass
        if key[pg.K_RIGHT]:
            pass
        if key[pg.K_SPACE]:
            if self.paused == 1:
                self.paused = 0
            else:
                self.paused = 1
            time.sleep(0.1)
        if self.paused == 1:
            font = pg.font.SysFont("Courier new", 50)
            pause = font.render('-- PAUSE --',0,(255,255,255))
            self.app.sc.blit(pause,(WIDTH//3,HEIGHT//2-50))
        # Font
        
class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.sc = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.game = Game(self)
        #pg.mixer.music.load("resources/music.mp3")
       # pg.mixer.music.play(-1)
    def exit(self):
        pg.quit()
        sys.exit()
    def play_music(self):
        pass
    def check_events(self):
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit() 
                    
    def run(self):
        
        while True:
            self.play_music()
            self.game.run()
            self.check_events()
            pg.display.update()
            self.clock.tick(75)

if __name__ == '__main__':
    app = App()
    app.run()