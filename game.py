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

class FlappyModel():
    """ Represents the game state of our Flappy bird clone """
    def __init__(self, width, height):
        """ Initialize the flappy model """
        self.width = width
        self.height = height
        self.background = Background(height)
        self.bird = Character(0,100)

    def update(self, delta_t, width, height):
        """ Updates the model and its constituent parts """
        self.bird.update(delta_t, width, height)

class Background():
    def __init__(self, screen_height):
        self.image = pygame.image.load('grass_strands.png')
        self.tiles = []
        for i in range(100):
            self.tiles.append(DrawableSurface(self.image, pygame.Rect(i*32,screen_height-32,32,32)))

    def draw(self, screen):
        for drawable_surface in self.tiles:
            screen.blit(drawable_surface.get_surface(),
                        drawable_surface.get_rect())

class Character():
    """ Represents the player in the game """
    def __init__(self,pos_x,pos_y):
        """ Initialize a character at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 50
        self.vel_y = 0
        # TODO: don't depend on relative path
        self.image = pygame.image.load('Stick_figure.png')
        self.image.set_colorkey((255,255,255))

    def draw(self, screen):
        """ get the drawables that makeup the character """
        screen.blit(self.image, self.image.get_rect().move(self.pos_x, self.pos_y))

    def update(self, delta_t, width, height):
        """ update character due to passage of time """
        if self.pos_x + self.vel_x*delta_t <= 0 or self.pos_x + self.vel_x*delta_t >= width:
            pass
        else:
            self.pos_x += self.vel_x*delta_t
        if self.pos_y + self.vel_y*delta_t <= 0 or self.pos_y + self.vel_y*delta_t >= height:
            pass
        else:
            self.pos_y += self.vel_y*delta_t
        # self.vel_y += 20*delta_t

    def move_down(self):
        self.vel_y += 50
    def move_up(self):
        self.vel_y -=50
    def move_right(self):
        self.vel_x += 50
    def move_left(self):
        self.vel_x -= 50
    def move_nowhere_horizontal(self):
        self.vel_x = 0
    def move_nowhere_vertical(self):
        self.vel_y = 0

class FlappyView():
    def __init__(self, model, width, height):
        """ Initialize the view for Flappy Bird.  The input model
            is necessary to find the position of relevant objects
            to draw. """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        self.model.background.draw(self.screen)
        self.model.bird.draw(self.screen)
        pygame.display.update()

class FlappyBird():
    """ The main Flappy Bird class """

    def __init__(self):
        """ Initialize the flappy bird game.  Use FlappyBird.run to
            start the game """
        self.model = FlappyModel(640, 480)
        self.view = FlappyView(self.model, 640, 480)
        self.controller = PygameKeyboardController(self.model)
        # we will code the controller later

    def run(self):
        """ the main runloop... loop until death """
        last_update = time.time()
        while True:
            self.view.draw()
            self.controller.process_events()
            delta_t = time.time() - last_update
            self.model.update(delta_t, 640, 480)
            last_update = time.time()

class PygameKeyboardController():
    def __init__(self, model):
        self.model = model
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False


    def process_events(self):
        pygame.event.pump()
        if not(pygame.key.get_pressed()[pygame.K_UP]):
            self.up_pressed = False
        elif not(self.up_pressed):
            self.up_pressed = True
            self.model.bird.move_up()
        if not(pygame.key.get_pressed()[pygame.K_DOWN]):
            self.down_pressed = False
        elif not(self.down_pressed):
            self.down_pressed = True
            self.model.bird.move_down()
        if not(pygame.key.get_pressed()[pygame.K_LEFT]):
            self.left_pressed = False
        elif not(self.left_pressed):
            self.left_pressed = True
            self.model.bird.move_left()
        if not(pygame.key.get_pressed()[pygame.K_RIGHT]):
            self.right_pressed = False
        elif not(self.right_pressed):
            self.right_pressed = True
            self.model.bird.move_right()
        if not(self.up_pressed) and not(self.down_pressed):
            self.model.bird.move_nowhere_vertical()
        if not(self.left_pressed) and not(self.right_pressed):
            self.model.bird.move_nowhere_horizontal()

if __name__ == '__main__':
    flappy = FlappyBird()
    flappy.run()