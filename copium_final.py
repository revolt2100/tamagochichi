import pygame
import pygame_widgets as pw
import os
import time
import threading
import random

from pygame.locals import (
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    QUIT,
    K_RETURN
)

os.chdir(os.path.dirname(__file__))


def absent(m, n, callbacks=[]):
    start_time = time.time()
    while time.time() - start_time < n:
        global state
        state = m
    state = 'RUNNING'
    for c in callbacks: c()


def f_with_timer(m, n=2, callbacks=[]):
    threadd = threading.Thread(target=lambda: absent(m, n, callbacks))
    threadd.start()


class MyButton:

    def __init__(self, path, x, y, callbacks=[],
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

pygame.display.set_caption('tamagochi~chi')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
image_background = 'assets/background.jpg'

pygame.mixer.init()
music = pygame.mixer.music.load('assets/waaaa_povle.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

background = pygame.image.load(image_background)
pile_of_books = pygame.image.load('assets/pile_of_books.png').convert_alpha()
very_normal_mushroom = pygame.image.load('assets/very_normal_mushroom.png').convert_alpha()
communication_device = pygame.image.load('assets/communication_device.png').convert_alpha()

eepy = pygame.image.load('assets/eepy.png').convert_alpha()
full = pygame.image.load('assets/full.png').convert_alpha()
fun = pygame.image.load('assets/fun.png').convert_alpha()
bunny = pygame.image.load('assets/bunny.png').convert_alpha()
bunny_eeping = pygame.image.load('assets/bunny_eeping.png').convert_alpha()
bunny_working = pygame.image.load('assets/bunny_working.png').convert_alpha()

bunny_width = bunny.get_width()
bunny_height = bunny.get_height()

item_shadow = pygame.image.load('assets/item_shadow.png').convert_alpha()

white = (255, 255, 255)
clock = pygame.time.Clock()


def work_done():
    # global money_count
    global state_of_items
    # money_count += random.randint(1, 12)
    item = random.choice([pile_of_books, very_normal_mushroom, communication_device])
    if item:
        state_of_items = item


food_bar = MyBar(414, 23, 0.005555, 2, (90, 169, 83))
sleep_bar = MyBar(414, 52, 0.003555, 3, (88, 187, 190))
fun_bar = MyBar(414, 81, 0.007555, 1, (228, 197, 112))

bars = [
    food_bar,
    sleep_bar,
    fun_bar
]

feed_button = MyButton('assets/feed.png', 25, 600, [food_bar.increasing])
play_button = MyButton('assets/play.png', 175, 605, [fun_bar.increasing])
sleep_button = MyButton('assets/sleep.png', 305, 605, [sleep_bar.increasing, lambda: f_with_timer('ABSENT_s', 10)])
work_button = MyButton('assets/work.png', 445, 605, [lambda: f_with_timer('ABSENT_w', 5, [work_done])])
settings_button = MyButton('assets/settings.png', 20, 20)
# shop_button = MyButton('shop.png', 20, 92)


buttons = [
    feed_button,
    play_button,
    sleep_button,
    work_button,
    settings_button,
    # shop_button
]

def die():  # смерть:(
    global running
    running = False

state = 'RUNNING'
global running
running = True
state_of_items = None

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
            for button in buttons:
                if state == 'ABSENT_w' or state == 'ABSENT_s':
                    continue
                else:
                    if button.clicked():
                        button.click()
                        continue
    for bar in bars:
        bar.decreasing()

    screen.blit(background, (0, 0))
    if state == 'RUNNING':
        screen.blit(bunny, (screen_width / 2 - bunny_width / 2, screen_height / 2 - bunny_height / 2))
    elif state == 'ABSENT_s':
        screen.blit(bunny_eeping, (
        screen_width / 2 - bunny_eeping.get_width() / 2, screen_height / 2 - bunny_eeping.get_height() / 2 + 110))
    elif state == 'ABSENT_w':
        screen.blit(bunny_working, (
        screen_width / 2 - bunny_working.get_width() / 2, screen_height / 2 - bunny_working.get_height() / 2 + 110))
    screen.blit(full, (383, 23))
    screen.blit(eepy, (381, 52))
    screen.blit(fun, (375, 81))
    if state_of_items != None:
        item_height = state_of_items.get_height()
        screen.blit(item_shadow, (454, 530))
        screen.blit(state_of_items, (454, 550 - item_height))
    for button in buttons:
        screen.blit(button.image, (button.x, button.y))
    for bar in bars:
        current_width = (bar.current_bar / bar.max_bar) * bar.width
        pygame.draw.rect(screen, white, (bar.x, bar.y, bar.width, bar.height))
        pygame.draw.rect(screen, bar.colour, (bar.x, bar.y, current_width, bar.height))
    pw.update(events)
    pygame.display.update()
    clock.tick(60)

font = pygame.font.Font(None, 30)
run = True
while running == False:
    pygame.mixer_music.stop()
    screen.fill((0, 0, 0))
    for button in buttons:
        if button == settings_button:
            screen.blit(button.image, (button.x, button.y))


    # my_font = pygame.font.SysFont('Comic Sans MS', 30)
    # text_surface = my_font.render('Some Text', False, (255, 255, 255))  # Вот тут если что, вводится текст, который нужно вывести
    # screen.blit(text_surface, (50, 500))
    timer = pygame.time.Clock()
    message = "А всё, а всё, игра закончилась"
    snip = font.render('', True, 'white')
    counter = 0
    speed = 3
    done = False

    if not done:
        while run:
            timer.tick(60)
            pygame.draw.rect(screen, "dark gray", [25, 485, 500, 50])
            if counter < speed * len(message):
                counter += 1
            elif counter >= speed * len(message):
                done = True
            events_run = pygame.event.get()
            if done:
                run = False

            snip = font.render(message[0:counter // speed], True, 'white')
            screen.blit(snip, (50, 500))
            pygame.display.update()
            pygame.display.flip()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = True
        elif event.type == pygame.K_RETURN:
            running = True


pygame.quit()
