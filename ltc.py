'''
list of some abbreviations in this code
ln - level number
sl - spawn location
fl - finish location
kb - killblock/killbrick
plr - player
l - left; t - top; w - width; h - height
lo - left offset; to - top offset
clr - colour; hclr - highlight colour; bclr - backup colour; pclr - press colour

list of hotkeys
space - pause
arrow up - previous level
arrow down - next level
arrow left - moves character up and left
escape - exit to menu
'''


import pygame as pg, random as r, sys, time
WIDTH, HEIGHT = 1024, 768
cursor = pg.Rect(0,0,1,1)

class Cover:
    def __init__(self, game):
        self.game = game
        self.cover = pg.Rect(500, 500, WIDTH/3.413, WIDTH/3.413)
        self.cover_img = pg.transform.scale(pg.image.load('assets/cover.png'), (self.cover.width, self.cover.height))
    def run(self):
        self.blit()
        self.cover.centerx = self.game.player.plr.left + self.game.player.plr.width/2
        self.cover.centery = self.game.player.plr.top + self.game.player.plr.height/2
        
    def blit(self):
        self.rect1 = pg.Rect(0,self.cover.top-HEIGHT,WIDTH,HEIGHT)
        self.rect2 = pg.Rect(0,self.cover.bottom,WIDTH,HEIGHT)
        self.rect3 = pg.Rect(self.cover.right,0,WIDTH,HEIGHT)
        self.rect4 = pg.Rect(self.cover.left-WIDTH,0,WIDTH,HEIGHT)
        self.game.app.sc.blit(self.cover_img,(self.cover.left,self.cover.top))
        pg.draw.rect(self.game.app.sc, (0,0,0), self.rect1)
        pg.draw.rect(self.game.app.sc, (0,0,0), self.rect2)
        pg.draw.rect(self.game.app.sc, (0,0,0), self.rect3)
        pg.draw.rect(self.game.app.sc, (0,0,0), self.rect4)
        
        
        
        
class Cursor:
    def __init__(self):
        global cursor
        self.cursor = cursor
    def run(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        cursor.left = self.mouse_x
        cursor.top = self.mouse_y 
class Player:
    def __init__(self, game, cap=0):
        self.game = game
        self.paused = False
        self.cursor = Cursor()
        self.icons = ['icon_cube', 'icon_box', 'icon_spinned', 'icon_8d']
        self.plr = pg.Rect(0,0,WIDTH/51.2,HEIGHT/38.4)
        self.plr_img = pg.transform.scale(pg.image.load('assets/icons/'+r.choice(self.icons)+'.png'), (self.plr.width, self.plr.height))
        self.cap = cap
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()
        
    def instance(self):
        self.cursor.run()
        if cursor.colliderect(self.plr):
            if not self.game.paused:
                if not self.cap:
                    self.cap = 1
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()
               
        self.game.app.sc.blit(self.plr_img,(self.plr.left,self.plr.top))   
        
        if self.cap:
            if self.game.app.cap_mode == 0:
                self.plr.left = self.mouse_x - self.plr.width/2
                self.plr.top = self.mouse_y - self.plr.height/2
            elif self.game.app.cap_mode == 1:
                self.plr.left = self.mouse_x - self.plr.width
                self.plr.top = self.mouse_y - self.plr.height
            elif self.game.app.cap_mode == 2:
                self.plr.left = self.mouse_x
                self.plr.top = self.mouse_y
        else:
            pass
    def check(self):
        for i in range(len(self.game.level.kb[self.game.level.ln])):
            self.kb = pg.Rect(self.game.level.kb[self.game.level.ln][i][0], self.game.level.kb[self.game.level.ln][i][1], self.game.level.kb[self.game.level.ln][i][2], self.game.level.kb[self.game.level.ln][i][3])
            if self.plr.colliderect(self.kb):
                self.reset()       
                self.cap = 0
    def check_win(self):
        if self.plr.colliderect(self.game.finish.rect):
            print('Level '+str(self.game.level.ln),'Completed')
            self.game.level.ln += 1
            self.reset()
      
    def reset(self):
        self.cap = 0
        self.plr.left = self.game.level.sl[self.game.level.ln][0]
        self.plr.top = self.game.level.sl[self.game.level.ln][1]
        
class Level:
    def __init__(self, game, ln=0):
        self.game = game
        self.frame = [[0,0,WIDTH,HEIGHT/21],[0,HEIGHT-HEIGHT/21+2,WIDTH,HEIGHT/21],
                     [0,0,WIDTH/30,HEIGHT],[WIDTH-WIDTH/30+1,0,WIDTH/30,HEIGHT]]
        self.ln = ln
        self.kb = [
                        [
                             self.frame[0], self.frame[1], self.frame[2], self.frame[3],
                             [WIDTH/1.77, HEIGHT/6.92, WIDTH/24.98, HEIGHT/1.17], [WIDTH/3.2, HEIGHT/2.19, WIDTH/1.83, HEIGHT/17.35],
                             [WIDTH/1.32, 0, WIDTH/4.11, HEIGHT/3.93], [WIDTH/1.39, HEIGHT/1.42, WIDTH/3.56, HEIGHT/17.35],
                             [0, HEIGHT/1.42, WIDTH/2.56, HEIGHT/17.35], [0, 0, WIDTH/6.09, HEIGHT/1.42], [0, 0, WIDTH/2.34, HEIGHT/3.89]
                        ], 
                        [
                              [0, 0, WIDTH/1.0, HEIGHT/38.4], [0, HEIGHT/38.4, WIDTH/51.5, HEIGHT/1.04], [0, HEIGHT/1.02, WIDTH/1.0, HEIGHT/38.4], [WIDTH/1.02, HEIGHT/38.4, WIDTH/51.5, HEIGHT/1.02], [WIDTH/8.58, HEIGHT/38.4, WIDTH/25.75, HEIGHT/1.48], [WIDTH/51.5, HEIGHT/1.1, WIDTH/2.71, HEIGHT/12.8], [WIDTH/2.86, HEIGHT/4.27, WIDTH/25.75, HEIGHT/1.38], [WIDTH/6.5, HEIGHT/1.54, WIDTH/10.3, HEIGHT/19.2], [WIDTH/3.96, HEIGHT/4.27, WIDTH/10, HEIGHT/19.2], [WIDTH/2.06, 0, WIDTH/25.75, HEIGHT/1.42], [WIDTH/2.71, HEIGHT/1.16, WIDTH/1.61, HEIGHT/7.68], [WIDTH/1.61, HEIGHT/5.49, WIDTH/25.75, HEIGHT/1.42], [WIDTH/4.29, HEIGHT/2.26, WIDTH/25.75, HEIGHT/19.2], [WIDTH/1.32, 0, WIDTH/25.75, HEIGHT/1.37], [WIDTH/1.12, HEIGHT/5.49, WIDTH/10.3, HEIGHT/1.42]

                        ],      
                        [
                            [300,300,20,20], [240,240,20,20] 
                        ]
                  ]
        self.sl = [
                    [WIDTH/5, HEIGHT/1.2],
                    [WIDTH/20.5, HEIGHT/13.4],
                    [WIDTH/1.5, HEIGHT/3]
                  ]
        self.fl = [
                    [WIDTH/1.33, HEIGHT/1.322, WIDTH/4.39, HEIGHT/2.48],
                    [WIDTH/1.12, HEIGHT/38.4, WIDTH/9.31, HEIGHT/6.45],
                    [0,0,85,80]
                  ]
        self.dark = [1.1,1]
        for i in range(900):
            self.kb.append([[r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(0,100),r.randint(0,100)],
                             [r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(10,400),r.randint(10,400)],
                             [r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(50,500),r.randint(50,500)]])
            self.sl.append([r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(0,100),r.randint(0,100)])
            self.fl.append([r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(0,100),r.randint(0,100)])
            self.dark.append(r.randint(0,1))
            
        self.game.finish = Obstacle(self.game, self.fl[self.ln][0], self.fl[self.ln][1], self.fl[self.ln][2], self.fl[self.ln][3], type='finish')
    def run(self):
        self.game.finish = Obstacle(self.game, self.fl[self.ln][0], self.fl[self.ln][1], self.fl[self.ln][2], self.fl[self.ln][3], type='finish')
        self.game.finish.blit()
        for i in range(len(self.kb[self.ln])):
            self.game.block = Obstacle(self.game, self.kb[self.ln][i][0], self.kb[self.ln][i][1], self.kb[self.ln][i][2], self.kb[self.ln][i][3])
            self.game.block.blit()
            
        self.ln_text = pg.font.SysFont('Courier new', round(WIDTH/85.33)).render('Level: '+str(self.ln),1,(100,255,100))
        self.game.app.sc.blit(self.ln_text,(0,0))
        if self.dark[self.ln]:
            self.game.cover.run()
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
    def __init__(self, game, l=0, t=0, w=150, h=60, shadow=1, text='Button', clr=(100,100,100), hclr=(150,150,150), pclr=(25,25,25), lo=0, to=0, action=None):
        self.game = game
        self.shadow = shadow
        self.shadow_rect = pg.Rect(l+2,t+2,w,h)
        self.font = pg.font.SysFont('Courier new', round(WIDTH/25.6))  
        self.text = self.font.render(text,1,(0,0,0))
        self.clr = clr
        self.bclr = clr
        self.pclr = pclr
        self.hclr = hclr
        self.rect = pg.Rect(l,t,w,h)
        self.l = l
        self.t = t
        self.w = w
        self.h = h
        self.lo = lo
        self.to = to
        self.action = action
        self.press = 0
    def run(self):
        self.blit()
        self.check()
    def blit(self):
        if self.shadow:
            pg.draw.rect(self.game.app.sc, (0,0,0), self.shadow_rect)
        pg.draw.rect(self.game.app.sc, self.clr, self.rect)
        self.game.app.sc.blit(self.text,(self.l+self.w/6-self.lo, self.t+self.h/10-self.to))
    def check(self):
        self.pressed = pg.mouse.get_pressed()
        if self.rect.colliderect(cursor):
            self.clr = self.hclr
            if self.pressed[0]:
                self.press = 1
                self.clr = self.pclr
            elif not self.pressed[0] and self.press:
                self.press = 0
                self.actions()
                self.clr = self.bclr
                time.sleep(0.01)
                
        else:
            self.press = 0
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
class Animation():
    def __init__(self, game):
        self.game = game
        self.player = Player(self)
        self.player.plr.left = WIDTH/1.5
        self.player.plr.top = -self.player.plr.height
        self.list = [pg.Rect(r.randint(round(WIDTH/3), round(WIDTH/1.001)), r.randint(0,HEIGHT-50), r.randint(round(WIDTH/64), round(WIDTH/16)), r.randint(round(HEIGHT/64), round(HEIGHT/8))) for i in range(5)]
    def run(self):
        pg.draw.rect(self.game.app.sc, (0,0,0), (WIDTH/3, 0, WIDTH/64, HEIGHT))
        pg.draw.rect(self.game.app.sc, (0,0,0), (WIDTH-WIDTH/64, 0, WIDTH/64, HEIGHT))
        for i in range(len(self.list)):
            self.kb = pg.Rect(self.list[i][0], self.list[i][1], self.list[i][2], self.list[i][3])
            if self.player.plr.colliderect(self.kb):
                self.player.plr.top = -self.player.plr.height
                self.player.plr.left = WIDTH/1.5
            if self.player.plr.left <= WIDTH/1.5:
                self.player.plr.left = WIDTH/1.5 + 10
            elif self.player.plr.left >= WIDTH-WIDTH/64:
                self.player.plr.left = WIDTH-WIDTH/64 - 10
        for i in range(5):
            pg.draw.rect(self.game.app.sc, (0,0,0), self.list[i])
        self.game.app.sc.blit(self.player.plr_img,(self.player.plr.left, self.player.plr.top))
        if r.randint(1,125) == 1:
            self.mov = r.randint(-10,10)
            for i in range(10):
                self.player.plr.left += self.mov
                self.player.plr.top += 1
        for i in range(2):
            self.player.plr.top += 1
        if self.player.plr.top >= HEIGHT+self.player.plr.height:
            self.player.plr.top = -15
            #self.player.plr.left = WIDTH/1.5
            
class Game:
    def __init__(self, app):
        self.app = app
        self.menu_animation = Animation(self)
        self.player = Player(self)
        self.level = Level(self)
        self.cover = Cover(self)
        self.cursor = Cursor()
        self.tab = 'menu'
        self.paused = False
        self.cap_mode_hint = ['Middle', 'Bottom-right', 'Top-left']
        self.font = pg.font.SysFont('Courier new', round(WIDTH/20.48))
        self.editor_font = pg.font.SysFont('Courier new', round(WIDTH/68.27))
        self.play_button = Button(self, 0, HEIGHT/3, WIDTH/6.67, HEIGHT/10, text='Play', action='play', to=-HEIGHT/125)
        self.icons_button = Button(self, 0, HEIGHT/3+HEIGHT/8, WIDTH/6.67, HEIGHT/10, text='Avatar', lo=WIDTH/50, to=-HEIGHT/125, action='icons')
        self.editor_button = Button(self, 0, HEIGHT/3+(HEIGHT/8)*2, WIDTH/6.67, HEIGHT/10, text='Editor', lo=WIDTH/50, to=-HEIGHT/125, action='editor') 
        self.settings_button = Button(self, 0, HEIGHT/3+(HEIGHT/8)*3, WIDTH/5, HEIGHT/10, text='Settings', lo=WIDTH/35, to=-HEIGHT/125, action='settings') 
        self.exit_button = Button(self, 0, HEIGHT/3+(HEIGHT/8)*4, WIDTH/6.67, HEIGHT/10, text='Exit', action='leave', to=-HEIGHT/125)
        self.bool_music_button = Button(self, WIDTH//25, HEIGHT//2.25, WIDTH/25, WIDTH/25, text='•', action='bool_music')
        self.bool_fullscreen_button = Button(self, WIDTH//25, HEIGHT//2.25+50, WIDTH/25, WIDTH/25, text='•', action='bool_fullscreen')
        self.bool_capmode_button = Button(self, WIDTH//25, HEIGHT//2.25+100, WIDTH/25, WIDTH/25, text='•', action='bool_cap_mode')
        self.bool = ''
        self.back_button = Button(self, 0, 0, WIDTH/20, WIDTH/20, text='←', action='menu', to=HEIGHT/125)
        self.logo = pg.Rect(0, WIDTH/64, WIDTH/4, (WIDTH/4)/1.45)
        #self.logo_img = self.plr_img = pg.transform.scale(pg.image.load('assets/logo.png'), (self.logo.width, self.logo.height))
        
        #Editor
        self.obj_list = self.level.frame
        self.grid_size = 10
        self.gridlist = []
        self.left, self.top, self.right, self.bottom = 0, 0, 0, 0 # To prevent crashes
        self.update_grid()
    def background(self):
        self.app.sc.fill((0,0,0))
        pg.draw.rect(self.app.sc,(255,255,255),(0,0,WIDTH,HEIGHT))
    def update_grid(self):
        self.gridlist = []
        self.linex_list = [pg.Rect(0, i*self.grid_size, WIDTH, 1) for i in range(round(WIDTH/self.grid_size)+1)]
        self.liney_list = [pg.Rect(i*self.grid_size, 0, 1, HEIGHT) for i in range(round(WIDTH/self.grid_size)+1)]
        for x in range(len(self.linex_list)):
            self.linex = self.linex_list.pop(len(self.linex_list)-1)
            self.gridlist.append(self.linex)
        for y in range(len(self.liney_list)):
            self.liney = self.liney_list.pop(len(self.liney_list)-1)  
            self.gridlist.append(self.liney)
    def draw_grid(self):
        for k in range(len(self.gridlist)):
            pg.draw.rect(self.app.sc, (25,25,25), self.gridlist[k])
    def set(self):
        self.bool = ''
        time.sleep(0.05)
        self.app.write_config()
    
    def run(self):
        self.key = pg.key.get_pressed()
        self.cursor.run()
        self.background()
        if self.tab == 'menu':
            #self.app.sc.blit(self.logo_img,(self.logo.left,self.logo.top))
            self.menu_animation.run()
            self.play_button.run()
            self.icons_button.run()
            self.editor_button.run()
            self.settings_button.run()  
            self.exit_button.run()
        elif self.tab == 'editor':
            self.pressed = pg.mouse.get_pressed()
            if self.pressed[0]:
                self.left, self.top = pg.mouse.get_pos()
                self.left = round(self.left/self.grid_size)*self.grid_size
                self.top = round(self.top/self.grid_size)*self.grid_size
                print(self.left, self.top)
                
            if self.pressed[2]:
                self.right, self.bottom = pg.mouse.get_pos()
                self.right = round(self.right/self.grid_size)*self.grid_size
                self.bottom = round(self.bottom/self.grid_size)*self.grid_size
                print(self.right, self.bottom)
                
            if self.key[pg.K_UP]:
                self.obj_list = [[0,0,WIDTH,HEIGHT/21],[0,HEIGHT-HEIGHT/21+2,WIDTH,HEIGHT/21],
                                [0,0,WIDTH/30,HEIGHT],[WIDTH-WIDTH/30+1,0,WIDTH/30,HEIGHT]]
            if self.key[pg.K_DOWN]:
                for i in range(len(self.obj_list)):
                    if self.obj_list[i][0] != 0:
                        self.obj_list[i][0] = 'WIDTH/'+str(round(WIDTH/self.obj_list[i][0],3))
                    else:
                        self.obj_list[i][0] = 0
                    if self.obj_list[i][1] != 0:
                        self.obj_list[i][1] = 'HEIGHT/'+str(round(HEIGHT/self.obj_list[i][1],3))
                    else:
                        self.obj_list[i][1] = 0
                    if self.obj_list[i][2] != 0:
                        self.obj_list[i][2] = 'WIDTH/'+str(round(WIDTH/self.obj_list[i][2],3))
                    else:
                        self.obj_list[i][2] = 0
                    if self.obj_list[i][3] != 0:
                        self.obj_list[i][3] = 'HEIGHT/'+str(round(HEIGHT/self.obj_list[i][3],3))
                    else:
                        self.obj_list[i][3] = 0
                             
                print(self.obj_list)
                self.obj_list = [[0,0,WIDTH,HEIGHT/21],[0,HEIGHT-HEIGHT/21+2,WIDTH,HEIGHT/21],
                                 [0,0,WIDTH/30,HEIGHT],[WIDTH-WIDTH/30+1,0,WIDTH/30,HEIGHT]]
                time.sleep(0.33)
                
            if self.key[pg.K_RIGHT]:
                self.grid_size += 5
                time.sleep(0.1)
                if self.grid_size == 4:
                    self.grid_size = 5
                self.update_grid()
                
            if self.key[pg.K_LEFT]:
                self.grid_size -= 5
                if self.grid_size == 0:
                    self.grid_size = -1
                time.sleep(0.1)
                self.update_grid()
                
            if self.key[pg.K_SPACE]:
                self.obj_list.append([self.left, self.top, self.right-self.left, self.bottom-self.top])
                time.sleep(0.2)
            
            if self.key[pg.K_TAB]:
                self.app.sc.blit(self.player.plr_img,(self.cursor.mouse_x-self.player.plr.width,self.cursor.mouse_y-self.player.plr.height))
            if self.key[pg.K_BACKSPACE]:
                if self.obj_list != []:
                    self.del_obj = self.obj_list.pop(len(self.obj_list)-1)
                else:
                    print('No elements in level editor to delete')
                time.sleep(0.2)
            
                
            for i in range(len(self.obj_list)):
                self.rect = Obstacle(self, self.obj_list[i][0],self.obj_list[i][1],self.obj_list[i][2],self.obj_list[i][3])
                self.rect.blit()
            self.draw_grid()
            self.app.sc.blit(self.editor_font.render('Grid:'+str(self.grid_size)+'; K_LEFT K_RIGHT to change the value; K_UP to reset; K_DOWN to print result into console and reset.',0,(150,215,150)),(0,0))
            self.app.sc.blit(self.editor_font.render('TAB to show test player; BACKSPACE to remove last object.',0,(150,215,150)),(0,15))
            self.app.sc.blit(self.editor_font.render('Total elements: '+str(len(self.obj_list))+'; LMB to set left&top of rect; RMB to set right&bottom of rect; SPACE to apply.',0,(150,215,150)),(0,HEIGHT-15))
            
                
            if self.key[pg.K_ESCAPE]:
                self.tab = 'menu'
                
        elif self.tab == 'icons':
            self.back_button.run()
        elif self.tab == 'settings':
            self.app.sc.blit(self.font.render('Res: '+str(WIDTH)+'; '+str(HEIGHT),0,(0,0,0)),(WIDTH//10,HEIGHT//2-100))
            self.app.sc.blit(self.font.render('Music: '+str(self.app.music_state),0,(0,0,0)),(WIDTH//10,HEIGHT//2-50))
            self.app.sc.blit(self.font.render('Fullscreen: '+str(self.app.fullscreen),0,(0,0,0)),(WIDTH//10,HEIGHT//2))
            self.app.sc.blit(self.font.render('Cap mode: '+str(self.app.cap_mode)+' ('+self.cap_mode_hint[self.app.cap_mode]+')',0,(0,0,0)),(WIDTH//10,HEIGHT//2+50))
            
            self.bool_music_button.run()
            self.bool_fullscreen_button.run()
            self.bool_capmode_button.run()
            self.back_button.run()
            if self.bool == 'music':
                if self.app.music_state:
                    self.app.music_state = 0
                else:
                    self.app.music_state = 1
                self.set()
            if self.bool == 'fullscreen':
                if self.app.fullscreen:
                    self.app.fullscreen = 0
                else:
                    self.app.fullscreen = 1
                self.app.check_fullscreen()
                self.set()
            if self.bool == 'cap_mode':
                self.app.cap_mode += 1
                if self.app.cap_mode > 2:
                    self.app.cap_mode = 0
                self.set()
            
        elif self.tab == 'play':
            self.player.instance()
            self.player.check()
            self.player.check_win()
            self.level.run()
            if self.key[pg.K_UP]:
                self.level.ln -= 1
                time.sleep(0.15)
            if self.key[pg.K_DOWN]:
                self.level.ln += 1
                time.sleep(0.15)
            if self.key[pg.K_LEFT]:
                self.player.plr.left -= 20
                self.player.plr.top -= 20
            if self.key[pg.K_ESCAPE]:
                self.tab = 'menu'
            if self.key[pg.K_SPACE]:
                if self.paused:
                    self.paused = 0
                else:
                    self.paused = 1
                time.sleep(0.1)
            if self.paused:
                self.pause = self.font.render('-- PAUSE --',0,(255,255,255))
                self.app.sc.blit(self.pause,(WIDTH//3,HEIGHT//2-50))
        else:
            print("This kind of tab does not exist.")
            self.tab = 'menu'

class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.read_config()
        self.check_music()
        self.play_music()
        self.game = Game(self)
        #print(self.config.read(1))
        
    def exit(self):
        pg.quit()
        sys.exit()
    def read_config(self):
        self.config = open('assets/cfg.txt', 'r')
        self.music_state = int(self.config.read(1))
        self.fullscreen = int(self.config.read(1))
        self.cap_mode = int(self.config.read(1))
        self.check_fullscreen()
        self.config.close()
    def write_config(self):
        self.config = open('assets/cfg.txt', 'w')
        self.config.write(str(self.music_state)+str(self.fullscreen)+str(self.cap_mode))
        self.config.close()
        self.config = open('assets/cfg.txt', 'r')
        print(self.config.read())
            
    def check_fullscreen(self):
        if self.fullscreen:
            self.sc = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        else:
            self.sc = pg.display.set_mode((WIDTH, HEIGHT))
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
        elif not self.music_state:
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