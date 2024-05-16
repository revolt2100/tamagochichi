import pygame
import pygame_widgets as pw
import os
import time
import threading

from pygame.locals import (
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
)

os.chdir(os.path.dirname(__file__))

def absent():
    start_time = time.time()
    while time.time() - start_time < 10:
        global state
        state = 'ABSENT'
    state = 'RUNNING'

def f_with_timer():
    threadd = threading.Thread(target=absent)
    threadd.start()

def ending():
    global state
    state = 'END'



class MyButton:

    def __init__(self, path, x, y, callbacks = [],
                 screen_width=600, 
                 screen_height=700) -> None:
        self.image = pygame.image.load(path).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        screen_width = screen_width
        screen_height = screen_height
        self.x = x
        self.y = y
        self.callbacks = callbacks

    def clicked(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= mouse_x <= self.x + self.width and \
            self.y <= mouse_y <= self.y + self.height:
            return True
        return False
    
    def click(self):
         for c in self.callbacks:
           c()

class MyBar:

    def __init__(self, x, y, decrease, increase, colour,
                 screen_width=600, 
                 screen_height=700) -> None:
        self.width = 166
        self.height = 23
        screen_width = screen_width
        screen_height = screen_height
        self.x = x
        self.y = y
        self.max_bar = 100
        self.current_bar = self.max_bar
        self.decrease = decrease
        self.colour = colour
        self.increase = increase
    
    def decreasing(self):
        self.current_bar -= self.decrease
        if self.current_bar < 0:
            self.current_bar = 0
    
    def increasing(self):
        self.current_bar += self.increase
        if self.current_bar > 100:
            self.current_bar = 100.5


pygame.init()

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
image_background = 'background.jpg'

pygame.mixer.init()
music = pygame.mixer.music.load('music.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops = -1)
background = pygame.image.load(image_background)
eepy = pygame.image.load('eepy.png')
full = pygame.image.load('full.png')
fun = pygame.image.load('fun.png')
bunny = pygame.image.load('bunny.png').convert_alpha()
bunny_width = bunny.get_width()
bunny_height = bunny.get_height()

white = (255, 255, 255)
clock = pygame.time.Clock()

food_bar = MyBar(414, 23, 0.005555, 2, (90, 169, 83))
sleep_bar = MyBar(414, 52, 0.003555, 3, (88, 187, 190))
fun_bar = MyBar(414,81, 0.007555, 1, (228, 197, 112))

bars = [
    food_bar,
    sleep_bar,
    fun_bar
]

feed_button = MyButton('feed.png', 25, 600, [food_bar.increasing])
play_button = MyButton('play.png', 175, 605, [fun_bar.increasing])
sleep_button = MyButton('sleep.png', 305, 605, [sleep_bar.increasing, f_with_timer])
work_button = MyButton('work.png', 445, 605, None)
settings_button = MyButton('settings.png', 20, 20, None)
shop_button = MyButton('shop.png', 20, 92, None)


buttons = [
    feed_button,
    play_button,
    sleep_button,
    work_button,
    settings_button,
    shop_button
]

state = 'RUNNING'
running = True
while running:
    print(state)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == 'ABSENT' or 'END':
                if button.clicked():
                    continue
            else:
                for button in buttons:
                    if button.clicked():
                        button.click()
    for bar in bars:
        bar.decreasing()
    
    screen.blit(background, (0, 0))
    if state == 'RUNNING':
        screen.blit(bunny, (screen_width / 2 - bunny_width / 2, screen_height / 2 - bunny_height / 2))
    elif state == 'ABSENT':
        
    screen.blit(full, (383, 23))
    screen.blit(eepy, (381, 52))
    screen.blit(fun, (375, 81))
    pw.update(events)
    for button in buttons:
        screen.blit(button.image, (button.x, button.y))
    for bar in bars:
        current_width = (bar.current_bar / bar.max_bar) * bar.width    
        pygame.draw.rect(screen, white, (bar.x, bar.y, bar.width, bar.height))
        pygame.draw.rect(screen, bar.colour, (bar.x, bar.y, current_width, bar.height))    
    pygame.display.update()
    clock.tick(60)

pygame.quit()