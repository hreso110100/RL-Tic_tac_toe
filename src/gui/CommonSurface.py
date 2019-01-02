from abc import ABCMeta, abstractmethod

import pygame


class CommonSurface(metaclass=ABCMeta):
    # colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (38, 50, 56)
    BLUE = (0, 145, 234)
    RED = (255, 0, 0)

    def __init__(self, main_surface):
        self.main_surface = main_surface
        self.main_surface.fill(self.GREY)

        self.current_screen = ""

        # fonts
        self.font_small = pygame.font.SysFont("comicsansms", 16)
        self.font_medium = pygame.font.SysFont("comicsansms", 24)
        self.font_big = pygame.font.SysFont("comicsansms", 40)

        # assets
        self.circle_img = pygame.image.load('../assets/circle.png')
        self.cross_img = pygame.image.load('../assets/cross.png')
        self.circle = pygame.transform.scale(self.circle_img, (120, 120))
        self.cross = pygame.transform.scale(self.cross_img, (120, 120))

    @abstractmethod
    def generate_surface(self, game_controller=None) -> str:
        pass

    @abstractmethod
    def handle_clicks(self, mouse_position, class_to_switch=None) -> str:
        pass

    def clear_surface(self):
        self.main_surface.fill(self.GREY)
