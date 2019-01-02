import pygame

from src.gui.Board import Board
from src.gui.Settings import Settings
from src.gui.TrainBoard import TrainBoard

# game constants
FPS = 30
WIDTH = 600
HEIGHT = 400


class Main:
    running = True

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        self.clock = pygame.time.Clock()
        self.main_surface = pygame.display.set_mode((WIDTH, HEIGHT))

        self.settings_surface = Settings(self.main_surface)
        self.board_surface = Board(self.main_surface)
        self.train_board_surface = TrainBoard(self.main_surface)

        self.current_screen = self.settings_surface.generate_surface()

    # main pygame loop
    def pygame_loop(self):
        while self.running:
            mouse_position = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == "SETTINGS":
                    self.current_screen = self.settings_surface.handle_clicks(mouse_position, [self.train_board_surface,
                                                                                               self.board_surface])
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == "TRAIN_BOARD":
                    self.current_screen = self.train_board_surface.handle_clicks(mouse_position, [self.settings_surface,
                                                                                                  self.board_surface])
                elif event.type == pygame.MOUSEBUTTONDOWN and self.current_screen == "BOARD":
                    self.current_screen = self.board_surface.handle_clicks(mouse_position, self.settings_surface)

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Main().pygame_loop()
