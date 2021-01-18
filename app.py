
import logging
import pygame
from app import *
from pygame.locals import *
from werkzeug.serving import run_simple

from web import webapp as w
import data_access as da

logging.basicConfig(filename='setlistmanager.log', level=logging.DEBUG)
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 128

class Button:
    pass


class Text():
    """Create a text object."""

    def __init__(self, surface, text, pos, **options):
        self.text = text
        self.surface = surface
        self.pos = pos
        self.bold = True
        self.italic = False
        self.underline = False
        self.background = None # Color('white')
        self.font = pygame.font.SysFont('Arial', 64)
        self.fontname = None # 'Free Sans'
        self.fontsize = 40
        self.fontcolor = Color('black')
        self.set_font()
        da.connect_db('db.db')
        songs = da.get_all_songs_as_json()
        print (songs)

        # self.words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.
        # self.space = self.font.size(' ')[0]  # The width of a space.
        # max_width, max_height = self.surface.get_size()
        # x, y = self.pos
        # for line in self.words:
        #     for word in line:
        #         word_surface = self.font.render(word, 0, self.fontcolor)
        #         # print(word)
        #         word_width, word_height = word_surface.get_size()
        #         if x + word_width >= max_width:
        #             x = pos[0]  # Reset the x.
        #             y += word_height  # Start on new row.
        #         surface.blit(word_surface, (x, y))
        #         x += word_width + self.space
        #     x = pos[0]  # Reset the x.
        #     y += word_height  # Start on new row.

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
        # Put the center of surf at the center of the display
        surf_center = (
            (SCREEN_WIDTH - self.rect.width)/2,
            (SCREEN_HEIGHT - self.rect.height)/2
        )
        App.screen.blit(self.img, surf_center)
        # App.screen.blit(self.img, self.rect)


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        logging.debug('Initializing App')
        pygame.init()
        pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        self.shortcuts = {
            (K_x, KMOD_LMETA): 'print("cmd+X")',
            (K_x, KMOD_LALT): 'print("alt+X")',
            (K_x, KMOD_LCTRL): 'print("ctrl+X")',
            (K_x, KMOD_LMETA + KMOD_LSHIFT): 'print("cmd+shift+X")',
            (K_x, KMOD_LMETA + KMOD_LALT): 'print("cmd+alt+X")',
            (K_x, KMOD_LMETA + KMOD_LALT + KMOD_LSHIFT): 'print("cmd+alt+shift+X")',
        }
        self.color = Color('green')
        self.flags = RESIZABLE
        self.rect = Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        App.screen = pygame.display.set_mode(self.rect.size, self.flags)
        App.t = Text(App.screen, 'Chorus', pos=(0, 0))
        App.running = True

    def run(self):
        """Run the main event loop."""
        logging.debug('entering method run')

        app = w.create_app()
        run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

        logging.debug('after start of flask')
        while App.running:
            logging.debug('.')
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
                if event.type == KEYDOWN:
                    self.do_shortcut(event)
            App.screen.fill(self.color)
            App.t.draw()
            pygame.display.update()
        logging.debug('exiting setlistmanager')
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
