"""
A great game in which the player has to collect pink hearts! However, the player will
lose points if a black heart is collected! If the score goes negative, the player loses.
See which of your friends can get the highest score!!!

Controls: anything that the player's computer thinks is arrow key input

@author: jovanduy
"""

import pygame
import random
import time

class DrawableSurface():
    """ A class that wraps a pygame.Surface and a pygame.Rect """

    def __init__(self, surface, rect):
        """ Initialize the drawable surface """
        self.surface = surface
        self.rect = rect

    def get_surface(self):
        """ Get the surface """
        return self.surface

    def get_rect(self):
        """ Get the rect """
        return self.rect

class GameModel():
    """ Represents the state of the Game """
    def __init__(self, width, height):
        """ Initialize the Game model """
        self.width = width
        self.height = height
        self.background = Background(height)
        # put character in middle of screen
        self.character = Character(width/2 - 15, height/2 - 20)
        pygame.font.init()
        self.font = pygame.font.Font('freesansbold.ttf', 80)
        self.hearts = []
        for i in range(25):
            if random.randint(0, 30) < 20:
                heart = Heart()
                self.hearts.append(heart)
            else:
                black_heart = BlackHeart()
                self.hearts.append(black_heart)

    def is_hit(self, heart, character):
        if (heart.x in range(int(character.x), int(character.x+14))) and (heart.y in range(int(character.y-48), int(character.y))):
            character.score += heart.points
            return True
        return False

    def display_score(self):
        self.score = self.font.render(str(self.character.score), False, (0,0,0))
        self.screen.blit(self.score_surf, (20,70))

    def update(self, delta_t, width, height):
        """ Updates the model and its constituent parts """
        self.character.update(delta_t, width, height)
        for heart in self.hearts:
            heart.update(delta_t)
            if self.is_hit(heart, self.character):
                heart.reset()
        self.display_score

class Background():
    def __init__(self, screen_height):
        """ Initializes the border """
        self.image = pygame.image.load('images/full_heart.png')
        self.tiles = []
        for i in range(100):
            self.tiles.append(DrawableSurface(self.image, pygame.Rect(i*32, screen_height-32, 32, 32)))
            self.tiles.append(DrawableSurface(self.image, pygame.Rect(i*32, 0, 32, 32)))
            self.tiles.append(DrawableSurface(self.image, pygame.Rect(0, i*32, 32, 32)))
            self.tiles.append(DrawableSurface(self.image, pygame.Rect(608, i*32, 32, 32)))

    def draw(self, screen):
        """ Draws the border """
        for drawable_surface in self.tiles:
            screen.blit(drawable_surface.get_surface(),
                        drawable_surface.get_rect())

class Character():
    """ Represents the player in the game """
    def __init__(self,x,y):
        """ Initialize the character at the specified position
            x, y """
        self.x = x
        self.y = y
        # velocities
        self.vx = 0
        self.vy = 0
        self.image = pygame.image.load('images/stand.png')
        self.image.set_colorkey((255,255,255))
        self.score = 0
        self.is_dead = False

    def draw(self, screen):
        """ get the drawables that make up the character """
        screen.blit(self.image, self.image.get_rect().move(self.x, self.y))

    def update(self, delta_t, width, height):
        """ Update the character over time. The character is not
            allowed past the border of hearts """
        if self.x + self.vx*delta_t <= 30 or self.x + self.vx*delta_t >= width-80:
            pass
        else:
            self.x += self.vx*delta_t
        if self.y + self.vy*delta_t <= 30 or self.y + self.vy*delta_t >= height-110:
            pass
        else:
            self.y += self.vy*delta_t

    def score(self, is_pink):
        """ Updates the score of the Character based on the color 
            of the heart """
        if is_pink:
            self.score += 1
        else:
            self.score -= 1

    def move_down(self):
        """ increases y velocity so the character can move down """
        self.vy += 150

    def move_up(self):
        """ decreases y velocity so the character can move up """
        self.vy -= 150

    def move_right(self):
        """ increases x velocity so the character can move right """
        self.vx += 150

    def move_left(self):
        """ decreases x velocity so the character can move left """
        self.vx -= 150

    def move_nowhere_horizontal(self):
        self.vx = 0

    def move_nowhere_vertical(self):
        self.vy = 0

class Heart(object):
    """ Represents the hearts to be collected in the game """
    def __init__(self):
        self.points = 1
        # randomly choose from which side of the screen the heart starts
        self.side = random.randint(1,4)
        if self.side == 1 or self.side == 3:
            self.x = random.randint(50,600)
            self.vx = 0
            if self.side == 1:
                self.y = 50
                self.vy = 150
            else:
                self.y = 480 - 10
                self.vy = -150
        else:
            self.y = random.randint(50,400)
            self.vy = 0
            if self.side == 2:
                self.x = 50
                self.vx = 150
            else:
                self.x = 400
                self.vx = -150
        self.image = pygame.image.load('images/full_heart.png')
        self.image.set_colorkey((255,255,255))
        self.been_hit = False

    def draw(self, screen):
        screen.blit(self.image, self.image.get_rect().move(self.x, self.y))

    def reach_end_screen(self):
        if self.side == 1:
            if self.y == 470:
                return True
        elif self.side == 2:
            if self.x == 0:
                return True
        elif self.side == 3:
            if self.y == 10:
                return True
        elif self.side == 4:
            if self.x == 630:
                return True
        return False

    def reset(self):
        self.side = random.randint(1,4)
        if self.side == 1 or self.side == 3:
            self.x = random.randint(50,600)
            self.vx = 0
            if self.side == 1:
                self.y = 50
                self.vy = 150
            else:
                self.y = 480 - 10
                self.vy = -150
        else:
            self.y = random.randint(50,400)
            self.vy = 0
            if self.side == 2:
                self.x = 50
                self.vx = 150
            else:
                self.x = 400
                self.vx = -150

    def update(self, delta_t):
        if self.reach_end_screen():
            self.reset()
        self.x += self.vx*delta_t
        self.y += self.vy*delta_t

class BlackHeart(Heart):
    def __init__(self):
        self.points = -1
        # randomly choose from which side of the screen the heart starts
        self.side = random.randint(1,4)
        if self.side == 1 or self.side == 3:
            self.x = random.randint(50,600)
            self.vx = 0
            if self.side == 1:
                self.y = 50
                self.vy = 150
            else:
                self.y = 480 - 10
                self.vy = -150
        else:
            self.y = random.randint(50,400)
            self.vy = 0
            if self.side == 1:
                self.x = 50
                self.vx = 150
            else:
                self.x = 400
                self.vx = -150
        self.image = pygame.image.load('images/black_heart.png')
        self.image.set_colorkey((255,255,255))
        self.been_hit = False

class GameView():
    def __init__(self, model, width, height):
        """ Initialize the view of the Game """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ draw the game window """
        # light blue background color
        self.screen.fill((68,218,255))
        self.model.background.draw(self.screen)
        self.model.character.draw(self.screen)
        for heart in self.model.hearts:
            heart.draw(self.screen)
        pygame.display.update()

class Game():
    """ The main Game class """
    def __init__(self):
        """ Initialize the Game game.  Use Game.run() to
            start the game """
        self.model = GameModel(640, 480)
        self.view = GameView(self.model, 640, 480)
        self.controller = Controller(self.model)

    def run(self):
        """ the main runloop... loop until character's score is negative """
        last_update = time.time()
        while True:
            self.view.draw()
            self.controller.process_events()
            delta_t = time.time() - last_update
            self.model.update(delta_t, 640, 480)
            last_update = time.time()

class Controller():
    def __init__(self, model):
        """ initialize the (what the computer thinks is) keyboard input controller """
        self.model = model
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

    def process_events(self):
        """ process an arrow key press """
        pygame.event.pump()
        if not(pygame.key.get_pressed()[pygame.K_UP]):
            self.up_pressed = False
        elif not(self.up_pressed):
            self.up_pressed = True
            self.model.character.move_up()
        if not(pygame.key.get_pressed()[pygame.K_DOWN]):
            self.down_pressed = False
        elif not(self.down_pressed):
            self.down_pressed = True
            self.model.character.move_down()
        if not(pygame.key.get_pressed()[pygame.K_LEFT]):
            self.left_pressed = False
        elif not(self.left_pressed):
            self.left_pressed = True
            self.model.character.move_left()
        if not(pygame.key.get_pressed()[pygame.K_RIGHT]):
            self.right_pressed = False
        elif not(self.right_pressed):
            self.right_pressed = True
            self.model.character.move_right()

        # if both up and down or left and right are pressed, do not move
        # vertically or horizontally, respectively
        if not(self.up_pressed) and not(self.down_pressed):
            self.model.character.move_nowhere_vertical()
        if not(self.left_pressed) and not(self.right_pressed):
            self.model.character.move_nowhere_horizontal()

if __name__ == '__main__':
    game = Game()
    game.run()