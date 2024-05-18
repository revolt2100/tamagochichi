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


class Item:
    def __init__(self, price, picture, is_purchased, x, y):
        self.price = price
        self.picture = picture
        self.is_purchased = is_purchased
        self.x = x
        self.y = y

class ItemGrid:
    def __init__(self, items, buttons):
        self.items = items
        self.buttons = buttons

    def show(self):
        screen.blit(shop_menu, (0, 0))

        for button in self.buttons:
            screen.blit(button.image, (button.x, button.y))

        if (not shop_items[0].is_purchased):
            screen.blit(pile_of_books, (125, 225))

        if (not shop_items[1].is_purchased):
            screen.blit(communication_device, (330, 210))

        if (not shop_items[2].is_purchased):
            screen.blit(very_normal_mushroom, (230, 430))

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
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
image_background = 'background.jpg'

pygame.mixer.init()
music = pygame.mixer.music.load('waaaa_povle.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

background = pygame.image.load(image_background)
pile_of_books = pygame.image.load('pile_of_books.png').convert_alpha()
very_normal_mushroom = pygame.image.load('very_normal_mushroom.png').convert_alpha()
communication_device = pygame.image.load('communication_device.png').convert_alpha()

eepy = pygame.image.load('eepy.png').convert_alpha()
full = pygame.image.load('full.png').convert_alpha()
fun = pygame.image.load('fun.png').convert_alpha()
bunny = pygame.image.load('bunny.png').convert_alpha()
bunny_eeping = pygame.image.load('bunny_eeping.png').convert_alpha()
bunny_working = pygame.image.load('bunny_working.png').convert_alpha()
shop_menu = pygame.image.load('shop_menu.png').convert_alpha()
shop_title = pygame.image.load('shop_tile.png').convert_alpha()
pile_of_books = pygame.image.load('pile_of_books.png').convert_alpha()
communication_device = pygame.image.load('communication_device.png').convert_alpha()
very_normal_mushroom = pygame.image.load('very_normal_mushroom.png').convert_alpha()

shop_items = [
    Item(10, pile_of_books, False, 50, 400),
    Item(10, communication_device, False, 370, 340),
    Item(10, very_normal_mushroom, False, 490, 450),
]

bunny_width = bunny.get_width()
bunny_height = bunny.get_height()

item_shadow = pygame.image.load('item_shadow.png').convert_alpha()

white = (255, 255, 255)
clock = pygame.time.Clock()


def work_done():
    # global money_count
    global state_of_items
    # money_count += random.randint(1, 12)
    item = random.choice([pile_of_books, very_normal_mushroom, communication_device])
    if item:
        state_of_items = item

def change_shop_mode():
    global shop_mode
    shop_mode = not shop_mode


food_bar = MyBar(414, 23, 0.005555, 2, (90, 169, 83))
sleep_bar = MyBar(414, 52, 0.003555, 3, (88, 187, 190))
fun_bar = MyBar(414, 81, 0.007555, 1, (228, 197, 112))

bars = [
    food_bar,
    sleep_bar,
    fun_bar
]

feed_button = MyButton('feed.png', 25, 600, [food_bar.increasing])
play_button = MyButton('play.png', 175, 605, [fun_bar.increasing])
sleep_button = MyButton('sleep.png', 305, 605, [sleep_bar.increasing, lambda: f_with_timer('ABSENT_s', 10)])
work_button = MyButton('work.png', 445, 605, [lambda: f_with_timer('ABSENT_w', 5, [work_done])])
settings_button = MyButton('settings.png', 20, 20)
shop_button = MyButton('shop.png', 20, 92, [change_shop_mode])

def buy_item(item_number):
    shop_items[item_number].is_purchased = True

shop_item1_button = MyButton('shop_tile.png', 100, 200, [lambda: buy_item(0)])
shop_item2_button = MyButton('shop_tile.png', 300, 200, [lambda: buy_item(1)])
shop_item3_button = MyButton('shop_tile.png', 200, 400, [lambda: buy_item(2)])

buttons = [
    feed_button,
    play_button,
    sleep_button,
    work_button,
    settings_button,
    shop_button,
    shop_item1_button,
    shop_item2_button,
    shop_item3_button
]

game_menu_buttons = [
    feed_button,
    play_button,
    sleep_button,
    work_button,
    settings_button,
    shop_button
]

shop_menu_buttons = [settings_button, shop_button, shop_item1_button, shop_item2_button, shop_item3_button]

state = 'RUNNING'
running = True
state_of_items = None
shop_mode = False

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
    for button in game_menu_buttons:
        screen.blit(button.image, (button.x, button.y))
    for bar in bars:
        current_width = (bar.current_bar / bar.max_bar) * bar.width
        pygame.draw.rect(screen, white, (bar.x, bar.y, bar.width, bar.height))
        pygame.draw.rect(screen, bar.colour, (bar.x, bar.y, current_width, bar.height))

    for shop_item in shop_items:
        if shop_item.is_purchased:
            screen.blit(shop_item.picture, (shop_item.x, shop_item.y))
    if (shop_mode):
        item_grid = ItemGrid(bars, shop_menu_buttons)
        item_grid.show()

    pw.update(events)
    pygame.display.update()
    clock.tick(60)

pygame.quit()