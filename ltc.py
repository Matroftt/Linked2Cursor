'''
list of some abbreviations in this code
ln - level number
sl - spawn location
fl - finish location
kb - killblock/killbrick
plr - player
l - left; t - top; w - width; h - height
lo - left offset; to - top offset
lw, lh - level width, level height
(x)l - x left, (x)w - x width (e.g. zone left)

clr - colour; hclr - highlight colour; bclr - backup colour; pclr - press colour
list of hotkeys
space - pause
arrow up - previous level
arrow down - next level
arrow left - moves character up and left
escape - exit to menu
backspace - reset resolution to 640, 480
'''


import pygame as pg, random as r, sys, time
cursor = pg.Rect(0,0,1,1)
WIDTH, HEIGHT = 800, 600
lw, lh = 800, 600

def draw_text(x=0, y=0, data='Text', size=32, color=(0, 255, 0), smooth=1):
    text = app.font.fonts[size].render(data, smooth, color)
    app.sc.blit(text,(x,y))
    

class Font:
    def __init__(self, app):
        self.app = app
        self.fonts = []
        for i in range(100):
            self.fonts.append(pg.font.SysFont('Courier new', i))
class Cover:
    def __init__(self, game):
        self.game = game
        self.cover = pg.Rect(500, 500, 296, 296)
        self.cover_img = pg.transform.scale(pg.image.load('assets/cover.png'), (self.cover.width, self.cover.height))
    def run(self):
        self.blit()
        self.cover.centerx = self.game.player.plr.left + self.game.player.plr.width/2
        self.cover.centery = self.game.player.plr.top + self.game.player.plr.height/2
        
    def blit(self):
        app.sc.blit(self.cover_img,(self.cover.left,self.cover.top))
        self.rect1 = pg.Rect(0,self.cover.top-HEIGHT,WIDTH,HEIGHT)
        self.rect2 = pg.Rect(0,self.cover.bottom,WIDTH,HEIGHT)
        self.rect3 = pg.Rect(self.cover.right,0,WIDTH,HEIGHT)
        self.rect4 = pg.Rect(self.cover.left-WIDTH,0,WIDTH,HEIGHT)
        pg.draw.rect(app.sc, (0,0,0), self.rect1)
        pg.draw.rect(app.sc, (0,0,0), self.rect2)
        pg.draw.rect(app.sc, (0,0,0), self.rect3)
        pg.draw.rect(app.sc, (0,0,0), self.rect4)
        
        
        
        
class Cursor:
    def __init__(self):
        global cursor
        self.cursor = cursor
    def run(self):
        self.mouse_x, self.mouse_y = pg.mouse.get_pos()
        cursor.left = lw*(self.mouse_x/WIDTH)
        cursor.top  = lh*(self.mouse_y/HEIGHT)
        #cursor.left = self.mouse_x
        #cursor.top = self.mouse_y
        
class Particle:
    def __init__(self, player, clr=(0,0,0), dir='random', type='rect', shrink=0):
        self.player = player
        self.clr = clr
        self.dir = dir
        self.type = type
        self.shrink = shrink
        if self.dir == 'random':
            self.x_dir, self.y_dir = r.randint(-4, 4), r.randint(-4, 4)
        self.x, self.y = self.player.died_x, self.player.died_y
        self.d = 10
        if self.type == 'rect':
            self.instance = pg.Rect(self.x, self.y, 4, 4)
            self.w, self.h = self.instance.width, self.instance.height
        elif self.type == 'circle':
            self.instance = (self.x, self.y, self.d)
    def run(self):
        if self.type == 'rect':
            self.instance = pg.Rect(self.x, self.y, self.w, self.h)
            pg.draw.rect(app.sc, self.clr, self.instance)
            self.x += self.x_dir
            self.y += self.y_dir
            if self.x_dir > 0:
                self.x_dir += 0.4
            else:
                self.x_dir -= 0.4
            if self.y_dir > 0:
                self.y_dir += 0.4
            else:
                self.y_dir -= 0.4
            if self.shrink:
                self.w, self.h = self.w - 0.05, self.h - 0.05
        if self.type == 'circle':
            pg.draw.circle(app.sc, self.clr, (self.x, self.y), self.d, 1)
            self.d += self.d/10
        
        
class Player:
    def __init__(self, game, cap=0):
        self.game = game
        self.cursor = Cursor()
        self.get_plr_size()
        self.icons = ['icon_cube', 'icon_box', 'icon_spinned', 'icon_8d']
        self.plr = pg.Rect(250,250,20,20)
        try:
            self.plr_img = pg.transform.smoothscale(pg.image.load('assets/icons/'+self.icon_dir+'/'+r.choice(self.icons)+'.png'), (self.plr.width, self.plr.height))
        except FileNotFoundError:
            self.plr_img = pg.transform.smoothscale(pg.image.load('assets/icons/default.png'), (self.plr.width, self.plr.height))
        self.particles = []
        self.trails = []
        self.trail_count = 3
        self.particle_emit = 0
        self.particle_count = 10
        self.died_x, self.died_y = 0, 0
        for i in range(self.trail_count):
            self.trails.append([-100, -100])
        self.cap = cap
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()
    
    def get_plr_size(self):
        self.icon_dir = "20"
    def instance(self):
        #self.particle = Particle(self)
        self.cursor.run()
        if cursor.colliderect(self.plr):
            if not self.cap:
                self.cap = 1
        self.mouse_x,self.mouse_y = pg.mouse.get_pos()  
        
        if self.cap:
            if self.game.app.cap_mode == 0:
                self.plr.left = cursor.left - self.plr.width/2
                self.plr.top = cursor.top - self.plr.height/2
            elif self.game.app.cap_mode == 1:
                self.plr.left = cursor.left - self.plr.width
                self.plr.top = cursor.top- self.plr.height
            elif self.game.app.cap_mode == 2:
                self.plr.left = cursor.left
                self.plr.top = cursor.top
        
    def blit(self):
        self.trail()
        app.sc.blit(self.plr_img,(self.plr.left,self.plr.top))
        if self.particle_emit > 0:
            for i in range(self.particle_count+round(self.particle_count/5)+2):
                self.particles[i].run()
            self.particle_emit -= 0.02
    def emit(self):
        self.particles = []
        for i in range(self.particle_count):
            self.particles.append(Particle(self, clr=(0, 0, 0), shrink=1))
            self.particles[i].x, self.particles[i].y = self.died_x, self.died_y
        for i in range(round(self.particle_count/5)):
            self.particles.append(Particle(self, clr=(200, 0, 0), shrink=1))
            self.particles[i].x, self.particles[i].y = self.died_x, self.died_y
        for i in range(2):
            self.particles.append(Particle(self, clr=(0, 0, 0), type='circle'))
            self.particles[i].x, self.particles[i].y = self.died_x, self.died_y
            self.particles[i+self.particle_count+round(self.particle_count/5)].d += i*3
        self.particle_emit = 1
        
    def check(self):
        self.check_kb()
        if self.game.level.chase_use[self.game.level.ln]:
            self.check_chaser()
        if self.game.level.key_use[self.game.level.ln]:
            self.check_key()
        self.check_win()
    def check_kb(self):
        for i in range(len(self.game.level.kb[self.game.level.ln])):
            self.kb = pg.Rect(self.game.level.kb[self.game.level.ln][i][0], self.game.level.kb[self.game.level.ln][i][1], self.game.level.kb[self.game.level.ln][i][2], self.game.level.kb[self.game.level.ln][i][3])
            if self.plr.colliderect(self.kb):
                self.reset(1)       
                self.cap = 0
    def check_key(self):
        # Check for the keys
        for i in range(len(self.game.level.keys[self.game.level.ln])):
            self.key = pg.Rect(self.game.level.keys[self.game.level.ln][i][0], self.game.level.keys[self.game.level.ln][i][1], self.game.level.key.key.width, self.game.level.key.key.height)
            if self.plr.colliderect(self.key):
                self.game.level.keys[self.game.level.ln][i] = [WIDTH, HEIGHT, 0, 0]
                try:
                    for j in range(len(self.game.level.key_kb[self.game.level.ln][i])):
                        self.game.level.key_kb[self.game.level.ln][i][j] = None
                except IndexError:
                    pass
        # Check for the assigned kb's to keys
        for key in range(len(self.game.level.key_kb[self.game.level.ln])):
            for j in range(len(self.game.level.key_kb[self.game.level.ln][key])):
                if self.game.level.key_kb[self.game.level.ln][key][j] != None:
                    self.kb = pg.Rect(self.game.level.key_kb[self.game.level.ln][key][j][0], self.game.level.key_kb[self.game.level.ln][key][j][1], self.game.level.key_kb[self.game.level.ln][key][j][2], self.game.level.key_kb[self.game.level.ln][key][j][3])
                    if self.plr.colliderect(self.kb):
                        self.reset(1)       
                        self.cap = 0
    def check_chaser(self):
        if self.plr.colliderect(self.game.level.chaser.chaser):
            self.reset(1)
    def check_win(self):
        if self.plr.colliderect(self.game.finish.rect):
            print('Level '+str(self.game.level.ln),'Completed')
            self.game.level.ln += 1
            self.reset()
      
    def reset(self, died=0):
        self.cap = 0
        if died:
            self.died_x = self.plr.left
            self.died_y = self.plr.top
            self.emit()
        self.plr.left = self.game.level.sl[self.game.level.ln][0]
        self.plr.top = self.game.level.sl[self.game.level.ln][1]
        if self.game.level.key_use[self.game.level.ln]:
            for i in range(4):
                self.game.level.keys[self.game.level.ln][0][i] = self.game.level.keys_backup[self.game.level.ln][0][i]
                self.game.level.key_kb = self.game.level.key_kb_backup # to be fixed
    def trail(self):
        if self.trail_count > 0:
            for i in range(self.trail_count):
                app.sc.blit(self.plr_img, (self.trails[i][0],self.trails[i][1]))
                
            if self.trails[0][0] == self.plr.left and self.trails[0][1] == self.plr.top:
                self.trails.insert(0, [WIDTH, HEIGHT])
                self.trails.pop(self.trail_count-1)
            else:
                self.trails.insert(0, [self.plr.left, self.plr.top])
                self.trails.pop(self.trail_count-1)
        
        
class Level:
    def __init__(self, game, ln=0):
        self.game = game
        self.frame = [[0,0,lw, 30],[0,lh-30,lw,32],
                     [0,0,30,lh],[lw-30+1,0,30+1,lh]]
        self.ln = ln
        self.kb = [
                        [
                            [0, 0, lw/1.0, lh/25.6667], [0, lh/25.6667, lw/34.3333, lh/1.0405], [0, lh/1.0405, lw/1.0, lh]
                        ],
                        [
                             self.frame[0], self.frame[1], self.frame[2], self.frame[3],
                             [lw/1.77, lh/6.92, lw/24.98, lh/1.17], [lw/3.2, lh/2.19, lw/1.83, lh/17.35],
                             [lw/1.32, 0, lw/4.11, lh/3.93], [lw/1.39, lh/1.42, lw/3.56, lh/17.35],
                             [0, lh/1.42, lw/2.56, lh/17.35], [0, 0, lw/6.09, lh/1.42], [0, 0, lw/2.34, lh/3.89]
                        ], 
                        [
                              [0, 0, lw/1.0, lh/38.4], [0, lh/38.4, lw/51.5, lh/1.04], [0, lh/1.02, lw/1.0, lh/38.4], [lw/1.02, lh/38.4, lw/5, lh/1], [lw/8.58, lh/38.4, lw/25.75, lh/1.48], [lw/51.5, lh/1.1, lw/2.71, lh/12.8], [lw/2.86, lh/4.27, lw/25.75, lh/1.38], [lw/6.5, lh/1.54, lw/10.3, lh/19.2], [lw/3.96, lh/4.27, lw/10, lh/19.2], [lw/2.06, 0, lw/25.75, lh/1.42], [lw/2.71, lh/1.16, lw/1.61, lh/7.68], [lw/1.61, lh/5.49, lw/25.75, lh/1.42], [lw/4.29, lh/2.26, lw/25.75, lh/19.2], [lw/1.32, 0, lw/25.75, lh/1.37], [lw/1.12, lh/5.49, lw/10.3, lh/1.42]
                        ],      
                        [
                            [0, 0, lw/1.0, lh/21.0], [0, lh/1.0471, lw/1.0, lh/21.0], [0, 0, lw/30.0, lh/1.0], [lw/1.0334, 0, lw/30.0, lh/1.0], [lw/10.3, 0, lw/4.2917, lh/4.2778], [0, lh/2.9615, lw/3.0294, lh/7.7], [lw/2.4524, 0, lw/10.3, lh/1.3276], [lw/3.9615, lh/2.5389, lw/12.875, lh/3.2], [lw/10.3, lh/1.8333, lw/6.4375, lh/5.625], [lw/10.3, lh/2.2389, lw/12.875, lh/30.5], [lw/51.5, lh/1.1667, lw/1.051, lh/9.625], [lw/2.1458, 0, lw/1.9808, lh/6.4167], [lw/1.1196, lh/6.4167, lw/12.875, lh/1.6042], [lw/1.3205, lh/4.2778, lw/25.75, lh/1.5], [lw/1.6613, lh/4.2778, lw/17.1667, lh/1.925]
                        ],
                        [
                            [0, 0, lw/34.3333, lh/1.0], [lw/34.3333, 0, lw/1.03, lh/25.6667], [lw/1.03, lh/25.6667, lw/34.3333, lh/1], [lw/34.3333, lh/1.0405, lw/1.03, lh], [lw/34.3333, lh/25.6667, lw/4.4783, lh/4.2778], [lw/2.8611, 0, lw/1.5373, lh/3.6667], [lw/9.3636, lh/2.5667, lw/1.6094, lh/2.2], [lw/1.4733, lh/1.7111, lw/2.12, lh/9.625]
                        ],
                        [
                            [0, 0, 800, 30], [0, 570, 800, 32], [0, 0, 30, 600], [771, 0, 31, 600], [320, 240, 50, 60], [440, 220, 120, 80], [460, 130, 80, 50], [150, 80, 130, 120], [160, 320, 160, 120], [340, 310, 40, 50], [330, 410, 240, 110], [400, 280, 40, 90], [380, 310, 10, 10], [490, 330, 300, 130], [520, 90, 280, 130], [160, 230, 120, 70], [220, 210, 10, 20], [180, 300, 80, 10], [280, 120, 100, 80], [70, 320, 90, 20], [30, 210, 90, 90], [30, 370, 80, 70], [200, 440, 20, 90], [200, 550, 20, 20], [160, 440, 20, 20], [160, 480, 20, 90], [130, 440, 30, 20], [120, 460, 20, 60], [120, 540, 20, 10], [50, 480, 80, 20], [80, 460, 10, 10], [50, 440, 10, 10], [430, 520, 10, 30], [470, 520, 30, 10], [470, 560, 30, 20], [350, 520, 10, 30], [380, 540, 10, 20], [280, 520, 20, 10], [240, 530, 50, 30], [260, 460, 20, 40], [240, 490, 20, 20], [250, 510, 10, 10], [220, 450, 20, 20], [290, 470, 20, 10], [320, 500, 10, 10], [310, 440, 10, 10], [50, 500, 5, 50], [55, 545, 40, 5], [90, 520, 5, 25], [70, 520, 20, 5], [70, 525, 5, 10], [595, 460, 5, 60], [620, 520, 10, 50], [660, 450, 15, 75], [700, 500, 20, 60], [750, 450, 25, 75], [700, 470, 60, 10], [630, 530, 10, 10], [540, 530, 20, 20], [580, 550, 20, 20], [440, 340, 20, 20], [480, 320, 10, 20], [450, 300, 10, 10], [530, 300, 20, 10], [490, 320, 20, 10], [590, 250, 150, 50], [590, 300, 10, 10], [610, 240, 10, 10], [620, 300, 20, 10], [640, 240, 20, 10], [670, 300, 30, 10], [710, 240, 30, 10], [680, 220, 10, 10], [720, 320, 20, 10], [50, 160, 100, 10], [30, 110, 100, 10], [50, 80, 100, 10], [50, 120, 10, 20], [120, 140, 10, 20], [80, 135, 5, 5], [90, 130, 5, 5], [105, 155, 5, 5], [50, 30, 230, 30], [300, 30, 470, 30], [289, 84, 5, 11], [303, 83, 8, 13], [317, 84, 5, 10], [333, 84, 6, 8], [346, 87, 6, 9], [362, 85, 18, 17], [388, 84, 9, 6], [405, 85, 15, 8], [428, 87, 9, 36], [433, 90, 19, 13], [463, 92, 19, 10], [470, 124, 12, 5], [617, 16, 168, 130], [486, 93, 3, 8], [516, 95, 6, 3], [455, 170, 5, 5], [445, 165, 5, 5], [435, 145, 5, 5], [405, 115, 25, 10], [410, 145, 5, 5], [390, 145, 5, 5], [405, 170, 5, 5], [420, 185, 5, 10], [440, 200, 5, 0], [430, 195, 70, 5], [390, 230, 30, 30], [330, 200, 10, 20], [360, 220, 10, 20], [300, 240, 20, 10], [300, 220, 10, 20], [280, 270, 20, 10], [290, 300, 10, 20], [361, 376, 55, 11], [430, 375, 10, 5], [430, 385, 10, 5], [470, 405, 5, 5], [460, 370, 10, 10], [310, 540, 5, 5], [620, 460, 10, 10], [740, 550, 10, 10]
                        ]
                        # Levels data before this string should be reworked
                  ]
        self.sl = [
                    [lw/2, lh/2],
                    [lw/5, lh/1.2],
                    [lw/20.5, lh/13.4],
                    [lw/17.167, lh/7],
                    [lw/3.5, lh/24],
                    [663, 549]
                  ]
        self.fl = [
                    [lw/1.03, 0, lw, lh], 
                    [lw/1.33, lh/1.322, lw/4.39, lh/2.48],
                    [lw/1.12, lh/38.4, lw, lh],
                    [lw/3.179, lh/42.78, lw/9.1964, lh/7],
                    [lw/1.4733, lh/1.5528, lw/2.12, lh/6.4167],
                  ]
        self.key = Key(self, l=500, t=500)
        self.chaser = Chase(self, zl=100, zt=100, zw=400, zh=400, speed=2)
        
        self.keys = [ # List
                        [], [], [],  # Level
                        [
                            [lw/5.33678, lh/2.01044, self.key.key.width, self.key.key.height], # Keys
                            [lw/1.1087, lh/1.248, self.key.key.width, self.key.key.height]
                        ]
                    ]
        self.key_kb = [ # List
                               [], [], [], # Level
                               [ # Key
                                  [ # Linked blocks | Note: Will be drew only if key is assigned
                                      [lw/1.9846, lh/1.4051, lw/3.9, lh/24.8387]
                                  ],
                                  [
                                      [lw/3.0383, lh/7.33, lw/10.875, lh/8.405]
                                  ],      
                               ]
                       ]
        self.keys_backup, self.key_kb_backup = self.keys, self.key_kb
        
        self.key_use = []
        self.cover_use = [0,0,0,0,1,0,0]
        self.chase_use = [0,0,0,0,0,0,1]
        self.fillers()
        
        for i in range(len(self.keys)):
            if self.keys[i] == []:
                self.key_use.append(0)
            else:
                self.key_use.append(1)
                
        self.game.finish = Obstacle(self.game, self.fl[self.ln][0], self.fl[self.ln][1], self.fl[self.ln][2], self.fl[self.ln][3], type='finish') 
    def fillers(self):
        for i in range(900):
            self.kb.append([[r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(0,100),r.randint(0,100)],
                             [r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(10,400),r.randint(10,400)],
                             [r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(50,500),r.randint(50,500)]])
            self.sl.append([r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(0,100),r.randint(0,100)])
            self.fl.append([r.randint(0,WIDTH),r.randint(0,HEIGHT),r.randint(0,100),r.randint(0,100)])
            self.keys.append([])
            self.cover_use.append(r.randint(0,1))
            self.chase_use.append(0)
            

        
    def run_info(self, debug=0):
        draw_text(data='Level: '+str(self.ln), size=10, color=(100,255,100))
        if debug:
            draw_text(x=0, y=10, data='Trail count: '+str(self.game.player.trail_count), size=10, color=(100,255,100))
            draw_text(x=0, y=20, data='Cap: '+str(self.game.player.cap), size=10, color=(100,255,100))
    def run_text(self):
        if self.ln == 0:
            draw_text(x=29, y=29, data='Welcome to Linked to cursor, aka LTC!', size=13, color=(0,0,0))
            draw_text(x=29, y=29*3, data='To move your character, cover your cursor over it to capture him, and then move your cursor ', size=13, color=(0,0,0))
            draw_text(x=29, y=29*7, data='Red rectangles will lead you to next level', size=13, color=(0,0,0))
        if self.ln == 1:
            draw_text(x=53, y=470, data='Black rectangles can kill you', size=13, color=(0,0,0))
        if self.ln == 3:
            draw_text(x=53, y=470, data='Collect keys in order to open some (unmarked) gates', size=13, color=(0,0,0))
        if self.ln == 4:
            draw_text(x=400, y=20, data='Some levels can be really dark', size=13, color=(255,255,255))
        
    def run(self):
        if self.chase_use[self.ln]:
            self.chaser.run()
        self.game.player.blit()
        self.game.finish = Obstacle(self.game, self.fl[self.ln][0], self.fl[self.ln][1], self.fl[self.ln][2], self.fl[self.ln][3], type='finish')
        self.game.finish.blit()
        for i in range(len(self.kb[self.ln])):
            self.game.block = Obstacle(self.game, self.kb[self.ln][i][0], self.kb[self.ln][i][1], self.kb[self.ln][i][2], self.kb[self.ln][i][3])
            self.game.block.blit()
        if self.key_use[self.ln]:
            for i in range(len(self.keys[self.ln])):
                self.game.key = Key(self.game, l=self.keys[self.ln][i][0], t=self.keys[self.ln][i][1])
                self.game.key.run()
            for key in range(len(self.key_kb[self.ln])):
                for j in range(len(self.key_kb[self.ln][key])):
                    if self.key_kb[self.ln][key][j] != None:
                        self.game.block = Obstacle(self.game, self.key_kb[self.ln][key][j][0], self.key_kb[self.ln][key][j][1], self.key_kb[self.ln][key][j][2], self.key_kb[self.ln][key][j][3])
                        self.game.block.blit()
            
        if self.cover_use[self.ln]:
            self.game.cover.run()
        self.run_info(self.game.debug)
        self.run_text()

class Chase:
    def __init__(self, level, l=0, t=0, zl=400, zt=400, zw=400, zh=200, speed=1):
        self.level = level
        self.zone = pg.Rect(zl, zt, zw, zh)
        self.chaser = pg.Rect(zl+zw/2,zt+zh/2,50,50)
        self.chaser_img = pg.transform.smoothscale(pg.image.load('assets/chaser.png'), (self.chaser.width, self.chaser.height))
        self.chasing = 1
        self.frame = 0
        self.speed = speed
        self.zl, self.zt, self.zw, self.zh = zl, zt, zw, zh
        self.plr = self.level.game.player.plr
        if self.speed > 10:
            self.speed = 10
    def run(self):
        pg.draw.rect(self.level.game.app.sc, (150+10*self.speed, 50+10*self.speed, 50+10*self.speed), self.zone)
        self.level.game.app.sc.blit(self.chaser_img,(self.chaser.left,self.chaser.top))
        if self.plr.colliderect(self.zone):
            self.chase()
    def chase(self):
        self.animation()
        if self.chaser.left > self.plr.left-self.plr.width:
            self.chaser.left -= self.speed
        if self.chaser.left < self.plr.left-self.plr.width:
            self.chaser.left += self.speed
        if self.chaser.top > self.plr.top-self.plr.height:
            self.chaser.top -= self.speed
        if self.chaser.top < self.plr.top-self.plr.height:
            self.chaser.top += self.speed
        
        # Bounds
        
        if self.chaser.left < self.zl:
            self.chaser.left = self.zl
        if self.chaser.top < self.zt:
            self.chaser.top = self.zt
        if self.chaser.top > self.zt + self.zh - self.chaser.height:
            self.chaser.top = self.zt + self.zh - self.chaser.height
        if self.chaser.left > self.zl + self.zw - self.chaser.width:
            self.chaser.left = self.zl + self.zw - self.chaser.width
        
    def animation(self):
        if self.chasing:
            if self.frame == 0:
                self.chaser_img = pg.transform.scale(pg.image.load('assets/chaser.png'), (self.chaser.width, self.chaser.height))
                self.frame = 1
            elif self.frame == 1:
                self.chaser_img = pg.transform.scale(pg.image.load('assets/chaser2.png'), (self.chaser.width, self.chaser.height))
                self.frame = 2
            else:
                self.chaser_img = pg.transform.scale(pg.image.load('assets/chaser3.png'), (self.chaser.width, self.chaser.height))
                self.frame = 0
        
class Key:
    def __init__(self, level, l=0, t=0):
        self.level = level
        self.key = pg.Rect(l,t,32,15)
        self.key_img = pg.transform.smoothscale(pg.image.load('assets/key.png'), (self.key.width, self.key.height))
        
    def run(self):
        self.level.app.sc.blit(self.key_img,(self.key.left,self.key.top))
            
class Obstacle:
    def __init__(self, game, l=10, t=10, w=100, h=100, color=(0,0,0), type='kb'):
        self.game = game
        self.color = color
        self.type = type
        self.rect = pg.Rect(l,t,w,h)
        
        if self.type == 'finish' and self.color == (0,0,0):
            self.color = (100,5,5)
        
    def blit(self):
        pg.draw.rect(app.sc, self.color, self.rect)
class Button:
    def __init__(self, game, l=0, t=0, w=150, h=60, shadow=1, text='Button', clr=(100,100,100), hclr=(150,150,150), pclr=(25,25,25), lo=0, to=0, action=None):
        self.game = game
        self.shadow = shadow
        self.shadow_rect = pg.Rect(l+2,t+2,w,h)
        self.font = pg.font.SysFont('Courier new', 30)  
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
            pg.draw.rect(app.sc, (0,0,0), self.shadow_rect)
        pg.draw.rect(app.sc, self.clr, self.rect)
        app.sc.blit(self.text,(self.l+self.w/6-self.lo, self.t+self.h/10-self.to))
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
        elif list(self.action)[0] == 'a' and list(self.action)[1] == 'c' and list(self.action)[6] == '_':
            self.game.action = str(self.action.split('action_')[1])
        else:
            self.game.tab = self.action
class Animation:
    def __init__(self, game):
        self.game = game
        self.player = Player(self)
        self.player.plr.left = 427
        self.player.plr.top = -self.player.plr.height
        self.player.particle_emit = 0
        self.player.particle_count = 10
        self.direction = 'none'
        self.list = [pg.Rect(r.randint(213, 640), r.randint(0,HEIGHT-50), r.randint(round(10), round(WIDTH/16)), r.randint(8, 60)) for i in range(5)]
    def run(self):
        pg.draw.rect(app.sc, (0,0,0), (213, 0, 10, HEIGHT))
        pg.draw.rect(app.sc, (0,0,0), (WIDTH-10, 0, 10, HEIGHT))
        for i in range(len(self.list)):
            self.kb = pg.Rect(self.list[i][0], self.list[i][1], self.list[i][2], self.list[i][3])
            if self.player.plr.colliderect(self.kb):
                self.player.died_x, self.player.died_y = self.player.plr.centerx, self.player.plr.centery
                self.player.plr.top = -self.player.plr.height
                self.player.plr.left = 427
                self.player.emit()
            if self.player.plr.left <= 427:
                self.player.plr.left = 427 + 10
            elif self.player.plr.left >= WIDTH-10:
                self.player.plr.left = WIDTH-10 - 10
        for i in range(5):
            pg.draw.rect(app.sc, (0,0,0), self.list[i])
        
        if r.randint(1, 100) == 1:
            self.direction = 'left'
        elif r.randint(1, 100) == 2:
            self.direction = 'right'
            
        if self.direction == 'left':
            self.player.plr.left -= 2
            if r.randint(1, 25) == 1:
                self.direction = 'none'
        if self.direction == 'right':
            self.player.plr.left += 2
            if r.randint(1, 25) == 1:
                self.direction = 'none'
        self.player.plr.top += 2
        if self.player.plr.top >= HEIGHT+self.player.plr.height:
            self.player.plr.top = -self.player.plr.height
            #self.player.plr.left = 427
        if self.player.particle_emit > 0:
            for i in range(self.player.particle_count+round(self.player.particle_count/5+2)):
                self.player.particles[i].run()
            self.player.particle_emit -= 0.03
        app.sc.blit(self.player.plr_img,(self.player.plr.left, self.player.plr.top))
            
class Game:
    def __init__(self, app):
        self.app = app
        self.menu_animation = Animation(self)
        self.player = Player(self)
        self.level = Level(self)
        self.cover = Cover(self)
        self.cursor = Cursor()
        self.tab = 'menu'
        self.cap_mode_hint = ['Middle', 'Bottom-right', 'Top-left']
        self.resolution = 0
        self.resolutions_list = [[800, 600], [1024, 768], [1440, 1080], [1366, 768], [1440, 900], [1920, 1080]] # 1440x1080 and 1920x1080 can be laggy
        for i in range(len(self.resolutions_list)):
            if [WIDTH, HEIGHT] == self.resolutions_list[i]:
                self.resolution = i
                break
        self.prev_resolution = self.resolution
        self.debug = 1
        self.bg_clr = (5, 5, 5)
        
        self.font = pg.font.SysFont('Courier new', 39)
        self.editor_font = pg.font.SysFont('Courier new', 12)
        
        
        # Main Menu
        self.play_button = Button(self, 0, 200, 120, 60, text='Play', action='play', to=-4.8)
        self.icons_button = Button(self, 0, 200+75, 120, 60, text='Avatar', lo=16, to=-4.8, action='icons')
        self.editor_button = Button(self, 0, 200+(75)*2, 120, 60, text='Editor', lo=16, to=-4.8, action='editor') 
        self.settings_button = Button(self, 0, 200+(75)*3, 133, 60, text='Options', lo=23, to=-4.8, action='settings') 
        self.continue_button = Button(self, 0, 200, 150, 60, text='Continue', lo=23, to=-4.8, action='play')
        self.menu_button = Button(self, 0, 200+(75), 150, 60, text='To Menu', action='menu', lo=16, to=-4.8)
        self.exit_button = Button(self, 0, 200+(75)*4, 120, 60, text='Exit', action='leave', to=-4.8)
        
        self.logo = pg.Rect(0, 10, WIDTH/4, (WIDTH/4)/1.45)
        #self.logo_img = self.plr_img = pg.transform.scale(pg.image.load('assets/logo.png'), (self.logo.width, self.logo.height))
        
        # Settings
        self.apply_resolution_button = Button(self, 421, 200, 100, 32, lo=13, to=4, text='Apply', action='action_apply_resolution')
        self.bool_resolution_button = Button(self, 40, 200, 32, 32, text='•', action='action_change_resolution')
        self.bool_music_button = Button(self, 40, 200+39*1, 32, 32, text='•', action='action_music')
        self.bool_fullscreen_button = Button(self, 40, 200+39*2, 32, 32, text='•', action='action_fullscreen')
        self.bool_smooth_button = Button(self, 40, 200+39*3, 32, 32, text='•', action='action_smooth')
        self.bool_showfps_button = Button(self, 40, 200+39*4, 32, 32, text='•', action='action_fps')
        self.bool_capmode_button = Button(self, 40, 200+39*5, 32, 32, text='•', action='action_cap_mode')
        
        
        self.action = ''
        
        self.set_w, self.set_h = WIDTH, HEIGHT
        
        self.back_button = Button(self, 0, 0, 40, 40, text='←', action='menu', to=4.8)
    
        
        # Editor
        self.obj_list = self.level.frame
        self.grid_size = 10
        self.gridlist = []
        self.left, self.top, self.right, self.bottom = 0, 0, 0, 0 
        self.update_grid()
    def background(self):
        app.sc.fill(self.bg_clr)
        pg.draw.rect(app.sc,(255,255,255),(0,0,WIDTH,HEIGHT))
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
            pg.draw.rect(app.sc, (25,25,25), self.gridlist[k])
    def set(self):
        self.action = ''
        time.sleep(0.05)
        self.app.write_config()
    
    def run(self):
        global WIDTH, HEIGHT
        self.input = pg.key.get_pressed()
        self.cursor.run()
        self.background()
        if self.tab == 'menu':
            #app.sc.blit(self.logo_img,(self.logo.left,self.logo.top))
            self.menu_animation.run()
            self.play_button.run()
            self.icons_button.run()
            self.editor_button.run()
            self.settings_button.run()  
            self.exit_button.run()
            
            if self.input[pg.K_BACKSPACE]:
                WIDTH, HEIGHT = 640, 480
                self.app.write_config()
                self.app.set_resolution()
                
            if self.resolution != self.prev_resolution:
                self.prev_resolution = self.resolution
            else:
                self.set_w, self.set_h = WIDTH, HEIGHT
                self.resolution = self.prev_resolution
            
            
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
                
            if self.input[pg.K_UP]:
                self.obj_list = self.level.frame
            if self.input[pg.K_DOWN]:
                for i in range(len(self.obj_list)):
                    if self.obj_list[i][0] != 0:
                        self.obj_list[i][0] = round(self.obj_list[i][0],4)
                    else:
                        self.obj_list[i][0] = 0
                    if self.obj_list[i][1] != 0:
                        self.obj_list[i][1] = round(self.obj_list[i][1],4)
                    else:
                        self.obj_list[i][1] = 0
                    if self.obj_list[i][2] != 0:
                        self.obj_list[i][2] = round(self.obj_list[i][2],4)
                    else:
                        self.obj_list[i][2] = 0
                    if self.obj_list[i][3] != 0:
                        self.obj_list[i][3] = round(self.obj_list[i][3],4)
                    else:
                        self.obj_list[i][3] = 0
                             
                print(self.obj_list)
                self.obj_list = self.level.frame
                time.sleep(0.33)
                
            if self.input[pg.K_RIGHT]:
                self.grid_size += 5
                time.sleep(0.1)
                if self.grid_size == 4:
                    self.grid_size = 5
                self.update_grid()
                
            if self.input[pg.K_LEFT]:
                self.grid_size -= 5
                if self.grid_size == 0:
                    self.grid_size = -1
                time.sleep(0.1)
                self.update_grid()
                
            if self.input[pg.K_SPACE]:
                self.obj_list.append([self.left, self.top, self.right-self.left, self.bottom-self.top])
                time.sleep(0.2)
            
            if self.input[pg.K_TAB]:
                app.sc.blit(self.player.plr_img,(self.cursor.mouse_x-self.player.plr.width,self.cursor.mouse_y-self.player.plr.height))
            if self.input[pg.K_BACKSPACE]:
                if self.obj_list != []:
                    self.del_obj = self.obj_list.pop(len(self.obj_list)-1)
                else:
                    print('No elements in level editor to delete')
                time.sleep(0.2)
            
                
            for i in range(len(self.obj_list)):
                self.rect = Obstacle(self, self.obj_list[i][0],self.obj_list[i][1],self.obj_list[i][2],self.obj_list[i][3])
                self.rect.blit()
            self.draw_grid()
            app.sc.blit(self.editor_font.render('Grid:'+str(self.grid_size)+'; K_LEFT K_RIGHT to change the value; K_UP to reset; K_DOWN to print result into console and reset.',0,(150,215,150)),(0,0))
            app.sc.blit(self.editor_font.render('TAB to show test player; BACKSPACE to remove last object.',0,(150,215,150)),(0,15))
            app.sc.blit(self.editor_font.render('Total elements: '+str(len(self.obj_list))+'; LMB to set left&top of rect; RMB to set right&bottom of rect; SPACE to apply.',0,(150,215,150)),(0,HEIGHT-15))
            
                
            if self.input[pg.K_ESCAPE]:
                self.tab = 'menu'
                
        elif self.tab == 'icons':
            self.back_button.run()
        elif self.tab == 'settings':
            draw_text(x=88, y=200, data='Res: '+str(self.set_w)+'; '+str(self.set_h), size=39, color=(0,0,0))
            draw_text(x=88, y=200+39*1, data='Music: '+str(self.app.music_state), size=39, color=(0,0,0))
            draw_text(x=88, y=200+39*2, data='Fullscreen: '+str(self.app.fullscreen), size=39, color=(0,0,0))
            draw_text(x=88, y=200+39*3, data='Smooth screen: '+str(self.app.smoothing_screen), size=39, color=(0,0,0))
            draw_text(x=88, y=200+39*4, data='Show FPS: '+str(self.app.show_fps), size=39, color=(0,0,0))
            draw_text(x=88, y=200+39*5, data='Cap mode: '+str(self.app.cap_mode)+' ('+self.cap_mode_hint[self.app.cap_mode]+')', size=39, color=(0,0,0))
            
            self.bool_resolution_button.run()
            self.apply_resolution_button.run()
            
            self.bool_music_button.run()
            self.bool_fullscreen_button.run()
            self.bool_capmode_button.run()
            self.bool_smooth_button.run()
            self.bool_showfps_button.run()
            
            self.back_button.run()
            
            
            if self.action == 'music':
                if self.app.music_state:
                    self.app.music_state = 0
                else:
                    self.app.music_state = 1
                self.set()
            if self.action == 'fullscreen':
                if self.app.fullscreen:
                    self.app.fullscreen = 0
                else:
                    self.app.fullscreen = 1
                self.app.check_fullscreen()
                self.set()
            if self.action == 'cap_mode':
                self.app.cap_mode += 1
                if self.app.cap_mode > 2:
                    self.app.cap_mode = 0
                self.set()
            if self.action == 'fps':
                if self.app.show_fps:
                    self.app.show_fps = 0
                else:
                    self.app.show_fps = 1
                self.set()
            
            if self.action == 'smooth':
                if self.app.smoothing_screen:
                    self.app.smoothing_screen = 0
                else:
                    self.app.smoothing_screen = 1
                self.set()
            if self.action == 'change_resolution':
                self.set_w, self.set_h = self.resolutions_list[self.resolution-1][0], self.resolutions_list[self.resolution-1][1]
                self.resolution -= 1
                if self.resolution < 0:
                    self.resolution = len(self.resolutions_list)-1
                self.action = '' #self.set()
            if self.action == 'apply_resolution':
                WIDTH, HEIGHT = self.set_w, self.set_h
                self.app.set_resolution()
                self.set()
        elif self.tab == 'pause':
            draw_text(data='Paused', size=80, color=(0,0,0))
            self.continue_button.run()
            self.menu_button.run()
        elif self.tab == 'play':
            self.player.instance()
            if self.input[pg.K_TAB] == False: # Press TAB to noclip
                self.player.check()
            self.level.run()
            if self.input[pg.K_UP]:
                self.level.ln -= 1
                self.player.reset()
                time.sleep(0.15)
            if self.input[pg.K_DOWN]:
                self.level.ln += 1
                self.player.reset()
                time.sleep(0.15)
            if self.input[pg.K_LEFT]:
                self.player.plr.left -= 20
                self.player.plr.top -= 20
            if self.input[pg.K_ESCAPE]:
                self.tab = 'menu'
            if self.input[pg.K_SPACE]:
                self.player.cap = 0
                self.tab = 'pause'
        else:
            print("This kind of tab does not exist.")
            self.tab = 'menu'

class App:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.set_prefs()
        try:
            self.read_config()
        except:
            self.write_config(defaults=1)
            print('[!] cfg.txt is corrupted, now restored to default')
            self.read_config()
        self.check_music()
        self.play_music()
        self.font = Font(self)
        self.game = Game(self)
        font = pg.font.SysFont('Courier new', 32)
        
    def exit(self):
        pg.quit()
        sys.exit()
    def set_prefs(self):
        pg.display.set_caption('Linked 2 Cursor')
        pg.display.set_icon(pg.image.load('assets/icons/default.png'))
    def read_config(self):
        global WIDTH, HEIGHT
        self.config = open('assets/cfg.txt', 'r')
        WIDTH, HEIGHT = int(self.config.readline()), int(self.config.readline())
        self.music_state = int(self.config.readline())
        self.fullscreen = int(self.config.readline())
        self.smoothing_screen = int(self.config.readline())
        self.show_fps = int(self.config.readline())
        self.cap_mode = int(self.config.readline())
        self.check_fullscreen()
        self.config.close()
        
        
    def write_config(self, defaults=0):
        if defaults != 1:
            self.config = open('assets/cfg.txt', 'w')
            self.config.write(str(WIDTH)+'\n'+str(HEIGHT)+'\n'+str(self.music_state)+'\n'+str(self.fullscreen)+'\n'+str(self.smoothing_screen)+'\n'+str(self.show_fps)+'\n'+str(self.cap_mode))
            self.config.close()
        else:
            self.config = open('assets/cfg.txt', 'w')
            self.config.write('800\n600\n0\n0\n1\n1\n0')
            self.config.close()
    def set_resolution(self):
        self.check_fullscreen()
        self.game = Game(self)
    def check_fullscreen(self):
        self.actual_sc = pg.display.set_mode((WIDTH, HEIGHT))
        if self.fullscreen:
            self.actual_sc = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        #self.sc = self.actual_sc.copy()
        self.sc = pg.Surface((lw, lh))
            
    def play_music(self):
        self.music = pg.mixer.music.load('assets/bullfrog_report_th.mp3')
        pg.mixer.music.play(-1)

    def check_events(self):     
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exit()
    
    def check_music(self):
        pg.mixer.music.pause()
        if self.music_state:
            pg.mixer.music.unpause()
    def run(self):
        while True:
            self.game.run()
            if self.show_fps:
                draw_text(x=lw-39, y=0, data=str(round(self.clock.get_fps())))
            if self.smoothing_screen:
                self.actual_sc.blit(pg.transform.smoothscale(self.sc, (WIDTH, HEIGHT)), (0,0))
            else:
                self.actual_sc.blit(pg.transform.scale(self.sc, (WIDTH, HEIGHT)), (0,0))
            self.check_events()
            self.check_music()
            pg.display.update()
            self.clock.tick(60)

if __name__ == '__main__':
    app = App()
    app.run()