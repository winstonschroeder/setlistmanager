import logging
import pygame
from app import *
from pygame.locals import *

logging.basicConfig(filename='setlistmanager.log', level=logging.DEBUG)


class Button:
    pass


class Text():
    """Create a text object."""

    def __init__(self, text, pos, **options):
        super().__init__(**options)
        self.__dict__.update(Text.options)
        self.text = text
        self.pos = pos

        self.fontname = None
        self.fontsize = 20
        self.fontcolor = Color('black')
        self.set_font()
        self.render()

    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor, self.background)
        self.rect = self.img.get_rect()
        self.rect.size = self.img.get_size()
        self.rect.topleft = self.pos

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)


class Scene:
    """Create a new scene (room, level, view)."""
    id = 0
    bg = Color('gray')

    def __init__(self, *args, **kwargs):
        # Append the new scene and make it the current scene
        App.scenes.append(self)
        App.scene = self
        # Set the instance id and increment the class id
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []
        self.bg = Scene.bg

    def draw(self):
        """Draw all objects in the scene."""
        App.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

    def __str__(self):
        return 'Scene {}'.format(self.id)


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        logging.debug('Initializing App')
        pygame.init()
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        self.flags = FULLSCREEN
        self.rect = Rect(0, 0, 160, 128)
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        App.t = Text('Setlistmanager', pos=(0, 0))

        App.running = True

    def run(self):
        """Run the main event loop."""
        logging.debug('entering loop')
        while App.running:
            logging.debug('.')
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
                if event.type == KEYDOWN:
                    self.do_shortcut(event)
            App.screen.fill(Color('gray'))
            App.t.draw()
            pygame.display.update()

        pygame.quit()

    def do_shortcut(self, event):
        """Find the the key/mod combination in the dictionary and execute the cmd."""
        k = event.key
        m = event.mod
        if (k, m) in self.shortcuts:
            exec(self.shortcuts[k, m])

    def toggle_fullscreen(self):
        """Toggle between full screen and windowed screen."""
        self.flags ^= FULLSCREEN
        pygame.display.set_mode((0, 0), self.flags)

    def toggle_resizable(self):
        """Toggle between resizable and fixed-size window."""
        self.flags ^= RESIZABLE
        pygame.display.set_mode(self.rect.size, self.flags)

    def toggle_frame(self):
        """Toggle between frame and noframe window."""
        self.flags ^= NOFRAME
        pygame.display.set_mode(self.rect.size, self.flags)
