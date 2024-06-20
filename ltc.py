'''
list of some abbreviations in this code
ln - level number
sl - spawn location
fl - finish location
kb - killblock/killbrick
plr - player
l - left; t - top; w - width; h - height
lo - left offset; to - top offset
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

def draw_text(x=0, y=0, data='Text', size=round(32), color=(100,100,100), smooth=1):
    text = pg.font.SysFont('Courier new', size).render(data, smooth, color)
    app.sc.blit(text,(x,y))
    
class Cover:
    def __init__(self, game):
        self.game = game
        self.cover = pg.Rect(500, 500, 235, 235)
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
        cursor.left = 640*(self.mouse_x/WIDTH)
        cursor.top  = 480*(self.mouse_y/HEIGHT)
        
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
        self.plr = pg.Rect(250,250,12,12)
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
                self.plr.left = self.mouse_x - self.plr.width/2
                self.plr.top = self.mouse_y - self.plr.height/2
            elif self.game.app.cap_mode == 1:
                self.plr.left = self.mouse_x - self.plr.width
                self.plr.top = self.mouse_y - self.plr.height
            elif self.game.app.cap_mode == 2:
                self.plr.left = self.mouse_x
                self.plr.top = self.mouse_y
        
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
        self.frame = [[0,0,WIDTH,HEIGHT/21],[0,HEIGHT-HEIGHT/21+2,WIDTH,HEIGHT/21],
                     [0,0,2130,HEIGHT],[WIDTH-2130+1,0,2130,HEIGHT]]
        self.ln = ln
        self.kb = [
                        [
                            [0, 0, WIDTH/1.0, HEIGHT/25.6667], [0, HEIGHT/25.6667, 2134.3333, HEIGHT/1.0405], [0, HEIGHT/1.0405, WIDTH/1.0, HEIGHT]
                        ],
                        [
                             self.frame[0], self.frame[1], self.frame[2], self.frame[3],
                             [WIDTH/1.77, HEIGHT/6.92, WIDTH/24.98, HEIGHT/1.17], [213.2, HEIGHT/2.19, WIDTH/1.83, HEIGHT/17.35],
                             [WIDTH/1.32, 0, WIDTH/4.11, 160.93], [WIDTH/1.39, HEIGHT/1.42, 213.56, HEIGHT/17.35],
                             [0, HEIGHT/1.42, WIDTH/2.56, HEIGHT/17.35], [0, 0, WIDTH/6.09, HEIGHT/1.42], [0, 0, WIDTH/2.34, 160.89]
                        ], 
                        [
                              [0, 0, WIDTH/1.0, 1608.4], [0, 1608.4, 1281.5, HEIGHT/1.04], [0, HEIGHT/1.02, WIDTH/1.0, 1608.4], [WIDTH/1.02, 1608.4, 128, HEIGHT/1], [WIDTH/8.58, 1608.4, 26.75, HEIGHT/1.48], [1281.5, HEIGHT/1.1, WIDTH/2.71, HEIGHT/12.8], [WIDTH/2.86, HEIGHT/4.27, 26.75, HEIGHT/1.38], [WIDTH/6.5, HEIGHT/1.54, WIDTH/10.3, HEIGHT/19.2], [213.96, HEIGHT/4.27, WIDTH/10, HEIGHT/19.2], [WIDTH/2.06, 0, 26.75, HEIGHT/1.42], [WIDTH/2.71, HEIGHT/1.16, WIDTH/1.61, HEIGHT/7.68], [WIDTH/1.61, HEIGHT/5.49, 26.75, HEIGHT/1.42], [WIDTH/4.29, HEIGHT/2.26, 26.75, HEIGHT/19.2], [WIDTH/1.32, 0, 26.75, HEIGHT/1.37], [WIDTH/1.12, HEIGHT/5.49, WIDTH/10.3, HEIGHT/1.42]

                        ],      
                        [
                            [0, 0, WIDTH/1.0, HEIGHT/21.0], [0, HEIGHT/1.0471, WIDTH/1.0, HEIGHT/21.0], [0, 0, 2130.0, HEIGHT/1.0], [WIDTH/1.0334, 0, 2130.0, HEIGHT/1.0], [WIDTH/10.3, 0, WIDTH/4.2917, HEIGHT/4.2778], [0, HEIGHT/2.9615, 213.0294, HEIGHT/7.7], [WIDTH/2.4524, 0, WIDTH/10.3, HEIGHT/1.3276], [213.9615, HEIGHT/2.5389, WIDTH/12.875, 160.2], [WIDTH/10.3, HEIGHT/1.8333, WIDTH/6.4375, HEIGHT/5.625], [WIDTH/10.3, HEIGHT/2.2389, WIDTH/12.875, 1600.5], [1281.5, HEIGHT/1.1667, WIDTH/1.051, HEIGHT/9.625], [WIDTH/2.1458, 0, WIDTH/1.9808, HEIGHT/6.4167], [WIDTH/1.1196, HEIGHT/6.4167, WIDTH/12.875, HEIGHT/1.6042], [WIDTH/1.3205, HEIGHT/4.2778, 26.75, HEIGHT/1.5], [WIDTH/1.6613, HEIGHT/4.2778, WIDTH/17.1667, HEIGHT/1.925]
                        ],
                        [
                            [0, 0, 2134.3333, HEIGHT/1.0], [2134.3333, 0, WIDTH/1.03, HEIGHT/25.6667], [WIDTH/1.03, HEIGHT/25.6667, 2134.3333, HEIGHT/1], [2134.3333, HEIGHT/1.0405, WIDTH/1.03, HEIGHT], [2134.3333, HEIGHT/25.6667, WIDTH/4.4783, HEIGHT/4.2778], [WIDTH/2.8611, 0, 427373, 160.6667], [WIDTH/9.3636, HEIGHT/2.5667, WIDTH/1.6094, HEIGHT/2.2], [WIDTH/1.4733, HEIGHT/1.7111, WIDTH/2.12, HEIGHT/9.625]
                        ]
                  ]
        self.sl = [
                    [WIDTH/2, HEIGHT/2],
                    [128, HEIGHT/1.2],
                    [32.5, HEIGHT/13.4],
                    [WIDTH/17.167, HEIGHT/7],
                    [213.5, HEIGHT/24]
                  ]
        self.fl = [
                    [WIDTH/1.03, 0, WIDTH, HEIGHT], 
                    [WIDTH/1.33, HEIGHT/1.322, WIDTH/4.39, HEIGHT/2.48],
                    [WIDTH/1.12, 1608.4, WIDTH, HEIGHT],
                    [213.179, HEIGHT/42.78, WIDTH/9.1964, HEIGHT/7],
                    [WIDTH/1.4733, HEIGHT/1.5528, WIDTH/2.12, HEIGHT/6.4167]
                  ]
        self.key = Key(self, l=500, t=500)
        self.chaser = Chase(self, zl=100, zt=100, zw=400, zh=400, speed=2)
        
        self.keys = [ # List
                        [], [], [],  # Level
                        [
                            [128.33678, HEIGHT/2.01044, self.key.key.width, self.key.key.height], # Keys
                            [WIDTH/1.1087, HEIGHT/1.248, self.key.key.width, self.key.key.height]
                        ]
                    ]
        self.key_kb = [ # List
                               [], [], [], # Level
                               [ # Key
                                  [ # Linked blocks | Note: Will be drew only if key is assigned
                                      [WIDTH/1.9846, HEIGHT/1.4051, 213.9, HEIGHT/24.8387]
                                  ],
                                  [
                                      [213.0383, HEIGHT/7.33, WIDTH/10.875, 60.405]
                                  ],      
                               ]
                       ]
        self.keys_backup, self.key_kb_backup = self.keys, self.key_kb
        
        self.key_use = []
        self.cover_use = [0,0,0,0,1,0]
        self.chase_use = [0,0,0,0,0,1]
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
            draw_text(x=WIDTH/15, y=WIDTH/1.7, data='Black rectangles can kill you', size=13, color=(0,0,0))
        if self.ln == 3:
            draw_text(x=WIDTH/15, y=WIDTH/1.7, data='Collect keys in order to open some (unmarked) gates', size=13, color=(0,0,0))
        if self.ln == 4:
            draw_text(x=WIDTH/2, y=WIDTH/40, data='Some levels can be really dark', size=13, color=(255,255,255))
        
    def run(self):
        if self.ln == 5:
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
        self.chaser = pg.Rect(zl+zw/2,zt+zh/2,32,32)
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
        self.key = pg.Rect(l,t,26.6,HEIGHT/40.421)
        self.key_img = pg.transform.scale(pg.image.load('assets/key.png'), (self.key.width, self.key.height))
        
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
        self.font = pg.font.SysFont('Courier new', 25)  
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
        self.resolutions_list = [[640, 480], [800, 600], [1024, 768]]
        for i in range(len(self.resolutions_list)):
            if [WIDTH, HEIGHT] == self.resolutions_list[i]:
                self.resolution = i
                break
        self.prev_resolution = self.resolution
        self.debug = 1
        self.bg_clr = (5, 5, 5)
        
        self.font = pg.font.SysFont('Courier new', 31)
        self.editor_font = pg.font.SysFont('Courier new', 9)
        
        
        # Main Menu
        self.play_button = Button(self, 0, 160, 96, 48, text='Play', action='play', to=-3.84)
        self.icons_button = Button(self, 0, 160+60, 96, 48, text='Avatar', lo=16, to=-3.84, action='icons')
        self.editor_button = Button(self, 0, 160+(60)*2, 96, 48, text='Editor', lo=16, to=-3.84, action='editor') 
        self.settings_button = Button(self, 0, 160+(60)*3, 128, 48, text='Settings', lo=18, to=-3.84, action='settings') 
        self.continue_button = Button(self, 0, 160, 128, 48, text='Continue', lo=18, to=-3.84, action='play')
        self.menu_button = Button(self, 0, 160+(60), 128, 48, text='To Menu', action='menu', lo=16, to=-3.84)
        self.exit_button = Button(self, 0, 160+(60)*4, 96, 48, text='Exit', action='leave', to=-3.84)
        
        self.logo = pg.Rect(0, 10, WIDTH/4, (WIDTH/4)/1.45)
        #self.logo_img = self.plr_img = pg.transform.scale(pg.image.load('assets/logo.png'), (self.logo.width, self.logo.height))
        
        # Settings
        self.apply_resolution_button = Button(self, 337, 213-(32), WIDTH/8, 26, lo=13, to=4, text='Apply', action='action_apply_resolution')
        self.bool_resolution_button = Button(self, 26, 213-(32), 26, 26, text='•', action='action_change_resolution')
        self.bool_music_button = Button(self, 26, 213, 26, 26, text='•', action='action_music')
        self.bool_fullscreen_button = Button(self, 26, 213+(32), 26, 26, text='•', action='action_fullscreen')
        self.bool_capmode_button = Button(self, 26, 213+(32)*2, 26, 26, text='•', action='action_cap_mode')
        self.action = ''
        
        self.set_w, self.set_h = WIDTH, HEIGHT
        
        self.back_button = Button(self, 0, 0, 32, 32, text='←', action='menu', to=3.84)
        
        # Editor
        self.obj_list = self.level.frame
        self.grid_size = 10
        self.gridlist = []
        self.left, self.top, self.right, self.bottom = 0, 0, 0, 0 # To prevent crashes
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
                self.obj_list = [[0,0,WIDTH,HEIGHT/21],[0,HEIGHT-HEIGHT/21+2,WIDTH,HEIGHT/21],
                                [0,0,2130,HEIGHT],[WIDTH-2130+1,0,2130,HEIGHT]]
            if self.input[pg.K_DOWN]:
                for i in range(len(self.obj_list)):
                    if self.obj_list[i][0] != 0:
                        self.obj_list[i][0] = 'WIDTH/'+str(round(WIDTH/self.obj_list[i][0],4))
                    else:
                        self.obj_list[i][0] = 0
                    if self.obj_list[i][1] != 0:
                        self.obj_list[i][1] = 'HEIGHT/'+str(round(HEIGHT/self.obj_list[i][1],4))
                    else:
                        self.obj_list[i][1] = 0
                    if self.obj_list[i][2] != 0:
                        self.obj_list[i][2] = 'WIDTH/'+str(round(WIDTH/self.obj_list[i][2],4))
                    else:
                        self.obj_list[i][2] = 0
                    if self.obj_list[i][3] != 0:
                        self.obj_list[i][3] = 'HEIGHT/'+str(round(HEIGHT/self.obj_list[i][3],4))
                    else:
                        self.obj_list[i][3] = 0
                             
                print(self.obj_list)
                self.obj_list = [[0,0,WIDTH,HEIGHT/21],[0,HEIGHT-HEIGHT/21+2,WIDTH,HEIGHT/21],
                                 [0,0,2130,HEIGHT],[WIDTH-2130+1,0,2130,HEIGHT]]
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
            app.sc.blit(self.font.render('Res: '+str(self.set_w)+'; '+str(self.set_h),1,(0,0,0)),(64,240-(32)*2))
            app.sc.blit(self.font.render('Music: '+str(self.app.music_state),1,(0,0,0)),(64,240-(32)))
            app.sc.blit(self.font.render('Fullscreen: '+str(self.app.fullscreen),1,(0,0,0)),(64,240))
            app.sc.blit(self.font.render('Cap mode: '+str(self.app.cap_mode)+' ('+self.cap_mode_hint[self.app.cap_mode]+')',1,(0,0,0)),(64,240+(32)))
            
            self.bool_resolution_button.run()
            self.apply_resolution_button.run()
            
            self.bool_music_button.run()
            self.bool_fullscreen_button.run()
            self.bool_capmode_button.run()
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
            draw_text(data='Paused', size=round(WIDTH/10), color=(0,0,0))
            self.continue_button.run()
            self.menu_button.run()
        elif self.tab == 'play':
            self.player.instance()
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
        self.read_config()
        self.check_music()
        self.play_music()
        self.game = Game(self)
    
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
        self.cap_mode = int(self.config.readline())
        self.check_fullscreen()
        self.config.close()
    def write_config(self):
        self.config = open('assets/cfg.txt', 'w')
        self.config.write(str(WIDTH)+'\n'+str(HEIGHT)+'\n'+str(self.music_state)+'\n'+str(self.fullscreen)+'\n'+str(self.cap_mode))
        self.config.close()
        self.config = open('assets/cfg.txt', 'r')
        print(self.config.read())
    def set_resolution(self):
        self.check_fullscreen()
        self.game = Game(self)
    def check_fullscreen(self):
        self.actual_sc = pg.display.set_mode((WIDTH, HEIGHT))
        if self.fullscreen:
            self.actual_sc = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        #self.sc = self.actual_sc.copy()
        self.sc = pg.Surface((640, 480))
            
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
            #self.actual_sc.fill((255,255,255))
            self.actual_sc.blit(pg.transform.smoothscale(self.sc, (WIDTH, HEIGHT)), (0,0))
            #self.actual_sc.blit(self.sc, (0,0))
            self.check_events()
            self.check_music()
            pg.display.update()
            pg.display.flip()
            self.clock.tick(75)

if __name__ == '__main__':
    app = App()
    app.run()