'''
list of some abbreviations in this code
ln - level number
sl - spawn location
fl - finish location
kb - killblock/killbrick
plr - player
l - left; t - top; w - width; h - height
lo - left offset; to - top offset
clr - colour; hclr - highlight colour; bclr - backup colour

list of hotkeys
space - pause
arrow up - previous level
arrow down - next level
arrow left - moves character up and left
'''


import pygame as pg, random, sys, time
WIDTH, HEIGHT = 1000, 750
plr_img = pg.image.load('assets/icon.png')
cursor = pg.Rect(0,0,1,1)

class Cursor:
    def __init__(self):
        global cursor
        self.cursor = cursor
    def run(self):
        self.mouse_xx, self.mouse_yy = pg.mouse.get_pos()
        cursor.left = self.mouse_xx
        cursor.top = self.mouse_yy 
class Player:
    def __init__(self, game):
        self.game = game
        self.paused = False
        self.cursor = Cursor()
        self.plr = pg.Rect(0,0,18,18)
        self.cap = 0
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()
        
    def instance(self):
        self.cursor.run()
        if cursor.colliderect(self.plr):
            if self.game.paused == 0:
                if self.cap == 0:
                    self.cap = 1
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()
               
        self.game.app.sc.blit(plr_img,(self.plr.left,self.plr.top))   
        
        if self.cap == 1:  
            self.plr.left = self.mouse_x - 9
            self.plr.top = self.mouse_y - 9
        else:
            pass
    def check(self):
        for i in range(len(self.game.level.lvl[self.game.level.ln])):
            self.kb = pg.Rect(self.game.level.lvl[self.game.level.ln][i][0], self.game.level.lvl[self.game.level.ln][i][1], self.game.level.lvl[self.game.level.ln][i][2], self.game.level.lvl[self.game.level.ln][i][3])
            if self.plr.colliderect(self.kb):
                self.reset()       
                self.cap = 0
    def check_win(self):
        if self.plr.colliderect(self.game.finish.rect):
            print('Level '+str(self.game.level.ln),'Completed')
            self.reset()
            self.game.level.ln += 1
      
    def reset(self):
        self.plr.left = self.game.level.sl[self.game.level.ln][0]
        self.plr.top = self.game.level.sl[self.game.level.ln][1]
        
class Level:
    def __init__(self, game, ln=0):
        self.game = game
        self.ln = ln
        self.lvl = [
                            [
                                [0,0,WIDTH,HEIGHT/14],[0,HEIGHT-HEIGHT/14+1,WIDTH,HEIGHT/14],
                                [0,0,WIDTH/20,HEIGHT],[WIDTH-WIDTH/20+1,0,WIDTH/20,HEIGHT]
                            ], 
                            [
                                [500,500,50,50]
                            ],      
                            [
                                [300,300,20,20], [240,240,20,20] 
                            ]
                        ]
        
        self.sl = [
                    [WIDTH/2, HEIGHT/2],
                    [WIDTH/1.5, HEIGHT/3],
                    [WIDTH/1.5, HEIGHT/3]
                    
                  ]
        self.fl = [
                    [WIDTH/10, HEIGHT/10, WIDTH/11, HEIGHT/11],
                    [100,100,10,10],
                    [0,0,85,80]
                  ]
        for i in range(900):
            self.lvl.append([[random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(0,100),random.randint(0,100)],
                             [random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(10,400),random.randint(10,400)],
                             [random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(50,500),random.randint(50,500)]])
            self.sl.append([random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(0,100),random.randint(0,100)])
            self.fl.append([random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(0,100),random.randint(0,100)])
            
        self.game.finish = Obstacle(self.game, self.fl[self.ln][0], self.fl[self.ln][1], self.fl[self.ln][2], self.fl[self.ln][3], type='finish')
    def run(self):
        for i in range(len(self.lvl[self.ln])):
            self.game.block = Obstacle(self.game, self.lvl[self.ln][i][0], self.lvl[self.ln][i][1], self.lvl[self.ln][i][2], self.lvl[self.ln][i][3])
            self.game.block.blit()
            self.game.finish = Obstacle(self.game, self.fl[self.ln][0], self.fl[self.ln][1], self.fl[self.ln][2], self.fl[self.ln][3], type='finish')
            self.game.finish.blit()
        numfont = pg.font.SysFont('Courier new', 50)
        numtext = numfont.render(str(self.ln),0,(100,100,100))
        self.game.app.sc.blit(numtext,(WIDTH//10,HEIGHT//5-50))
class Obstacle:
    def __init__(self, game, l=10, t=10, w=100, h=100, color=(0,0,0), type='kb'):
        self.game = game
        self.color = color
        self.type = type
        self.rect = pg.Rect(l,t,w,h)
        
        if self.type == 'finish' and self.color == (0,0,0):
            self.color = (100,5,5)
        
    def blit(self):
        pg.draw.rect(self.game.app.sc, self.color, self.rect)
class Button:
    def __init__(self, game, l=0, t=0, w=150, h=60, shadow=1, text='Button', clr=(100,100,100), hclr=(150,150,150), lo=0, to=0, action=None):
        self.game = game
        self.shadow = shadow
        self.font = pg.font.SysFont('Courier new', 40)  
        self.text = self.font.render(text,1,(0,0,0))
        self.clr = clr
        self.bclr = clr
        self.hclr = hclr
        self.rect = pg.Rect(l,t,w,h)
        self.l = l
        self.t = t
        self.w = w
        self.h = h
        self.lo = lo
        self.to = to
        self.action = action
        if self.shadow == 1:
            self.shadow_rect = pg.Rect(l+2,t+2,w,h)
    def run(self):
        self.blit()
        self.check()
    def blit(self):
        if self.shadow == 1:
            pg.draw.rect(self.game.app.sc, (0,0,0), self.shadow_rect)
        pg.draw.rect(self.game.app.sc, self.clr, self.rect)
        self.game.app.sc.blit(self.text,(self.l+self.w/6-self.lo, self.t+self.h/10-self.to))
    def check(self):
        self.pressed = pg.mouse.get_pressed()
        if self.rect.colliderect(cursor):
            self.clr = self.hclr
            if self.pressed[0]:
                self.actions()
                time.sleep(0.1)
        else:
            self.clr = self.bclr
    def actions(self):
        if self.action == 'exit' or self.action == 'leave':
            self.game.app.exit()
        elif self.action == None:
            print('No action set for this button!', self.rect)
        elif list(self.action)[0] == 'b' and list(self.action)[3] == 'l' and list(self.action)[4] == '_':
            self.bool_action = str(self.action.split('bool_')[1])
            self.game.bool = self.bool_action
        else:
            self.game.tab = self.action
class Game:
    def __init__(self, app):
        self.app = app
        self.player = Player(self)
        self.level = Level(self)
        self.cursor = Cursor()
        self.tab = 'menu'
        self.paused = False
        self.font = pg.font.SysFont('Courier new', 50)
        self.play_button = Button(self, 0, HEIGHT/3, WIDTH/6.67, HEIGHT/10, text='Play', action='play', to=-HEIGHT/125)
        self.icons_button = Button(self, 0, HEIGHT/3+HEIGHT/8, WIDTH/6.67, HEIGHT/10, text='Avatar', lo=WIDTH/50, to=-HEIGHT/125)
        self.settings_button = Button(self, 0, HEIGHT/3+(HEIGHT/8)*2, WIDTH/5, HEIGHT/10, text='Settings', lo=WIDTH/35, to=-HEIGHT/125, action='settings') 
        self.exit_button = Button(self, 0, HEIGHT/3+(HEIGHT/8)*3, WIDTH/6.67, HEIGHT/10, text='Exit', action='leave', to=-HEIGHT/125)
        self.bool_music_button = Button(self, WIDTH//50, HEIGHT//3+75, WIDTH/20, WIDTH/20, text='•', action='bool_music')
        
        self.bool = ''
        self.back_button = Button(self, 0, 0, WIDTH/20, WIDTH/20, text='←', action='menu', to=HEIGHT/125)
        
    def background(self):
        global a, b, c, clr
        self.app.sc.fill((0,0,0))
        pg.draw.rect(self.app.sc,(255,255,255),(0,0,WIDTH,HEIGHT))
        
    def setup(self):
        pass
    
    def run(self):
        self.cursor.run()
        self.background()
        if self.tab == 'menu':
            self.play_button.run()
            self.icons_button.run()
            self.settings_button.run()  
            self.exit_button.run()
        elif self.tab == 'settings':
            self.app.sc.blit(self.font.render('Music: '+str(self.app.music_state),0,(0,0,0)),(WIDTH//10,HEIGHT//2-50))
            self.app.sc.blit(self.font.render('Res: '+str(WIDTH)+'; '+str(HEIGHT),0,(0,0,0)),(WIDTH//10,HEIGHT//2-100))
            self.bool_music_button.run()
            self.back_button.run()
            if self.bool == 'music':
                if self.app.music_state == 0:
                    self.app.music_state = 1
                else:
                    self.app.music_state = 0
                self.bool = ''
                time.sleep(0.05)
        elif self.tab == 'play':
            self.player.instance()
            self.player.check()
            self.player.check_win()
            self.level.run()
            
            key = pg.key.get_pressed()
            if key[pg.K_UP]:
                self.level.ln -= 1
                time.sleep(0.15)
            if key[pg.K_DOWN]:
                self.level.ln += 1
                time.sleep(0.15)
                
            if key[pg.K_LEFT]:
                self.player.plr.left -= 20
                self.player.plr.top -= 20
            if key[pg.K_RIGHT]:
                pass
            if key[pg.K_SPACE]:
                if self.paused == 1:
                    self.paused = 0
                else:
                    self.paused = 1
                time.sleep(0.1)
            if self.paused == 1:
                self.pause = self.font.render('-- PAUSE --',0,(255,255,255))
                self.app.sc.blit(self.pause,(WIDTH//3,HEIGHT//2-50))
        else:
            print("This kind of tab does not exist.")
            self.tab = "menu"

class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.sc = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.game = Game(self)
        self.read_config()
        self.play_music()
        #print(self.config.read(1))
        
    def exit(self):
        pg.quit()
        sys.exit()
    def read_config(self):
        self.config = open('assets/cfg.txt', 'r')
        self.music_state = int(self.config.read(1))
        # 0 - music do not play; 1 - music plays
        self.config.close()
    def play_music(self):
        self.music = pg.mixer.music.load('assets/bullfrog_report_th.mp3')
        pg.mixer.music.play(-1)

    def check_events(self):     
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()
    
    def check_music(self):
        if self.music_state:
            pg.mixer.music.unpause()
        elif self.music_state == 0:
            pg.mixer.music.pause()
    def run(self):
        while True:
            
            self.game.run()
            self.check_events()
            self.check_music()
            pg.display.update()
            self.clock.tick(75)

if __name__ == '__main__':
    app = App()
    app.run()