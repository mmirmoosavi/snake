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
clicked_green = (0, 100, 0)
clicked_red = (100, 0, 0)
bright_green = (0, 255, 0)
bright_red = (255, 0, 0)
yellow = (255, 255, 0)
clock = pygame.time.Clock()


################### singleton pattern ###################
class Singleton(type):
    """
    Define an Instance operation that lets clients access its unique
    instance.
    """

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


################################################

##################### abstract factory pattern#######################

# abstract product Background
class Background:
    __metaclass__ = ABCMeta

    @abstractmethod
    def draw(self, surface):
        pass


# concrete product Backgroud
class BlackBackground(Background):

    def draw(self, surface):
        surface.fill(black)


# concrete product Backgroud
class WhiteBackground(Background):

    def draw(self, surface):
        surface.fill(white)


# concrete product Backgroud
class GreenBackground(Background):

    def draw(self, surface):
        surface.fill(green)


# abstract product Player
class PlayerTheme:
    __metaclass__ = ABCMeta

    @abstractmethod
    def image(self):
        pass


# concrete product Player
class PlayerWhiteTheme(PlayerTheme):

    def image(self):
        return pygame.image.load("image/block.png").convert()


# concrete product Player
class PlayerBlackTheme(PlayerTheme):

    def image(self):
        return pygame.image.load("image/block.png").convert()


# concrete product Player
class PlayerGreenTheme(PlayerTheme):

    def image(self):
        return pygame.image.load("image/block.png").convert()


# abstract factory class
class ThemeFactory(metaclass=Singleton):

    @abstractmethod
    def createbackground(self):
        pass

    @abstractmethod
    def createplayer(self):
        pass


# concrete factory class
class BlackFactoryTheme(ThemeFactory):

    def createbackground(self):
        return BlackBackground()

    def createplayer(self):
        return PlayerBlackTheme()



# concrete factory class
class WhiteFactoryTheme(ThemeFactory):

    def createbackground(self):
        return WhiteBackground()

    def createplayer(self):
        return PlayerWhiteTheme()


# concrete factory class
class GreenFactoryTheme(ThemeFactory):

    def createbackground(self):
        return GreenBackground()

    def createplayer(self):
        return PlayerGreenTheme()


#####################################################

############################ strategy pattern ################################
class GameStrategy():
    __metaclass__ = ABCMeta

    @abstractmethod
    def speed(self):
        pass


class EasyStrategy(GameStrategy):

    def speed(self):
        return 15


class MediumStratgey(GameStrategy):

    def speed(self):
        return 100


class HardStrategy(GameStrategy):

    def speed(self):
        return 285


############################################################
################### visitor pattern ########################
NOT_IMPLEMENTED = "Not Implemented !!!!!!"
class ItemVisitor():
    __metaclass__ = ABCMeta

    @abstractmethod
    def visit_lengthItem(self, player, s):
        raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visit_speedItem(self, player, s):
        raise NotImplementedError(NOT_IMPLEMENTED)

    # @abstractmethod
    # def visit_skipWallItem(self, player, s):
    #     raise NotImplementedError(NOT_IMPLEMENTED)

    # @abstractmethod
    # def visit_skipItselfItem(self, player, s):
    #     raise NotImplementedError(NOT_IMPLEMENTED)

    # @abstractmethod
    # def visit_reverseItem(self, player, s):
    #     raise NotImplementedError(NOT_IMPLEMENTED)

    @abstractmethod
    def visit_shortenItem(self, player, s):
        raise NotImplementedError(NOT_IMPLEMENTED)


class FoodItemVisitor(ItemVisitor):
    def visit_lengthItem(self, player, s):
        # raise NotImplementedError(NOT_IMPLEMENTED)
        player.length = player.length + 1
        player.score += 1

    def visit_speedItem(self, player, s):
        # raise NotImplementedError(NOT_IMPLEMENTED)
        s.speed += 20

    # def visit_skipWallItem(self, player, speed):
    #     raise NotImplementedError(NOT_IMPLEMENTED)

    # def visit_skipItselfItem(self, player, speed):
    #     raise NotImplementedError(NOT_IMPLEMENTED)

    def visit_reverseItem(self, player, s):
        s.reverse_direction = True

    def visit_shortenItem(self, player, s):
        if (player.length > 1):
            player.length -= 1

##############################################################
class Food:
    __metaclass__ = ABCMeta

    x = 0
    y = 0
    step = 20

    def __init__(self, x, y):
        self.x = x * self.step
        self.y = y * self.step



    @abstractmethod
    def image(self):
        pass

    @abstractmethod
    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    @abstractmethod
    def accept(self, visitor, player, s):
        raise NotImplementedError("Not Implemented !!!!!!")

class LengthItem(Food):
    def image(self):
        return pygame.image.load("image/aubergine.png").convert()

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def accept(self, visitor, player, s):
        visitor.visit_lengthItem(player, s)


class SpeedItem(Food):
    def image(self):
        return pygame.image.load("image/burger.png").convert()

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def accept(self, visitor, player, s):
        visitor.visit_speedItem(player, s)


# class SkipWallItem(Food):
#     def image(self):
#         return pygame.image.load("image/cheese.png").convert()
#
#     def draw(self, surface, image):
#         surface.blit(image, (self.x, self.y))
#
#     def accept(self, visitor, player, s):
#         visitor.visit_skipWalItem(player, s)


# class SkipItselfItem(Food):
#     def image(self):
#         return pygame.image.load("image/icecream.png").convert()
#
#     def draw(self, surface, image):
#         surface.blit(image, (self.x, self.y))
#
#     def accept(self, visitor, player, s):
#         visitor.visit_skipItselfItem(player, s)


class ReverseItem(Food):
    def image(self):
        return pygame.image.load("image/lettuce.png").convert()

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def accept(self, visitor, player, s):
        visitor.visit_reverseItem(player, s)


class ShortenItem(Food):
    def image(self):
        return pygame.image.load("image/watermelon.png").convert()

    def draw(self, surface, image):
        surface.blit(image, (self.x, self.y))

    def accept(self, visitor, player, s):
        visitor.visit_shortenItem(player, s)


class Player:
    x = [0]
    y = [0]
    step = 20
    direction = 0
    length = 1
    score = 0
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
        self.x[1] = 1 * self.step
        self.x[2] = 2 * self.step

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
        if self.direction != 1:
            self.direction = 0

    def moveLeft(self):
        if self.direction != 0:
            self.direction = 1

    def moveUp(self):
        if self.direction != 3:
            self.direction = 2

    def moveDown(self):
        if self.direction != 2:
            self.direction = 3

    def draw(self, surface, image):
        for i in range(0, self.length):
            surface.blit(image, (self.x[i], self.y[i]))

    def draw_score(self, surface, x, y):
        smallfont = pygame.font.Font("freesansbold.ttf", 25)
        text = smallfont.render("SCORE: " + str(self.score), True, yellow)
        surface.blit(text, [x, y])


###################### game  main class #####################
class App:
    windowWidth = 1000
    windowHeight = 800
    player = 0
    Food = 0

    def __init__(self):
        self.game_strategy = EasyStrategy()
        self.speed = self.game_strategy.speed()
        self._themefactory = BlackFactoryTheme()
        self.reverse_direction = False
        self.paused = False
        self._running = True
        self._display_surf = None
        self.gameover = False
        self.background_obj = self._themefactory.createbackground()
        self._image_surf = self._themefactory.createplayer()
        self.player = Player(1)
        self.food = LengthItem(5, 5)

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # does snake eat apple?
        for i in range(0, self.player.length):
            if self.is_collision(self.food.x, self.food.y, self.player.x[i], self.player.y[i], 19):

                v = FoodItemVisitor()
                self.food.accept(v, self.player, self)


                randomItem = randint(1, 100)

                if 1 <= randomItem <= 70:
                    self.food = LengthItem(self.food.x, self.food.y)

                elif 71 <= randomItem <= 80:
                    self.food = SpeedItem(self.food.x, self.food.y)

                # elif randomItem == 3:
                #     self.food = SkipItselfItem(self.food.x, self.food.y)

                # elif randomItem == 4:
                #     self.food = SkipWallItem(self.food.x, self.food.y)

                elif 81 <= randomItem == 90:
                    self.food = ReverseItem(self.food.x, self.food.y)

                elif 91 <= randomItem <= 100:
                    self.food = ShortenItem(self.food.x, self.food.y)

                self.food.x = randint(2, 20) * 40
                self.food.y = randint(2, 15) * 40

        # does snake collide with itself?
        for i in range(2, self.player.length):
            if self.is_collision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], 19):
                self.game_over()

    def on_render(self):
        self.background_obj.draw(self._display_surf)
        self.player.draw(self._display_surf, self._image_surf.image())
        self.player.draw_score(self._display_surf, 860, 0)
        self.food.draw(self._display_surf, self.food.image())
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
            self.button("Play Again", 150, 450, 100, 50, green, bright_green, clicked_green, self.restart_game)
            self.button("Quit", 750, 450, 100, 50, red, bright_red, clicked_red, self.quit_game)
            self.message_display("Gameover", 30, self.windowWidth / 2, self.windowHeight / 3)
            pygame.display.flip()

    def quit_game(self):
        pygame.quit()
        quit()

    def run_game(self):
        counter = 0
        while self._running:

            while self.gameover:
                self.game_over()
                self._running = False
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            if not self.reverse_direction:
                if (keys[K_RIGHT]):
                    self.player.moveRight()

                if (keys[K_LEFT]):
                    self.player.moveLeft()

                if (keys[K_UP]):
                    self.player.moveUp()

                if (keys[K_DOWN]):
                    self.player.moveDown()
            elif self.reverse_direction:
                counter += 1
                if counter >= 200:
                    self.reverse_direction = False
                    counter = 0
                if (keys[K_RIGHT]):
                    self.player.moveLeft()

                if (keys[K_LEFT]):
                    self.player.moveRight()

                if (keys[K_UP]):
                    self.player.moveDown()

                if (keys[K_DOWN]):
                    self.player.moveUp()

            if (keys[K_ESCAPE]):
                self._running = False

            if keys[K_p]:
                self.pause()

            self.on_loop()
            self.on_render()

            clock.tick(self.speed)

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
            self.button("Continue", 150, 450, 100, 50, green, bright_green, clicked_green, self.unpause)
            self.button("Quit", 750, 450, 100, 50, red, bright_red, clicked_red, self.quit_game)
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

            self.button("PLAY", 150, 450, 100, 50, green, bright_green, clicked_green, self.run_game)
            self.button("Setting", 450, 450, 100, 50, green, bright_green, clicked_green, self.choose_gameoptions)
            self.button("Quit", 750, 450, 100, 50, red, bright_red, clicked_red, self.quit_game)
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
            self.button("easy", 300, 450, 100, 50, green, bright_green, clicked_green, self.game_difficulty, "easy")
            self.button("medium", 500, 450, 100, 50, green, bright_green, clicked_green, self.game_difficulty, "medium")
            self.button("hard", 700, 450, 100, 50, green, bright_green, clicked_green, self.game_difficulty, "hard")

            self.button("green", 700, 350, 100, 50, green, bright_green, clicked_green,
                        self.set_theme_start_game, "green")
            self.button("black", 300, 350, 100, 50, green, bright_green, clicked_green,
                        self.set_theme_start_game, "black")
            self.button("white", 500, 350, 100, 50, green, bright_green, clicked_green,
                        self.set_theme_start_game, "white")

            self.button("Quit", 800, 600, 100, 50, red, bright_red, clicked_red, self.quit_game)
            self.button("Play", 200, 600, 100, 50, green, bright_green, clicked_green, self.run_game)
            pygame.display.flip()

    def button(self, msg, x, y, w, h, inactive_color, active_color, clicked_color, action, *action_parameters):
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        if x < mouse_pos[0] < x + w and y < mouse_pos[1] < y + h:
            pygame.draw.rect(self._display_surf, active_color, (x, y, w, h))
            if clicked[0] == 1 and action is not None:
                action(*action_parameters)
                pygame.draw.rect(self._display_surf, clicked_color, (x, y, w, h))
                return
        else:
            pygame.draw.rect(self._display_surf, inactive_color, (x, y, w, h))

        self.message_display(msg, 20, (x + (w / 2)), (y + (h / 2)))

    def set_theme_start_game(self, color):
        if color == "green":
            self._themefactory = GreenFactoryTheme()
        elif color == "black":
            self._themefactory = BlackFactoryTheme()
        elif color == "white":
            self._themefactory = WhiteFactoryTheme()

        self.background_obj = self._themefactory.createbackground()
        self._image_surf = self._themefactory.createplayer()

    def restart_game(self):
        self.player = Player(1)
        self.reverse_direction = False
        self.food = LengthItem(5, 5)
        self.game_strategy = EasyStrategy()
        self.speed = self.game_strategy.speed()
        self.run_game()

    def game_difficulty(self, difficulty):
        if difficulty == "easy":
            self.game_strategy = EasyStrategy()
            self.speed = self.game_strategy.speed()

        elif difficulty == "medium":
            self.game_strategy = MediumStratgey()
            self.speed = self.game_strategy.speed()

        elif difficulty == "hard":
            self.game_strategy = HardStrategy()
            self.speed = self.game_strategy.speed()


if __name__ == "__main__":
    theApp = App()
    theApp.game_intro()
