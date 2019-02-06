from pygame.locals import *
from random import randint
import pygame
import time

from abc import ABCMeta, abstractmethod

### colors

white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)

bright_green = (0, 255, 0)
bright_red = (255, 0, 0)

clock = pygame.time.Clock()


class Background:
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw(self, surface):
        pass


class BlackBackground(Background):

    def draw(self, surface):
        surface.fill(black)


class WhiteBackground(Background):

    def draw(self, surface):
        surface.fill(white)


class PlayerTheme:
    __metaclass__ = ABCMeta

    @abstractmethod
    def image(self):
        pass


class PlayerWhiteTheme(PlayerTheme):

    def image(self):
        return pygame.image.load("image/block.jpg").convert()


class PlayerBlackTheme(PlayerTheme):

    def image(self):
        return pygame.image.load("image/block.jpg").convert()


class FoodTheme:
    __metaclass__ = ABCMeta

    @abstractmethod
    def image(self):
        pass


class FoodWhiteTheme(FoodTheme):

    def image(self):
        return pygame.image.load("image/block.jpg").convert()


class FoodBlackTheme(FoodTheme):

    def image(self):
        return pygame.image.load("image/block.jpg").convert()


class ThemeFactory:
    __metaclass__ = ABCMeta

    @abstractmethod
    def createbackground(self):
        pass


class BlackFactoryTheme(ThemeFactory):

    def createbackground(self):
        return BlackBackground()

    def createplayer(self):
        return PlayerBlackTheme()

    def createfood(self):
        return FoodBlackTheme()


class WhiteFactoryTheme(ThemeFactory):

    def createbackground(self):
        return WhiteBackground()

    def createplayer(self):
        return PlayerWhiteTheme()

    def createfood(self):
        return FoodWhiteTheme()


class Food:
    x = 0
    y = 0
    step = 44

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))


class Player:
    x = [0]
    y = [0]
    step = 44
    direction = 0
    length = 1

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length):
        self.x = [0]
        self.y = [0]
        self.length = length
        for i in range(0, 2000):
            self.x.append(-100)
            self.y.append(-100)

        # initial positions, no collision.
        self.x[1] = 1 * 44
        self.x[2] = 2 * 44


    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0

    def moveRight(self):
        self.direction = 0

    def moveLeft(self):
        self.direction = 1

    def moveUp(self):
        self.direction = 2

    def moveDown(self):
        self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))


class App:
    windowWidth = 1000
    windowHeight = 800
    player = 0
    Food = 0

    def __init__(self):
        self._themefactory = BlackFactoryTheme()
        self.paused = False
        self._running = True
        self._display_surf = None
        self.gameover = False
        self.background_obj = self._themefactory.createbackground()
        self._image_surf = self._themefactory.createplayer()
        self._food_surf = self._themefactory.createfood()
        self.player = Player(1)
        self.food = Food(5, 5)


    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # does snake eat apple?
        for i in range(0, self.player.length):
            if self.is_collision(self.food.x, self.food.y, self.player.x[i], self.player.y[i], 44):
                self.food.x = randint(2, 9) * 44
                self.food.y = randint(2, 9) * 44
                self.player.length = self.player.length + 1

        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.is_collision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 40):
                self.game_over()

    def on_render(self):
        self.background_obj.draw(self._display_surf)
        self.player.draw(self._display_surf, self._image_surf.image())
        self.food.draw(self._display_surf, self._food_surf.image())
        pygame.display.flip()

    def is_collision(self, x1, y1, x2, y2, bsize):
        if x2 <= x1 <= x2 + bsize:
            if y2 <= y1 <= y2 + bsize:
                return True
        return False

    def out_of_screen(self):
        # for i in range(self.player.length):
        #     if self.player.x[i] >= self.windowWidth or self.player.x[i] < 0 or self.player.y[i]>=
        if self.player.x[self.player.length] >= self.windowWidth or self.player.x[self.player.length] < 0 or \
                self.player.y[self.player.length] >= self.windowHeight or self.player.y[self.player.length] < 0:
            self.gameover = True

    def game_over(self):

        while True:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            self._display_surf.fill((0, 0, 0))
            self.button("Play Again", 150, 450, 100, 50, green, bright_green, self.restart_game)
            self.button("Quit", 750, 450, 100, 50, red, bright_red, self.quit_game)
            self.message_display("Gameover", 30, self.windowWidth / 2, self.windowHeight / 3)
            pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        quit()

    def run_game(self):

        while self._running:

            while self.gameover:
                self.game_over()
                self._running = False
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()

            if (keys[K_LEFT]):
                self.player.moveLeft()

            if (keys[K_UP]):
                self.player.moveUp()

            if (keys[K_DOWN]):
                self.player.moveDown()

            if (keys[K_ESCAPE]):
                self._running = False

            if keys[K_p]:
                self.pause()

            self.on_loop()
            self.on_render()
            clock.tick(15)

        self.quit_game()

    def unpause(self):
        self.paused = False

    def pause(self):
        self.paused = True
        while self.paused:
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if keys[K_c]:
                self.paused = False

            if keys[K_ESCAPE]:
                self.paused = False
                self._running = False

            self._display_surf.fill((0, 0, 0))
            self.button("Continue", 150, 450, 100, 50, green, bright_green, self.unpause)
            self.button("Quit", 750, 450, 100, 50, red, bright_red, self.quit_game)
            self.message_display("game paused", 30, self.windowWidth / 2, self.windowHeight / 3)
            pygame.display.flip()

    @staticmethod
    def text_objects(text, font):
        text_surface = font.render(text, True, white)
        return text_surface, text_surface.get_rect()

    def message_display(self, text, fontsize, windowwidth, windowheight):
        text_font = pygame.font.Font('freesansbold.ttf', fontsize)
        TextSurf, TextRect = self.text_objects(text, text_font)
        TextRect.center = ((windowwidth), (windowheight))
        self._display_surf.blit(TextSurf, TextRect)

    def game_intro(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth, self.windowHeight), pygame.HWSURFACE)
        intro = True
        while intro:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                intro = False

            self._display_surf.fill(black)
            self.message_display('Snake game', 40, self.windowWidth / 2, self.windowHeight / 3)

            self.button("PLAY", 150, 450, 100, 50, green, bright_green, self.run_game)
            self.button("Setting", 450, 450, 100, 50, green, bright_green, self.choose_gameoptions)
            self.button("Quit", 750, 450, 100, 50, red, bright_red, self.quit_game)
            pygame.display.flip()

    def choose_gameoptions(self):
        intro = True
        while intro:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if keys[K_ESCAPE]:
                intro = False

            self._display_surf.fill(black)
            self.message_display("Game Theme", 30, 130, 370)
            self.message_display("Difficulty", 30, 130, 470)
            self.button("easy", 300, 450, 100, 50, green, bright_green, None)
            self.button("medium", 500, 450, 100, 50, green, bright_green, None)
            self.button("hard", 700, 450, 100, 50, red, bright_red, None)
            self.button("black", 300, 350, 100, 50, green, bright_green, self.set_theme_start_game("black"))
            self.button("white", 500, 350, 100, 50, green, bright_green, self.set_theme_start_game("white"))
            self.button("green", 700, 350, 100, 50, red, bright_red, None)
            self.button("Quit", 800, 600, 100, 50, red, bright_red, self.quit_game)
            self.button("Play", 200, 600, 100, 50, green, bright_green, self.restart_game)
            pygame.display.flip()

    def button(self, msg, x, y, w, h, inactive_color, active_color, action):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:
            pygame.draw.rect(self._display_surf, active_color, (x, y, w, h))
            if clicked[0] == 1 and action is not None:
                action()
                return
        else:
            pygame.draw.rect(self._display_surf, inactive_color, (x, y, w, h))

        self.message_display(msg, 20, (x + (w / 2)), (y + (h / 2)))

    def set_theme_start_game(self, color):
        if color == "black":
            self._themefactory = BlackFactoryTheme()
        if color == "white":
            self._themefactory = WhiteFactoryTheme()
        self.background_obj = self._themefactory.createbackground()
        self._image_surf = self._themefactory.createplayer()
        self._food_surf = self._themefactory.createfood()

    def restart_game(self):
        del self.player
        del self.food
        self.player = 0
        self.food = 0
        self.player = Player(1)
        self.food = Food(5, 5)
        self.run_game()


if __name__ == "__main__":
    theApp = App()
    theApp.game_intro()
