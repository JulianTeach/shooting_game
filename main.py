from pygame import*
from random import randint
mixer.init()
#mixer.music.load("jungle.ogg")
#mixer.music.play
#fire_sound = mixer.Sound('fire.ogg')

font.init()
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

class GameSprite(sprite.Sprite):
    #class constructor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
    
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
    
        #every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #method drawing the character on the window
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < WIDTH - 80:
            self.rect.x += self.speed
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.bottom = 0
            self.rect.x = randint(0, WIDTH-self.rect.width)

class TextSprite(sprite.Sprite):
    def __init__(self, text, color, pos, font_size):
        self.font = font.Font(None, font_size)
        self.color = color
        self.pos = pos
        self.update_text(text)
        self.rect = self.image.get_rect()
    def update_text(self, new_text):
        self.image = self.font.render(new_text,True, self.color)
    def draw(self, surface):
        surface.blit(self.image, self.pos)

def fire():
    b = Bullet("bullet.png", ship.rect.centerx-8, ship.rect.centery, 16, 20, 15)
    bullets.add(b)

WIDTH = 700
HEIGHT = 500
display.set_caption('Alien shooting game')
window = display.set_mode((WIDTH, HEIGHT))
background = transform.scale(image.load(img_back), (WIDTH, HEIGHT))
bullets = sprite.Group()
ship = Player(img_hero, 5, HEIGHT - 100, 80, 100, 10)
score = 0
lives = 3
win = transform.scale(image.load('thumb.jpg'), (WIDTH, HEIGHT))
scoreboard = TextSprite(text='Score: 0', color='orangered', pos=(40,40), font_size=72)

enemies = sprite.Group()
for _ in range(8):
    e1 = Enemy("cyborg.png", randint(0, WIDTH-30), -60, 60, 60, randint(3, 7))
    enemies.add(e1)

finish = False
run = True
clock = time.Clock()
while run:
    for ev in event.get():
        if ev.type == QUIT:
            run = False
        if ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                fire()
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        enemies.update()
        bullets.update()

        enemy_hits = sprite.groupcollide(bullets, enemies, True, True)
        for hit in enemy_hits:
            e1 = Enemy("cyborg.png", randint(0, WIDTH-30), -60, 60, 60, randint(3, 7))
            enemies.add(e1)
            score += 1
            scoreboard.update_text("Score: "+str(score))
        
        if score >= 10:
            finish = True

        bullets.draw(window)
        ship.draw(window)
        enemies.draw(window)
        scoreboard.draw(window)

        
    else:
        if score >= 10:
            window.blit(win, (0,0))
            
    display.update()
    clock.tick(60)